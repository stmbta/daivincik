from sqlalchemy import create_engine, MetaData, Table, Integer, String, Column, ForeignKeyConstraint, ForeignKey, Boolean
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

from sqlalchemy.sql.schema import PrimaryKeyConstraint
import random
from token import correcttoken
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
    subject = Column(Integer, ForeignKey('users.id'))
    object = Column(Integer, ForeignKey('users.id'))
    __table_args__ = (
        PrimaryKeyConstraint(
            subject,
            object),
            {}
        )


def user_registration(chat_id, conf_arr):
    u1 = Users(id=chat_id, age=conf_arr[1], name=conf_arr[0], reg_time=str(datetime.now()), photo=conf_arr[2], about=conf_arr[3], msfile=conf_arr[4], inspection=conf_arr[5], is_admin=0, is_delete=0)
    session.add(u1)
    session.commit()

def check_user1(chat_id):
    arr = []
    is_exists = session.query(Likes.object).filter(Likes.subject == chat_id).all()
    for element in is_exists:
        arr.append(element[0])
    return arr

def check_user2(chat_id):
    arr = []
    userss = session.query(Users.id).filter(Users.is_admin == 0, Users.id != chat_id, Users.is_delete == 0).all()
    for element in userss:
        arr.append(element[0])
    return arr


def get_user_profiles():
    arr = []
    message_date_arr = [random.randint(10, 29) for _ in range(30)]
    users = session.query(Users.id).filter(Users.is_admin == 0, Users.is_delete == 0).all()
    date_arr = [0 for _ in range(30)]

    for element in users:
        arr.append({'picture': session.query(Users.photo).filter(Users.id == element[0]).first()[0], 'name': session.query(Users.name).filter(Users.id == element[0]).first()[0], "age": session.query(Users.age).filter(Users.id == element[0]).first()[0], "joined_at": session.query(Users.reg_time).filter(Users.id == element[0]).first()[0], 'inspection_id': session.query(Users.inspection).filter(Users.id == element[0]).first()[0], "inviter_name": session.query(Invites.createdby).filter(Invites.usedby == element[0]).first()[0]})
        datetime_string = session.query(Users.reg_time).filter(Users.id == element[0]).first()[0][0:-7]
        datetime_obj = datetime.strptime(datetime_string, '%m-%d-%y %H:%M:%S').date()
        if datetime.date() - datetime_obj > 30:
            date_arr[datetime.date() - datetime_obj] = date_arr[datetime.date() - datetime_obj] + 1
    return {
        "newuserstate": date_arr,
        "newmessagestate": message_date_arr,
        "user_profiles": arr
    }

def get_current_user(user_id):
    
    invites_count = session.query(Invites).filter(Invites.usedby == None, Invites.createdby == user_id).count()
    activated_invitess = session.query(Invites.invite).filter(Invites.usedby != None, Invites.createdby == user_id).all()
    arr = []
    for elem in activated_invitess: 
        arr.append({"username": session.query(Invites.usedby.name).filter(Invites.invite == elem[0]).first()[0], "users_invite": elem[0]})
    return {
        "invites_count": invites_count,
        "user_id": user_id,
        "activated_invites": arr
    }

def change_invites(user_id, count):
    invites_count = session.query(Invites).filter(Invites.usedby == None, Invites.createdby == user_id).count()
    if invites_count > count:
        for _ in range(invites_count - count):
            u1 = session.query(Invites).filter(Invites.usedby == None, Invites.createdby == user_id).first()
            session.delete(u1)
            session.commit
    elif invites_count < count:
        chars = '+-/*!&$#?=@<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
        for _ in range(count - invites_count):
            password =''
            for _ in range(10):
                password += random.choice(chars)
            t1 = Invites(invite=password, createdby=id)
            session.add(t1)
            session.commit()
    return {
        "invites_count": invites_count
    }

def ban_user(invite):
    u1 = session.query(Invites).get(invite)
    u1.usedby.is_delete = 1
    session.commit()

def invites_str():
    arr = session.query(Invites.invite).all()
    arr2 = []
    for elem in arr:
        arr2.append({"created_by": session.query(Invites.createdby).filter(Invites.invite == elem[0]), "used_by": session.query(Invites.usedby).filter(Invites.invite == elem[0]), "invite": elem[0]})
    return {
        "invites": arr2
    }



def closed_acess(token):
    global correct_token
    if correcttoken == token:
        
        return {'is_correct': True}
    else:
        return {'is_correct': False}




