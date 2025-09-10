import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.core.mail import send_mail

def generate_magic_link_token(user):
    payload = {
        "user_id": user.id,
        "purpose": "magic_link",
        "exp": datetime.utcnow() + timedelta(minutes=10)
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    return token

def send_email(token,user):
    link = f"http://127.0.0.1:8000/users/changepassword_link/?token={token}"
    send_mail(
        "لینک ورود",
        f"برای ورود کلیک کن: {link}",
        "mohammadrezaheidarnia@gmail.com",
        [user.email],
    )
