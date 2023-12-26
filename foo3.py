import time
from typing import Union, Annotated, Any
from datetime import date
from pydantic import BaseModel, Field
from fastapi import FastAPI, Query, Path, Body, Header, Response, status, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import RedirectResponse, JSONResponse
from enum import Enum
import json


class Gender(str, Enum):
    MALE = 'male'
    FEMALE = 'female'


class Person(BaseModel):
    first_name: str = 'John'
    last_name: str = 'Doe'
    gender: Union[Gender, None] = None
    dob: date


class Item(BaseModel):
    id: int | None = None
    value: int = Field(alias='val', gt=0, le=100, description="The value, dummy!")


transformed_nums = [i**2 for i in range(100, 20, -1)]

app = FastAPI()


@app.get('/greeting')
def greet(name: str, greeting: Annotated[str | None, Query(max_length=10)] = None):
    return f"Hello {name}! {'Howdy' if greeting is None else greeting}!"


@app.get('/items')
def get_items():
    return transformed_nums


@app.get("/items/{item_id}")
def get_item(item_id: Annotated[int, Path(ge=0)]):
    return Item(id=item_id, val=transformed_nums[item_id])


@app.get('/person', response_model=Person)
def get_person(gender: Gender | None = None):

    p = Person(dob=date.today(), gender=gender)
    print("Person:", p)
    print("Person dict:", p.dict())

    encodable = jsonable_encoder(p)
    print("Person encodable:", encodable)
    print("Person json:", json.dumps(encodable))

    return JSONResponse(status_code=404, content=encodable)


@app.get('/people')
def get_people(accounts_ids: Annotated[
    list[int],
    Query(
        alias='id',
        title="Account ID's",
        description="Account numbers of the people to search for in the database",
        deprecated=True,
        # include_in_schema=False
    )
] = ...):
    return {
        "params": accounts_ids
    }


@app.post('/add-user-item')
def book_and_register(person: Annotated[Person, Body(alias='user', embed=True)], item: Item):
    transformed_nums.append(item.value)

    return {
        "new_item": {
            "user": person,
            "item": item
        }
    }


@app.post("/add-new-item", response_model=Item)
def add_item(item: Annotated[Item, Body(embed=True, alias='item')]):
    print("adding a new item...")

    # item = Item(**item_dict)
    transformed_nums.append(item.value)
    item.id = len(transformed_nums)

    return {
        "id": item.id,
        "val": item.value
    }


@app.post('/add-multiple-items')
def add_multiple(items: list[Item]) -> dict[str, list[Item]]:
    for item in items:
        item.id = len(transformed_nums)
        transformed_nums.append(item.value)

    return {
        "items": items
    }


@app.get('/headers')
def get_headers(
        user_agent: Annotated[str | None, Header()] = None,
        authority: Annotated[str | None, Header()] = None,
        path: Annotated[str | None, Header()] = None,
        scheme: Annotated[str | None, Header()] = None,
        accept: Annotated[Any | None, Header()] = None,
        accept_encoding: Annotated[Any | None, Header()] = None,
        cookie: Annotated[Any | None, Header()] = None
    ):
    return {
        "agent": user_agent,
        "authority": authority,
        "path": path,
        "scheme": scheme,
        "accept": accept,
        "encoding": accept_encoding,
        "cookie": cookie
    }


class BaseUser(BaseModel):
    id: int | None = None
    username: str


class UserIn(BaseUser):
    email: str
    full_name: str | None = None
    password: str


@app.post("/user/")
async def create_user(user: UserIn) -> BaseUser:
    user.id = time.time()
    return user


@app.get("/teleport")
async def get_teleport() -> Response:
    """
    Aye you wan teleport or what my G
    Follow this link
    ASAP
    """
    return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")


@app.get("/foo")
async def foo(response: Response):
    # pass
    # return Response(content="created", status_code=201, media_type='text')
    response.status_code = 201
    return response


@app.get("/pho0pho")
async def not_found():
    raise HTTPException(status_code=404, detail='not existing bud')


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('foo3:app', port=8000, reload=True)
