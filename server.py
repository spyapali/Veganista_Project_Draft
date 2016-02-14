"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage"""

    return render_template('homepage.html')

@app.route('/sign-up-form')
def sign_up():
    """Sign Up""" 

    return render_template('sign_up.html')

# @app.route("/sign-up", methods=["POST"])
# def sign_up_new_user():
#     """Add a new user to the database and session."""

#     sign-up = request.form.get("")
#     password = request.form.get("password")
#     age = int(request.form.get("age"))
#     zipcode = request.form.get("zipcode")
    
#     # Creating new user in our database based on email, password, age, and zipcode. 
#     new_user = User(email=email, password=password, age=age, zipcode=zipcode)
#     db.session.add(new_user)
#     db.session.commit()

#     new_user_id = new_user.user_id
#     # Add the new user to the session. 
#     session["user_id"] = new_user_id
#     flash("Thank you. Your account has been created.")  

#     new_user_details = "/users/%d" % (new_user_id)
#     return redirect(new_user_details)

#     return render_template("sign_up.html")


@app.route('/sign-up')
def sign_up_process():
    """Sign up processing""" 




@app.route('/login')
def log_in():
    """Sign Up""" 

    return render_template("login.html")


@app.route("/process-login", methods=["POST"])
def process_user_login():
    """Log in existing users, otherwise redirect to sign up page."""

    username = request.form.get("username")
    password = request.form.get("password")
    
    # Grab the user object that matches the email and password values.
    user = User.query.filter_by(username=username, password=password).first()

    # If the user object exists, then add the user_id to the session (logged in).
    # Otherwise, redirect to sign up form to create a new user account.
    if user:
        user_id = user.user_id
        session["user_id"] = user_id
        flash("Logged In")
        user_details = "/users/%d" % (user_id)
        return redirect(user_details)
    else:
        flash("Sorry, you're not a registered user. Please sign up.")
        return redirect("/sign-up-form")



@app.route('/user/<int:user_id>', methods=['POST', 'GET'])
def input_ingredient():
    """User homepage."""
    # To-do: Store e-mail and password in user data table. 
    firstname = request.form.get('firstname')


    return render_template('user.html', firstname=firstname)


@app.route('/recipe', methods=['GET'])
def show_recipe_info():
	"""Display page for the ingredient."""

	recipe = request.args.get('recipe')


	return render_template('recipe.html', recipe=recipe)



# @app.route('/ingredient', methods=['GET'])
# def show_ingredient_info():
#     """Display page for the ingredient."""

#     ingredient = request.args.get('ingredient')
#     # TO-DO: If the ingredient is vegan, it'll get stored in my database. 

#     return render_template('ingredient.html', ingredient=ingredient)





if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
