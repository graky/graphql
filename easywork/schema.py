import graphql_jwt
from graphene import ObjectType, Schema
from users.mutations import (
    CreateUser,
    CreateEmployer,
    CreateRecruiter,
)
from candidates.mutations import CreateCandidate
from vacancies.mutations import CreateVacancy, ProofExit
from users.schema import UserQuery
from candidates.schema import CandidateQuery
from vacancies.schema import VacancyQuery


class Query(UserQuery, CandidateQuery, VacancyQuery, ObjectType):
    ...


class Mutation(ObjectType):
    create_user = CreateUser.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    create_recruiter = CreateRecruiter.Field()
    create_employer = CreateEmployer.Field()
    create_vacancy = CreateVacancy.Field()
    create_candidate = CreateCandidate.Field()
    proof_exit = ProofExit.Field()


schema = Schema(query=Query, mutation=Mutation)
