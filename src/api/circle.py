from typing import Callable,Optional
from fastapi import FastAPI, APIRouter, Body, HTTPException
from app.__internal import Function
import requests
from pydantic import BaseModel
import json
import uuid
import datetime
from config import cfg

class PaymentReq(BaseModel):
    amount: str
    description: Optional[str]
    card_exp: str
    line1: str
    line2: Optional[str]
    city: str
    district: str
    postalCode: str
    country: str
    name: str
    email: str
    cardData:str
    keyid:str


class CircleApi(Function):
    def __init__(self, error: Callable):
        ...

    def Bootstrap(self, app: FastAPI):
        router = APIRouter(prefix="/api/circle", tags=["circle"])

        @router.get("/")
        def index():
            return {"hello": "world"}

        @router.get("/getpublickey")
        def getPublicKey():
            try:
                baseurl= cfg.CIRCLE_API_URL
                url =  baseurl + "/encryption/public"
                headers = {
                    "accept": "application/json",
                    "authorization": "Bearer "+ cfg.CIRCLE_API_KEY,
                }
                response = requests.get(url, headers=headers)
                r= response.json()['data']
                return r
            except Exception:
                raise HTTPException(status_code=400, detail=f"Circle Service returned an error: {response.text}")
        @router.post("/payment")
        def createCard(paymentreq:PaymentReq):
            baseurl= cfg.CIRCLE_API_URL
            try:
                yaer= str(datetime.datetime.now().year)[:2]
                month= int(paymentreq.card_exp.split(" / ")[0])
                yearInput=int(paymentreq.card_exp.split(" / ")[1])  
                year=yaer + str(yearInput)

            except Exception:
                raise HTTPException(status_code=400, detail=f"Invalid card expiry date")
            try:
                        
                id=uuid.uuid4()
                url = baseurl +"/cards"
                cardpayload = {
                "billingDetails": {
                "name": paymentreq.name,
                "city": paymentreq.city,
                "country":paymentreq.country,
                "line1":paymentreq.line1, 
                "line2": "Suite 1",
                "district": paymentreq.district,
                "postalCode": paymentreq.postalCode,
                },
                "metadata": {
                "email": paymentreq.email,
                "sessionId": "DE6FA86F60BB47B379307F851E238617",
                "ipAddress": "244.28.239.130"
                },
                "idempotencyKey": f"{id}",
                "keyId":  paymentreq.keyid,
                "encryptedData":  paymentreq.cardData,
                "expMonth": month,
                "expYear": int(year),
                }

                postheader = {
                    "accept": "application/json",
                    "content-type": "application/json",
                    "authorization": "Bearer "+ cfg.CIRCLE_API_KEY,
                }

                cardresponse = requests.post(url, json=cardpayload, headers=postheader)
                cardresponseData=cardresponse.json()
            except Exception:
                raise HTTPException(status_code=400, detail=f"Circle Service returned an error: {cardresponse.text}")
            try:
                cardId=cardresponseData['data']['id']
            except Exception:
                raise HTTPException(status_code=400, detail=f"{cardresponseData['message']}")
            try:
                url = baseurl + "/payments"
                id=uuid.uuid4()
                payment_payload = {
                    "metadata": {
                        "email": paymentreq.email,
                        "ipAddress": "244.28.239.130",
                        "sessionId": "DE6FA86F60BB47B379307F851E238617"
                    },
                    "amount": {
                        "currency": "USD",
                        "amount": paymentreq.amount
                    },
                    "autoCapture": True,
                    "source": {
                        "id": f"{cardId}",
                        "type": "card"
                    },
                    "idempotencyKey": f"{id}",
                    "keyId": paymentreq.keyid,
                    "verification": "cvv",
                    "description": "Payment",
                }

                paymentresponse = requests.post(url, json=payment_payload, headers=postheader)
                
                return paymentresponse.json()
            except Exception:
                raise HTTPException(status_code=400, detail=f"{paymentresponse.text}")
                
                
        app.include_router(router)
