from typing import List
import uuid
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from classes.schema_dto import products, productsNoID
from database.firebase import db
router = APIRouter(prefix='/products', tags=['products'])

class Product(BaseModel):
    id: str
    name: str

class ProductNoID(BaseModel):
    name: str

products_list = [
    Product(id="s1", name="Apple"),
    Product(id="s2", name="Poire"),
    Product(id="ss3", name="Table")
]

@router.get('/', response_model=List[products])
async def get_product():
    return products_list

@router.post('/', response_model=products, status_code=201)
async def create_product(givenName: productsNoID): 
    generatedId = str(uuid.uuid4())   
    new_product = Product(id=generatedId, name=givenName.name)    
    products_list.append(new_product)
    db.child("products").child(generatedId).set(new_product.model_dump())  
    return new_product

@router.get('/{products_id}', response_model=products)
async def get_products_by_ID(products_id: str):
    for product in products_list:
        if product.id == products_id:
            return product
    raise HTTPException(status_code=404, detail="Product not found")

@router.patch('/{products_id}', status_code=204)
async def modify_products_name(products_id: str, modified_product: productsNoID):
    for product in products_list:
        if product.id == products_id:
            product.name = modified_product.name
            return
    raise HTTPException(status_code=404, detail="Product not found")

@router.delete('/{products_id}', status_code=204)
async def delete_product(products_id: str):
    for product in products_list:
        if product.id == products_id:
            products_list.remove(product)
            return
    raise HTTPException(status_code=404, detail="Product not found")
