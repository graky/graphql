from graphql_jwt.testcases import JSONWebTokenTestCase
from django.contrib.auth import get_user_model
from graphql_jwt.shortcuts import get_token
from users.models import Employer, Recruiter, Vacancy, Candidate


class TestProofExit(JSONWebTokenTestCase):
    def setUp(self):
        self.user = get_user_model()(
            username="employer1", password="test", last_name="test", first_name="test"
        )
        self.user2 = get_user_model()(
            username="recruiter", password="test", last_name="test", first_name="test"
        )
        self.user.save()
        self.user2.save()
        self.employer = Employer.objects.create(user=self.user)
        self.vacancy = Vacancy.objects.create(
            creator=self.employer,
            vacancy_name="test_vacancy",
            duties="test_duties",
            requirements="test_requirements",
            conditions="test_conditions",
            pay_level="PR",
            recruiter_reward=5000,
        )
        self.recruiter = Recruiter.objects.create(user=self.user2)
        self.candidate = Candidate.objects.create(
            recruiter=self.recruiter,
            vacancy=self.vacancy,
            name="name",
            interview="interview",
            contact="contact",
        )
        self.token = get_token(self.user)
        self.client.authenticate(self.user)

    def tearDown(self):
        self.user.delete()
        self.user2.delete()
        self.employer.delete()
        self.vacancy.delete()
        self.recruiter.delete()
        self.candidate.delete()

    def test_proof_exit(self):
        mutation_proof_exit = """
            mutation ProofExit{
                proofExit(candidateId: %s){
                    ok
                }
            }
        """
        mutation_proof_exit %= self.candidate.id
        response = self.client.execute(mutation_proof_exit)
        self.assertIsNone(response.errors, response.errors)
        result = response.data.get("proofExit")
        self.assertIsNotNone(result, "Doesn't get proofExit object")
        self.assertTrue(result.get("ok"), "Exit not proofed")
        employer = Employer.objects.get(pk=self.employer.id)
        recruiter = Recruiter.objects.get(pk=self.recruiter.id)
        vacancy = Vacancy.objects.get(pk=self.vacancy.id)
        self.assertEqual(
            employer.payed_vacancies, 1, "payed_vacancies parameter not changed"
        )
        self.assertEqual(
            recruiter.closed_vacancies, 1, "closed_vacancies parameter not changed"
        )
        self.assertFalse(vacancy.active, "active parameter not changed")
