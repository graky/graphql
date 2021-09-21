from django.db import models
from users.models import Recruiter
from vacancies.models import Vacancy


class Candidate(models.Model):
    id = models.BigAutoField(unique=True, primary_key=True)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    recruiter = models.ForeignKey(Recruiter, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    interview = models.CharField(max_length=255)
    contact = models.CharField(max_length=255)
    exit_proof = models.BooleanField(default=False)
