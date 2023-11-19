import typing
from typing import Optional

from graphene import ObjectType, Field, Int, List
from graphql import GraphQLError

from app.db.database import Session
from app.db.models import User, Note
from app.gql.types import UserObject, NoteObject
from app.utils.decorators import admin_user, logged_in
from app.utils.user import get_authenticated_user


class Query(ObjectType):
    get_users = List(UserObject)
    get_user = Field(UserObject, user_id=Int(required=True))

    get_all_notes = List(NoteObject)
    get_all_user_notes = List(NoteObject, user_id=Int(required=True))
    get_note = Field(NoteObject, user_id=Int(required=True), note_id=Int(required=True))

    @staticmethod
    @admin_user
    def resolve_get_users(root, info) -> Optional[typing.List[UserObject]]:
        return Session().query(User).all()

    @staticmethod
    @logged_in
    def resolve_get_user(root, info, user_id: int) -> Optional[UserObject]:
        user = get_authenticated_user(info.context)[0]
        if not user or (user.is_admin is not True and user.id != user_id):
            raise GraphQLError(
                "Cannot authenticate user or you cannot query other users"
            )

        return Session().query(User).filter_by(id=user_id).first()

    @staticmethod
    @admin_user
    def resolve_get_all_notes(root, info) -> Optional[typing.List[NoteObject]]:
        return Session().query(Note).all()

    @staticmethod
    @logged_in
    def resolve_get_all_user_notes(
        root, info, user_id: int
    ) -> Optional[typing.List[NoteObject]]:
        user = get_authenticated_user(info.context)[0]
        if not user or (user.is_admin is not True and user.id != user_id):
            raise GraphQLError(
                "Cannot authenticate user or you cannot query other users' notes"
            )

        return Session().query(Note).filter_by(owner_id=user_id).all()

    @staticmethod
    @logged_in
    def resolve_get_note(
        root, info, user_id: int, note_id: int
    ) -> Optional[NoteObject]:
        user = get_authenticated_user(info.context)[0]
        if not user or (user.is_admin is not True and user.id != user_id):
            raise GraphQLError(
                "Cannot authenticate user or you cannot query other users' notes"
            )

        return Session().query(Note).filter_by(owner_id=user_id, id=note_id).first()
