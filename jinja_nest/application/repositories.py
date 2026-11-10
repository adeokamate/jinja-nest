from abc import ABC, abstractmethod
from jinja_nest.domain.entities import Room, Booking

class RoomNotFoundException(Exception): pass
class BookingNotFoundException(Exception): pass

class RoomRepository(ABC):
    @abstractmethod
    def get_by_id(self, room_id: str) -> Room:
        pass
        
    @abstractmethod
    def save(self, room: Room) -> None:
        pass

class BookingRepository(ABC):
    @abstractmethod
    def get_by_id(self, booking_id: str) -> Booking:
        pass

    @abstractmethod
    def save(self, booking: Booking) -> None:
        pass