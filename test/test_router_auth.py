import httpx
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def secure_endpoint(token: str = Depends(oauth2_scheme)):
    # Vous pouvez ajouter ici la logique de validation du token
    # Par exemple, décodez le token, vérifiez s'il est valide, etc.
    # Si le token n'est pas valide, vous pouvez lever une HTTPException

    # Exemple basique : vérifier si le token est égal à "secure_token"
    if token != "secure_token":
        raise HTTPException(status_code=401, detail="Token non valide")

    # Logique supplémentaire si le token est valide
    return {"token": token}
def test_signup_and_login():
    # Test signup
    signup_data = {
        "email": "test@example.com",
        "password": "password123"
    }

    signup_response = httpx.post("http://127.0.0.1:8000/auth/signup", json=signup_data)
    assert signup_response.status_code == 409

    # Test login
    login_data = {
        "username": "test@example.com",
        "password": "password123"
    }

    login_response = httpx.post("http://127.0.0.1:8000/auth/login", data=login_data)
    assert login_response.status_code == 200
    assert "access_token" in login_response.json()

    # Extract the access token for further requests
    access_token = login_response.json()["access_token"]

    me_response = httpx.get("http://127.0.0.1:8000/auth/me", headers={"Authorization": f"Bearer {access_token}"})
    assert me_response.status_code == 200
    assert "desired_property" in me_response.json()  # Remplacez "desired_property" par la propriété attendue dans la répons