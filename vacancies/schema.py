import graphene
from django.db import models
from graphene import ObjectType
from graphene_django import DjangoObjectType
from .models import Vacancy, Category, City


class CityType(DjangoObjectType):
    class Meta:
        model = City
        fields = "__all__"


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = "__all__"


class VacancyType(DjangoObjectType):
    class Meta:
        model = Vacancy
        fields = "__all__"

    @staticmethod
    def filter_pay_level(info, kwargs):
        user = info.context.user
        if pay_level := kwargs.get("pay_level"):
            return Vacancy.objects.filter(
                models.Q(pay_level=pay_level) & models.Q(active=True)
            )
        elif hasattr(user, "recruiter"):
            return Vacancy.objects.filter(
                models.Q(pay_level=user.recruiter.level) & models.Q(active=True)
            )
        else:
            return Vacancy.objects.filter(active=True)


class VacancyQuery(ObjectType):
    vacancies = graphene.List(VacancyType, pay_level=graphene.String(), city_id=graphene.Int(), category=graphene.Int())
    vacancy = graphene.Field(VacancyType, vacancy_id=graphene.Int())
    categories = graphene.List(CategoryType)
    cities = graphene.List(CityType)


    def resolve_vacancies(root, info, **kwargs):
        vacancies = Vacancy.objects.all()
        if pay_level := kwargs.get("pay_level"):
            vacancies = vacancies.filter(
                models.Q(pay_level=pay_level) & models.Q(active=True)
            )
        if category := kwargs.get("category"):
            vacancies = vacancies.filter(
                models.Q(category_id=category) & models.Q(active=True)
            )
        if city := kwargs.get("city"):
            vacancies = vacancies.filter(
                models.Q(city_id=city) & models.Q(active=True)
            )
        return vacancies

    def resolve_vacancy(root, info, vacancy_id):
        return Vacancy.objects.get(pk=vacancy_id)

    def resolve_categories(root, info, **kwargs):
        return Category.objects.all()

    def resolve_cities(root, info, **kwargs):
        return City.objects.all()