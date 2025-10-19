from datetime import datetime, timedelta
from random import randint, choice

from database import Base, engine, SessionLocal
from models import Flight, Passenger, FlightStatus


def seed():
    # Ensure tables exist
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # Avoid duplicate seeding: if flights already exist, skip
        existing = db.query(Flight).first()
        if existing:
            print("Data already exists. Skipping seeding.")
            return

        # Seed flights
        airlines = ["IndiGo", "Air India", "Vistara", "SpiceJet", "Akasa Air"]
        airports = [
            ("DEL", "BOM"), ("BLR", "DEL"), ("MAA", "HYD"), ("CCU", "BLR"), ("PNQ", "DEL"),
            ("BOM", "GOI"), ("DEL", "SXR"), ("BLR", "COK"), ("JAI", "DEL"), ("BOM", "UDR")
        ]
        base_time = datetime.now().replace(minute=0, second=0, microsecond=0) + timedelta(days=1)

        flights = []
        for i in range(15):
            dep, arr = choice(airports)
            dep_time = base_time + timedelta(hours=randint(6, 120))
            arr_time = dep_time + timedelta(hours=randint(1, 4), minutes=choice([0, 15, 30, 45]))
            total = choice([120, 150, 180])
            price = choice([3499.0, 4299.0, 5199.0, 5999.0, 6999.0])

            flight = Flight(
                flight_number=f"FS{i+101}",
                airline=choice(airlines),
                departure_airport=dep,
                arrival_airport=arr,
                departure_time=dep_time,
                arrival_time=arr_time,
                total_seats=total,
                available_seats=total - randint(0, 20),
                price=price,
                status=FlightStatus.SCHEDULED,
            )
            flights.append(flight)

        db.add_all(flights)

        # Seed one passenger
        passenger = Passenger(
            first_name="Demo",
            last_name="User",
            email="demo.user@example.com",
            phone="9999999999",
            passport_number="P1234567",
            date_of_birth=datetime(1998, 5, 20).date(),
        )
        db.add(passenger)

        db.commit()
        print("Seeded demo flights and a passenger successfully.")
    except Exception as e:
        db.rollback()
        print(f"Seeding failed: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
