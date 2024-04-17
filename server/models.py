from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, ForeignKey, UniqueConstraint
from datetime import datetime, timezone

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    profile_picture = db.Column(db.String(255))
    phone_number = db.Column(db.String(20))
    address = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    # Relationship
    user_profile = db.relationship('UserProfile', back_populates='user')
    messages = db.relationship('Message', back_populates='user', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<User id={self.id}, username={self.username}, email={self.email}>"

class UserProfile(db.Model):
    __tablename__ = 'user_profiles'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    bio = db.Column(db.Text)
    website = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    # Relationship
    user = db.relationship('User', back_populates='user_profile')

    def __repr__(self):
        return f"<UserProfile id={self.id}, user_id={self.user_id}>"

class Receiver(db.Model):
    __tablename__ = 'receivers'
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(20))
    email = db.Column(db.String(120), unique=True, nullable=False)

    # Relationship
    messages = db.relationship('Message', back_populates='receiver', cascade='all, delete-orphan')

class Message(db.Model):
    __tablename__ ='messages'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    received_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('receivers.id'), nullable=False)

    # Relationship
    user = db.relationship('User', back_populates='messages', foreign_keys=[user_id])
    receiver = db.relationship('Receiver', back_populates='messages', foreign_keys=[receiver_id])

    # Constraint
    db.UniqueConstraint('user_id', 'receiver_id', name='unique_user_receiver')

if __name__ == "__main__":
    # Create the database tables if they don't exist
    db.create_all()
