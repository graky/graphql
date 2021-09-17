from graphql_jwt.testcases import JSONWebTokenTestCase
from django.contrib.auth import get_user_model
from graphql_jwt.shortcuts import get_token
from work.models import Employer, Recruiter


class TestCreateEmployerRecruiter(JSONWebTokenTestCase):
    def setUp(self):
        self.user = get_user_model()(
            username="test", password="test", last_name="test", first_name="test"
        )
        self.user.save()
        self.token = get_token(self.user)
        self.client.authenticate(self.user)

    def tearDown(self):
        self.user.delete()

    def test_create_employer(self):
        mutation_create_employer = """
            mutation CreateEmployer {
                createEmployer {
                    ok
                }
            }
        """
        response = self.client.execute(mutation_create_employer)
        self.assertIsNone(response.errors, response.errors)
        result = response.data.get("createEmployer")
        self.assertIsNotNone(result, "Doesn't get createEmployer object")
        self.assertTrue(result.get("ok"), "Employer not created")
        employer_db = Employer.objects.filter(user=self.user)
        self.assertTrue(employer_db.exists(), "Employer not registered in db")
        response = self.client.execute(mutation_create_employer)
        self.assertIsNone(response.errors, response.errors)
        result = response.data.get("createEmployer")
        self.assertIsNotNone(result, "Doesn't get createEmployer object")
        self.assertFalse(result.get("ok"), "Employer created two times")

    def test_create_recruiter(self):
        mutation_create_recruiter = """
            mutation CreateRecruiter {
                createRecruiter {
                    ok
                }
            }
        """
        response = self.client.execute(mutation_create_recruiter)
        self.assertIsNone(response.errors, response.errors)
        result = response.data.get("createRecruiter")
        self.assertIsNotNone(result, "Doesn't get createRecruiter object")
        self.assertTrue(result.get("ok"), "Recruiter not created")
        recruiter_db = Recruiter.objects.filter(user=self.user)
        self.assertTrue(recruiter_db.exists(), "Recruiter not registered in db")
        response = self.client.execute(mutation_create_recruiter)
        self.assertIsNone(response.errors, response.errors)
        result = response.data.get("createRecruiter")
        self.assertIsNotNone(result, "Doesn't get createRecruiter object")
        self.assertFalse(result.get("ok"), "Recruiter created two times")
