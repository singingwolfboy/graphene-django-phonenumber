from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from phonenumber_field.formfields import PhoneNumberField

from .models import UserProfile


class UserRegistrationForm(forms.ModelForm):
    phone_number = PhoneNumberField()

    class Meta:
        model = User
        fields = ("username", "password", "first_name", "last_name")

    def save(self, commit=True):
        user = super().save(commit=commit)
        user.profile.phone_number = self.cleaned_data["phone_number"]
        user.profile.save()
        return user
