from datetime import datetime
from typing import Optional, Type

from graphene import Mutation, String, Boolean, Field, Int
from graphql import GraphQLError

from app.db.database import Session
from app.db.models import Note
from app.gql.types import NoteObject
from app.utils.decorators import logged_in
from app.utils.user import get_authenticated_user


class CreateNote(Mutation):
    """
    A class used to represent the CreateNote mutation in GraphQL.

    Attributes:
        title (String): A string representing the title of the note (required).
        description (String): A string representing the description of the note (optional).
        done (Boolean): A boolean representing the completion status of the note (optional).
        note (Field): A field that holds the NoteObject.

    Methods:
        mutate(root, info, title, description=None, done=False): Creates a new note with the given title, description, and done status.
    """

    class Arguments:
        title = String(required=True)
        description = String()
        done = Boolean()

    note = Field(NoteObject)

    @staticmethod
    @logged_in
    def mutate(
        root, info, title: str, description: Optional[str] = None, done: bool = False
    ) -> Type["CreateNote"]:
        """
        Creates a new note with the given title, description, and done status.

        Args:
            root (Any): The root object that GraphQL uses to look up the initial value for the query.
            info (ResolveInfo): An object containing various information about the current execution state.
            title (str): The title of the note.
            description (str, optional): The description of the note (default is None).
            done (bool, optional): The completion status of the note (default is False).

        Returns:
            CreateNote: An instance of the CreateNote mutation with the newly created note.
        """
        user_token = get_authenticated_user(info.context)

        if not user_token:
            raise GraphQLError("Cannot authenticate user")

        user = user_token[0]

        if not user:
            raise GraphQLError("Cannot authenticate user")

        note = Note(title=title, description=description, done=done, owner_id=user.id)

        session = Session()

        session.add(note)
        session.commit()
        session.refresh(note)
        session.close()

        return CreateNote(note=note)


class EditNote(Mutation):
    """
    A class used to represent the EditNote mutation in GraphQL.

    Attributes:
        note_id (Int): An integer representing the ID of the note (required).
        title (String): A string representing the title of the note (optional).
        description (String): A string representing the description of the note (optional).
        done (Boolean): A boolean representing the completion status of the note (optional).
        note (Field): A field that holds the NoteObject.

    Methods:
        mutate(root, info, note_id, title=None, description=None, done=False): Edits an existing note with the given note_id, title, description, and done status.
    """

    class Arguments:
        note_id = Int(required=True)
        title = String()
        description = String()
        done = Boolean()

    note = Field(NoteObject)

    @staticmethod
    @logged_in
    def mutate(
        root,
        info,
        note_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        done: bool = False,
    ) -> Type["EditNote"]:
        """
        Edits an existing note with the given note_id, title, description, and done status.

        Args:
            root (Any): The root object that GraphQL uses to look up the initial value for the query.
            info (ResolveInfo): An object containing various information about the current execution state.
            note_id (int): The ID of the note.
            title (str, optional): The title of the note (default is None).
            description (str, optional): The description of the note (default is None).
            done (bool, optional): The completion status of the note (default is False).

        Returns:
            EditNote: An instance of the EditNote mutation with the edited note.
        """
        user_token = get_authenticated_user(info.context)

        if not user_token:
            raise GraphQLError("Cannot authenticate user")

        user = user_token[0]

        if not user:
            raise GraphQLError("Cannot authenticate user")

        session = Session()

        note = session.query(Note).filter(Note.id == note_id).first()

        if not note:
            raise GraphQLError(f"Note with this id: {note_id} doesn't exist")

        if note.owner_id != user.id and user.is_admin is False:
            raise GraphQLError("You're not authorized to perform this action")

        if title:
            note.title = title
        if description:
            note.description = description
        if done != note.done:
            note.done = done

        note.updated_at = datetime.now()

        session.commit()
        session.refresh(note)
        session.close()

        return EditNote(note=note)


class DeleteNote(Mutation):
    """
    A class used to represent the DeleteNote mutation in GraphQL.

    Attributes:
        note_id (Int): An integer representing the ID of the note (required).
        success (Field): A field that holds a boolean value indicating whether the deletion was successful.

    Methods:
        mutate(root, info, note_id): Deletes an existing note with the given note_id.
    """

    class Arguments:
        note_id = Int(required=True)

    success = Field(Boolean)

    @staticmethod
    @logged_in
    def mutate(root, info, note_id: int) -> Type["DeleteNote"]:
        """
        Deletes an existing note with the given note_id.

        Args:
            root (Any): The root object that GraphQL uses to look up the initial value for the query.
            info (ResolveInfo): An object containing various information about the current execution state.
            note_id (int): The ID of the note.

        Returns:
            DeleteNote: An instance of the DeleteNote mutation with the success status of the deletion.
        """
        user_token = get_authenticated_user(info.context)

        if not user_token:
            raise GraphQLError("Cannot authenticate user")

        user = user_token[0]

        if not user:
            raise GraphQLError("Cannot authenticate user")

        session = Session()

        note = session.query(Note).filter(Note.id == note_id).first()

        if not note:
            raise GraphQLError(f"Note with this id: {note_id} doesn't exist")

        if note.owner_id != user.id and user.is_admin is False:
            raise GraphQLError("You're not authorized to perform this action")

        session.delete(note)
        session.commit()
        session.close()

        return DeleteNote(success=True)
