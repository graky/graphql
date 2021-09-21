import graphene
from django.db import models
from graphene import ObjectType
from graphene_django import DjangoObjectType
from .models import Recruiter, Employer, User
from .mutations import UserType


class UserInterface(graphene.Interface):
    full_name = graphene.String()

    def resolve_full_name(root, info, **kwargs):
        return "{0} {1}".format(root.user.last_name, root.user.first_name)


class EmployerType(DjangoObjectType):
    class Meta:
        model = Employer
        fields = "__all__"
        interfaces = (UserInterface,)


class RecruiterType(DjangoObjectType):
    class Meta:
        model = Recruiter
        fields = "__all__"
        interfaces = (UserInterface,)


class SearchUsers(graphene.Union):
    class Meta:
        types = (EmployerType, RecruiterType)


class UserQuery(ObjectType):
    recruiter = graphene.Field(RecruiterType, recruiter_id=graphene.Int())
    employer = graphene.Field(EmployerType, employer_id=graphene.Int())
    users = graphene.List(UserType)
    search = graphene.List(SearchUsers, search_text=graphene.String())

    def resolve_users(root, info, **kwargs):
        return User.objects.all()

    def resolve_recruiter(root, info, recruiter_id):
        return Recruiter.objects.get(pk=recruiter_id)

    def resolve_employer(root, info, employer_id):
        return Employer.objects.get(pk=employer_id)

    def resolve_search(root, info, search_text):
        result = []
        filter_ = models.Q(user__first_name__icontains=search_text) | models.Q(
            user__last_name__icontains=search_text
        )
        employers = Employer.objects.filter(filter_)
        recruiters = Recruiter.objects.filter(filter_)
        result.extend(employers)
        result.extend(recruiters)
        return result
