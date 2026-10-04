from fastapi_mail import FastMail,MessageSchema,ConnectionConfig,MessageType
from typing import List
from dotenv import load_dotenv
import os

load_dotenv()

MAIL_USERNAME=os.environ.get("MAIL_USERNAME")
MAIL_PASSWORD =os.environ.get("MAIL_PASSWORD")
MAIL_FROM=os.environ.get("MAIL_FROM")


conf = ConnectionConfig(
   MAIL_USERNAME=MAIL_USERNAME,
   MAIL_PASSWORD=MAIL_PASSWORD,
   MAIL_FROM=MAIL_FROM,
   MAIL_PORT=587,
   MAIL_SERVER="smtp.gmail.com",
   MAIL_FROM_NAME="Admin",
   MAIL_STARTTLS=True,
   MAIL_SSL_TLS=False,
   USE_CREDENTIALS=True,
   VALIDATE_CERTS=True
)

async def send_mail(email:List[str]):
   html = """
        <p>Dear Donor,</p>

    <p>
        Thank you for your generous donation.
        Your support means a lot to us and will help us continue our work.
    </p>

    <p>
        We truly appreciate your kindness and contribution.
    </p>

    <p>
        Best regards,<br>
        Admin Team
    </p>
   """
   message = MessageSchema(
       subject="Thank You for Your Donation",
       recipients=email,
       body=html,
       subtype=MessageType.html
   )

   fm = FastMail(conf)
   await fm.send_message(message)
   return {"message": "email has been sent"}
