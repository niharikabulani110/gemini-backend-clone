import stripe
from app.models.user import User, SubscriptionTier
from app.core.config import settings
from fastapi.responses import JSONResponse
from app.database import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        return db
    except Exception:
        db.close()
        raise

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_stripe_checkout(user_id: int):
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price": "price_1RkAo9Q90nTltBUXni2ZtlQj",  # <-- Use your real recurring price ID here
            "quantity": 1,
        }],
        mode="subscription",
        success_url="http://localhost:3000/success",
        cancel_url="http://localhost:3000/cancel",
        metadata={"user_id": user_id}
    )
    return {"checkout_url": checkout_session.url}

def handle_stripe_webhook(payload, sig_header):
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return JSONResponse(status_code=400, content={"error": "Invalid payload"})
    except stripe.error.SignatureVerificationError:
        return JSONResponse(status_code=400, content={"error": "Invalid signature"})

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        user_id = session["metadata"]["user_id"]
        db = get_db()
        try:
            user = db.query(User).filter_by(id=user_id).first()
            if user:
                user.subscription = SubscriptionTier.PRO
                db.commit()
        finally:
            db.close()

    return JSONResponse(status_code=200, content={"status": "success"})

def get_subscription_status(user_id: int) -> str:
    db = get_db()
    try:
        user = db.query(User).filter_by(id=user_id).first()
        if not user:
            return "unknown"
        return user.subscription.value
    finally:
        db.close()
