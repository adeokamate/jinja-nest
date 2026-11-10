from enum import Enum
from .exceptions import RoomUnavailableException, MissingOccupantException
from .value_objects import BookingPeriod, PrimaryOccupant

class RoomStatus(Enum):
    AVAILABLE = "AVAILABLE"
    RESERVED = "RESERVED"
    MAINTENANCE = "MAINTENANCE"
    OCCUPIED = "OCCUPIED"

class Room:
    def __init__(self, room_id: str, base_price: float):
        self.room_id = room_id
        self.base_price = base_price
        self.status = RoomStatus.AVAILABLE

    def reserve(self):
        if self.status != RoomStatus.AVAILABLE:
            raise RoomUnavailableException(f"Cannot reserve room. Current status: {self.status.name}")
        self.status = RoomStatus.RESERVED

class BookingStatus(Enum):
    DRAFT = "DRAFT"
    CONFIRMED = "CONFIRMED"

class Booking:
    def __init__(self, booking_id: str, room_id: str, period: BookingPeriod, calculated_fee: float):
        self.booking_id = booking_id
        self.room_id = room_id
        self.period = period
        self.calculated_fee = calculated_fee
        self.status = BookingStatus.DRAFT
        self.occupant: PrimaryOccupant | None = None

    def attach_occupant(self, occupant: PrimaryOccupant):
        self.occupant = occupant

    def confirm_booking(self):
        if not self.occupant:
            raise MissingOccupantException("Cannot confirm booking without a Primary Occupant.")
        self.status = BookingStatus.CONFIRMED