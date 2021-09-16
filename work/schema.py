import graphene
import graphql_jwt
from django.db import models
from graphene import ObjectType, String, Schema
from graphene_django import DjangoObjectType
from .models import Recruiter, Vacancy, Employer, Candidate, User
from .mutations import CreateUser, UserType, CreateEmployer, CreateRecruiter, CreateVacancy, CreateCandidate, ProofExit


def filter_pay_level(info, kwargs):
    user = info.context.user
    if kwargs.get("pay_level"):
        return Vacancy.objects.filter(models.Q(pay_level=kwargs.get("pay_level")) & models.Q(active=True))
    elif hasattr(user, "recruiter"):
        return Vacancy.objects.filter(models.Q(pay_level=user.recruiter.level) & models.Q(active=True))
    else:
        return Vacancy.objects.filter(active=True)


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
        fields = "__all__"

    def resolve_pay_level(root, info, **kwargs):
        return root.pay_level


class WorkQuery(ObjectType):
    recruiter = graphene.Field(RecruiterType, recruiter_id=graphene.Int())
    vacancies = graphene.List(VacancyType, FIELDS)
    vacancy = graphene.Field(VacancyType, vacancy_id=graphene.Int())
    employer = graphene.Field(EmployerType, employer_id=graphene.Int())
    users = graphene.List(UserType)
    candidate = graphene.Field(CandidateType, candidate_id=graphene.Int())
    candidates = graphene.List(CandidateType)

    def resolve_users(root, info, **kwargs):
        return User.objects.all()

    def resolve_recruiter(root, info, recruiter__id):
        return Recruiter.objects.get(pk=recruiter__id)

    def resolve_vacancies(root, info, **kwargs):
        return filter_pay_level(info, kwargs)

    def resolve_vacancy(root, info, vacancy_id):
        return Vacancy.objects.get(pk=vacancy_id)

    def resolve_employer(root, info, employer_id):
        return Employer.objects.get(pk=employer_id)

    def resolve_candidate(root, info, candidate_id):
        return Candidate.objects.get(pk=candidate_id)

    def resolve_candidates(root, info, **kwargs):
        if hasattr(info.context.user, "employer"):
            employer = info.context.user.employer
            vacancies = Vacancy.objects.filter(models.Q(creator=employer) & models.Q(active=True))
            candidates = Candidate.objects.filter(vacancy__in=vacancies)
            return candidates
        else:
            return []


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    create_recruiter = CreateRecruiter.Field()
    create_employer = CreateEmployer.Field()
    create_vacancy = CreateVacancy.Field()
    create_candidate = CreateCandidate.Field()
    proof_exit = ProofExit.Field()


schema = Schema(query=WorkQuery, mutation=Mutation)
