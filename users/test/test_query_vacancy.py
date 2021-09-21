from graphql_jwt.testcases import JSONWebTokenTestCase
from django.contrib.auth import get_user_model
from graphql_jwt.shortcuts import get_token
from users.models import Employer, Recruiter, Vacancy, Candidate


class TestQuery(JSONWebTokenTestCase):
    def setUp(self):
        self.user = get_user_model()(
            username="query_test1", password="test", last_name="test", first_name="test"
        )
        self.user2 = get_user_model()(
            username="query_test2", password="test", last_name="test", first_name="test"
        )
        self.user.save()
        self.user2.save()
        self.employer = Employer.objects.create(user=self.user2)
        self.vacancy = Vacancy.objects.create(
            creator=self.employer,
            vacancy_name="vacancy_name",
            duties="duties",
            requirements="requirements",
            conditions="conditions",
            pay_level="LG",
            recruiter_reward=1000,
        )
        self.vacancy2 = Vacancy.objects.create(
            creator=self.employer,
            vacancy_name="vacancy_name2",
            duties="duties2",
            requirements="requirements2",
            conditions="conditions2",
            pay_level="PR",
            recruiter_reward=1000,
        )
        self.recruiter = Recruiter.objects.create(user=self.user)
        self.token = get_token(self.user)
        self.client.authenticate(self.user)

    def tearDown(self):
        self.user.delete()
        self.user2.delete()
        self.employer.delete()
        self.vacancy.delete()
        self.vacancy2.delete()
        self.recruiter.delete()

    def test_query_vacancies(self):
        query_vacancy = """
            query Vacancies{
                vacancies{
                    id
                    vacancyName
                    payLevel
                }
            }
        """
        response = self.client.execute(query_vacancy)
        self.assertIsNone(response.errors, response.errors)
        result = response.data.get("vacancies")
        self.assertEqual(len(result), 1, "Not 1 vacancy object")
        vacancy1 = result[0]
        ID = int(vacancy1.get("id"))
        self.assertEqual(ID, self.vacancy.id, "Not right vacancy object id")

        query_vacancy = """
                    query Vacancies{
                        vacancies(payLevel:"PR"){
                            id
                            vacancyName
                            payLevel
                        }
                    }
                """
        response = self.client.execute(query_vacancy)
        self.assertIsNone(response.errors, response.errors)
        result = response.data.get("vacancies")
        self.assertEqual(len(result), 1, "Not 1 vacancy object")
        vacancy2 = result[0]
        ID = int(vacancy2.get("id"))
        self.assertEqual(ID, self.vacancy2.id, "Not right vacancy object id")

    def test_query_vacancy(self):
        query_vacancy = """
            query Vacancies{
                vacancy(vacancyId:%s){
                    id
                    vacancyName
                }
            }
        """
        query_vacancy %= self.vacancy2.id
        response = self.client.execute(query_vacancy)
        self.assertIsNone(response.errors, response.errors)
        result = response.data.get("vacancy")
        ID = int(result.get("id"))
        self.assertEqual(ID, self.vacancy2.id, "Not right id")
        self.assertEqual(
            result.get("vacancyName"),
            self.vacancy2.vacancy_name,
            "Not right vacancy name",
        )
