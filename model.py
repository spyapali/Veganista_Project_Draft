"""Models and database functions for Rating  ss project."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime  

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User of Veganista website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    username = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)

class Input(db.Model):
    """Recipe User enters."""

    __tablename__ = "inputs"


    input_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    eaten_at = db.Column(db.DateTime, default=datetime.utcnow())
    input_name = db.Column(db.String(64), nullable=False)

    user = db.relationship("User", backref=db.backref("inputs", order_by=input_id))
    

class Caching_Data_Recipes(db.Model):
    """Json responses for recipes stored when making an API call."""

    __tablename__ = "recipes" 

    recipe_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    search_term = db.Column(db.String(64))
    json_response = db.Column(db.String(2000))


# Supplement reminders through text will be a nice-to-have feature
class Supplements(db.Model):
    """Supplements taken"""

    __tablename__ = "supplements"

    unique_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    supplement_id = db.Column(db.String(64), nullable=False)
    supplement_taken_at = db.Column(db.DateTime, nullable=False)



##############################################################################
# Helper functions



def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///nutrition'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    db.create_all()
    print "Connected to DB."
