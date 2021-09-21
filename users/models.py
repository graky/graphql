from django.db import models
from django.utils import timezone
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
