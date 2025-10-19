from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Float, Boolean, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base
import enum

class FlightClass(enum.Enum):
    ECONOMY = "Economy"
    BUSINESS = "Business"
    FIRST = "First Class"

class FlightStatus(enum.Enum):
    SCHEDULED = "Scheduled"
    DELAYED = "Delayed"
    CANCELLED = "Cancelled"
    DEPARTED = "Departed"
    ARRIVED = "Arrived"

class Flight(Base):
    __tablename__ = "flights"
    
    id = Column(Integer, primary_key=True, index=True)
    flight_number = Column(String(20), unique=True, nullable=False)
    airline = Column(String(100), nullable=False)
    departure_airport = Column(String(100), nullable=False)
    arrival_airport = Column(String(100), nullable=False)
    departure_time = Column(DateTime, nullable=False)
    arrival_time = Column(DateTime, nullable=False)
    total_seats = Column(Integer, nullable=False)
    available_seats = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    status = Column(Enum(FlightStatus), default=FlightStatus.SCHEDULED)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    bookings = relationship("Booking", back_populates="flight")

class Passenger(Base):
    __tablename__ = "passengers"
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20), nullable=False)
    passport_number = Column(String(50), unique=True, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    bookings = relationship("Booking", back_populates="passenger")

class Booking(Base):
    __tablename__ = "bookings"
    
    id = Column(Integer, primary_key=True, index=True)
    booking_reference = Column(String(10), unique=True, nullable=False)
    flight_id = Column(Integer, ForeignKey("flights.id"), nullable=False)
    passenger_id = Column(Integer, ForeignKey("passengers.id"), nullable=False)
    seat_number = Column(String(10), nullable=False)
    flight_class = Column(Enum(FlightClass), nullable=False)
    booking_date = Column(DateTime, default=datetime.utcnow)
    is_cancelled = Column(Boolean, default=False)
    
    flight = relationship("Flight", back_populates="bookings")
    passenger = relationship("Passenger", back_populates="bookings")
