from jinja_nest.domain.events import BookingConfirmedEvent
from jinja_nest.application.repositories import RoomRepository

class BookingConfirmedEventHandler:
    def __init__(self, room_repository: RoomRepository):
        # Inject the RoomRepository interface (Dependency Injection)
        self.room_repository = room_repository

    def handle(self, event: BookingConfirmedEvent) -> None:
        """
        BR5: Domain Event handling between aggregates.
        When a booking is confirmed, this handler catches the event,
        fetches the corresponding Room aggregate, and calls its reserve() method.
        """
        # 1. Fetch Room (Aggregate B) using the ID from the event payload
        room = self.room_repository.get_by_id(event.room_id)
        
        # 2. Tell Aggregate B to transition state to RESERVED (Enforces BR2)
        room.reserve()
        
        # 3. Persist the updated state of Aggregate B
        self.room_repository.save(room)