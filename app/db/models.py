from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

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
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    is_admin = Column(Boolean, default=0)
    is_active = Column(Boolean, default=0)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    last_login = Column(DateTime)

    notes = relationship("Note", back_populates="owner", lazy="joined")


class Note(Base):
    """
    Note model representing a note in the application.

    Attributes:
        id (Integer): A column in the database that uses integer values. This is the primary key for the note.
        owner_id (Integer): A foreign key column in the database that uses integer values. This is the id of the user who owns the note.
        owner (relationship): A relationship that represents the user who owns the note.
        title (String): A column in the database that uses string values. This is the title of the note.
        description (String): A column in the database that uses string values. This is the description of the note.
        done (Boolean): A column in the database that uses boolean values. This represents whether the note is done or not.
        created_at (DateTime): A column in the database that uses DateTime values. This is used to store the date and time when the note was created.
        updated_at (DateTime): A column in the database that uses DateTime values. This is used to store the date and time when the note was last updated.
    """

    __tablename__ = "notes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="notes", lazy="joined")
    title = Column(String, nullable=False)
    description = Column(String)
    done = Column(Boolean, default=0)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    updated_at = Column(DateTime)
