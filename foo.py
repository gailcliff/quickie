from datetime import date, datetime
from typing import Optional, Union

from pydantic import BaseModel


def foo(bar: tuple[int, bool, str, float]):
    pass


foo((3,False,"",0))


def maz(lar: dict[str, list[int]]):

    for choo, loo in lar.items():
        print(choo.upper())


maz({
    "foo": []
})


def say_hi(name: Union[str, int, None] = None):
    print(f"Hey {name}!")


say_hi()


class Person(BaseModel):
    name: str
    dob: date
    gender: str | None = None
    hobbies: list[str] = []


person_map = {
    "name": "Cliff",
    "dob": '2001-11-17',
    # "gender": "male",
    "hobbies": [1, "coding", "ideation", "introspection", "awesomeness", True]
}

person = Person(name='foo')
print(person)
