from datetime import datetime, timedelta
from enum import Enum
from typing import Annotated

from fastapi import FastAPI, Body
from pydantic import BaseModel, Field, HttpUrl
from main import Gender


class CarType(str, Enum):
    SUV = 'suv'
    SUPER = 'super-car'
    SEDAN = 'sedan'
    CABRIOLET = 'cabriolet'
    HYPER = 'hyper-car'


class Price(BaseModel):
    price: float = Field(gt=100, description="We don't sell cars less than 100 bucks")
    currency: str


class Car(BaseModel):
    brand_name: str = Field(max_length=10)
    color: str
    car_type: CarType
    price: Price
    icon: HttpUrl
    images: list[HttpUrl]


class CarBuyerProfile(BaseModel):
    gender: Gender
    age: int = Field(le=30, description="Our buyers are not old")
    industry: str
    net_worth: int
    car: Car | None = None


app = FastAPI()


@app.post("/cars")
def car_bid(car: Annotated[Car, Body(alias='vehicle')], buyer_profile: CarBuyerProfile, buyer_name: Annotated[str, Body(alias='buyer', max_length=10)]):
    if buyer_profile.car is None:
        buyer_profile.car = car

    buyer_profile_dict = buyer_profile.dict()
    buyer_profile_dict['buyer_name'] = buyer_name

    timedelta()
    return {
        "buyer": buyer_profile,
        "buy_date": datetime.now()
    }


@app.post("/foobar")
def foobar(choo: Annotated[dict[int, int], Body()]):
    return choo


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('foo2:app', port=10000, reload=True)
