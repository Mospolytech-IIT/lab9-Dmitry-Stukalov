from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

username = 'postgres'
password = 'password'
host = 'localhost'
port = '5432'
database = 'Laba_9_BackEnd'

connection_string = f'postgresql://{username}:{password}@{host}:{port}/{database}'
engine = create_engine(connection_string)

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key = True, autoincrement = True)
    username = Column(String(255), unique = True, nullable = False)  
    email = Column(String(255), unique = True, nullable = False)     
    password = Column(String, nullable = False)

class Post(Base):
    __tablename__ = 'posts'
    
    id = Column(Integer, primary_key = True, autoincrement = True)
    title = Column(String, nullable = False)
    content = Column(Text, nullable = False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable = False)

    user = relationship("User", backref = "posts")

Base.metadata.create_all(engine)
