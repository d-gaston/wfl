from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin
import string, datetime

metadata = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
)
db = SQLAlchemy(metadata=metadata)


class User(db.Model, SerializerMixin):
    __tablename__ = "user_table"
    serialize_rules = ["-ducks.user"]
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    # we store the hash of the password, not the password itself
    # DO NOT store the password itself
    password_hash = db.Column(db.String)

    # the cascade means that if we delete a user, all of its associated
    # reviews will be deleted as well.
    reviews = db.relationship("Review", back_populates="user", cascade="all,delete")


class Restaurant(db.Model, SerializerMixin):
    __tablename__ = "restaurant_table"
    serialize_rules = ["-reviews.restaurant"]
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    photo = db.Column(db.String)
    address = db.Column(db.String)
    cuisine = db.Column(db.String)

    reviews = db.relationship(
        "Review", back_populates="restaurant", cascade="all,delete"
    )


class Review(db.Model, SerializerMixin):
    __tablename__ = "review_table"
    serialize_rules = ["-restaurant.reviews", '-user.reviews']
    # canvas serialize_rules = ('-restaurant.reviews',)
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)
    review = db.Column(db.String)
    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurant_table.id"))
    reviewer_id = db.Column(db.Integer, db.ForeignKey("user_table.id"))

    user = db.relationship("User", back_populates="reviews")
    restaurant = db.relationship("Restaurant", back_populates="reviews")
