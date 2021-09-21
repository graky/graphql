import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model
from .models import Employer, Recruiter


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        fields = "__all__"


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)
    failed = graphene.Boolean()

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        username = kwargs.get("username")
        password = kwargs.get("password")
        first_name = kwargs.get("first_name")
        last_name = kwargs.get("last_name")
        user, created = get_user_model().objects.get_or_create(
            username=username,
            defaults={
                "password": password,
                "first_name": first_name,
                "last_name": last_name,
            },
        )
        if created:
            return CreateUser(user=user)


class CreateEmployer(graphene.Mutation):
    ok = graphene.Boolean()
    message = graphene.String()

    @classmethod
    def mutate(cls, root, info, **kwargs):
        if isinstance(info.context.user.id, int):
            user = info.context.user
            employer, created = Employer.objects.get_or_create(user=user)
            if created:
                return {"ok": True}
            else:
                return {"ok": False, "message": "Employer already exists"}
        else:
            return {"ok": False, "message": "User not signed in"}


class CreateRecruiter(graphene.Mutation):
    ok = graphene.Boolean()
    message = graphene.String()

    @classmethod
    def mutate(cls, root, info, **kwargs):
        if isinstance(info.context.user.id, int):
            user = info.context.user
            recruiter, created = Recruiter.objects.get_or_create(user=user)
            if created:
                return {"ok": True}
            else:
                return {"ok": False, "message": "Recruiter already exists"}
        else:
            return {"ok": False, "message": "User not signed in"}
