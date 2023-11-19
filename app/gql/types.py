from graphene import ObjectType, Int, String, Boolean, DateTime, Field, List


class UserObject(ObjectType):
    id = Int()
    username = String()
    email = String()
    is_admin = Boolean()
    is_active = Boolean()
    created_at = DateTime()
    last_login = DateTime()

    notes = List(lambda: NoteObject)

    @staticmethod
    def resolve_notes(root, info):
        return root.notes


class NoteObject(ObjectType):
    id = Int()
    title = String()
    description = String()
    done = Boolean()
    created_at = DateTime()
    updated_at = DateTime()

    owner_id = Int()
    owner = Field(lambda: UserObject)

    @staticmethod
    def resolve_owner(root, info):
        return root.owner
