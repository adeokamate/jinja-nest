from datetime import date
from dataclasses import dataclass
from .exceptions import InvalidBookingPeriodException

@dataclass(frozen=True)
class BookingPeriod:
    start_date: date
    end_date: date

    def __post_init__(self):
        if self.start_date <= date.today():
            raise InvalidBookingPeriodException("Start date must be in the future.")
        if self.end_date <= self.start_date:
            raise InvalidBookingPeriodException("End date must be strictly after the start date.")

@dataclass(frozen=True)
class PrimaryOccupant:
    student_id: str
    name: str