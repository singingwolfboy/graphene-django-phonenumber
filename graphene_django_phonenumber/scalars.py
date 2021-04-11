from typing import Optional
from functools import lru_cache
from graphene.types import Scalar
from graphql.language import ast
from phonenumber_field.phonenumber import PhoneNumber


class PhoneNumber(Scalar):
    """An international phone number, formatted using the E.164 standard."""

    @staticmethod
    def serialize(pn: PhoneNumber) -> str:
        return pn.as_e164

    @staticmethod
    def parse_literal(node: ast.Node) -> Optional[PhoneNumber]:
        if isinstance(node, ast.StringValue):
            pn = PhoneNumber.from_string(node.value)
            if pn.is_valid():
                return pn

    @staticmethod
    def parse_value(value: str) -> Optional[PhoneNumber]:
        pn = PhoneNumber.from_string(value)
        if pn.is_valid():
            return pn


@lru_cache
def make_national_phone_number_scalar(region):

    class NationalPhoneNumber(PhoneNumber):
        """A national phone number, specific to the region specified in
        the Django settings (`PHONENUMBER_DEFAULT_REGION`)."""

        class Meta:
            name = f"{region}PhoneNumber"
            description = f"A national phone number, specific to the {region} region."

        @staticmethod
        def serialize(pn: PhoneNumber) -> str:
            return pn.as_national

    return NationalPhoneNumber
