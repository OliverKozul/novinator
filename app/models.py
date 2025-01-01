from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Subscriber(Base):
    __tablename__ = "subscribers"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    subjects = relationship("Subscription", back_populates="subscriber")

class Subscription(Base):
    __tablename__ = "subscriptions"
    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String, nullable=False)
    subscriber_id = Column(Integer, ForeignKey("subscribers.id"))
    subscriber = relationship("Subscriber", back_populates="subjects")
