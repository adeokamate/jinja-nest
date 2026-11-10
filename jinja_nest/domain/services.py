from enum import Enum
from .entities import Room
from .exceptions import PricingCalculationException

class StudentTier(Enum):
    FREE = "FREE"
    SUBSCRIBED = "SUBSCRIBED"

class BookingFeeCalculator:
    def calculate_fee(self, room: Room, tier: StudentTier) -> float:
        if not room.base_price or room.base_price <= 0:
            raise PricingCalculationException("Room must have a valid base price to calculate fees.")
            
        if tier == StudentTier.FREE:
            return room.base_price * 0.10
        elif tier == StudentTier.SUBSCRIBED:
            return room.base_price * 0.05
        else:
            raise PricingCalculationException("Unrecognized student subscription tier.")