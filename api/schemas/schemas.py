from pydantic import BaseModel, Field
from typing import Optional
from tortoise.contrib.pydantic import pydantic_model_creator
from api.models.models import Classes, Bookings

from datetime import datetime

GetClasses = pydantic_model_creator(Classes, name="classes")
GetBookings = pydantic_model_creator(Bookings, name="bookings")


class PostClasses(BaseModel):
    name: str = Field("Yoga Class", max_length=100)
    bookings: int = Field(0)
    date_time: datetime = Field(
        default_factory=lambda: datetime.now().replace(
            hour=9, minute=0, second=0, microsecond=0
        )
    )
    closed: bool = Field(False)

    @classmethod
    def create_schedule(cls):
        schedule = []
        # Morning classes 9am-12pm
        for hour in range(9, 12):
            schedule.append(cls(
                name="Morning Yoga",
                date_time=datetime.now().replace(hour=hour, minute=0, second=0, microsecond=0)
            ))
        
        # Lunch break 12pm-1pm
        schedule.append(cls(
            name="Lunch Break",
            date_time=datetime.now().replace(hour=12, minute=0, second=0, microsecond=0),
            closed=True
        ))
        
        # Afternoon classes 1pm-6pm
        for hour in range(13, 19):
            schedule.append(cls(
                name="Afternoon Yoga",
                date_time=datetime.now().replace(hour=hour, minute=0, second=0, microsecond=0)
            ))
        
        return schedule

class GetUserBookings(BaseModel):
    user_name:str = Field(..., max_length=100)
    user_email:str = Field(..., max_length=100)

class PostBookings(BaseModel):
    class_id:int = Field(...)
    user_name:str = Field(..., max_length=100)
    user_email:str = Field(..., max_length=100)
    date_time:datetime = Field(...)


class DeleteBookings(BaseModel):
    class_id:int = Field(...)
    user_name:str = Field(..., max_length=100)
    user_email:str = Field(..., max_length=100)
