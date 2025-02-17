from database import engine, User, Post
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

def add_user(username: str, email: str, password: str):
    user = User(username = username, email = email, password = password)
    session.add(user)
    session.commit()
    return user

def add_post(title: str, content: str, user_id: int):
    post = Post(title = title, content = content, user_id = user_id)
    session.add(post)
    session.commit()
    return post