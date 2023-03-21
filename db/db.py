from sqlalchemy import create_engine, MetaData, Table, Integer, String, Column, ForeignKeyConstraint, ForeignKey, Boolean
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, date

from sqlalchemy.sql.schema import PrimaryKeyConstraint
import random

from telebot.types import InputInvoiceMessageContent
# from config import correct_token
# from flask_jwt_extended import create_acess_token 

engine = create_engine('sqlite:///last5db.db?check_same_thread=False')
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

    __table_args__ = (
        PrimaryKeyConstraint(
            user1,
            user2),
            {}
        )


class Messages(Base):
    __tablename__ = 'msg'
    id = Column(Integer, primary_key=True)
    subject = Column(Integer, ForeignKey('users.id'))
    object = Column(Integer, ForeignKey('users.id'))
    text = Column(String)
    date = Column(String)



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

class Dislikes(Base):
    __tablename__= 'dislikes'
    subject = Column(Integer, ForeignKey('users.id'))
    object = Column(Integer, ForeignKey('users.id'))
    time = Column(String())
    __table_args__ = (
        PrimaryKeyConstraint(
            subject,
            object),
            {}
        )
    

# class SiteUsers(Base):
#     __tablename__ = 'siteusers'
#     login = Column(String, primary_key=True)
#     password = Column(String)
#     sec_level = Column(Integer)

#     def get_token(self):
#         token = create_acess_token(identity=self.login)
#         return token 

def user_pre_registration(chat_id):
    try:
        u1 = session.query(Users).filter(Users.id == chat_id).first()
    except:
        u1 = Users(id=chat_id, name='Незарегистрированный пользователь', is_delete=1)
        session.add(u1)
        session.commit()



def user_registration(chat_id, conf_arr):
    try:
        u1 = session.query(Users).filter(Users.id == chat_id).first()
        u1.age = conf_arr[1]
        u1.name = conf_arr[0]
        u1.reg_time = str(datetime.now())
        u1.photo = conf_arr[2]
        u1.about = conf_arr[3]
        u1.msfile = conf_arr[4]
        u1.inspection = conf_arr[5]
        u1.is_admin = 0
        u1.is_delete = 0
    except:
        u1 = Users(id=chat_id, age=conf_arr[1], name=conf_arr[0], reg_time=str(datetime.now()), photo=conf_arr[2], about=conf_arr[3], msfile=conf_arr[4], inspection=conf_arr[5], is_admin=0, is_delete=0)
        session.add(u1)
        chars = '+-/*!&$#?=@abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
                
        for _ in range(3):
            password =''
            for _ in range(10):
                password += random.choice(chars)
 
            t1 = Invites(invite=password, createdby=chat_id)
            session.add(t1)
            session.commit()

        session.add(u1)

    session.commit()

def check_user0(chat_id):
    arr = [] 
    is_exists = session.query(Dislikes.object).filter(Dislikes.subject == chat_id).all()
    for element in is_exists:
        arr.append(element[0])
    return arr

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


def get_mainpage():
    arr = []
    message_date_arr = [0 for _ in range(30)]
    users = session.query(Users.id).filter(Users.is_admin == 0, Users.is_delete == 0).all()
    date_arr = [0 for _ in range(30)]
    messages = session.query(Messages).all()
    ccunt = 0
    for element in messages:
        datetime_string = element.date[0:-7]
        # datetime_string = session.query(Messages.date).filter(Messages.id == element[0]).first()[0][0:-7]
        datetime_obj = datetime.strptime(datetime_string, '%Y-%m-%d %H:%M:%S').date()

        delt = datetime.now().date() - datetime_obj
        print(type(delt))
        
        d = delt.days
        print(type(d))

        if d < 30:
            if d == 0:
                ccunt += 1
            message_date_arr[-d] = message_date_arr[-d] + 1
    message_date_arr.append(ccunt)

    ccount = 0
    for element in users:
        arr2 = []
        datetime_string = session.query(Users.reg_time).filter(Users.id == element[0]).first()[0][0:-7]
        datetime_obj = datetime.strptime(datetime_string, '%Y-%m-%d %H:%M:%S').date()
        tr_inviter = session.query(Invites.createdby).filter(Invites.usedby == element[0]).first()[0]

        tr_inviter_name = session.query(Users.name).filter(Users.id == tr_inviter).first()[0]

        
        activated_invitess = session.query(Invites.invite).filter(Invites.usedby != None, Invites.createdby == element[0]).all()
        about = session.query(Users.about).filter(Users.id == element[0]).first()[0]
        for elem in activated_invitess:
            
            invite_us_id = session.query(Invites.usedby).filter(Invites.invite == elem[0]).first()[0]
            
            try:
                invite_us_name = session.query(Users.name).filter(Users.id == invite_us_id).first()[0]
            except:
                invite_us_name = 'Unregistered_user'

            arr2.append({"username": invite_us_name, "users_invite": elem[0], "invite_user_id": session.query(Invites.usedby).filter(Invites.invite == elem[0]).first()[0]})

        
        
        arr.append({'id': element[0], 'activated_invites': arr2, 'about': about, 'invites_count': session.query(Invites).filter(Invites.usedby == None, Invites.createdby == element[0]).count(), 'picture': session.query(Users.photo).filter(Users.id == element[0]).first()[0], 'name': session.query(Users.name).filter(Users.id == element[0]).first()[0], "age": session.query(Users.age).filter(Users.id == element[0]).first()[0], "joined_at": datetime_obj.strftime('%d.%m.%Y'), 'inspection_id': session.query(Users.inspection).filter(Users.id == element[0]).first()[0], "inviter_name": tr_inviter_name})
        delt = datetime.now().date() - datetime_obj
        print(type(delt))
        d = delt.days
        print(type(d))
        
        print(delt)
        if d < 30:
            if d == 0:
                ccount += 1
            else:
                date_arr[-d] = date_arr[-d] + 1
    date_arr.append(ccount)
    if len(arr) > 4:
        arr = arr[0:3]
    return {
        "newuserstate": date_arr,
        "newmessagestate": message_date_arr,
        "user_profiles": arr
    }

