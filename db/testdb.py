from sqlalchemy import create_engine, MetaData, Table, Integer, String, Column, ForeignKeyConstraint, ForeignKey, Boolean
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy.sql.operators import is_

from sqlalchemy.sql.schema import PrimaryKeyConstraint
import random

from telebot.types import InputInvoiceMessageContent

engine = create_engine('sqlite:///thedb.db?check_same_thread=False')
engine.connect()
session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base(engine)
metadata = MetaData()
diction = {}



class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, unique=True)
    age = Column(Integer)
    reg_time = Column(String())
    name = Column(String())
    photo = Column(String())
    about = Column(String())
    msfile = Column(String)
    inspection = Column(String, ForeignKey('inspections.id'))
    is_admin = Column(Integer)
    is_delete = Column(Integer)


class UsersAndDialogs(Base):
    __tablename__ = 'users_dialog'
    user1 = Column(Integer, ForeignKey('users.id'))
    user2 = Column(Integer, ForeignKey('users.id'))
    last_msg = Column(Integer, ForeignKey('msg.id'))
    __table_args__ = (
        PrimaryKeyConstraint(
            user1,
            user2),
            {}
        )


class Messages(Base):
    __tablename__ = 'msg'
    id = Column(Integer, primary_key=True)
    author = Column(Integer, ForeignKey('users.id'))
    text = Column(String)
    previous_msg = Column(Integer, ForeignKey('msg.id'))


class Inspections(Base):
    __tablename__ = 'inspections'
    id = Column(String, primary_key=True)
    name = Column(String)
    number = Column(String)


class Invites(Base):
    __tablename__= 'invites'
    invite = Column(String, primary_key=True)
    createdby = Column(Integer, ForeignKey('users.id'))
    usedby = Column(Integer, ForeignKey('users.id'))


class Likes(Base):
    __tablename__= 'likes'
    subject = Column(Integer, ForeignKey('users.id'), primary_key=True)
    object = Column(Integer, ForeignKey('users.id'), primary_key=True)


def chkusr(chat_id, fr_id):
    is_exists = session.query(Likes).filter(Likes.subject == chat_id, Likes.object == fr_id).all()
    if is_exists:
        print(0)
        return False
    else:
        print(1)
        return True


def find_friend(chat_id):
    global diction

    if not diction.get(chat_id):
        diction.update({chat_id: []})
    friend_id = session.query(Users.id).filter(Users.is_admin == 0, Users.id != chat_id, chkusr(chat_id, Users.id)).all()
    # friend_id = random.choice(session.query(Users.id).filter(Users.is_admin == 0, Users.id != chat_id, Users.id not in diction[chat_id], session.query(Likes).filter(Likes.subject == chat_id, Likes.object == Users.id).all().count() == 0))

    if friend_id:
        friend_id = random.choice(friend_id)[0]
        print(friend_id)
        u1 = session.query(Users).get(friend_id)
        print(u1.name)
        return (u1.id, u1.name, u1.photo, u1.about, u1.age)
    else:
        return 0

arr = []
is_exists = session.query(Likes.object).filter(Likes.subject == 5).all()
for element in is_exists:
    arr.append(element[0])
if arr:
    print(arr)
        
# chat_id = 785704774
# # session.query(Likes).filter(Likes.subject == chat_id, Likes.object == Users.id).all()).count() == 0
# for _ in range(5):
#     fr_id = session.query(Users.id).filter(Users.is_admin == 0, Users.id != chat_id, chkusr(chat_id, Users.id)).all()
#     print(fr_id)

# chars = '+-/*!&$#?=@<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
# for _ in range(10):
#     password =''
#     for _ in range(10):
#         password += random.choice(chars)

#     print(password)
#     t1 = Invites(invite=password, createdby=0)
#     session.add(t1)
#     session.commit()

# def stop_dialogue(id, fr_id):
#     if session.query(UsersAndDialogs).filter(UsersAndDialogs.user1 == id, UsersAndDialogs.user2 == fr_id).scalar():
#         return True
#     else:
#         return False


# friend_id = session.query(Users.id).filter(Users.is_admin == 0, Users.id != 785704774, chkusr(785704774, Users.id)).all()
# print(friend_id[0])

# i1 = session.query(Inspections).filter(Inspections.id == '5918').scalar()
# if i1:
#     print('Такая инспекция есть')
# else:
#     print('такой нет')
