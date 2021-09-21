from graphene import ObjectType, relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from .models import Vacancy


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


class VacancyQuery(ObjectType):
    vacancies = DjangoFilterConnectionField(VacancyType)
    vacancy = relay.Node.Field(VacancyType)
