import os
import random
import string
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func
import colorama
from colorama import Fore, Style

from database import engine, Base, get_db
from models import Flight, Passenger, Booking, FlightClass, FlightStatus

# Initialize colorama
colorama.init()

# Create database tables
def init_db():
    Base.metadata.create_all(bind=engine)
    print(f"{Fore.GREEN}Database initialized successfully!{Style.RESET_ALL}")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def generate_booking_reference():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

def display_menu():
    clear_screen()
    print(f"{Fore.CYAN}=== Flight Reservation System ==={Style.RESET_ALL}")
    print("1. Add New Flight")
    print("2. View All Flights")
    print("3. Search Flights")
    print("4. Add Passenger")
    print("5. Book a Flight")
    print("6. View Bookings")
    print("7. Cancel Booking")
    print("8. Exit")
    print("-" * 30)
    return input("Enter your choice (1-8): ")

def add_flight(db: Session):
    clear_screen()
    print(f"{Fore.YELLOW}=== Add New Flight ==={Style.RESET_ALL}")
    
    flight_number = input("Enter flight number (e.g., AA123): ")
    airline = input("Enter airline name: ")
    departure_airport = input("Enter departure airport code (e.g., JFK): ").upper()
    arrival_airport = input("Enter arrival airport code (e.g., LAX): ").upper()
    departure_time = input("Enter departure time (DD-MM-YYYY HH:MM): ")
    arrival_time = input("Enter arrival time (DD-MM-YYYY HH:MM): ")
    total_seats = int(input("Enter total number of seats: "))
    price = float(input("Enter ticket price: "))
    
    try:
        departure_time = datetime.strptime(departure_time, "%d-%m-%Y %H:%M")
        arrival_time = datetime.strptime(arrival_time, "%d-%m-%Y %H:%M")
        
        flight = Flight(
            flight_number=flight_number,
            airline=airline,
            departure_airport=departure_airport,
            arrival_airport=arrival_airport,
            departure_time=departure_time,
            arrival_time=arrival_time,
            total_seats=total_seats,
            available_seats=total_seats,
            price=price,
            status=FlightStatus.SCHEDULED
        )
        
        db.add(flight)
        db.commit()
        print(f"{Fore.GREEN}Flight added successfully!{Style.RESET_ALL}")
    except Exception as e:
        db.rollback()
        print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
    
    input("\nPress Enter to continue...")

def view_flights(db: Session):
    clear_screen()
    print(f"{Fore.YELLOW}=== Available Flights ==={Style.RESET_ALL}\n")
    
    flights = db.query(Flight).all()
    
    if not flights:
        print("No flights found.")
    else:
        print(f"{'ID':<5} {'Flight':<10} {'From':<5} {'To':<5} {'Departure':<20} {'Arrival':<20} {'Seats':<10} {'Price':<10} {'Status':<15}")
        print("-" * 100)
        for flight in flights:
            print(f"{flight.id:<5} {flight.flight_number:<10} {flight.departure_airport:<5} {flight.arrival_airport:<5} "
                  f"{flight.departure_time.strftime('%Y-%m-%d %H:%M'):<20} {flight.arrival_time.strftime('%Y-%m-%d%H:%M'):<20} "
                  f"{flight.available_seats}/{flight.total_seats:<9} Rs.{flight.price:<9.2f} {flight.status.value:<15}")
    
    input("\nPress Enter to continue...")

def search_flights(db: Session):
    clear_screen()
    print(f"{Fore.YELLOW}=== Search Flights ==={Style.RESET_ALL}\n")
    
    departure = input("Enter departure airport (leave empty to skip): ").upper()
    arrival = input("Enter arrival airport (leave empty to skip): ").upper()
    date = input("Enter date (DD-MM-YYYY, leave empty to skip): ")
    
    query = db.query(Flight)
    
    if departure:
        query = query.filter(Flight.departure_airport == departure)
    if arrival:
        query = query.filter(Flight.arrival_airport == arrival)
    if date:
        try:
            date_obj = datetime.strptime(date, "%d-%m-%Y")
            next_day = date_obj + timedelta(days=1)
            query = query.filter(Flight.departure_time >= date_obj, Flight.departure_time < next_day)
        except ValueError:
            print(f"{Fore.RED}Invalid date format. Please use DD-MM-YYYY.{Style.RESET_ALL}")
    
    flights = query.all()
    
    if not flights:
        print("No flights found matching your criteria.")
    else:
        print(f"\n{'ID':<5} {'Flight':<10} {'From':<5} {'To':<5} {'Departure':<20} {'Arrival':<20} {'Seats':<10} {'Price':<10}")
        print("-" * 90)
        for flight in flights:
            print(f"{flight.id:<5} {flight.flight_number:<10} {flight.departure_airport:<5} {flight.arrival_airport:<5} "
                  f"{flight.departure_time.strftime('%d-%m-%Y %H:%M'):<20} {flight.arrival_time.strftime('%d-%m-%Y %H:%M'):<20} "
                  f"{flight.available_seats}/{flight.total_seats:<9} Rs.{flight.price:<9.2f}")
    
    input("\nPress Enter to continue...")

