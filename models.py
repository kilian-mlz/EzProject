from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
import enum

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    login = Column(String(255), index=True)
    password = Column(String(255))
    email = Column(String(255), unique=True, index=True)

    tickets = relationship("Ticket", back_populates="user")

class StatusEnum(enum.Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"

class Ticket(Base):
    __tablename__ = 'tickets'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    description = Column(String(255))
    user_id = Column(Integer, ForeignKey('users.id'))
    status = Column(Enum(StatusEnum), default=StatusEnum.TODO, nullable=False)  # Utilisation de l'Enum pour status

    user = relationship("User", back_populates="tickets")

