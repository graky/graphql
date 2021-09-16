import time
from datetime import datetime
from django.db import models
from django.db.models import Prefetch
from django.utils import timezone
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    id = models.BigAutoField(primary_key=True)


class Employer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    payed_vacancies = models.IntegerField(default=0)


class Recruiter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    level = models.CharField(
        max_length=2,
        choices=[
            ("LG", "LIGHT"),
            ("MD", "MEDIUM"),
            ("HR", "HARD"),
            ("PR", "PRO"),
        ],
        default="LG",
    )
    closed_vacancies = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Рекрутер"
        verbose_name_plural = "Рекрутеры"


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


class Candidate(models.Model):
    id = models.BigAutoField(unique=True, primary_key=True)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    recruiter = models.ForeignKey(Recruiter, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    interview = models.CharField(max_length=255)
    contact = models.CharField(max_length=255)
    exit_proof = models.BooleanField(default=False)
