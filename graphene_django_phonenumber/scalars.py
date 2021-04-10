from typing import Optional
from graphene.types import Scalar
from graphql.language import ast
from phonenumber_field.phonenumber import PhoneNumber


class PhoneNumber(Scalar):
    """A phone number, formatted using the E.164 standard."""

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
