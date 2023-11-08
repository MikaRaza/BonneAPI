from pydantic import BaseModel

# Model Pydantic = Datatype
class Product(BaseModel):
    id: str
    name: str
    price: float

class ProductNoID(BaseModel):
    name: str
    price: float

    
class User(BaseModel):

    email: str
    password: str