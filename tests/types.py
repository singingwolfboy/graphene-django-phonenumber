from graphene_django import DjangoObjectType
from django.contrib.auth.models import User
from .models import UserProfile


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "profile")


class UserProfileType(DjangoObjectType):
    class Meta:
        model = UserProfile
        fields = "__all__"