def add_passenger(db: Session):
    clear_screen()
    print(f"{Fore.YELLOW}=== Add New Passenger ==={Style.RESET_ALL}")
    
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    email = input("Enter email: ")
    phone = input("Enter phone number: ")
    passport = input("Enter passport number: ")
    dob = input("Enter date of birth (YYYY-MM-DD): ")
    
    try:
        dob_date = datetime.strptime(dob, "%Y-%m-%d").date()
        
        passenger = Passenger(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            passport_number=passport,
            date_of_birth=dob_date
        )
        
        db.add(passenger)
        db.commit()
        print(f"{Fore.GREEN}Passenger added successfully!{Style.RESET_ALL}")
    except Exception as e:
        db.rollback()
        print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
    
    input("\nPress Enter to continue...")

def book_flight(db: Session):
    clear_screen()
    print(f"{Fore.YELLOW}=== Book a Flight ==={Style.RESET_ALL}")
    
    # Show available flights
    flights = db.query(Flight).filter(Flight.available_seats > 0, Flight.status == FlightStatus.SCHEDULED).all()
    
    if not flights:
        print("No available flights found.")
        input("\nPress Enter to continue...")
        return
    
    print("\nAvailable Flights:")
    print(f"{'ID':<5} {'Flight':<10} {'From':<5} {'To':<5} {'Departure':<20} {'Price':<10}")
    print("-" * 70)
    for flight in flights:
        print(f"{flight.id:<5} {flight.flight_number:<10} {flight.departure_airport:<5} {flight.arrival_airport:<5} "
              f"{flight.departure_time.strftime('%d-%m-%Y %H:%M'):<20} Rs.{flight.price:<.2f}")
    
    try:
        flight_id = int(input("\nEnter flight ID to book: "))
        flight = db.query(Flight).filter(Flight.id == flight_id).first()
        
        if not flight:
            print(f"{Fore.RED}Flight not found.{Style.RESET_ALL}")
            input("\nPress Enter to continue...")
            return
            
        if flight.available_seats <= 0:
            print(f"{Fore.RED}No available seats on this flight.{Style.RESET_ALL}")
            input("\nPress Enter to continue...")
            return
        
        # Get passenger details
        print("\nPassenger Details:")
        first_name = input("First Name: ")
        last_name = input("Last Name: ")
        email = input("Email: ")
        
        # Check if passenger exists, if not create new
        passenger = db.query(Passenger).filter(Passenger.email == email).first()
        
        if not passenger:
            phone = input("Phone: ")
            passport = input("Passport Number: ")
            dob = input("Date of Birth (DD-MM-YYYY): ")
            
            try:
                dob_date = datetime.strptime(dob, "%d-%m-%Y").date()
                
                passenger = Passenger(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    phone=phone,
                    passport_number=passport,
                    date_of_birth=dob_date
                )
                
                db.add(passenger)
                db.flush()  # Get the passenger ID without committing the transaction
            except Exception as e:
                db.rollback()
                print(f"{Fore.RED}Error creating passenger: {str(e)}{Style.RESET_ALL}")
                input("\nPress Enter to continue...")
                return
        
        # Get seat class
        print("\nAvailable Classes:")
        for i, cls in enumerate(FlightClass, 1):
            print(f"{i}. {cls.value}")
        
        class_choice = int(input("Select class (1-3): "))
        if class_choice < 1 or class_choice > len(FlightClass):
            print(f"{Fore.RED}Invalid class selection.{Style.RESET_ALL}")
            input("\nPress Enter to continue...")
            return
            
        flight_class = list(FlightClass)[class_choice - 1]
        
        # Generate seat number (simple implementation)
        seat_number = f"{flight_class.value[0]}{flight.available_seats}"
        
        # Create booking
        booking = Booking(
            booking_reference=generate_booking_reference(),
            flight_id=flight.id,
            passenger_id=passenger.id,
            seat_number=seat_number,
            flight_class=flight_class
        )
        
        # Update available seats
        flight.available_seats -= 1
        
        db.add(booking)
        db.commit()
        
        print(f"\n{Fore.GREEN}Booking successful!{Style.RESET_ALL}")
        print(f"Booking Reference: {booking.booking_reference}")
        print(f"Flight: {flight.flight_number} from {flight.departure_airport} to {flight.arrival_airport}")
        print(f"Passenger: {passenger.first_name} {passenger.last_name}")
        print(f"Seat: {seat_number} ({flight_class.value})")
        
    except ValueError:
        print(f"{Fore.RED}Invalid input. Please enter a valid number.{Style.RESET_ALL}")
    except Exception as e:
        db.rollback()
        print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
    
    input("\nPress Enter to continue...")