def get_user_profiles():
    arr = []
    users = session.query(Users.id).filter(Users.is_admin == 0, Users.is_delete == 0).all()
    for element in users:
        arr2 = []
        datetime_string = session.query(Users.reg_time).filter(Users.id == element[0]).first()[0][0:-7]
        datetime_obj = datetime.strptime(datetime_string, '%Y-%m-%d %H:%M:%S').date()
        tr_inviter = session.query(Invites.createdby).filter(Invites.usedby == element[0]).first()[0]
        tr_inviter_name = session.query(Users.name).filter(Users.id == tr_inviter).first()[0]
        activated_invitess = session.query(Invites.invite).filter(Invites.usedby != None, Invites.createdby == element[0]).all()
        about = session.query(Users.about).filter(Users.id == element[0]).first()[0]
        for elem in activated_invitess:
            invite_us_id = session.query(Invites.usedby).filter(Invites.invite == elem[0]).first()[0]
            print(invite_us_id)
            try:
                invite_us_name = session.query(Users.name).filter(Users.id == invite_us_id).first()[0]
            except:
                invite_us_name = 'Unregistered_user'

            arr2.append({"username": invite_us_name, "users_invite": elem[0], "invite_user_id": session.query(Invites.usedby).filter(Invites.invite == elem[0]).first()[0]})

        
        
        
        arr.append({'id': element[0], 'activated_invites': arr2, 'about': about, 'invites_count': session.query(Invites).filter(Invites.usedby == None, Invites.createdby == element[0]).count(), 'picture': session.query(Users.photo).filter(Users.id == element[0]).first()[0], 'name': session.query(Users.name).filter(Users.id == element[0]).first()[0], "age": session.query(Users.age).filter(Users.id == element[0]).first()[0], "joined_at": datetime_obj.strftime('%d.%m.%Y'), 'inspection_id': session.query(Users.inspection).filter(Users.id == element[0]).first()[0], "inviter_name": tr_inviter_name})



    return {

        "user_profiles": arr
    }


def get_current_user(user_id):
    
    invites_count = session.query(Invites).filter(Invites.usedby == None, Invites.createdby == user_id).count()
    activated_invitess = session.query(Invites.invite).filter(Invites.usedby != None, Invites.createdby == user_id).all()
    arr = []
    photo = session.query(Users.photo).filter(Users.id == user_id).first()[0]
  
    datetime_string = session.query(Users.reg_time).filter(Users.id == user_id).first()[0][0:-7]
    datetime_obj = datetime.strptime(datetime_string, '%Y-%m-%d %H:%M:%S').date()
    inspection = session.query(Users.inspection).filter(Users.id == user_id).first()[0]
    about = session.query(Users.about).filter(Users.id == user_id).first()[0]
    tr_inviter = session.query(Invites.createdby).filter(Invites.usedby == user_id).first()[0]
    tr_inviter_name = session.query(Users.name).filter(Users.id == tr_inviter).first()[0]
    activated_invitess = session.query(Invites.invite).filter(Invites.usedby != None, Invites.createdby == user_id).all()
    about = session.query(Users.about).filter(Users.id == user_id).first()[0]
    for elem in activated_invitess:
        invite_us_id = session.query(Invites.usedby).filter(Invites.invite == elem[0]).first()[0]
        invite_us_name = session.query(Users.name).filter(Users.id == invite_us_id).first()[0]
        arr.append({"username": invite_us_name, "users_invite": elem[0], "invite_user_id": session.query(Invites.usedby).filter(Invites.invite == elem[0]).first()[0]})
    return {
        "reg_time": datetime_obj.strftime('%d.%m.%Y'),
        "invites_count": invites_count,
        "user_id": user_id,
        "activated_invites": arr,
        "inspection": inspection,
        "about": about,
        "picture": photo
    }

