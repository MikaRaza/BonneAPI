from pydantic import BaseModel

# Model Pydantic = Datatype
class products(BaseModel):
    id: str
    name: str

class productsNoID(BaseModel):
    name: str