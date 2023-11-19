from graphene import ObjectType

from app.notes.mutations import CreateNote, EditNote, DeleteNote
from app.user.mutations import RegisterUser, LoginUser, RegenerateJWT, UpdateUser


class Mutation(ObjectType):
    register_user = RegisterUser.Field()
    login_user = LoginUser.Field()
    update_user = UpdateUser.Field()
    regenerate_jwt = RegenerateJWT.Field()

    create_note = CreateNote.Field()
    edit_note = EditNote.Field()
    delete_note = DeleteNote.Field()
