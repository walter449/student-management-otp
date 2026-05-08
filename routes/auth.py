from fastapi import APIRouter
from pydantic import BaseModel
import random
import smtplib
from email.mime.text import MIMEText

router = APIRouter(prefix="/auth")

otp_storage = {}

EMAIL = "walteramaya.ac@gmail.com"
PASSWORD = "ccvl gqzv yplv unqn"

class EmailRequest(BaseModel):
    email: str

class VerifyRequest(BaseModel):
    email: str
    otp: str

@router.post("/send-otp")
def send_otp(data: EmailRequest):

    otp = str(random.randint(100000, 999999))

    otp_storage[data.email] = otp

    message = MIMEText(f"Tu código OTP es: {otp}")

    message["Subject"] = "Código OTP"
    message["From"] = EMAIL
    message["To"] = data.email

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    server.login(EMAIL, PASSWORD)

    server.send_message(message)

    server.quit()

    return {
        "message": "OTP enviado correctamente"
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