from graphql_jwt.testcases import JSONWebTokenTestCase
from django.contrib.auth import get_user_model
from graphql_jwt.shortcuts import get_token
from work.models import Employer, Recruiter, Vacancy, Candidate


class TestQuery(JSONWebTokenTestCase):
    def setUp(self):
        self.user = get_user_model()(
            username="query_test3", password="test", last_name="test", first_name="test"
        )
        self.user2 = get_user_model()(
            username="query_test4", password="test", last_name="test", first_name="test"
        )
        self.user3 = get_user_model()(
            username="query_test5", password="test", last_name="test", first_name="test"
        )
        self.user.save()
        self.user2.save()
        self.user3.save()
        self.employer = Employer.objects.create(user=self.user)
        self.employer2 = Employer.objects.create(user=self.user2)
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
            creator=self.employer2,
            vacancy_name="vacancy_name2",
            duties="duties2",
            requirements="requirements2",
            conditions="conditions2",
            pay_level="PR",
            recruiter_reward=1000,
        )
        self.recruiter = Recruiter.objects.create(user=self.use3)
        self.candidate = Candidate.objects.create(
            recruiter=self.recruiter,
            vacancy=self.vacancy,
            name="name",
            interview="interview",
            contact="contact",
        )
        self.candidate2 = Candidate.objects.create(
            recruiter=self.recruiter,
            vacancy=self.vacancy2,
            name="name",
            interview="interview",
            contact="contact",
        )
        self.token = get_token(self.user)
        self.client.authenticate(self.user)

    def tearDown(self):
        self.user.delete()
        self.user2.delete()
        self.user3.delete()
        self.employer.delete()
        self.employer2.delete()
        self.vacancy.delete()
        self.vacancy2.delete()
        self.recruiter.delete()
        self.candidate.delete()
        self.candidate2.delete()

    def test_query_candidates(self):
        query_candidates = """
            query Candidates{
                candidates{
                    id
                    name
                }
            }
        """
        response = self.client.execute(query_candidates)
        self.assertIsNone(response.errors, response.errors)
        result = response.data.get("candidates")
        self.assertEqual(len(result), 1, "Not 1 candidate object")
        candidate1 = result[0]
        ID = int(candidate1.get("id"))
        self.assertEqual(ID, self.candidate.id, "Not right candidate1 object id")
