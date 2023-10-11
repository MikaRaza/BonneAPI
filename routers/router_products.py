from typing import List
import uuid
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from classes.schema_dto import products, productsNoID

router = APIRouter(prefix='/products', tags=['products'])

# Model Pydantic = Datatype
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

# Verbs + Endpoints
@router.get('/', response_model=List[products])
async def get_product():
    return products_list

# 1. Exercice (10min) Create new products: POST
# response_model permet de définir de type de réponse (ici nous retournons le products avec sont id)
# status_code est défini sur 201-Created car c'est un POST
@router.post('/', response_model=products, status_code=201)
async def create_product(givenName: productsNoID):
    # génération de l'identifiant unique
    generatedId = str(uuid.uuid4())
    # création de l'object/dict products
    newproducts = products(id=generatedId, name=givenName.name)
    # Ajout du nouveau products dans la List/Array
    products.append(newproducts)
    # Réponse définie par le products avec son ID
    return newproducts

# 2. Exercice (10min) products GET by ID
# response_model est un products car nous souhaitons trouver l'étudiant correspondant à l'ID
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

# 3. Exercice (10min) PATCH products (name)
@router.patch('/{products_id}', status_code=204)
async def modify_products_name(products_id: str, modifiedproducts: productsNoID):
    for products in products:
        if products.id == products_id:
            products.name = modifiedproducts.name
            return
    raise HTTPException(status_code=404, detail="products not found")

# 4. Exercice (10min) DELETE products
@router.delete('/{products_id}', status_code=204)
async def delete_products(products_id: str):
    for products in products:
        if products.id == products_id:
            products.remove(products)
            return
    raise HTTPException(status_code=404, detail="products not found")

