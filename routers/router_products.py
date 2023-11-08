from typing import List
import uuid
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from classes.schema_dto import Product, ProductNoID
from database.firebase import db
router = APIRouter(prefix='/products', tags=['products'])



@router.get('/', response_model=List[Product])
async def get_product():
    products = []

    # Retrieve products from Firebase
    products_data = db.child("products").get().val()

    if products_data:
        # Convert Firebase data to a list of product objects
        for product_id, product_info in products_data.items():
            products.append(Product(id=product_id, name=product_info['name']))

    return products

@router.post('/', response_model=Product, status_code=201)
async def create_product(givenName: ProductNoID, givenPrice: ProductNoID): 
    generatedId = str(uuid.uuid4())   
    new_product = Product(id=generatedId, name=givenName.name, price=givenPrice) 
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
