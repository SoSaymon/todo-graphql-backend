from typing import Optional

from graphene import ObjectType, Field, Int, List

from app.db.database import Session
from app.db.models import User
from app.gql.types import UserObject


class Query(ObjectType):
    get_users = List(UserObject)
    get_user = Field(UserObject, user_id=Int(required=True))

    @staticmethod
    def resolve_get_users(root, info) -> None:
        return Session().query(User).all()

    @staticmethod
    def resolve_get_user(root, info, user_id: int) -> Optional[UserObject]:
        return Session().query(User).filter(user_id == User.id).first()
