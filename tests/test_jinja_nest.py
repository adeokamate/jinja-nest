import unittest
from datetime import date, timedelta
from jinja_nest.domain.exceptions import (
    InvalidBookingPeriodException, RoomUnavailableException,
    MissingOccupantException, PricingCalculationException
)
from jinja_nest.domain.value_objects import BookingPeriod, PrimaryOccupant
from jinja_nest.domain.entities import Room, Booking, RoomStatus, BookingStatus
from jinja_nest.domain.services import BookingFeeCalculator, StudentTier
from jinja_nest.domain.events import BookingConfirmedEvent
from jinja_nest.application.repositories import RoomNotFoundException
from jinja_nest.application.handlers import BookingConfirmedEventHandler
from jinja_nest.application.services import BookingApplicationService
from jinja_nest.application.dtos import BookRoomRequestDTO
from jinja_nest.infrastructure.repositories import InMemoryRoomRepository, InMemoryBookingRepository

class JinjaNestTests(unittest.TestCase):
    def setUp(self):
        self.room_repo = InMemoryRoomRepository()
        self.booking_repo = InMemoryBookingRepository()
        self.event_handler = BookingConfirmedEventHandler(self.room_repo)
        self.app_service = BookingApplicationService(self.room_repo, self.booking_repo, self.event_handler)
        self.calculator = BookingFeeCalculator()
        
        self.test_room = Room("ROOM-101", 500000.0)
        self.room_repo.save(self.test_room)
        
        self.valid_start = date.today() + timedelta(days=1)
        self.valid_end = self.valid_start + timedelta(days=30)

    # T1: Value rule (BR1) - Rejection case
    def test_t1_br1_invalid_booking_period_throws_exception(self):
        past_date = date.today() - timedelta(days=1)
        with self.assertRaises(InvalidBookingPeriodException):
            BookingPeriod(past_date, self.valid_end)

    # T2: Identity/state rule (BR2) - Rejection case
    def test_t2_br2_reserve_unavailable_room_throws_exception(self):
        self.test_room.reserve() # State is now RESERVED
        with self.assertRaises(RoomUnavailableException):
            self.test_room.reserve()

    # T3: Invariant rule (BR3) - Rejection case
    def test_t3_br3_confirm_without_occupant_throws_exception(self):
        period = BookingPeriod(self.valid_start, self.valid_end)
        booking = Booking("B-1", "ROOM-101", period, 50000.0)
        with self.assertRaises(MissingOccupantException):
            booking.confirm_booking()

    # T4: Cross-concept rule (BR4) - Boundary/Success cases
    def test_t4_br4_fee_calculation_applies_correct_tier_percentages(self):
        free_fee = self.calculator.calculate_fee(self.test_room, StudentTier.FREE)
        sub_fee = self.calculator.calculate_fee(self.test_room, StudentTier.SUBSCRIBED)
        
        self.assertEqual(free_fee, 50000.0)  # 10% of 500,000
        self.assertEqual(sub_fee, 25000.0)   # 5% of 500,000

    # T5: Follow-up rule (BR5) - Event handler functionality
    def test_t5_br5_booking_confirmed_event_handler_reserves_room(self):
        event = BookingConfirmedEvent("B-1", "ROOM-101")
        self.event_handler.handle(event)
        
        updated_room = self.room_repo.get_by_id("ROOM-101")
        self.assertEqual(updated_room.status, RoomStatus.RESERVED)

    # T6: Lookup rule (BR6) - Rejection case
    def test_t6_br6_initiate_booking_with_missing_room_throws_exception(self):
        request = BookRoomRequestDTO("GHOST-ROOM", "S-1", "John", self.valid_start, self.valid_end, StudentTier.FREE)
        with self.assertRaises(RoomNotFoundException):
            self.app_service.initiate_booking(request)

    # T7: Successful main use case
    def test_t7_successful_main_use_case_confirms_booking_and_reserves_room(self):
        request = BookRoomRequestDTO("ROOM-101", "S-1", "John", self.valid_start, self.valid_end, StudentTier.SUBSCRIBED)
        init_result = self.app_service.initiate_booking(request)
        
        confirm_result = self.app_service.confirm_booking(init_result.booking_id, "S-1", "John")
        
        booking = self.booking_repo.get_by_id(init_result.booking_id)
        room = self.room_repo.get_by_id("ROOM-101")
        
        self.assertEqual(booking.status, BookingStatus.CONFIRMED)
        self.assertEqual(room.status, RoomStatus.RESERVED)
        self.assertEqual(confirm_result.message, "Booking confirmed and room reserved.")

    # T8: Aggregate B rejects follow-up action
    def test_t8_aggregate_b_rejects_follow_up_action(self):
        # Two students try to book the exact same room
        req1 = BookRoomRequestDTO("ROOM-101", "S-1", "John", self.valid_start, self.valid_end, StudentTier.FREE)
        req2 = BookRoomRequestDTO("ROOM-101", "S-2", "Mary", self.valid_start, self.valid_end, StudentTier.FREE)
        
        booking1 = self.app_service.initiate_booking(req1)
        booking2 = self.app_service.initiate_booking(req2)
        
        # Student 1 confirms first. Room becomes RESERVED.
        self.app_service.confirm_booking(booking1.booking_id, "S-1", "John")
        
        # Student 2 tries to confirm. The event fires, but the Room (Aggregate B) rejects it.
        with self.assertRaises(RoomUnavailableException):
            self.app_service.confirm_booking(booking2.booking_id, "S-2", "Mary")