from sqlalchemy import Column,String,Integer,Date,DateTime
from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin

Base = declarative_base()


class leave_note(Base):
    __tablename__ = 'leavenote'
    num_id = Column(Integer,primary_key=True,unique=True)
    write_time = Column(Date)
    person = Column(String(10))
    notetext = Column(String(500))
    status = Column(Integer)
    check_time = Column(DateTime)
    upload_time = Column(DateTime)


class meetingrecord(Base):
    __tablename__ = 'meetingrecord'
    id = Column(Integer,primary_key=True,unique=True)
    time = Column(Date)
    host = Column(String(12))
    recordperson = Column(String(10))
    late = Column(String(45))
    leave = Column(String(45))
    join = Column(String(60))
    recordtext = Column(String(500))


class notice(Base):
    __tablename__ = 'notice'
    id = Column(Integer,primary_key=True,unique=True)
    time = Column(DateTime)
    person = Column(String(10))
    noticetext = Column(String(500))


# basicinfo表
class Basicinfo(UserMixin,Base):
    __tablename__ = 'basicinfo'
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=True)
    name = Column(String(10))
    department = Column(String(30))
    zhiwei = Column(String(10))
    password = Column(String(73))


# detailinfo表
class detailinfo(Base):
    __tablename__="detailinfo"
    id=Column(Integer,primary_key=True,unique=True)
    name=Column(String(10))
    school=Column(String(15))
    Class=Column(String(20))
    tel=Column(String(15))
    qq=Column(String(20))
    email=Column(String(20))
    image=Column(String(50))
    position=Column(String(10))
    birth=Column(Date)
    sex=Column(Integer)
    department=Column(String(20))
    place=Column(String(35))


class freetime(Base):
    __tablename__="freetime"
    id=Column(Integer,primary_key=True,unique=True)
    timea = Column(Integer)
    timeb = Column(Integer)
    timec = Column(Integer)
    timed = Column(Integer)
    timee = Column(Integer)
    timef = Column(Integer)
    timeg = Column(Integer)
    timeh = Column(Integer)
    timei = Column(Integer)
    timej = Column(Integer)
    timek = Column(Integer)
    timel = Column(Integer)
    timem = Column(Integer)
    timen = Column(Integer)
