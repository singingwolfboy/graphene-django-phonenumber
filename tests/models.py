from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone_number = PhoneNumberField()


def create_profile(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        user_profile = UserProfile(user=user)
        user_profile.save()

post_save.connect(create_profile, sender=User)
