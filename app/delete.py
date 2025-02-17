from database import engine, User, Post
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

def delete_post(post_id):
    post = session.query(Post).filter_by(id=post_id).first()
    if post:
        session.delete(post)
        session.commit()
        return { f"Post ID {post_id} deleted"}
    return {"error": "Post not found"}

def delete_user_and_posts(user_id):
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        posts = session.query(Post).filter_by(user_id=user_id).all()
        for post in posts:
            session.delete(post)
        session.delete(user)
        session.commit()
        return { f"User {user.username} and all posts deleted"}
    return {"error": "User not found"}