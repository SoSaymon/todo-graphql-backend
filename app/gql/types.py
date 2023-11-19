from graphene import ObjectType, Int, String, Boolean, DateTime


class UserObject(ObjectType):
    id = Int()
    username = String()
    email = String()
    is_admin = Boolean()
    is_active = Boolean()
    created_at = DateTime()
    last_login = DateTime()
