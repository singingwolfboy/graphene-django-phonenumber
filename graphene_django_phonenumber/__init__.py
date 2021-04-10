from graphene_django.converter import convert_django_field, get_django_field_description
from phonenumber_field.modelfields import PhoneNumberField
from .scalars import PhoneNumber


@convert_django_field.register(PhoneNumberField)
def convert_field_to_phone_number(field, registry=None):
    return PhoneNumber(
        description=get_django_field_description(field), required=not field.null
    )