def change_invites(user_id, count):
    invites_count = session.query(Invites).filter(Invites.usedby == None, Invites.createdby == user_id).count()
    if invites_count > count:
        for _ in range(invites_count - count):
            u1 = session.query(Invites).filter(Invites.usedby == None, Invites.createdby == user_id).first()
            session.delete(u1)
            session.commit()
    elif invites_count < count:
        chars = '+-/*!&$#?=@<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
        for _ in range(count - invites_count):
            password =''
            for _ in range(10):
                password += random.choice(chars)
            t1 = Invites(invite=password, createdby=user_id)
            session.add(t1)
            session.commit()
    return {
        "invites_count": count
    }

def ban_user(invite):
    u1 = session.query(Invites).get(invite)
    u1.usedby.is_delete = 1
    session.commit()

def invites_str():
    arr = session.query(Invites.invite).filter(Invites.usedby != None)
    arr2 = []
    for elem in arr:
        try:
            cr_by = session.query(Invites.createdby).filter(Invites.invite == elem[0]).first()[0]
            cr_by_name = session.query(Users.name).filter(Users.id == cr_by).first()[0]
            cr_by_pic = session.query(Users.photo).filter(Users.id == cr_by).first()[0]
            us_by = session.query(Invites.usedby).filter(Invites.invite == elem[0]).first()[0]
            us_by_name = session.query(Users.name).filter(Users.id == us_by).first()[0]
            us_by_pic = session.query(Users.photo).filter(Users.id == us_by).first()[0]
            arr2.append({"created_by": cr_by_name, "used_by": us_by_name, "cr_by_pic": cr_by_pic, 'us_by_pic': us_by_pic, "invite": elem[0]})
        except:
            continue
    return {
        "invites": arr2
    }

def date_sort(dic):
    datetime_string = dic['time'][0:-7]

    datetime_obj = datetime.strptime(datetime_string, '%Y-%m-%d %H:%M:%S')

    return datetime_obj

def closed_acess():
    users = session.query(Users.id).filter(Users.is_delete == 0, Users.is_admin == 0).all()
    arr = []
    for elem in users:
        arr2 = []
        umsgs = session.query(Messages.subject).filter(Messages.object == elem[0]).all()
        ussmgs = session.query(Messages.object).filter(Messages.subject == elem[0]).all()
        
        usmgs = []
        for t in ussmgs:
            if t[0] not in usmgs:
                usmgs.append(t[0])
        for element in umsgs:
            if element[0] not in ussmgs:
                usmgs.append(element[0])
        usmgs = set(usmgs)
        for element in usmgs:
            from_user_name = session.query(Users.name).filter(Users.id == elem[0]).first()[0]
            to_user_name = session.query(Users.name).filter(Users.id == element).first()[0]
            to_user_name_pic = session.query(Users.photo).filter(Users.id == element).first()[0]
        
            arr3 = []

            msg_from = session.query(Messages).filter(Messages.object == element, Messages.subject == elem[0]).all()
            
            msg_to = session.query(Messages).filter(Messages.subject == element, Messages.object == elem[0]).all()
            
            for msg in msg_to:
                arr3.append({'text': msg.text, 'from_name': to_user_name, 'time': msg.date, 'to_name': from_user_name})
            for msg in msg_from:
                arr3.append({'text': msg.text, 'from_name': from_user_name, 'time': msg.date, 'to_name': to_user_name})
            arr4 = sorted(arr3, key=date_sort)
            
            arr2.append({'to_user_name': to_user_name, 'to_user_name_pic': to_user_name_pic, 'messages': arr4})
        arr.append({'username': session.query(Users.name).filter(Users.id == elem[0]).first()[0], 'user_pic': session.query(Users.photo).filter(Users.id == elem[0]).first()[0],  'dialogs': arr2})
    return {'results': arr}

def sorted_dislike():
    current_date = datetime.now()

    for d in session.query(Dislikes):
        delta = current_date - datetime.strptime(d.time, '%Y-%m-%d')
        if int(str(delta).split(' ')[0]) > 7:
            session.delete(d)
            session.commit()



