from django.db import models
from django.utils import timezone
from users.models import Employer


class City(models.Model):
    city_name = models.CharField(max_length=255)

class Category(models.Model):
    category_name = models.CharField(max_length=255)

class Vacancy(models.Model):
    id = models.BigAutoField(unique=True, primary_key=True)
    vacancy_name = models.CharField(max_length=255)
    duties = models.CharField(max_length=255)
    requirements = models.CharField(max_length=255)
    conditions = models.CharField(max_length=255)
    pay_level = models.CharField(
        max_length=2,
        choices=[
            ("LG", "LIGHT"),
            ("MD", "MEDIUM"),
            ("HR", "HARD"),
            ("PR", "PRO"),
        ],
    )
    creation_date = models.DateTimeField(default=timezone.now, editable=False)
    recruiter_reward = models.IntegerField()
    active = models.BooleanField(default=True)
    creator = models.ForeignKey(
        Employer, on_delete=models.CASCADE, verbose_name="Работодатель"
    )

    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name="Город", null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория", null=True)

    class Meta:
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансии"