def view_bookings(db: Session):
    clear_screen()
    print(f"{Fore.YELLOW}=== View Bookings ==={Style.RESET_ALL}\n")
    
    ref_or_email = input("Enter booking reference or passenger email (leave empty to view all): ").strip()
    
    if ref_or_email:
        # Search by booking reference or email
        bookings = db.query(Booking).join(Passenger).filter(
            (Booking.booking_reference == ref_or_email) | 
            (Passenger.email == ref_or_email)
        ).all()
    else:
        # Get all bookings
        bookings = db.query(Booking).all()
    
    if not bookings:
        print("No bookings found.")
    else:
        print(f"{'Ref':<10} {'Passenger':<20} {'Flight':<10} {'From':<5} {'To':<5} "
              f"{'Departure':<20} {'Seat':<10} {'Class':<15} {'Status':<10}")
        print("-" * 100)
        
        for booking in bookings:
            status = "Cancelled" if booking.is_cancelled else "Confirmed"
            print(f"{booking.booking_reference:<10} "
                  f"{booking.passenger.first_name} {booking.passenger.last_name:<15} "
                  f"{booking.flight.flight_number:<10} {booking.flight.departure_airport:<5} {booking.flight.arrival_airport:<5} "
                  f"{booking.flight.departure_time.strftime('%d-%m-%Y %H:%M'):<20} "
                  f"{booking.seat_number:<10} {booking.flight_class.value:<15} {status:<10}")
    
    input("\nPress Enter to continue...")

def cancel_booking(db: Session):
    clear_screen()
    print(f"{Fore.YELLOW}=== Cancel Booking ==={Style.RESET_ALL}\n")
    
    ref = input("Enter booking reference to cancel: ").strip()
    
    if not ref:
        print(f"{Fore.RED}Booking reference is required.{Style.RESET_ALL}")
        input("\nPress Enter to continue...")
        return
    
    booking = db.query(Booking).filter(Booking.booking_reference == ref).first()
    
    if not booking:
        print(f"{Fore.RED}Booking not found.{Style.RESET_ALL}")
    elif booking.is_cancelled:
        print(f"{Fore.YELLOW}This booking is already cancelled.{Style.RESET_ALL}")
    else:
        # Show booking details
        print("\nBooking Details:")
        print(f"Passenger: {booking.passenger.first_name} {booking.passenger.last_name}")
        print(f"Flight: {booking.flight.flight_number} from {booking.flight.departure_airport} to {booking.flight.arrival_airport}")
        print(f"Date: {booking.flight.departure_time.strftime('%Y-%m-%d %H:%M')}")
        print(f"Seat: {booking.seat_number} ({booking.flight_class.value})")
        
        confirm = input("\nAre you sure you want to cancel this booking? (y/n): ").lower()
        
        if confirm == 'y':
            booking.is_cancelled = True
            booking.flight.available_seats += 1  # Make the seat available again
            db.commit()
            print(f"{Fore.GREEN}Booking has been cancelled successfully.{Style.RESET_ALL}")
        else:
            print("Cancellation aborted.")
    
    input("\nPress Enter to continue...")

def main():
    # Initialize database
    init_db()
    
    # Create a database session
    db = next(get_db())
    
    # Main menu loop
    while True:
        try:
            choice = display_menu()
            
            if choice == '1':
                add_flight(db)
            elif choice == '2':
                view_flights(db)
            elif choice == '3':
                search_flights(db)
            elif choice == '4':
                add_passenger(db)
            elif choice == '5':
                book_flight(db)
            elif choice == '6':
                view_bookings(db)
            elif choice == '7':
                cancel_booking(db)
            elif choice == '8':
                print("\nThank you for using FlyNow. Goodbye!")
                break
            else:
                print(f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")
                input("\nPress Enter to continue...")
                
        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
        except Exception as e:
            print(f"\n{Fore.RED}An error occurred: {str(e)}{Style.RESET_ALL}")
            input("\nPress Enter to continue...")
    
    db.close()

if __name__ == "__main__":
    main()
