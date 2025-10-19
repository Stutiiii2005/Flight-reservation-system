# Flight Reservation System

A console-based Flight Reservation System built with Python and SQLite. This system allows users to manage flights, passengers, and bookings through an easy-to-use command-line interface.

## Features

- **Flight Management**: Add, view, and manage flight details
- **Passenger Management**: Add and manage passenger information
- **Booking System**: Book flights, assign seats, and manage reservations
- **Search Functionality**: Search for flights by route, date, and availability
- **Booking Management**: View and cancel existing bookings

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## Installation

1. Clone the repository or download the source code
2. Navigate to the project directory:
   ```
   cd flight_reservation_system
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## How to Run

1. Run the application:
   ```
   python main.py
   ```

2. Follow the on-screen menu to perform various operations:
   - Add new flights
   - View available flights
   - Search for flights
   - Add passengers
   - Book flights
   - View bookings
   - Cancel bookings

## Database

The application uses SQLite as the database, which will be automatically created as `flight_reservation.db` in the project directory when you first run the application.

## Usage Examples

1. **Add a new flight**:
   - Select option 1 from the main menu
   - Enter flight details when prompted

2. **Book a flight**:
   - Select option 5 from the main menu
   - Choose from available flights
   - Enter passenger details
   - Select seat class
   - Receive booking confirmation

3. **View bookings**:
   - Select option 6 from the main menu
   - View all bookings or search by reference/email

## Project Structure

- `main.py`: Main application with the command-line interface
- `models.py`: Database models (Flight, Passenger, Booking)
- `database.py`: Database connection and initialization
- `requirements.txt`: Project dependencies

## Dependencies

- SQLAlchemy: ORM for database operations
- python-dateutil: Date and time utilities
- colorama: Cross-platform colored terminal text

## License

This project is open source and available under the [MIT License](LICENSE).
