import os
from dotenv import load_dotenv

load_dotenv()

AUTHORIZED_CHANNEL_ID : str = os.getenv("DEBUG_CHANNEL_ID") or ""
WELCOME_CHANNEL_ID : int = int(os.getenv("WELCOME_CHANNEL_ID") or 1328935304437956610)
TURSO_TOKEN : str = os.getenv("TURSO_TOKEN") or ""
TURSO_URL : str = os.getenv("TURSO_URL") or ""

INVITE_XP = 30

COURSES = [
    {
        "name": "200+ Exercices Python pour apprendre à coder",
        "url": "https://www.udemy.com/course/exercices-python/?referralCode=F0901265E01B4DC4DDE98EF9AFF6"
    }
]

SOCIALS = {
    "youtube": "https://www.youtube.com/channel/UCEztUC2WwKEDkVl9c6oUoTw?sub_confirmation=1",
    "udemy": "https://www.udemy.com/user/thomas-collart/?referralCode=F0901265E01C7FDADABC",
    "tiktok": "https://www.tiktok.com/@commentcoder",
    "instagram": "https://www.instagram.com/commentcoder_com",
    "github": "https://github.com/commentcoder",
    "linkedin": "https://linkedin.com/in/thomascollart/"
}