from fastapi import (
    FastAPI,
    Depends,
    Header,
    HTTPException,
    status
)
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
import random


class Multiplier:

    num: int
    multiples: list[int]

    def __init__(self, num: int | None = None, topline: int = 20):
        self.num = num if num else random.randrange(1, 10000)
        self.multiples = [self.num * i for i in range(1, topline + 1)]


async def verify_security_key(x_secret_key: Annotated[str | None, Header()] = None):
    if x_secret_key is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='No password provided')
    if x_secret_key != 'zdash9na9na':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid password')


allowed_origins = [
    'localhost'
]

app = FastAPI(dependencies=[Depends(verify_security_key)])
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
)


@app.get('/multiples/{number}')
def get_multiples(muls: Annotated[Multiplier, Depends(Multiplier)]):

    return {
        "multiples": muls.multiples
    }


@app.get('/investment_returns/{investor}')
async def invest_returns(investor: str, multiplier: Annotated[Multiplier, Depends()]):
    return {
        "investor": investor,
        "investment_returns": multiplier
    }


@app.get('/secret_resource')
async def fetch_secret_resource():
    return "here's the secret. shhh don't tell anyone"


@app.post('/stuff', status_code=201)
async def add_stuff():
    return "added stuff"
