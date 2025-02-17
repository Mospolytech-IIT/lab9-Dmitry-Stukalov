from database import engine, User, Post
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

def get_all_users():
    users = session.query(User).all()
    return users 

def get_all_posts_with_users():
    posts = session.query(Post).all()
    result = []
    for post in posts:
        result.append({
            "post_id": post.id,
            "title": post.title,
            "content": post.content,
            "user": {
                "username": post.user.username,
                "email": post.user.email
            }
        })
    return result  

def get_posts_by_user(user_id):
    posts = session.query(Post).filter_by(user_id = user_id).all()
    result = []
    for post in posts:
        result.append({
            "post_id": post.id,
            "title": post.title,
            "content": post.content
        })
    return result  