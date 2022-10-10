"""Seed file for Feedback app"""

from models import db, User
from app import app

db.drop_all()
db.create_all()

'''
u1 = User(
    username="",
    password="",
    email="",
    first_name="",
    last_name=""
)
'''

u1 = User.register(
    username="HappySlappy",
    password="islappeople",
    email="slapper69@gmail.com",
    first_name="Happy",
    last_name="Slappy"
)

u2 = User.register(
    username="SaddyWaddy",
    password="iamasadwad",
    email="sadface420@sadmail.com",
    first_name="Sad",
    last_name="Wad"
)

db.session.add_all([u1, u2])
db.session.commit()