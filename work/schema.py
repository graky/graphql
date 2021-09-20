import graphene
from django.db import models
from graphene import ObjectType, relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from .models import Recruiter, Vacancy, Employer, Candidate, User
from .mutations import UserType


class CandidateType(DjangoObjectType):
    class Meta:
        model = Candidate
        fields = "__all__"


class EmployerType(DjangoObjectType):
    class Meta:
        model = Employer
        fields = "__all__"

    full_name = graphene.String()

    def resolve_full_name(root, info, **kwargs):
        return "{0} {1}".format(root.user.last_name, root.user.first_name)


class RecruiterType(DjangoObjectType):
    class Meta:
        model = Recruiter
        fields = "__all__"

    full_name = graphene.String()

    def resolve_full_name(root, info, **kwargs):
        return "{0} {1}".format(root.user.last_name, root.user.first_name)


class VacancyType(DjangoObjectType):
    class Meta:
        model = Vacancy
        filter_fields = {
            "vacancy_name": ["exact", "icontains", "istartswith"],
            "duties": ["exact", "icontains", "istartswith"],
            "requirements": ["exact", "icontains", "istartswith"],
            "pay_level": ["exact"],
            "active": ["exact"],
        }
        interfaces = (relay.Node,)


class WorkQuery(ObjectType):
    recruiter = graphene.Field(RecruiterType, recruiter_id=graphene.Int())
    vacancies = DjangoFilterConnectionField(VacancyType)
    vacancy = relay.Node.Field(VacancyType)
    employer = graphene.Field(EmployerType, employer_id=graphene.Int())
    users = graphene.List(UserType)
    candidate = graphene.Field(CandidateType, candidate_id=graphene.Int())
    candidates = graphene.List(CandidateType)

    def resolve_users(root, info, **kwargs):
        return User.objects.all()

    def resolve_recruiter(root, info, recruiter_id):
        return Recruiter.objects.get(pk=recruiter_id)

    def resolve_employer(root, info, employer_id):
        return Employer.objects.get(pk=employer_id)

    def resolve_candidate(root, info, candidate_id):
        return Candidate.objects.get(pk=candidate_id)

    def resolve_candidates(root, info, **kwargs):
        if hasattr(info.context.user, "employer"):
            employer = info.context.user.employer
            vacancies = Vacancy.objects.filter(
                models.Q(creator=employer) & models.Q(active=True)
            )
            candidates = Candidate.objects.filter(vacancy__in=vacancies)
            return candidates
        else:
            return []
