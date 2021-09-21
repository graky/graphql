import graphene
from graphene import ObjectType
from django.db import models
from graphene_django import DjangoObjectType
from .models import Candidate
from vacancies.models import Vacancy


class CandidateType(DjangoObjectType):
    class Meta:
        model = Candidate
        fields = "__all__"


class CandidateQuery(ObjectType):
    candidate = graphene.Field(CandidateType, candidate_id=graphene.Int())
    candidates = graphene.List(CandidateType)

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
