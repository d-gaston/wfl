from flask import Flask, make_response, jsonify, request, session, g
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import dotenv_values
from flask_bcrypt import Bcrypt
from models import db, Restaurant, Review, User
import json

# load the .env file where our secrets are stored
config = dotenv_values(".env")

app = Flask(__name__)
app.debug = True
# get the flask secret key from the .env
# (this is how you'll store and retrieve api keys as well)
app.secret_key = config['FLASK_SECRET_KEY']
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)

db.init_app(app)
###############################
# Authentication
###############################
@app.get('/check_session')
def check_session():
    '''
    This route is what keeps us logged in when we refresh the page or 
    leave and come back. Because we set the session in the login route,
    it will persist in the session object. We then see if there is a 
    user id stored in the session, and if there is we get the user
    object with that id and return it. 
    '''
    user = db.session.get(User, session.get('user_id'))
    print(f'check session {session.get("user_id")}')
    if user:
        return user.to_dict(rules=['-password_hash']), 200
    else:
        # The first time a user visits a page (i.e. is not logged in)
        # we will return this.
        return {"message": "No user logged in"}, 401

@app.delete('/logout')
def logout():
    # logging out is simply removing the key we set in the session from log in
    session.pop('user_id')
    return { "message": "Logged out"}, 200



@app.post('/login')
def login():
    # get the data from the post request (dict of username/password)
    data = request.json
    # get the user based on username
    user = User.query.filter(User.name == data.get('name')).first()

    # check that the hash of supplied password matches the hash stored in the db
    if user and bcrypt.check_password_hash(user.password_hash, data.get('password')):
        # if successful, set a key in the session with the user id
        session["user_id"] = user.id
        print("success")
        # return the user we just logged in
        return user.to_dict(), 200
    else:
        # DO NOT say which was wrong; you don't want to tell a malicious user
        # if e.g. they got the user name correct but password wrong
        return { "error": "Invalid username or password" }, 401
###############################
    
@app.get("/reviews")
def get_reviews():
    reviews = Review.query.all()

    return [r.to_dict() for r in reviews]


@app.post("/reviews")
def post_review():
    data = request.json

    try:
        restaurant = Restaurant.query.filter(
            Restaurant.name == data.get("restaurant")
        ).first()
        new_review = Review(
            reviewer=data.get("reviewer"),
            review=data.get("review"),
            rating=data.get("rating"),
            restaurant=restaurant,
        )
        db.session.add(new_review)
        db.session.commit()
        return new_review.to_dict(), 201
    except Exception as e:
        print(e)
        return {"error": f"could not post review: {e}"}, 405


@app.get("/restaurants")
def get_restaurants():
    # get all the restaurants from the table
    restaurants = Restaurant.query.all()
    """
    SELECT * FROM restaurant_table
    """
    print(restaurants)
    # convert restaurant python objects to dictionaries
    restaurant_dicts = []
    for r in restaurants:
        restaurant_dicts.append(r.to_dict())
    return restaurant_dicts
    # return [r.to_dict() for r in restaurants]


@app.get("/restaurants/<int:id>")
def get_restaurant_by_id(id):
    # restaurant = Restaurant.query.filter(Restaurant.id == id) # canvas method
    # print(restaurant)
    # same as above but less typing
    restaurant = db.session.get(Restaurant, id)
    """
    SELECT * FROM restaurant_table WHERE id = :id:
    """
    # if the id was not there, restaurant will be None. If so return error
    if not restaurant:
        return {"error": f"restaurant with id {id} not found"}, 404
    return restaurant.to_dict()


@app.post("/restaurants")
def post_restaurant():
    # get the json from the request that the user sent
    data = request.json
    try:
        # make a new object from the request json
        restaurant = Restaurant(
            name=data.get("name"),
            photo=data.get("photo"),
            address=data.get("address"),
            cuisine=data.get("cuisine"),
        )
        # add to the db
        db.session.add(restaurant)
        db.session.commit()
        # return object we just made
        return restaurant.to_dict(), 201
    except Exception as e:
        # if anything in the try block goes wrong, execute this
        print(e)
        return {"error": f"could not post restaurant {e}"}, 405


@app.delete("/restaurants/<int:id>")
def delete_restaurant(id):
    restaurant = db.session.get(Restaurant, id)
    if not restaurant:
        return {"error": "restaurant not found"}, 404
    # remove object from db
    db.session.delete(restaurant)
    db.session.commit()
    return {}, 202


@app.patch("/restaurants/<int:id>")
def patch_restaurant(id):
    restaurant = db.session.get(Restaurant, id)
    if not restaurant:
        return {"error": "restaurant not found"}, 404
    try:
        data = request.json
        # if 'name' in data:
        #     restaurant.name = data['name']

        # each key in the request json should correspond to the name
        # of an attribute in the Restaurant object.
        # This loop sets the attribute to the value of the key in the json
        for key in data:
            setattr(restaurant, key, data[key])
        db.session.add(restaurant)
        db.session.commit()
        return restaurant.to_dict(), 201
    except Exception as e:
        return {"error": f"{e}"}


if __name__ == "__main__":
    app.run(port=5555, debug=True)
