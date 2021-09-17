import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model
from .models import Employer, Candidate, Vacancy, Recruiter


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

    @classmethod
    def mutate(cls, root, info, **kwargs):
        if isinstance(info.context.user.id, int):
            user = info.context.user
            employer, created = Employer.objects.get_or_create(user=user)
            if created:
                return {"ok": True}
            else:
                return {"ok": False}
        else:
            return {"ok": False}


class CreateRecruiter(graphene.Mutation):
    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, **kwargs):
        if isinstance(info.context.user.id, int):
            user = info.context.user
            recruiter, created = Recruiter.objects.get_or_create(user=user)
            if created:
                return {"ok": True}
            else:
                return {"ok": False}
        else:
            return {"ok": False}


class CreateVacancy(graphene.Mutation):
    class Arguments:
        vacancy_name = graphene.String(required=True)
        duties = graphene.String(required=True)
        requirements = graphene.String(required=True)
        conditions = graphene.String(required=True)
        pay_level = graphene.String(required=True)
        recruiter_reward = graphene.Int(required=True)

    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, **kwargs):
        user = info.context.user
        if hasattr(user, "employer"):
            creator = user.employer
            vacancy_name = kwargs.get("vacancy_name")
            duties = kwargs.get("duties")
            requirements = kwargs.get("requirements")
            conditions = kwargs.get("conditions")
            pay_level = kwargs.get("pay_level")
            recruiter_reward = kwargs.get("recruiter_reward")
            Vacancy.objects.create(
                creator=creator,
                vacancy_name=vacancy_name,
                duties=duties,
                requirements=requirements,
                conditions=conditions,
                pay_level=pay_level,
                recruiter_reward=recruiter_reward,
            )
            return {"ok": True}
        else:
            return {"ok": False}


class CreateCandidate(graphene.Mutation):
    class Arguments:
        vacancy_id = graphene.Int(required=True)
        name = graphene.String(required=True)
        interview = graphene.String(required=True)
        contact = graphene.String(required=True)

    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, **kwargs):
        user = info.context.user
        if hasattr(user, "recruiter"):
            recruiter = user.recruiter
            vacancy = Vacancy.objects.get(pk=kwargs.get("vacancy_id"))
            name = kwargs.get("name")
            interview = kwargs.get("interview")
            contact = kwargs.get("contact")
            Candidate.objects.create(
                recruiter=recruiter,
                vacancy=vacancy,
                name=name,
                interview=interview,
                contact=contact,
            )
            return {"ok": True}
        else:
            return {"ok": False}


class ProofExit(graphene.Mutation):
    class Arguments:
        candidate_id = graphene.Int()

    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, **kwargs):
        user = info.context.user
        if hasattr(user, "employer"):
            employer = user.employer
            candidate = Candidate.objects.get(pk=kwargs.get("candidate_id"))
            vacancy = candidate.vacancy
            recruiter = candidate.recruiter
            employer.payed_vacancies += 1
            employer.save()
            vacancy.active = False
            vacancy.save()
            recruiter.closed_vacancies += 1
            recruiter.save()
            return {"ok": True}
        else:
            return {"ok": False}
