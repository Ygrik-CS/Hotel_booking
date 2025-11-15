"""Seed generator using Faker for test data."""
from faker import Faker
from datetime import datetime, timedelta
import random
from database.session import SessionLocal, init_db
from models.user import User
from models.Hotel import Hotel
from models.room_type import RoomType
from models.rate_plan import RatePlan
from models.Price import Price
from models.Availability import Availability
from models.Guest import Guest
from models.Rule import Rule
from passlib.context import CryptContext

fake = Faker()
# Use bcrypt directly with truncation
import bcrypt

def hash_password(password: str) -> str:
    """Hash password using bcrypt with proper truncation."""
    # Bcrypt has 72 byte limit, truncate password
    password_bytes = password.encode('utf-8')[:72]
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password_bytes, salt).decode('utf-8')


def generate_test_data():
    """Generate test data for the hotel booking system."""
    init_db()
    db = SessionLocal()
    
    try:
        # Clear existing data
        print("Clearing existing data...")
        db.query(User).delete()
        db.query(Price).delete()
        db.query(Availability).delete()
        db.query(RatePlan).delete()
        db.query(RoomType).delete()
        db.query(Hotel).delete()
        db.query(Guest).delete()
        db.query(Rule).delete()
        db.commit()
        
        # Create users
        print("Creating users...")
        users = []
        for _ in range(5):
            user = User(
                username=fake.user_name(),
                email=fake.email(),
                hashed_password=hash_password("password123"),
                is_active=True
            )
            users.append(user)
        db.add_all(users)
        db.commit()
        
        # Create hotels
        print("Creating hotels...")
        cities = ["Tashkent", "Samarkand", "Bukhara", "Khiva", "Nukus"]
        hotels = []
        for _ in range(10):
            hotel = Hotel(
                name=fake.company() + " Hotel",
                stars=random.randint(3, 5),
                city=random.choice(cities),
                features='["WiFi", "Pool", "Spa", "Restaurant", "Parking"]'
            )
            hotels.append(hotel)
        db.add_all(hotels)
        db.commit()
        
        # Create room types and rate plans
        print("Creating room types and rate plans...")
        room_types = []
        rate_plans = []
        
        for hotel in hotels:
            # 2-4 room types per hotel
            for _ in range(random.randint(2, 4)):
                room_type = RoomType(
                    hotel_id=hotel.id,
                    name=random.choice(["Standard", "Deluxe", "Suite", "Presidential"]),
                    capacity=random.randint(1, 4),
                    beds='["Double", "Single"]',
                    features='["TV", "Minibar", "Safe", "Balcony"]'
                )
                db.add(room_type)
                db.flush()
                room_types.append(room_type)
                
                # 1-3 rate plans per room type
                for _ in range(random.randint(1, 3)):
                    rate_plan = RatePlan(
                        hotel_id=hotel.id,
                        room_type_id=room_type.id,
                        title=random.choice(["Best Price", "Flexible", "Non-refundable"]),
                        meal=random.choice(["BB", "HB", "FB", "AI"]),
                        refundable=random.choice([True, False]),
                        cancel_before_days=random.randint(1, 7)
                    )
                    db.add(rate_plan)
                    db.flush()
                    rate_plans.append(rate_plan)
        
        db.commit()
        
        # Create prices for next 90 days
        print("Creating prices...")
        prices = []
        start_date = datetime.now().date()
        
        for rate_plan in rate_plans:
            base_price = random.randint(50000, 500000)  # in tiyin
            for day_offset in range(90):
                date = start_date + timedelta(days=day_offset)
                # Weekend prices +20%
                multiplier = 1.2 if date.weekday() >= 5 else 1.0
                price = Price(
                    rate_id=rate_plan.id,
                    date=date.isoformat(),
                    amount=int(base_price * multiplier),
                    currency="UZS"
                )
                prices.append(price)
        
        db.bulk_save_objects(prices)
        db.commit()
        
        # Create availability
        print("Creating availability...")
        availabilities = []
        
        for room_type in room_types:
            for day_offset in range(90):
                date = start_date + timedelta(days=day_offset)
                availability = Availability(
                    room_type_id=room_type.id,
                    date=date.isoformat(),
                    available=random.randint(0, 10)
                )
                availabilities.append(availability)
        
        db.bulk_save_objects(availabilities)
        db.commit()
        
        # Create guests
        print("Creating guests...")
        guests = []
        for _ in range(20):
            guest = Guest(
                name=fake.name(),
                email=fake.email()
            )
            guests.append(guest)
        db.add_all(guests)
        db.commit()
        
        # Create business rules
        print("Creating business rules...")
        rules = [
            Rule(kind="min_stay", payload='{"days": 1}'),
            Rule(kind="max_stay", payload='{"days": 30}'),
            Rule(kind="advance_booking", payload='{"days": 365}'),
        ]
        db.add_all(rules)
        db.commit()
        
        print("✅ Test data generated successfully!")
        print(f"  - {len(users)} users")
        print(f"  - {len(hotels)} hotels")
        print(f"  - {len(room_types)} room types")
        print(f"  - {len(rate_plans)} rate plans")
        print(f"  - {len(prices)} prices")
        print(f"  - {len(availabilities)} availability records")
        print(f"  - {len(guests)} guests")
        
    except Exception as e:
        print(f"❌ Error generating test data: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    generate_test_data()
