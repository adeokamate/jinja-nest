import uuid
from .dtos import BookRoomRequestDTO, BookingResultDTO
from .repositories import RoomRepository, BookingRepository, RoomNotFoundException
from .handlers import BookingConfirmedEventHandler
from jinja_nest.domain.value_objects import BookingPeriod, PrimaryOccupant
from jinja_nest.domain.entities import Booking
from jinja_nest.domain.services import BookingFeeCalculator
from jinja_nest.domain.events import BookingConfirmedEvent

class BookingApplicationService:
    def __init__(self, room_repo: RoomRepository, booking_repo: BookingRepository, event_handler: BookingConfirmedEventHandler):
        # Dependency Injection
        self.room_repo = room_repo
        self.booking_repo = booking_repo
        self.event_handler = event_handler
        self.fee_calculator = BookingFeeCalculator()

    # Use Case 1: Initiate Booking
    def initiate_booking(self, request: BookRoomRequestDTO) -> BookingResultDTO:
        # BR6: Lookup Rule
        room = self.room_repo.get_by_id(request.room_id)
        if not room:
            raise RoomNotFoundException(f"Room {request.room_id} does not exist.")

        # BR4: Cross-Concept Rule
        fee = self.fee_calculator.calculate_fee(room, request.tier)

        # BR1: Value Rule (enforced upon instantiation)
        period = BookingPeriod(request.start_date, request.end_date)

        booking_id = str(uuid.uuid4())
        booking = Booking(booking_id, room.room_id, period, fee)
        
        self.booking_repo.save(booking)

        return BookingResultDTO(
            booking_id=booking.booking_id,
            status=booking.status.name,
            fee=booking.calculated_fee,
            message="Booking initiated successfully."
        )

    # Use Case 2: Confirm Booking
    def confirm_booking(self, booking_id: str, student_id: str, student_name: str) -> BookingResultDTO:
        booking = self.booking_repo.get_by_id(booking_id)
        
        occupant = PrimaryOccupant(student_id, student_name)
        booking.attach_occupant(occupant)
        
        # BR3: Invariant Rule 
        booking.confirm_booking()
        self.booking_repo.save(booking)

        # BR5: Domain Event creation and dispatch
        event = BookingConfirmedEvent(booking.booking_id, booking.room_id)
        self.event_handler.handle(event)

        return BookingResultDTO(
            booking_id=booking.booking_id,
            status=booking.status.name,
            fee=booking.calculated_fee,
            message="Booking confirmed and room reserved."
        )

    