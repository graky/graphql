from graphql_jwt.testcases import JSONWebTokenTestCase
from django.contrib.auth import get_user_model
from graphql_jwt.shortcuts import get_token
from users.models import Employer
from vacancies.models import Vacancy


class TestCreateVacancy(JSONWebTokenTestCase):
    def setUp(self):
        self.user = get_user_model()(
            username="employer1", password="test", last_name="test", first_name="test"
        )
        self.user.save()
        self.employer = Employer.objects.create(user=self.user)
        self.client.authenticate(self.user)

    def tearDown(self):
        self.user.delete()
        self.employer.delete()

    def test_create_vacancy(self):
        mutation_create_vacancy = """
            mutation CreateVacancy {
                createVacancy(
                    vacancyName: "test vacancy"
                    conditions: "test conditions"
                    duties: "test duties"
                    requirements: "test requirements"
                    payLevel: "HD"
                    recruiterReward: 5000
                ) {
                    ok
                    message
                }
            }
        """
        response = self.client.execute(mutation_create_vacancy)
        self.assertIsNone(response.errors, response.errors)
        result = response.data.get("createVacancy")
        self.assertIsNotNone(result, "Doesn't get createVacancy object")
        self.assertTrue(result.get("ok"), "Vacancy not created")
        self.assertIsNone(result.get("message"), "Get a message")
        vacancy_db = Vacancy.objects.filter(creator=self.employer)
        self.assertTrue(vacancy_db.exists(), "Vacancy not registered in db")
