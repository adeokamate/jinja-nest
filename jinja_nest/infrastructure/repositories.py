from typing import Dict
from jinja_nest.domain.entities import Room, Booking
from jinja_nest.application.repositories import (
    RoomRepository, 
    BookingRepository, 
    RoomNotFoundException, 
    BookingNotFoundException
)

class InMemoryRoomRepository(RoomRepository):
    def __init__(self):
        self._rooms: Dict[str, Room] = {}

    def get_by_id(self, room_id: str) -> Room:
        room = self._rooms.get(room_id)
        if not room:
            raise RoomNotFoundException(f"Room with ID {room_id} not found.")
        return room

    def save(self, room: Room) -> None:
        self._rooms[room.room_id] = room

class InMemoryBookingRepository(BookingRepository):
    def __init__(self):
        self._bookings: Dict[str, Booking] = {}

    def get_by_id(self, booking_id: str) -> Booking:
        booking = self._bookings.get(booking_id)
        if not booking:
            raise BookingNotFoundException(f"Booking with ID {booking_id} not found.")
        return booking

    def save(self, booking: Booking) -> None:
        self._bookings[booking.booking_id] = booking