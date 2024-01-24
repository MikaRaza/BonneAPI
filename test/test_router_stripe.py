import httpx

def test_stripe_checkout():
    response = httpx.get("http://127.0.0.1:8000/Stripe/checkout")
    assert response.status_code == 200
    assert "url" in response.json()

def test_stripe_usage(auth_user):
    response = auth_user.get("/Stripe/usage")
    assert response.status_code == 200
    assert "desired_property" in response.json()  # Remplacez "desired_property" par la propriété attendue dans la réponse
