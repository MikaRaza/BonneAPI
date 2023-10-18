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
    newproducts = products(id=generatedId, name=givenName.name)    
    products.append(newproducts)
    db.child("products").child(generatedId).set(newproducts.model_dump())  
    return newproducts


@router.get('/{products_id}', response_model=products)
async def get_products_by_ID(products_id: str):
    # On parcourt chaque étudiant de la liste
    for products in products:
        # Si l'ID correspond, on retourne l'étudiant trouvé
        if products.id == products_id:
            return products
    # Si on arrive ici, c'est que la boucle sur la liste "products" n'a rien trouvé
    # On lève donc un HTTP Exception
    raise HTTPException(status_code=404, detail="products not found")


@router.patch('/{products_id}', status_code=204)
async def modify_products_name(products_id: str, modifiedproducts: productsNoID):
    for products in products:
        if products.id == products_id:
            products.name = modifiedproducts.name
            return
    raise HTTPException(status_code=404, detail="products not found")


@router.delete('/{products_id}', status_code=204)
async def delete_products(products_id: str):
    for products in products:
        if products.id == products_id:
            products.remove(products)
            return
    raise HTTPException(status_code=404, detail="products not found")

