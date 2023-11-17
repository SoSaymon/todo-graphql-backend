from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """
    App user model

    Attributes:
        id (Integer): A column in the database that uses integer values, this is the primary key for the user.
        username (String): A column in the database that uses string values, this is a unique identifier for the user.
        email (String): A column in the database that uses string values, this is a unique identifier for the user's email.
        password_hash (String): A column in the database that uses string values, this is used to store the hashed password of the user.
        is_admin (Boolean): A column in the database that uses boolean values, this is used to identify if the user has admin privileges.
        created_at (DateTime): A column in the database that uses DateTime values, this is used to store the date and time when the user was created.
        last_login (DateTime): A column in the database that uses DateTime values, this is used to store the date and time of the user's last login.

    """

    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password_hash = Column(String)
    is_admin = Column(Boolean)
    created_at = Column(DateTime)
    # last_login = Column(DateTime)
