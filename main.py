from enum import Enum
from typing import Union, Annotated

from fastapi import FastAPI, Query, Body, Header
from pydantic import BaseModel


class Gender(str, Enum):
    MALE = 'male'
    FEMALE = 'female'
    NA = None


class Pet(BaseModel):
    animal: str
    name: str
    gender: Union[Gender, None] = None


pets = [
    Pet(animal="dog", name="symba", gender=Gender.MALE),
    Pet(animal="dog", name="chocked", gender=Gender.FEMALE),
    Pet(animal="stallion", name="meg", gender=Gender.MALE, ),
    Pet(animal="lizard", name="lizzo"),
    Pet(animal="cat", name="kitty", gender=Gender.FEMALE),
    Pet(animal="goat", name="cliff", gender=Gender.MALE)
]

quickie = FastAPI()


@quickie.get("/")
async def home(user_agent: Annotated[str, Header()]):
    return f"Hello World! I am agent 007, you are agent: {user_agent}"


@quickie.get("/pets")
async def get_pets():
    return pets


@quickie.get("/pets/{pet_id}")
async def get_animal(pet_id: int, name: Union[str, None] = None):
    return {
        "pet": pets[pet_id],
        "search_name": name
    }


@quickie.get("/multiple/pets")
# async def get_multiple_by_name(arg: list[str] | None = None):
async def get_multiple_by_name(
        name_list: Annotated[
            set[str] | None,
            Query(
                alias="user-name",
                title="Multiple search list",
                description="Searching for multiple pets using multiple names",
                deprecated=True,
                include_in_schema=True
            )
        ] = None):

    print(f"name list: {name_list}")

    if name_list is not None:
        return {
            "requested_names": name_list,
            "results": (pet for pet in pets if pet.name in name_list)
        }
    return []


@quickie.get("/pets/gender/{gender}")
async def get_by_gender(gender: Union[Gender, None] = None):
    pets_by_gender = (pet for pet in pets if pet.gender == gender)

    return {
        f"{gender}_pets": pets_by_gender
    }


@quickie.put('/pets/{pet_id}')
async def update_pet(pet_id: int, name: str):
    pet = pets[pet_id]
    pet.name = name

    return {
        "updated_pet_id": pet_id,
        **pet.dict()
    }


@quickie.post('/pets')
async def add_pet(pet: Annotated[Pet, Body(embed=True)]):
    pets.append(pet)


@quickie.delete('/pets/{pet_id}')
async def delete_pet(pet_id: int):
    del pets[pet_id]


@quickie.get("/pets/filter/by")
async def get_by_details(animal: str | None = None, name: str | None = None, gender: Gender | None = None):
    fetched_pets = []

    if animal is not None and name is not None:
        fetched_pets = (pet for pet in pets if pet.name == name and pet.animal == animal)
    if animal is not None and name is None:
        fetched_pets = (pet for pet in pets if pet.animal == animal)
    if animal is None and name is not None:
        fetched_pets = (pet for pet in pets if pet.name == name)
    if gender is not None and animal is None and name is None:
        return (pet for pet in pets if pet.gender == gender)

    if gender is not None:
        return (pet for pet in fetched_pets if pet.gender == gender)
    else:
        return fetched_pets


if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:quickie", port=9000, reload=True)
