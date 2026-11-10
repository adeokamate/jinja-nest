from datetime import date, timedelta
from jinja_nest.infrastructure.repositories import InMemoryRoomRepository, InMemoryBookingRepository
from jinja_nest.application.handlers import BookingConfirmedEventHandler
from jinja_nest.application.services import BookingApplicationService
from jinja_nest.application.dtos import BookRoomRequestDTO
from jinja_nest.domain.entities import Room
from jinja_nest.domain.services import StudentTier

def run_jinja_nest_simulation():
    # 1. Setup Infrastructure (Dependency Injection)
    room_repo = InMemoryRoomRepository()
    booking_repo = InMemoryBookingRepository()
    event_handler = BookingConfirmedEventHandler(room_repo)
    
    app_service = BookingApplicationService(room_repo, booking_repo, event_handler)

    # 2. Seed the database with a test room
    test_room = Room(room_id="ROOM-101", base_price=500000.0) # 500k UGX base price
    room_repo.save(test_room)
    print(f"Initial Room Status: {test_room.status.name}")

    # 3. Execute Use Case 1: Initiate Booking
    start = date.today() + timedelta(days=5)
    end = start + timedelta(days=30)
    
    request = BookRoomRequestDTO(
        room_id="ROOM-101",
        student_id="2023/BCS/123",
        student_name="Kato John",
        start_date=start,
        end_date=end,
        tier=StudentTier.SUBSCRIBED
    )
    
    print("\n--- Initiating Booking ---")
    init_result = app_service.initiate_booking(request)
    print(f"Result: {init_result.message} | Fee: {init_result.fee} | Status: {init_result.status}")

    # 4. Execute Use Case 2: Confirm Booking (Triggers the Domain Event)
    print("\n--- Confirming Booking ---")
    confirm_result = app_service.confirm_booking(
        booking_id=init_result.booking_id,
        student_id=request.student_id,
        student_name=request.student_name
    )
    print(f"Result: {confirm_result.message} | Status: {confirm_result.status}")

    # 5. Verify Aggregate B (Room) reacted to Aggregate A (Booking)
    updated_room = room_repo.get_by_id("ROOM-101")
    print(f"\nFinal Room Status: {updated_room.status.name}")

if __name__ == "__main__":
    run_jinja_nest_simulation()