from app import app
from models import db, User, UserProfile, Message, Receiver

from faker import Faker

fake = Faker()

def seed_users():
    # Delete existing users
    User.query.delete()  
    # Create 10 users
    for _ in range(10):  
        user = User(
            username=fake.user_name(),
            email=fake.email(),
            password=fake.password(),
            phone_number=fake.phone_number(),
            address=fake.address()
        )
        db.session.add(user)
    db.session.commit()


def seed_user_profiles():
    UserProfile.query.delete()  # Delete existing user profiles
    for user_id in range(1, 11):  # Assuming user IDs start from 1 and go up to 10
        profile = UserProfile(
            user_id=user_id,
            bio=fake.text(),
            website=fake.url()
        )
        db.session.add(profile)
    db.session.commit()


def seed_messages():
    Message.query.delete()  # Delete existing messages
    for _ in range(20):  # Create 20 messages
        message = Message(
            content=fake.text(max_nb_chars=200),
            user_id=fake.random_int(min=1, max=10)  # Assuming you have 10 users already created
        )
        db.session.add(message)
    db.session.commit()


def seed_receivers():
    Receiver.query.delete()  # Delete existing receivers
    for _ in range(10):  # Create 10 receivers
        receiver = Receiver(
            phone_number=fake.phone_number(),
            email=fake.email()
        )
        db.session.add(receiver)
    db.session.commit()


if __name__ == "__main__":
    # Initialize the Flask application and create the database connection
    app.app_context().push()
    db.create_all()

    # Seed the database with fake data
    # seed_users()
    # seed_user_profiles()
    # seed_messages()
    # seed_receivers()

    print('Seeded database with fake data.')
