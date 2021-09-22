from graphene.test import Client
from easywork.schema import schema
from graphql_jwt.testcases import JSONWebTokenTestCase


class TestCreateUser(JSONWebTokenTestCase):
    def test_create_user(self):
        create_user_mutation = """
            mutation CreateUser {
                createUser(
                    firstName: "Name"
                    lastName: "Surname"
                    username: "test_username"
                    password: "test_password"
                    ) {
                    user {
                        username
                        password
                    }
                }
            }
        """
        response = self.client.execute(create_user_mutation)
        self.assertIsNone(response.errors, response.errors)
        result = response.data.get("createUser")
        self.assertIsNotNone(result, "Doesn't get createUser field")
        user = result.get("user")
        self.assertIsNotNone(user, "Doesn't get user field")
        self.assertEqual(user.get("username"), "test_username", "Not right username")
        self.assertEqual(user.get("password"), "test_password", "Not right password")
        client = Client(schema)
        response = client.execute(create_user_mutation)
        self.assertIsNone(response.get("errors"), response.get("errors"))
        result = response.get("data").get("createUser")
        self.assertIsNone(result, "CreateUser field is not None")


class TestToken(JSONWebTokenTestCase):
    @classmethod
    def setUpClass(cls):
        super(TestToken, cls).setUpClass()
        sign_in_mutation = """
                         mutation CreateUser {
                            createUser(
                                firstName: "Name"
                                lastName: "Surname"
                                username: "token_username"
                                password: "test_password"
                                ) {
                                user {
                                    username
                                    password
                                }
                            }
                        }
                    """
        client = Client(schema)
        client.execute(sign_in_mutation)
        cls.username = "token_username"
        cls.password = "password"

    def test_token(self):
        token_auth_mutation = """
            mutation TokenAuth {
                tokenAuth(
                    username: "token_username",
                    password: "test_password") {
                        token
                    }
                }
        """
        response = self.client.execute(token_auth_mutation)
        self.assertIsNone(response.errors, response.errors)
        result = response.data.get("tokenAuth")
        self.assertIsNotNone(result, "Doesn't get tokenAuth field")
        token = result.get("token")
        self.assertIsNotNone(token, "Doesn't get token")

        token_verify_mutation = """
        mutation VerifyToken {
            verifyToken(
                token: "%s"
            ) {
                payload
            }
        }
        """
        token_verify_mutation %= token
        response = self.client.execute(token_verify_mutation)
        self.assertIsNone(response.errors, response.errors)
        result = response.data.get("verifyToken")
        self.assertIsNotNone(result, "Doesn't get verifyToken field")
        payload = result.get("payload")
        self.assertIsNotNone(payload, "Doesn't get payload field")
        self.assertEqual(
            payload.get("username"), "token_username", "Not right username"
        )
