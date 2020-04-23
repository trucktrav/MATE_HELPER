from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# pwd = 'C:\\Users\\travi\\PycharmProjects\\MATE_HELPER\\DB_Helper'
# database = pwd + '\\metrics_database.db'
# engine = create_engine('sqlite:///{0}'.format(database))
# Session = sessionmaker(bind=engine)
Base = declarative_base()
