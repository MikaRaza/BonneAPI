from typing import List
import uuid
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database.firebase import db
router = APIRouter(prefix='/products', tags=['products'])

class Product(BaseModel):
    id: str
    name: str
    price: float
    availability: bool


class ProductNoID(BaseModel):
    name: str
    price: float
    
    
class User(BaseModel):

    email: str
    password: str

@router.get('/', response_model=List[Product])
async def get_product():
    firebase_object = db.child('products').get().val()
    result_array = [value for value in firebase_object.values()]
    return result_array

@router.post('/', response_model=Product, status_code=201)
async def create_product(givenName: ProductNoID):
    generatedId = str(uuid.uuid4())   
    new_product = Product(id=generatedId, name=givenName.name, price=givenName.price)
    db.child("products").child(generatedId).set(new_product.model_dump())  
    return new_product

@router.get('/{products_id}', response_model=Product)
async def get_products_by_ID(products_id: str):
    product = None

    # Retrieve a specific product by ID from Firebase
    product_data = db.child("products").child(products_id).get().val()

    if product_data:
        product = Product(id=products_id, name=product_data['name'])
    else:
        raise HTTPException(status_code=404, detail="Product not found")

    return product

@router.patch('/{products_id}', status_code=204)
async def modify_products_name(products_id: str, modified_product: ProductNoID):
    # Retrieve the product from Firebase
    product_data = db.child("products").child(products_id).get().val()

    if product_data:
        # Update the product's name with the new value
        product_data['name'] = modified_product.name

        # Update the product data in Firebase
        db.child("products").child(products_id).set(product_data)
    else:
        raise HTTPException(status_code=404, detail="Product not found")

@router.delete('/{products_id}', status_code=204)
async def delete_product(products_id: str):
    # Retrieve the product from Firebase
    product_data = db.child("products").child(products_id).get().val()

    if product_data:
        # Delete the product from Firebase
        db.child("products").child(products_id).remove()
    else:
        raise HTTPException(status_code=404, detail="Product not found")
