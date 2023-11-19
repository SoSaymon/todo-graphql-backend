from typing import Optional

from graphene import ObjectType, Field, Int, List
from graphql import GraphQLError

from app.db.database import Session
from app.db.models import User
from app.gql.types import UserObject
from app.utils.decorators import admin_user, logged_in
from app.utils.user import get_authenticated_user


class Query(ObjectType):
    get_users = List(UserObject)
    get_user = Field(UserObject, user_id=Int(required=True))

    @staticmethod
    @admin_user
    def resolve_get_users(root, info) -> Optional[UserObject]:
        return Session().query(User).all()

    @staticmethod
    @logged_in
    def resolve_get_user(root, info, user_id: int) -> Optional[UserObject]:
        user_token = get_authenticated_user(info.context)
        user: User = user_token[0]

        if user.is_admin is not True:
            if user.id != user_id:
                raise GraphQLError("You cannot query other users")

        return Session().query(User).filter(user_id == User.id).first()
