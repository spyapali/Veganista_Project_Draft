"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template('sign_up.html')

@app.route('/user', methods=['POST', 'GET'])
def input_ingredient():
    """User homepage."""
    # To-do: Store e-mail and password in user data table. 
    name = request.form.get('name')
    

    return render_template('user.html', name=name)


@app.route('/recipe', methods=['GET'])
def show_recipe_info():
	"""Display page for the ingredient."""

	recipe = request.args.get('recipe')

	return render_template('recipe.html', recipe=recipe)



@app.route('/ingredient', methods=['GET'])
def show_ingredient_info():
    """Display page for the ingredient."""

    ingredient = request.args.get('ingredient')

    return render_template('ingredient.html', ingredient=ingredient)





if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
