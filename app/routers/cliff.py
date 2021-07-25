import logging
from typing import List

from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder

from app.crud.item import Item
from app.schemas.item import ItemUpdate, ItemCreate, ItemRead

LOGGER = logging.getLogger()
cliff_router = APIRouter()


@cliff_router.get("/items", response_model=List[ItemRead])
async def read_item(skip: int = 0, limit: int = 100):
    items = await Item.get(limit=limit, skip=skip)
    if not items:
        raise HTTPException(status_code=404, detail="No items found")
    return items


@cliff_router.get("/item/{item_id}", response_model=ItemRead)
async def read_item_by_id(item_id: int):
    items = await Item.get_item_by_id(id=item_id)
    if not items:
        raise HTTPException(status_code=404, detail=f"No item found with id {item_id}")
    return items


@cliff_router.get("/item/brand/{brand_name}")
async def read_item_by_brand_name(brand_name: str):
    brand_item = await Item.get_item_by_brand_name(brand_name=brand_name)
    if not brand_item:
        raise HTTPException(
            status_code=404, detail=f"No item found with brand_name {brand_name}"
        )
    return brand_item


@cliff_router.post("/item")
async def create_item(item_in: ItemCreate):
    item_in = jsonable_encoder(item_in)
    item = await Item.create(item_in)
    return item


@cliff_router.patch("/item/{id}")
async def update_item(id: int, updated_item: ItemUpdate):
    item = await Item.get_item_by_id(id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    updated_item = updated_item.dict(exclude_unset=True)
    if not updated_item:
        raise HTTPException(
            status_code=404, detail="Empty body. Cannot update the item."
        )
    item = await Item.update(id=id, item_obj=updated_item)
    return item


@cliff_router.delete("/item/{id}")
async def delete_item(id: int):
    item = await Item.get_item_by_id(id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    query_id = await Item.remove(id=id)
    if query_id:
        return {"success": True, "id": query_id}
    return {"success": False}