from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from firebase_admin import auth
from database.firebase import db

router = APIRouter(
    tags=["Auth"],
    prefix='/auth'
)

class User(BaseModel):
    email: str
    password: str

# Create new user
@router.post('/signup', status_code=201)
async def create_an_account(user_body: User):
    try:
        user = auth.create_user(
            email=user_body.email,
            password=user_body.password
        )
        # You can optionally store additional user information in Firebase
        user_data = {"email": user.email, "uid": user.uid}
        db.child("users").child(user.uid).set(user_data)
        return {"message": f"New user created with id: {user.uid}"}
    except auth.EmailAlreadyExistsError:
        raise HTTPException(
            status_code=409,
            detail=f"An account already exists for: {user_body.email}"
        )

# Login endpoint
@router.post('/login')
async def create_swagger_token(user: User):
    # Implement your login logic here
    # Typically, you'd verify the user's credentials, generate a JWT token, and return it.
    # You can use a library like PyJWT for JWT token creation.
    # For the sake of example, a simple response is provided here.
    return {"message": "Logged in successfully"}

# Protect route to get personal data
@router.get('/me')
async def secure_endpoint(current_user: dict = Depends(auth.get_user)):
    # The `Depends(auth.get_user)` decorator will require authentication.
    # You can now access the user's information.
    user_uid = current_user.uid
    # Fetch the user's data from Firebase or your database
    user_data = db.child("users").child(user_uid).get().val()
    return {"message": "Secure endpoint", "user_data": user_data}
