# Jinja Nest — Core Room Reservation System

This repository contains the Python implementation of the core **Room Reservation Subsystem** for the Jinja Nest platform. The implementation strictly adheres to **Domain-Driven Design (DDD)** principles and **Clean Architecture** patterns, as required by the coursework specification.

---

## 🏛️ Clean Architecture Project Structure

The codebase is organized into four concentric layers to enforce strict inward dependency boundaries:

```text
Jinja_Nest/
├── jinja_nest/                     # Core Application Package
│   ├── domain/                     # Layer 1: Enterprise Business Rules
│   │   ├── entities.py             # Aggregate Roots: Booking (Agg A), Room (Agg B)
│   │   ├── value_objects.py        # Immutable VOs: BookingPeriod, PrimaryOccupant
│   │   ├── services.py             # Domain Services: BookingFeeCalculator (BR4)
│   │   ├── events.py               # Domain Events: BookingConfirmedEvent (BR5)
│   │   └── exceptions.py           # Domain Boundary Invariant Exceptions
│   │
│   ├── application/                # Layer 2: Application Business Rules
│   │   ├── dtos.py                 # Data Transfer Objects (BookRoomRequestDTO, BookingResultDTO)
│   │   ├── repositories.py         # Abstract Repository Interfaces (RoomRepository, BookingRepository)
│   │   ├── handlers.py             # Event Handler bridging Aggregate A and Aggregate B
│   │   └── services.py             # Application Service Orchestrator (BookingApplicationService)
│   │
│   ├── infrastructure/             # Layer 3: Frameworks & Drivers (In-Memory Persistence)
│   │   └── repositories.py         # Concrete InMemoryRoomRepository & InMemoryBookingRepository
│   │
│   └── interface/                  # Layer 4: Presentation / Entry Point
│       └── main.py                 # CLI Simulation script executing Use Cases 1 & 2
│
├── tests/                          # Automated Test Suite
│   └── test_jinja_nest.py          # 8 Automated Tests (T1–T8) covering BR1–BR6
└── README.md                       # Documentation & AI Declaration
```

---

## 📋 Business Rules & Invariants Mapping

| Rule ID | Name | Architectural Location | Description / Enforcement |
| :--- | :--- | :--- | :--- |
| **BR1** | Booking Period | `domain/value_objects.py` | `BookingPeriod` ensures end date is after start date and start date is not in the past. |
| **BR2** | Room Availability | `domain/entities.py` | `Room.reserve()` state machine allows reservation only when status is `AVAILABLE`. |
| **BR3** | Primary Occupant Invariant | `domain/entities.py` | `Booking.confirm_booking()` prevents confirmation without an attached `PrimaryOccupant`. |
| **BR4** | Tiered Pricing Service | `domain/services.py` | `BookingFeeCalculator` applies 10% fee for `FREE` tier and 5% fee for `SUBSCRIBED` tier. |
| **BR5** | Booking Confirmed Event | `domain/events.py` & `application/handlers.py` | Confirmation emits `BookingConfirmedEvent` to instruct Aggregate B (`Room`) to update state. |
| **BR6** | Room Lookup | `application/services.py` | Application Service verifies target room exists before initiating a draft booking. |

---

## 🚀 Execution Commands

### 1. Run Main Simulation Script
To demonstrate the end-to-end execution of Use Case 1 (*Initiate Booking*) and Use Case 2 (*Confirm Booking & Lock Room*), run:

```bash
python -m jinja_nest.interface.main
```

### 2. Run Automated Test Suite (T1–T8)
To run all 8 automated unit tests with verbose output:

```bash
python -m unittest discover -s tests -v
```

---

## 🧪 TDD Evidence Generation Guide

To capture the **Fail/Pass (Red/Green)** evidence required for Slide 12:

1. **Force Failing Test (Red Phase):**
   * Open `jinja_nest/domain/entities.py`.
   * Comment out the invariant check inside `Booking.confirm_booking()`:
     ```python
     # if not self.occupant:
     #     raise MissingOccupantException("Cannot confirm booking without a Primary Occupant.")
     ```
   * Execute `python -m unittest discover -s tests -v`.
   * Test `T3` will fail with an `AssertionError`. Save/screenshot terminal output.

2. **Restore Passing Test (Green Phase):**
   * Uncomment the invariant check in `jinja_nest/domain/entities.py`.
   * Execute `python -m unittest discover -s tests -v` again.
   * All 8 tests will pass (`OK`). Save/screenshot terminal output.

---

## 🤖 AI Tools Declaration

AI tools (Gemini) were utilized to assist with scaffolding Clean Architecture directory layouts, refining domain invariant definitions, and structuring automated test cases.