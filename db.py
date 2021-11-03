from sqlalchemy import create_engine, MetaData, Table, Integer, String, Column, ForeignKeyConstraint, ForeignKey
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime


engine = create_engine('sqlite:///db.db')
engine.connect()
session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base(engine)



class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    age = Column(Integer)
    reg_time = Column(String())
    name = Column(String())
    photo = Column(String())
    about = Column(String())
    msfile = Column(String)
    inspection = Column(Integer, ForeignKey('inspections.id'))
    

class UsersAndDialogs(Base):
    __tablename__ = 'users_dialog'
    user1 = Column(Integer, ForeignKey('users.id'), primary_key=True)
    user2 = Column(Integer, ForeignKey('users.id'), primary_key=True)
    last_msg = Column(Integer, ForeignKey('msg.id'))


class Messages(Base):
    __tablename__ = 'msg'
    id = Column(Integer, primary_key=True)
    author = Column(Integer, ForeignKey('users.id'))
    text = Column(String)
    previous_msg = Column(Integer, ForeignKey('msg.id'))


class Inspections(Base):
    __tablename__ = 'inspections'
    id = Column(Integer, primary_key=True)
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


def user_registration(ide, ag, nam, phot, abou, msfil, inspectio):
    u1 = Users(id=ide, age=ag, name=nam, reg_time=str(datetime.now()), photo=phot, about=abou, msfile=msfil, inspection=inspectio)
    session.add(u1)
    session.commit()




# u1 = Users( 
#     id = 88053,
#     age = 15,
#     reg_time = datetime.now(),
#     name = 'Олег',
#     photo = '/huy/tro',
#     about = 'Работаю в ментовке 40 лет',
#     msfile = 'kfkfkf',
#     inspection = 1
# )


#