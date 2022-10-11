"""Seed file for Feedback app"""

from models import db, User, Feedback
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
    username="DerpyMan",
    password="hippoMonkey1980",
    email="sadface420@sadmail.com",
    first_name="Sad",
    last_name="Wad"
)

db.session.add_all([u1, u2])
db.session.commit()

'''
p1 = Feedback(
    title="",
    content="",
    username=""
)
'''

p1 = Feedback(
    title="Why",
    content="Should I worry?",
    username="DerpyMan"
)

p2 = Feedback(
    title="Whyn't",
    content="Should I caaaaaare?",
    username="DerpyMan"
)

p3 = Feedback(
    title="Tacos!",
    content="I'm carving tacos like a drunk college kid!",
    username="DerpyMan"
)

p4 = Feedback(
    title="My daiper is full",
    content="Did I spell diaper correctly?",
    username="HappySlappy"
)

db.session.add_all([p1, p2, p3, p4])
db.session.commit()