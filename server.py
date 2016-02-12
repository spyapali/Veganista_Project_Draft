"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Recipe

from datetime import utc 


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


@app.route('/sign-up', methods=['POST'])
def sign_up_process():
    """Sign up processing""" 

    firstname = request.form.get("firstname")
    lastname = request.form.get("lastname")
    username = request.form.get("username")
    password = request.form.get("password")

    user = User(first_name=firstname, last_name=lastname,
                    username=username, password=password)

    db.session.add(user)
    db.session.commit()

    flash("Thanks for signing up! Please log in to continue.")
    return redirect("/login")


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
        user_details = "/user/%d" % (user_id)
        return redirect(user_details)
    else:
        flash("Sorry, you're not a registered user. Please sign up.")
        return redirect("/sign-up-form")



@app.route('/user/<int:user_id>', methods=['POST', 'GET'])
def show_user_page(user_id):
    """User homepage."""
    # To-do: Store e-mail and password in user data table. 
    user = User.query.get(user_id)
    firstname = user.first_name
    # creating a user object.

    

    return render_template('user.html', firstname=firstname, user=user)


# @app.route('/user/<int:user_id>/recipe', methods=['POST'])
# def process_recipe(user_id):

#     recipe = request.form.get("recipe")
#     recipe = Input(user_id=user_id, eaten_at=datetime.utc.now())


@app.route('/recipe/<int:recipe_id>', methods=['GET'])
def show_recipe_info():
	"""Display page for the ingredient."""

	recipe = request.args.get('recipe')
    # To-Do list: display the recipe name and the time during which the recipe appeared.

	return render_template('recipe.html', recipe=recipe)


@app.route("/logout")
def log_out_user():
    """Logging out user and redirecting to homepage."""

    del session["user_id"]
    flash("Logged out")
    return redirect("/")





if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
