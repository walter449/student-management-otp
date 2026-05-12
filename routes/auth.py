from fastapi import APIRouter
from pydantic import BaseModel
import random
import requests
import os

router = APIRouter(prefix="/auth")

otp_storage = {}

API_KEY = os.getenv("BREVO_API_KEY")


class EmailRequest(BaseModel):
    email: str


class VerifyRequest(BaseModel):
    email: str
    otp: str


@router.post("/send-otp")
def send_otp(data: EmailRequest):

    try:

        otp = str(random.randint(100000, 999999))

        otp_storage[data.email] = otp

        url = "https://api.brevo.com/v3/smtp/email"

        headers = {
            "accept": "application/json",
            "api-key": API_KEY,
            "content-type": "application/json"
        }

        payload = {
            "sender": {
                "name": "UniGestion",
                "email": "walter.amaya@unisimon.edu.co"
            },
            "to": [
                {
                    "email": data.email
                }
            ],
            "subject": "Código OTP",
            "htmlContent": f"""
            <h2>Tu código OTP es:</h2>
            <h1>{otp}</h1>
            <p>No compartas este código con nadie.</p>
            """
        }

        response = requests.post(
            url,
            json=payload,
            headers=headers
        )

        if response.status_code == 201:

            return {
                "message": "OTP enviado correctamente"
            }

        return {
            "message": "Error enviando OTP",
            "details": response.text
        }

    except Exception as e:

        return {
            "message": f"Error interno: {str(e)}"
        }


@router.post("/verify-otp")
def verify_otp(data: VerifyRequest):

    saved_otp = otp_storage.get(data.email)

    if not saved_otp:

        return {
            "success": False,
            "message": "OTP no encontrado"
        }

    if saved_otp != data.otp:

        return {
            "success": False,
            "message": "OTP incorrecto"
        }

    return {
        "success": True,
        "message": "Login exitoso"
    }