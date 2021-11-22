import graphene
from candidates.models import Candidate
from .models import Vacancy, Category, City


class CreateVacancy(graphene.Mutation):
    class Arguments:
        vacancy_name = graphene.String(required=True)
        duties = graphene.String(required=True)
        requirements = graphene.String(required=True)
        conditions = graphene.String(required=True)
        pay_level = graphene.String(required=True)
        recruiter_reward = graphene.Int(required=True)
        city = graphene.ID()
        category = graphene.ID()

    ok = graphene.Boolean()
    message = graphene.String()

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
            city_id = kwargs.get("city")
            category_id = kwargs.get("category")
            Vacancy.objects.create(
                creator=creator,
                vacancy_name=vacancy_name,
                duties=duties,
                requirements=requirements,
                conditions=conditions,
                pay_level=pay_level,
                recruiter_reward=recruiter_reward,
                city=City.objects.get(pk=city_id),
                category=Category.objects.get(pk=category_id)
            )
            return {"ok": True}
        else:
            return {"ok": False, "message": "User has no Employer profile"}


class ProofExit(graphene.Mutation):
    class Arguments:
        candidate_id = graphene.Int()

    ok = graphene.Boolean()
    message = graphene.String()

    @classmethod
    def mutate(cls, root, info, **kwargs):
        user = info.context.user
        if hasattr(user, "employer"):
            employer = user.employer
            candidate = Candidate.objects.get(pk=kwargs.get("candidate_id"))
            vacancy = candidate.vacancy
            recruiter = candidate.recruiter
            if vacancy.creator == employer:
                employer.payed_vacancies += 1
                employer.save()
                vacancy.active = False
                vacancy.save()
                recruiter.closed_vacancies += 1
                recruiter.save()
                return {"ok": True}
            else:
                return {
                    "ok": False,
                    "message": "Vacancy doesn't belong to this Employer",
                }
        else:
            return {"ok": False, "message": "User has no Employer profile"}
