from graphql_jwt.testcases import JSONWebTokenTestCase
from django.contrib.auth import get_user_model
from graphql_jwt.shortcuts import get_token
from users.models import Employer, Recruiter
from vacancies.models import Vacancy


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
            vacancy_name="Водитель тягача",
            duties="duties",
            requirements="requirements",
            conditions="conditions",
            pay_level="LG",
            recruiter_reward=1000,
        )
        self.vacancy2 = Vacancy.objects.create(
            creator=self.employer,
            vacancy_name="Водитель грузовика",
            duties="duties2",
            requirements="requirements2",
            conditions="conditions2",
            pay_level="LG",
            recruiter_reward=3000,
        )
        self.vacancy3 = Vacancy.objects.create(
            creator=self.employer,
            vacancy_name="Водитель автобуса",
            duties="duties3",
            requirements="requirements3",
            conditions="conditions3",
            pay_level="HR",
            recruiter_reward=2000,
        )
        self.vacancy4 = Vacancy.objects.create(
            creator=self.employer,
            vacancy_name="Грузчик",
            duties="duties4",
            requirements="requirements4",
            conditions="conditions4",
            pay_level="LG",
            recruiter_reward=500,
        )
        self.token = get_token(self.user)
        self.client.authenticate(self.user)

    def tearDown(self):
        self.user.delete()
        self.user2.delete()
        self.employer.delete()
        self.vacancy.delete()
        self.vacancy2.delete()
        self.vacancy3.delete()
        self.vacancy4.delete()

    def test_query_vacancies(self):
        query_vacancy = """
            query {
                vacancies(active: true, vacancyName_Icontains: "водитель", payLevel: "LG") {
                    edges {
                          node {
                            id
                            vacancyName
                            duties
                            requirements
                            conditions
                            payLevel
                            creationDate
                            recruiterReward
                            active
                            creator {
                              fullName
                              id
                              user {
                                username
                              }
                            }
                        }
                    }
                }
            }
        """
        response = self.client.execute(query_vacancy)
        # print(response)
        self.assertIsNone(response.errors, response.errors)
        result = response.data.get("vacancies").get("edges")
        self.assertEqual(len(result), 2, "Not 2 vacancy objects")
        vacancy1 = result[0].get("node")
        vacancy2 = result[1].get("node")
        self.assertTrue(
            "Водитель" in vacancy1.get("vacancyName")
            and vacancy1.get("payLevel") == "LG",
            "Wrong vacancy object",
        )
        self.assertTrue(
            "Водитель" in vacancy2.get("vacancyName")
            and vacancy2.get("payLevel") == "LG",
            "Wrong vacancy object",
        )
        vacancy1_id = vacancy1.get("id")
        query_vacancy = """
                    query Vacancy {
                        vacancy(id: "%s") {
                            id
                            vacancyName
                          }
                        }
                """
        query_vacancy %= vacancy1_id
        response = self.client.execute(query_vacancy)
        self.assertIsNone(response.errors, response.errors)
        result = response.data.get("vacancy")
        vacancy_name = result.get("vacancyName")
        self.assertEqual(vacancy_name, "Водитель тягача", "Wrong vacancy object")
