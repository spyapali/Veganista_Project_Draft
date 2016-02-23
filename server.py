"""Veganista Project."""

from __future__ import division 

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session, json, url_for

from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Input, Caching_Data_Recipes

import json 

import pprint 

from sys import argv 

from datetime import datetime





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



@app.route("/user/<int:user_id>", methods=['GET', 'POST'])
def show_user_page(user_id):
    """User homepage."""
    # To-do: Store e-mail and password in user data table. 
    user = User.query.get(user_id)
    firstname = user.first_name
    # creating a user object.

    

    return render_template('user.html', firstname=firstname, user=user)


@app.route('/user/<int:user_id>/input', methods=['GET', 'POST'])
def process_input(user_id):

    input_resp = request.args.get('input')
    input_obj = Input(user_id=user_id, eaten_at=datetime.utcnow(), input_name=input_resp)

    db.session.add(input_obj)
    db.session.commit()

    user = User.query.get(user_id)
    firstname = user.first_name

    input_name = input_obj.input_name

    flash('Your recipe has been stored.')
    # return redirect('/recipe/input')
    return redirect(url_for('show_user_log', user_id=user_id))


# @app.route('/user/<int:user_id>/recipe')
# def process_recipe(user_id):


@app.route('/user-log/<int:user_id>/input_name')
def show_user_log(user_id):
    """show log of user inputs. """

    user = User.query.get(user_id)
    firstname = user.first_name


    return render_template("user_log.html", user=user, firstname=firstname)

@app.route('/show_recipes_date', methods=['GET','POST'])
def show_recipe_date():
    """Show recipes for each date selected"""
#   Grab the date from the URL. 
    date = request.args.get("date")
    print date 

    # datetime.today() = datetime.now()
    return "<HTML><p>This page shows recipes on a particular date.</p></HTML>"


@app.route('/recipe/input/<input_name>', methods=['GET'])
def process_recipe_info(input_name):
    """Make API call, store stuff for the ingredient."""

    try:
  
        # user_recipe = request.args.get('input_name')
        user_recipe_obj = Caching_Data_Recipes.query.filter_by(search_term=input_name).first()

        if user_recipe_obj:
            search_term = user_recipe_obj.search_term 
            percentage_of_fat = user_recipe_obj.percentage_of_fat
            percentage_of_carbs = user_recipe_obj.percentage_of_carbs
            percentage_of_protein = user_recipe_obj.percentage_of_protein

            #create a dictionary for chart.js 
            recipe_data = {}
            recipe_data['percentage_of_fat'] = percentage_of_fat
            recipe_data['percentage_of_carbs'] = percentage_of_carbs
            recipe_data['percentage_of_protein'] = percentage_of_protein

            recipe_data = json.dumps(recipe_data)

        # search for the term within the database. 
        # if not there, call the api and search for the information within the api. 
        else:
            json_string = open(argv[1]).read()
            json_dict = json.loads(json_string)

            json_recipe = json_dict['hits'][0]
            recipe = json_recipe['recipe']

            # grabbing serving of the recipe from json object. 
            serving = recipe['yield']

            # grabbing name of the recipe from json object. 
            search_term = recipe['label'].lower()

            # grabbing fat percentage of the recipe from the json object. 
            total_fat = recipe['totalDaily']['FAT']
            percentage_of_fat = total_fat['quantity']
            percentage_of_fat = float(percentage_of_fat)/float(serving)
            print percentage_of_fat

            # grabbing carbs percentage of the recipe from the json object. 
            total_carbs = recipe['totalDaily']['CHOCDF']
            percentage_of_carbs = total_carbs['quantity']
            percentage_of_carbs = float(percentage_of_carbs)/float(serving)
            print percentage_of_carbs

            # grabbing protein percentage of the recipe from the json object. 
            total_protein = recipe['totalDaily']['PROCNT']
            percentage_of_protein = total_protein['quantity']
            percentage_of_protein = float(percentage_of_protein)/float(serving)
            print percentage_of_protein

            # cache the data being called from the api.

            stored_recipe = Caching_Data_Recipes(search_term=search_term, percentage_of_protein=percentage_of_protein,
                                                    percentage_of_fat=percentage_of_fat, percentage_of_carbs=percentage_of_carbs)

            db.session.add(stored_recipe)
            db.session.commit()

            #create a dictionary for chart.js 
            recipe_data = {}
            recipe_data['percentage_of_fat'] = percentage_of_fats
            recipe_data['percentage_of_carbs'] = percentage_of_carbs
            recipe_data['percentage_of_protein'] = percentage_of_protein

            recipe_data = json.dumps(recipe_data)





        return render_template("recipe.html", search_term=search_term, percentage_of_fat=percentage_of_fat, percentage_of_carbs=percentage_of_carbs,
                                                 percentage_of_protein=percentage_of_protein, data=recipe_data)


    except ValueError or IndexError:
        print "<HTML><p>I'm sorry, but our database has not found your request</p></HTML>."


    # return "<HTML><body>%s</body></HTML>" %(user_recipe)


    # if ingredient is in cache 
    # get object from the database 
    # get protein, fat and carbs 
    # calc efficiency of daily requirements for one serving. 

    # else:

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                





    # recipe = request.args.get('recipe')
    # To-Do list: display the recipe name and the time during which the recipe appeared.


    # return render_template('recipe.html', recipe=recipe)


@app.route('/')

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