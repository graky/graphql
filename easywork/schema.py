import graphql_jwt
from graphene import ObjectType, Schema
from work.mutations import (
    CreateUser,
    CreateEmployer,
    CreateRecruiter,
    CreateVacancy,
    CreateCandidate,
    ProofExit,
)
from work.schema import WorkQuery


class Query(WorkQuery, ObjectType):
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
