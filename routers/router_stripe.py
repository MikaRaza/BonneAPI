from fastapi import APIRouter, Depends, Header, Request
from routers.router_auth import secure_endpoint
import stripe
from firebase_admin import auth
from database.firebase import db
router = APIRouter(tags=["Stripe"], 
                   prefix="/Stripe")

YOUR_DOMAIN = 'http://localhost'

from dotenv import dotenv_values
config = dotenv_values(".env")
stripe.api_key = config['STRIPE_SK']

@router.get('/checkout')
async def stripe_checkout():
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': 'price_1O51z4DKGmYqeYyOAyG0zLxK',
                    'quantity': 1
                },
            ],
            mode='subscription',
            payment_method_types=['card'],
            success_url=YOUR_DOMAIN + '/stripe/success', # à modif par u noveau endpoint pour ajouter le success -> webhook
            cancel_url=YOUR_DOMAIN + '/stripe/cancel',
            client_reference_id= "client_reference_id102312301230"
        )
        # return checkout_session
        response = RedirectResponse(url=checkout_session['url'])
        return response
    except Exception as e:
        return str(e)

@router.post('/webhook')

async def webhook_received(request:Request, stripe_signature: str = Header (None)):
    
    webhook_secret = "whsec_d54dd32ce8049b8ea5168eae93058053f324b55e2a1e21aa1128c5488f7f0d3c"
    data = await request.body()
    try:

        event = stripe.Webhook.construct_event(

            payload = data,

            sig_header=stripe_signature,

            secret=webhook_secret

        )
        event_data = event["data"]
        
    except Exception as e:
        return {"error" :str(e)}
    
    
    event_type = event['type']

    if event_type == 'checkout.session.completed':

        print('checkout session completed')

    elif event_type == 'invoice.paid':

        print('invoice paid')

        cust_email = event_data['object']['customer_email'] # Email de notre customer

        fireBase_user = auth.get_user_by_email(cust_email) # identifiant firebase correspondant (uid)

        cust_id=event_data['object']['customer'] # Stripe ref du customer

        item_id= event_data['object']['lines']['data'][0]['subscription_item']
        
        db.child("users").child(fireBase_user.uid).child("stripe").set({"item_id": item_id, "cust_id":cust_id}) # écriture dans la DB Firebase

    elif event_type == 'invoice.payment_failed':

        print('invoice payment failed')

    else:

        print(f'unhandled event: {event_type}')

 

    return {"status": "success"}

@router.get('/usage')
async def stripe_usage(userData: int = Depends(secure_endpoint)):
    fireBase_user= auth.get_user(userData['uid']) #identifint firebase correspondant (uid)
    stripe_data= db.child("users").child(fireBase_user.uid).child("stripe").get().val()
    cust_id = stripe_data["cust_id"]
    return stripe.Invoice.upcoming(customer=cust_id)
def increment_stripe(userId:str):
    firebase_user= auth.get_user(userId) #identifiant firebase correspondant (uid)]
    stripe_data = db.child("users").child(firebase_user.uid).child("stripe").get().val()
    print(stripe_data.values())
    item_id= stripe_data['item_id']
    stripe.SubscriptionItem.create_usage_record(item_id, quantity=1)
    return