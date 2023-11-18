from graphene import ObjectType

from app.user.mutations import RegisterUser


class Mutation(ObjectType):
    register_user = RegisterUser.Field()