def find_friend(chat_id):
    global diction
    friend_arr0 = check_user0(chat_id)
    friend_arr1 = check_user1(chat_id)
    friend_arr2 = check_user2(chat_id)
    arr = []
    if friend_arr2:
        for e in friend_arr2:
            if e not in friend_arr1:
                if e not in friend_arr0:
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

def dislike(id, friend_id):
    d1 = Dislikes(subject=id, object=friend_id, time=str(date.today()))
    session.add(d1)
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
    # l1 = session.query(Likes).filter(Likes.subject == id, Likes.object == fr_id).one()
    # session.delete(l1)
    # session.commit()
    # l2 = session.query(Likes).filter(Likes.subject == fr_id, Likes.object == id).one()
    # session.delete(l2)
    # session.commit()
    session.add(d1)
    session.commit()

def cur_dial_find(id):
    w1 = session.query(UsersAndDialogs.user2).filter(UsersAndDialogs.user1 == id).first()
    if not w1: 
        w1 = session.query(UsersAndDialogs.user1).filter(UsersAndDialogs.user2 == id).first()

    return w1

def new_message_add(m_id, user_id, fr_id, text):
    m1 = Messages(id=m_id, subject=user_id, object=fr_id, text=text, date = str(datetime.now()))
    session.add(m1)
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
    invite_arr = []
    if True: 
        file = open('time.txt', 'r')
        text = file.read()
        file.close()
        print(text)
        datetime_obj = datetime.strptime(text, '%Y-%m-%d %H:%M:%S.%f')
        if (datetime.now() - datetime_obj).days >= 7:
            file = open('time.txt', 'w')
            file.write(str(datetime.now()))
            file.close()
            for user in session.query(Users).filter(Users.is_admin == 0, Users.is_delete == 0):
                token_arr = []
                b = session.query(Invites).filter(Invites.usedby == None, Invites.createdby == user.id).count()
                print(f'b - {b}')
                if b < 3:
                    chars = '+-/*!&$#?=@abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
                    print(3 - b)
                    for _ in range(3 - b):
                        password =''
                        for _ in range(10):
                            password += random.choice(chars)
                        token_arr.append(password)
                        t1 = Invites(invite=password, createdby=user.id)
                        session.add(t1)
                        session.commit()
    
    for invite in session.query(Invites).filter(Invites.usedby == None, Invites.createdby == id):
        invite_arr.append(invite.invite)
    return invite_arr
                    


# def get_user_invites(id):
#     invite_arr = []
#     for invite in session.query(Invites).filter(Invites.usedby == None, Invites.createdby == id):
#         invite_arr.append(invite.invite)
#         print(invite.invite)
#     token_arr = []
#     if len(invite_arr) == 0:
        
#         chars = '+-/*!&$#?=@<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
#         for _ in range(3):
#             password =''
#             for _ in range(10):
#                 password += random.choice(chars)
#             token_arr.append(password)
#             t1 = Invites(invite=password, createdby=id)
#             session.add(t1)
#             session.commit()
#     elif len(invite_arr) == 1:
#         token_arr.append(invite_arr)
#         chars = '+-/*!&$#?=@<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'

#         for _ in range(2):
#             password =''
#             for _ in range(10):
#                 password += random.choice(chars)
#             token_arr.append(password)
#             t1 = Invites(invite=password, createdby=id)
#             session.add(t1)
#             session.commit()


    # elif len(invite_arr) >= 2:
    #     for invite in invite_arr:
    #         token_arr.append(invite)
    # return token_arr

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

def check_dislike(id, fr_id):
    if session.query(Dislikes).filter(Dislikes.subject == id, Dislikes.object == fr_id).scalar():
        return True
    else:
        return False
    
def check_register(id):
    if session.query(Users).filter(Users.id == id).scalar():
        return True
    else:
        return False

def get_users():
    arr = []
    for user in session.query(Users).filter(Users.is_admin != 1, Users.is_delete != 1):
        arr.append(user.id)
    return arr

def parse_inspection():
    file1 = open("inspections.txt", "r")


    lines = file1.readlines()


    for line in lines:
        l1 = line.strip()
        if len(l1) == 3:
            l1 = f'0{l1}'
        l2 = Inspections(id=l1)
        session.add(l2)
    l3 = Inspections(id='0000')
    session.add(l3)
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
        
        t1 = Invites(invite=password, createdby=0)
        session.add(t1)
        session.commit()
    return token_arr



# def is_correct_login(login, password):
#     u1 = session.query(SiteUsers).get(login)
#     if u1: 
#         if u1.password == password:
#             return True


# def get_user_site(id):
#     u1 = session.query(SiteUsers).get(id)
#     return u1 

def print_invites():
    arr = []
    for elem in session.query(Invites).filter(Invites.createdby == 0, Invites.usedby == None):
        arr.append(elem.invite)
    return arr


Base.metadata.create_all(engine)