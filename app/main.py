from fastapi import FastAPI, HTTPException, Form, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from crud import (
    create_user, create_post,
    read_all_users, read_all_posts_with_users,
    update_user_email, update_post_content,
    delete_user_and_posts, delete_post
)

appp = FastAPI()
templates = Jinja2Templates(directory="HTML")

@appp.get("/", response_class=HTMLResponse)
async def root():
    return """
    <p><a href="/users/new">Create User</a></p>
    <p><a href="/posts/new">Create Post</a></p>
    <p><a href="/users/list">List Users</a></p>
    <p><a href="/posts/list">List Posts</a></p>
    """

@appp.get("/users/new", response_class = HTMLResponse)
async def create_user_form(request: Request):
    return templates.TemplateResponse("create_user.html", {"request": request})

@appp.post("/users/")
async def api_create_user(username: str = Form(...), email: str = Form(...), password: str = Form(...)):
    try:
        create_user(username = username, email = email, password = password)
        return RedirectResponse("/users/list", status_code = 303)
    except Exception as e:
        raise HTTPException(status_code = 500, detail = f"Error creating user: {e}")

@appp.get("/posts/new", response_class = HTMLResponse)
async def create_post_form(request: Request):
    users = read_all_users()
    return templates.TemplateResponse("create_post.html", {"request": request, "users": users})

@appp.post("/posts/")
async def api_create_post(title: str = Form(...), content: str = Form(...), user_id: int = Form(...)):
    try:
        create_post(title = title, content = content, user_id = user_id)
        return RedirectResponse("/posts/list", status_code = 303)
    except Exception as e:
        raise HTTPException(status_code = 500, detail = f"Error creating post: {e}")

@appp.get("/users/list", response_class=HTMLResponse)
async def list_users(request: Request):
    users = read_all_users()
    return templates.TemplateResponse("list_users.html", {"request": request, "users": users})

@appp.get("/posts/list", response_class=HTMLResponse)
async def list_posts(request: Request):
    posts = read_all_posts_with_users()
    return templates.TemplateResponse("list_posts.html", {"request": request, "posts": posts})

@appp.get("/users/edit/{user_id}", response_class=HTMLResponse)
async def edit_user_form(request: Request, user_id: int):
    user = next((u for u in read_all_users() if u.id == user_id), None)
    if user:
        return templates.TemplateResponse("edit_user.html", {"request": request, "user": user})
    raise HTTPException(status_code = 404, detail = "User not found")

@appp.post("/users/edit/{user_id}")
async def api_edit_user(user_id: int, email: str = Form(...)):
    try:
        update_user_email(user_id, email)
        return RedirectResponse("/users/list", status_code=303)
    except Exception as e:
        raise HTTPException(status_code = 500, detail = f"Error updating user: {e}")

@appp.post("/users/delete/{user_id}")
async def api_delete_user(user_id: int):
    try:
        delete_user_and_posts(user_id)
        return RedirectResponse("/users/list", status_code=303)
    except Exception as e:
        raise HTTPException(status_code = 500, detail = f"Error deleting user: {e}")
    
@appp.post("/posts/delete/{post_id}")
async def api_delete_post(post_id: int):
    try:
        delete_post(post_id)
        return RedirectResponse("/posts/list", status_code=303)
    except Exception as e:
        raise HTTPException(status_code = 500, detail = f"Error deleting post: {e}")

@appp.get("/posts/edit/{post_id}", response_class = HTMLResponse)
async def edit_post_form(request: Request, post_id: int):
    posts = read_all_posts_with_users()
    post = next((p for p in posts if p.post_id == post_id), None)
    if post:
        return templates.TemplateResponse("edit_post.html", {"request": request, "post": post})
    raise HTTPException(status_code = 404, detail = "Post not found")

@appp.post("/posts/edit/{post_id}")
async def api_edit_post(post_id: int, content: str = Form(...)):
    try:
        update_post_content(post_id, content)
        return RedirectResponse("/posts/list", status_code = 303)
    except Exception as e:
        raise HTTPException(status_code = 500, detail = f"Error updating post: {e}")
