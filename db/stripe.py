import stripe
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from dotenv import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY

stripe_credit = APIRouter()

class CheckoutSessionRequest(BaseModel):
    amount: int  # Amount to purchase credits

@stripe_credit.post("/create-checkout-session")
async def create_checkout_session(request: CheckoutSessionRequest):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': 'Credit Purchase',
                        },
                        'unit_amount': request.amount * 100,  # Amount in cents
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url="http://localhost:3000/success",
            cancel_url="http://localhost:3000/cancel",
        )
        return {"id": session.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
