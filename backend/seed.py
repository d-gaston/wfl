from app import app
from models import Restaurant, Review, db, User
import json
from flask_bcrypt import Bcrypt
import random

if __name__ == "__main__":
    with app.app_context():
        # this will be needed for when we get to passwords
        bcrypt = Bcrypt(app)
        data = {}
        # get the json as a dict
        with open("db.json") as f:
            data = json.load(f)
        # clear the data from the restaurant table. If we don't do this
        # running this file will cause repeated data to accumulate
        Restaurant.query.delete()
        Review.query.delete()
        User.query.delete()
        restaurant_list = []
        # loop over the list of restaurant dicts
        for rev in data["restaurants"]:
            # read the data from the dict into a Restaurant object
            restaurant = Restaurant(
                name=rev.get("name"),
                photo=rev.get("photo"),
                address=rev.get("address"),
                cuisine=rev.get("cuisine"),
            )
            restaurant_list.append(restaurant)
        # add all of the restaurants to the db at once
        db.session.add_all(restaurant_list)
        db.session.commit()
        review_list = []
        
        # add a user to go with all of the reviews
        reviewer = User(
                name='Kirstyn',
                password_hash=bcrypt.generate_password_hash("a"),
            )
        db.session.add(reviewer)
        db.session.commit()
        for rev in data["reviews"]:
            restaurant = [
                rst for rst in restaurant_list if rst.name == rev["restaurant"]
            ][0]
            
            
            review = Review(
                reviewer_id=reviewer.id,
                review=rev.get("review"),
                rating=int(rev.get("rating")),
                restaurant=restaurant,
            )
            review_list.append(review)
        db.session.add_all(review_list)
        db.session.commit()

        # I make a test user with a simple username and password
        # -- please don't make a real username and password for testing
        # notice that we DON'T store the letter 'a' in the db, we store
        # the hash of it
        db.session.add(User(name="a", password_hash=bcrypt.generate_password_hash("a")))
        db.session.commit()
print("seeding complete")
