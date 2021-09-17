from graphql_jwt.testcases import JSONWebTokenTestCase
from django.contrib.auth import get_user_model
from graphql_jwt.shortcuts import get_token
from work.models import Employer, Recruiter, Vacancy, Candidate


class TestQuery(JSONWebTokenTestCase):
    def setUp(self):
        self.user = get_user_model()(
            username="query_test", password="test", last_name="test", first_name="test"
        )
        self.user.save()
        self.employer = Employer.objects.create(user=self.user)
        self.recruiter = Recruiter.objects.create(user=self.user)
        self.token = get_token(self.user)
        self.client.authenticate(self.user)

    def tearDown(self):
        self.user.delete()
        self.employer.delete()
        self.recruiter.delete()

    def test_query_employer(self):
        query_employer = """
            query Employer{
                employer(employerId: %s){
                id
                fullName
                payedVacancies
                }
            }
        """
        query_employer %= self.employer.id
        response = self.client.execute(query_employer)
        self.assertIsNone(response.errors, response.errors)
        result = response.data.get("employer")
        ID = int(result.get("id"))
        self.assertEqual(ID, self.employer.id, "Not right id")
        full_name = self.user.last_name + " " + self.user.first_name
        self.assertEqual(result.get("fullName"), full_name, "Not right full name")
        self.assertEqual(
            result.get("payedVacancies"),
            self.employer.payed_vacancies,
            "Not right payed vacancies",
        )

    def test_query_recruiter(self):
        query_recruiter = """
            query Recruiter{
                recruiter(recruiterId: %s){
                id
                fullName
                closedVacancies
                }
            }
        """
        query_recruiter %= self.recruiter.id
        response = self.client.execute(query_recruiter)
        self.assertIsNone(response.errors, response.errors)
        result = response.data.get("recruiter")
        ID = int(result.get("id"))
        self.assertEqual(ID, self.recruiter.id, "Not right id")
        full_name = self.user.last_name + " " + self.user.first_name
        self.assertEqual(result.get("fullName"), full_name, "Not right full name")
        self.assertEqual(
            result.get("closedVacancies"),
            self.recruiter.closed_vacancies,
            "Not right closed_vacancies",
        )