def find_friend(chat_id):
    global diction
    friend_arr1 = check_user1(chat_id)
    friend_arr2 = check_user2(chat_id)
    arr = []
    if friend_arr2:
        for e in friend_arr2:
            if e not in friend_arr1:
                arr.append(e)

    if arr:
        friend_id = random.choice(arr)
        u1 = session.query(Users).get(friend_id)
        print(u1.name)
        return (u1.id, u1.name, u1.photo, u1.about, u1.age)
    else:
        return 0

def like(id, friend_id):
    l1 = Likes(subject=id, object=friend_id)
    session.add(l1)
    session.commit()
    
def is_matching(id):
    arr = []
    for fr_id in session.query(Users.id).all():
        if session.query(Likes).get((id, fr_id[0])):
            if session.query(Likes).get((fr_id[0], id)):
                u2 = session.query(Users).get(fr_id[0])
                arr.append((u2.id, u2.name))
    return arr

def user_arr():
    arr = []
    for id in  session.query(Users.id).all():
        arr.append(str(id[0]))
    return arr
        
def start_dial(id, fr_id):
    d1 = UsersAndDialogs(user1=id, user2=fr_id)
    l1 = session.query(Likes).filter(Likes.subject == id, Likes.object == fr_id).one()
    session.delete(l1)
    session.commit()
    l2 = session.query(Likes).filter(Likes.subject == fr_id, Likes.object == id).one()
    session.delete(l2)
    session.commit()
    session.add(d1)
    session.commit()

def cur_dial_find(id):
    w1 = session.query(UsersAndDialogs.user2).filter(UsersAndDialogs.user1 == id).first()
    if not w1: 
        w1 = session.query(UsersAndDialogs.user1).filter(UsersAndDialogs.user2 == id).first()

    return w1

def new_message_add(m_id, user_id, fr_id, text):
    m1 = Messages(id=m_id, author=user_id, text=text)
    ud1 = UsersAndDialogs(user1=user_id, user2=fr_id, last_msg=m_id)
    session.add(m1)
    session.add(ud1)
    session.commit()

def check_invite(invite, user_id):
    try: 
        i1 = session.query(Invites).get(invite)
        if i1.usedby == None:
            i1.usedby = user_id
            session.commit()
            return 1
        else: 

            return 0
    except:
        return -1

def get_user_invites(id):
    invite_arr = session.query(Invites.invite).filter(Invites.usedby == None, Invites.createdby == id).all()
    token_arr = []
    if len(invite_arr) == 0:
        
        chars = '+-/*!&$#?=@<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
        for _ in range(2):
            password =''
            for _ in range(10):
                password += random.choice(chars)
            token_arr.append(password)
            t1 = Invites(invite=password, createdby=id)
            session.add(t1)
            session.commit()
    elif len(invite_arr) == 1:
        token_arr.append(invite_arr[0])
        chars = '+-/*!&$#?=@<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'

        password =''
        for _ in range(10):
            password += random.choice(chars)
        token_arr.append(password)
        t1 = Invites(invite=password, createdby=id)
        session.add(t1)
        session.commit()

    elif len(invite_arr) >= 2:
        for invite in invite_arr:
            token_arr.append(invite[0])
    return token_arr

def stop_dialogue(id, fr_id):
    if session.query(UsersAndDialogs).filter(UsersAndDialogs.user1 == id, UsersAndDialogs.user2 == fr_id).all():
        session.query(UsersAndDialogs).filter(UsersAndDialogs.user1 == id, UsersAndDialogs.user2 == fr_id).delete()
        session.commit()
    else:
        session.query(UsersAndDialogs).filter(UsersAndDialogs.user1 == fr_id, UsersAndDialogs.user2 == id).delete()
        session.commit()


def check_islike(id, fr_id):
    if session.query(Likes).filter(Likes.subject == id, Likes.object == fr_id).scalar():
        return True
    else:
        return False
    
def check_register(id):
    if session.query(Users).filter(Users.id == id).scalar():
        return True
    else:
        return False

def parse_inspection():
    file1 = open("inspections.txt", "r")


    lines = file1.readlines()


    for line in lines:
        l1 = line.strip()
        if len(l1) == 3:
            l1 = f'0{l1}'
        l2 = Inspections(id=l1)
        session.add(l2)
    session.commit()


    file1.close


# parse_inspection()
def check_inspection(id):
    i1 = session.query(Inspections).filter(Inspections.id == id).scalar()
    if i1:
        return True
    else:
        return False

def get_name(id):
    return session.query(Users.name).filter(Users.id == id).first()[0]
     
def generate_tokens():
    token_arr = []
    chars = '+-/*!&$#?=@<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    for _ in range(50):
        password =''
        for _ in range(10):
            password += random.choice(chars)
        token_arr.append(password)
        print(password)
        t1 = Invites(invite=password, createdby=0)
        session.add(t1)
        session.commit()



Base.metadata.create_all(engine)