from graphql_jwt.testcases import JSONWebTokenTestCase
from django.contrib.auth import get_user_model
from graphql_jwt.shortcuts import get_token
from users.models import Employer, Recruiter


class TestQuery(JSONWebTokenTestCase):
    def setUp(self):
        self.user = get_user_model()(
            username="test1", password="test", last_name="Щеколдин", first_name="Кирилл"
        )
        self.user.save()
        self.user2 = get_user_model()(
            username="test2", password="test", last_name="Кирилов", first_name="Степан"
        )
        self.user2.save()
        self.user3 = get_user_model()(
            username="test3", password="test", last_name="Гребенкин", first_name="Аким"
        )
        self.user3.save()
        self.employer = Employer.objects.create(user=self.user)
        self.recruiter = Recruiter.objects.create(user=self.user2)
        self.token = get_token(self.user)
        self.client.authenticate(self.user)

    def tearDown(self):
        self.user.delete()
        self.user2.delete()
        self.user3.delete()
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
        full_name = self.user2.last_name + " " + self.user2.first_name
        self.assertEqual(result.get("fullName"), full_name, "Not right full name")
        self.assertEqual(
            result.get("closedVacancies"),
            self.recruiter.closed_vacancies,
            "Not right closed_vacancies",
        )

    def test_search(self):
        query_search = """
                        query {
                            search(searchText: "Кирил") {
                                ... on EmployerType {
                                      id
                                      fullName
                                      user{
                                        id
                                      }
                                }
                                ... on RecruiterType {
                                  id
                                  fullName
                                  user{
                                    id
                                  }
                                }
                              }
                            }
        """
        response = self.client.execute(query_search)
        self.assertIsNone(response.errors, response.errors)
        result = response.data.get("search")
        self.assertEqual(len(result), 2, "Not two users")
        first_name, second_name = result[0].get("fullName"), result[1].get("fullName")
        self.assertTrue("Кирил" in first_name, "Wrong result")
        self.assertTrue("Кирил" in second_name, "Wrong result")
