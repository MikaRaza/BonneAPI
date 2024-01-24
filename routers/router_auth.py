from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from classes.schema_dto import User
from firebase_admin import auth
from database.firebase import authSession

router = APIRouter(
    tags=["Auth"],
    prefix='/auth'
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
def get_current_user(provided_token: str = Depends(oauth2_scheme)):
    decoded_token = auth.verify_id_token(provided_token)
    decoded_token['idToken'] = provided_token
    return decoded_token
def secure_endpoint(current_user: User = Depends(get_current_user)):
    """
    Secure endpoint example. The function depends on the current user being authenticated.
    """
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Get the current user based on the OAuth2 token.
    """
    user_data = db.child("users").child(token).get().val()
    if user_data:
        return UserInDB(**user_data)
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")
# create new user
@router.post('/signup', status_code=201)
async def create_an_account(user_body: User):
    # Check if user with the same email exists
    existing_user = auth.get_user_by_email(user_body.email)
    if existing_user:
        raise HTTPException(
            status_code=409,
            detail=f"Un compte existe déjà pour : {user_body.email}"
        )

    # Create a new user
    user = auth.create_user(
        email=user_body.email,
        password=user_body.password
    )
    return {
        "message": f"Nouvel utilisateur créé avec id : {user.uid}"
    }
# Login endpoint
@router.post('/login')
async def create_swagger_token(user_credentials: OAuth2PasswordRequestForm = Depends()):
    try:
        print(user_credentials)
        user = authSession.sign_in_with_email_and_password(email=user_credentials.username, password=user_credentials.password)
        token = user['idToken']
        print(token)
        return {
            "access_token": token,
            "token_type": "bearer"
        }
    except:
        raise HTTPException(
            status_code=401, details="Invalid Credentials"
        )

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")




