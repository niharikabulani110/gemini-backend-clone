from fastapi import APIRouter, Request, HTTPException
from app.services.stripe_service import handle_stripe_webhook

router = APIRouter()

@router.post("/webhook/stripe")
async def stripe_webhook(request: Request):
    try:
        payload = await request.body()
        sig_header = request.headers.get("stripe-signature")
        return handle_stripe_webhook(payload, sig_header)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 