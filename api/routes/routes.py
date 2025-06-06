from fastapi import APIRouter, HTTPException, status
from api.models.models import Classes, Bookings
from api.schemas.schemas import GetClasses, GetBookings, PostBookings, DeleteBookings, GetUserBookings
from datetime import datetime
home_router = APIRouter(prefix="/api", tags=["home"])

@home_router.on_event("startup")
async def create_initial_schedule():
    """Creates the initial class schedule when the API starts"""
    # Check if any classes exist
    existing_classes = await Classes.all()
    if not existing_classes:
        # Morning classes 9am-12pm
        for hour in range(9, 12):
            await Classes.create(
                name="Morning Yoga",
                bookings=10,
                date_time=datetime.now().replace(hour=hour, minute=0, second=0, microsecond=0),
                closed=False
            )
        
        # Lunch break 12pm-1pm
        await Classes.create(
            name="Lunch Break",
            bookings=0,
            date_time=datetime.now().replace(hour=12, minute=0, second=0, microsecond=0),
            closed=True
        )
        
        # Afternoon classes 1pm-6pm
        for hour in range(13, 19):
            await Classes.create(
                name="Afternoon Yoga",
                bookings=10,
                date_time=datetime.now().replace(hour=hour, minute=0, second=0, microsecond=0),
                closed=False
            )

@home_router.get("/classes")
async def get_classes():
    """Returns a list of all upcoming fitness classes"""
    classes = Classes.all()
    return await GetClasses.from_queryset(classes)

@home_router.post("/book")
async def create_booking(booking: PostBookings):
    """Creates a new booking for a fitness class"""
    # Check if class exists and has available slots
    fitness_class = await Classes.get_or_none(id=booking.class_id)
    if not fitness_class:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found"
        )
    
    if fitness_class.closed or fitness_class.bookings <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No available slots for this class"
        )
    
    # Check if user already has a booking for this class
    existing_booking = await Bookings.filter(
        class_id=booking.class_id,
        user_email=booking.user_email
    ).first()
    
    if existing_booking:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You already have a booking for this class"
        )
    
    # Create booking and update available slots
    booking_obj = await Bookings.create(**booking.dict())
    fitness_class.bookings -= 1
    await fitness_class.save()
    
    return await GetBookings.from_tortoise_orm(booking_obj)

@home_router.get("/bookings")
async def get_bookings(email: str):
    """Returns all bookings for a specific email address"""
    bookings = await Bookings.filter(user_email=email)
    return await GetBookings.from_queryset(Bookings.filter(user_email=email))

@home_router.delete("/bookings")
async def delete_booking(booking: DeleteBookings):
    """Deletes a booking and frees up the slot"""
    # Check if booking exists
    booking_obj = await Bookings.get_or_none(
        class_id=booking.class_id,
        user_email=booking.user_email,
        user_name=booking.user_name,
    )
    if not booking_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    
    # Get the class and update available slots
    fitness_class = await Classes.get(id=booking.class_id)
    fitness_class.bookings += 1
    await fitness_class.save()
    
    # Delete the booking and update IDs
    await booking_obj.delete()
    
    # Update IDs of remaining bookings
    remaining_bookings = await Bookings.all().order_by('id')
    for index, booking in enumerate(remaining_bookings, 1):
        booking.id = index
        await booking.save()
    
    return {"message": "Booking deleted successfully"}
