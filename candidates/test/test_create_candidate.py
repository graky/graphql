from graphql_jwt.testcases import JSONWebTokenTestCase
from django.contrib.auth import get_user_model
from graphql_jwt.shortcuts import get_token
from users.models import Employer, Recruiter
from candidates.models import Candidate
from vacancies.models import Vacancy


class TestCreateCandidate(JSONWebTokenTestCase):
    def setUp(self):
        self.user = get_user_model()(
            username="employer1", password="test", last_name="test", first_name="test"
        )
        self.user2 = get_user_model()(
            username="employer2", password="test", last_name="test", first_name="test"
        )
        self.user.save()
        self.user2.save()
        self.employer = Employer.objects.create(user=self.user)
        self.employer2 = Employer.objects.create(user=self.user2)
        self.vacancy = Vacancy.objects.create(
            creator=self.employer2,
            vacancy_name="vacancy_name",
            duties="duties",
            requirements="requirements",
            conditions="conditions",
            pay_level="ES",
            recruiter_reward=1000,
        )
        self.recruiter = Recruiter.objects.create(user=self.user)
        self.token = get_token(self.user)
        self.client.authenticate(self.user)

    def tearDown(self):
        self.user.delete()
        self.user2.delete()
        self.employer.delete()
        self.employer2.delete()
        self.vacancy.delete()
        self.recruiter.delete()

    def test_create_candidate(self):
        mutation_create_candidate = """
        mutation CreateCandidate {
                createCandidate(
                    vacancyId: %s
                    contact: "test contact"
                    interview: "test interviwe"
                    name: "test name"
                    ) {
                        ok
                    }
                }
        """
        mutation_create_candidate %= self.vacancy.id
        response = self.client.execute(mutation_create_candidate)
        self.assertIsNone(response.errors, response.errors)
        result = response.data.get("createCandidate")
        self.assertIsNotNone(result, "Doesn't get createCandidate object")
        self.assertTrue(result.get("ok"), "Candidate not created")
        self.assertIsNone(result.get("message"), "Get a message")
        candidate_db = Candidate.objects.filter(
            recruiter=self.recruiter, vacancy=self.vacancy
        )
        self.assertTrue(candidate_db.exists(), "Candidate not registered in db")
