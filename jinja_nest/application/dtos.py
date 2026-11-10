from dataclasses import dataclass
from datetime import date
from jinja_nest.domain.services import StudentTier

@dataclass(frozen=True)
class BookRoomRequestDTO:
    room_id: str
    student_id: str
    student_name: str
    start_date: date
    end_date: date
    tier: StudentTier

@dataclass(frozen=True)
class BookingResultDTO:
    booking_id: str
    status: str
    fee: float
    message: str