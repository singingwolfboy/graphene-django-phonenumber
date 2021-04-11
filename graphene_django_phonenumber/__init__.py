from graphene_django.converter import convert_django_field, get_django_field_description
from phonenumber_field.modelfields import PhoneNumberField
from .scalars import PhoneNumber, make_national_phone_number_scalar


@convert_django_field.register(PhoneNumberField)
def convert_field_to_phone_number(field, registry=None):
    from django.conf import settings

    pn_format = getattr(settings, "PHONENUMBER_DB_FORMAT", "E164")
    if pn_format == "NATIONAL":
        pn_region = getattr(settings, "PHONENUMBER_DEFAULT_REGION", None)
        if not pn_region:
            raise Exception("settings.PHONENUMBER_DEFAULT_REGION is required for NationalPhoneNumber scalar")
        Scalar = make_national_phone_number_scalar(pn_region)
    else:
        Scalar = PhoneNumber

    return Scalar(
        description=get_django_field_description(field), required=not field.null
    )
