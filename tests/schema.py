import graphene
from graphene_django import DjangoObjectType, DjangoListField
from django.contrib.auth.models import User
from .models import UserProfile
from .types import UserType
from .mutations import UserRegistrationFormMutation


class Query(graphene.ObjectType):
    users = DjangoListField(UserType)


class Mutation(graphene.ObjectType):
    create_user = UserRegistrationFormMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
