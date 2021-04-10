import graphene
from graphene_django import DjangoObjectType, DjangoListField
from django.contrib.auth.models import User
from .models import UserProfile

class UserProfileType(DjangoObjectType):
    class Meta:
        model = UserProfile
        fields = "__all__"


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("username", "profile")


class Query(graphene.ObjectType):
    users = DjangoListField(UserType)


schema = graphene.Schema(query=Query)
