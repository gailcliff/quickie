from fastapi import APIRouter, Body, Path

from typing import Any, Annotated


router = APIRouter()

items: list[Any] = []


@router.get('/')
def get_all_items():
    return items


@router.post('/')
def add_new_item(item: Annotated[Any, Body(embed=True)]):
    items.append(item)
    return {
        "item_id": len(items) - 1
    }


@router.get('/{item_id}')
def get_item_at(pos: Annotated[int, Path(alias='item_id')]):
    return {
        "item": items[pos]
    }
