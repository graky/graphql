import graphene
from .models import Candidate
from vacancies.models import Vacancy


class CreateCandidate(graphene.Mutation):
    class Arguments:
        vacancy_id = graphene.Int(required=True)
        name = graphene.String(required=True)
        interview = graphene.String(required=True)
        contact = graphene.String(required=True)

    ok = graphene.Boolean()
    message = graphene.String()

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
            return {"ok": False, "message": "User has no Recruiter profile"}
