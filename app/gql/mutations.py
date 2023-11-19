from graphene import ObjectType

from app.user.mutations import RegisterUser, LoginUser, RegenerateJWT


class Mutation(ObjectType):
    register_user = RegisterUser.Field()
    login_user = LoginUser.Field()
    regenerate_jwt = RegenerateJWT.Field()
