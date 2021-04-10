from graphene import Field
from graphene_django.forms.mutation import DjangoModelFormMutation
from .forms import UserRegistrationForm


class UserRegistrationFormMutation(DjangoModelFormMutation):
    class Meta:
        form_class = UserRegistrationForm
