from datetime import date
from dataclasses import dataclass

@dataclass(frozen=True)
class BookingConfirmedEvent:
    booking_id: str
    room_id: str
    occurred_on: date = date.today()