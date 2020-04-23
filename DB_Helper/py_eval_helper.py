from sqlalchemy import Column, String, Integer
from DB_Helper.base import Base
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# pwd = 'C:\\Users\\travi\\PycharmProjects\\MATE_HELPER\\DB_Helper'
# database = pwd + '\\metrics_database.db'
# engine = create_engine('sqlite:///{0}'.format(database))
# Session = sessionmaker(bind=engine)
# Base = declarative_base()


class EvalHelp(Base):
    __tablename__ = 'tbl_eval'
    id = Column('_id', Integer, primary_key=True)
    name = Column('str_name', String)
    function = Column('str_function', String)
    display = Column('str_display', String)
    type = Column('str_type', String)


class HeaderHelp(Base):
    __tablename__ = 'tbl_header'
    id = Column('_id', Integer, primary_key=True)
    name = Column('header', String)


