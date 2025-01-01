from pydantic import BaseModel, EmailStr
from typing import List

class SubscriptionBase(BaseModel):
    subject: str

class SubscriptionCreate(SubscriptionBase):
    pass

class Subscription(SubscriptionBase):
    id: int

    class Config:
        orm_mode = True

class SubscriberBase(BaseModel):
    email: EmailStr

class SubscriberCreate(SubscriberBase):
    subjects: List[SubscriptionCreate]

class Subscriber(SubscriberBase):
    id: int
    subjects: List[Subscription]

    class Config:
        orm_mode = True
