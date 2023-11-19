from app.db.database import Session, engine
from app.db.models import Base, User
from app.utils.password import hash_password


def create_database() -> None:
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    user = User(
        username="Admin",
        email="admin@admin.com",
        password_hash=hash_password("12345678"),
        is_admin=True,
        is_active=True,
    )

    session = Session()
    session.add(user)
    session.commit()
    session.close()
