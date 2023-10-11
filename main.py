
from fastapi import FastAPI

# Documentation
from documentation.description import api_description
from documentation.tags import tags_metadata

#Routers
import routers.router_products
# Initialisation de l'API
from fastapi import FastAPI


app = FastAPI(
    title="Bon API-tit!",
    description=api_description,
    openapi_tags= tags_metadata
)

app.include_router(routers.router_products.router)


