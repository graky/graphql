from django.db import models
from django.utils import timezone
from users.models import Employer


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

    class Meta:
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансии"
