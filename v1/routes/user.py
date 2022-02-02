
from fastapi import APIRouter
from core.models.user import users
from core.config.db import conn


user = APIRouter()


#Get All Users
@user.get(
    path="/users",
    tags=["Users"],
    summary="Get all users from the app"
)
def get_users():
    return conn.execute(users.select()).fetchall()