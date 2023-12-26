from typing import Annotated

from pydantic import Required

from fastapi import FastAPI, Query, Path
import random

app = FastAPI()


@app.get('/profile/me')
def get_current_profile():

    return {
        "user": "current user"
    }


@app.get("/profile/{user_name}")
def get_profile(user_name: str, is_current_user: bool = False):
    return {
        "user": user_name,
        "meta": f"This user is {'current' if is_current_user else 'not current'}"
    }


@app.get("/profile/filter/by")
def filter_profile(
        user_name: Annotated[str, Query(min_length=4)] = Required,
        age: Annotated[int | None, Query(gt=0, lt=100)] = None):
    return {
        "matches": [
            {
                "user_name": user_name,
                "age": age
            }
        ]
    }


@app.get('/users/age/{age}')
def get_users_by_age(age: Annotated[int, Path(description="Get users whose age is the one specified", ge=6, le=100)]):
    return {
        "users_at_least": age,
        "how_many": int(random.random() * 1_000_000)
    }


@app.get("/files/{file}")
def get_file(file: str):
    content = ""

    try:
        with open(file, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        pass

    return content


if __name__ == '__main__':
    import uvicorn
    uvicorn.run("quick:app", reload=True)
