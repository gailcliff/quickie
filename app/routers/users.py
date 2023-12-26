from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel, EmailStr

from enum import Enum
import time

from . import woke


class Gendr(str, Enum):
    MALE = 'male'
    FEMALE = 'female'


class User(BaseModel):
    id: int | None = None
    user_name: str
    email: EmailStr

    country: str
    gender: Gendr | None = None


user_db: dict[float, User] = {}


async def verify_user(user: User):
    print(f"Sending verification email to {user.user_name}'s email: {user.email}")
    time.sleep(12)
    print("Verified user:", user)

# You can think of APIRouter as a "mini FastAPI" class. All the same operations are supported
# All the same parameters, responses, dependencies, tags, etc.

router = APIRouter(
    prefix='/users',    # you can either set these parameters here in the APIRouter constructor
    tags=['users']      # or set them in the 'include_router' function of your FastAPI instance
)
router.include_router(woke.router)  # you can include a router inside another router
# Make sure you do it before including router in the FastAPI app, so that the path operations from
# other_router are also included.
# You can nest routers as much as you need.


@router.get('/')
def get_all_users():
    return [user for user in user_db.values()]


@router.post('/', response_model_include={'id'})
def add_user(user: User, jobs: BackgroundTasks) -> User:
    user.id = round(time.time())
    user_db[user.id] = user

    jobs.add_task(verify_user, user)

    return user


@router.get('/{user_id}')
def get_user(user_id: float):
    return user_db[user_id]


@router.put('/{user_id}', response_model_include={'id'})
def update_user(user_id: float, user: User):
    user_db[user_id] = user
    return user
