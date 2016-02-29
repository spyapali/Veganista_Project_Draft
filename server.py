"""Veganista Project."""

from __future__ import division 

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session, json, url_for

import requests

from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, User_Stats, Input, Recipe 

import json 

import pprint 

from sys import argv 

from datetime import datetime, date

from sqlalchemy import func 




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


    flash("Thanks for signing up! Please fill out more information below.")
    return redirect("/login")

# @app.route('/user-stats'):
#     """User logs in information about their height, weight, age, and gender"""

#     return render_template ("user_stats.html")
    


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
    input_resp = input_resp.lower()
    input_obj = Input(user_id=user_id, eaten_at=date.today(), input_name=input_resp)

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

@app.route('/show_recipes_date/date', methods=['GET','POST'])
def show_recipe_date():
    """Show recipes for each date selected"""
#   Grab the date from the URL. 
    recipe_date = request.args.get("date") # A unicode string. 
    # 2016-02-18
    recipe_date = datetime.strptime(recipe_date, "%Y-%m-%d") # coverted into datetime object. 
    recipe_date = recipe_date.date()
    recipe_inputs = Input.query.filter_by(eaten_at = recipe_date).all()
    user_id = session['user_id']
    user = User.query.get(user_id)
    firstname = user.first_name

     

    # resulting_inputs = Input.query.filter_by(eaten_at.date=date)

    # print resulting_inputs

    # datetime.today() = datetime.now()
    return render_template("dynamic_user_log.html", recipe_inputs=recipe_inputs, user=user, firstname=firstname, recipe_date=recipe_date)

@app.route('/calculate-recipe-totals')
def calculate_recipe_totals():
    # divide up the recipes based on time 
    # calculate each total based on macronutrient in question 
    # render an html page which allows viewers to select whether they'd like to see progress over week or month. 
    recipe_dates = db.session.query(Input.eaten_at).group_by(Input.eaten_at).all()
    print recipe_dates
    date_list = []
    for date_combo in recipe_dates:
        date = date_combo[0]
        date_list.append(date)

    date_dictionary = {}
    for i in range(len(date_list)):
        date_dictionary[date_list[i]] = Input.query.filter(Input.eaten_at == date_list[i]).all()

    d_total_fat = []
    d_total_carbs = []
    d_total_protein = []

    for value in date_dictionary.values():
        total_fat = 0 
        total_protein = 0 
        total_carbs = 0 

        for recipe in value:
            recipe_obj = Recipe.query.filter_by(input_name = recipe.input_name).first()
            total_fat += recipe_obj.percentage_of_fat
            total_protein += recipe_obj.percentage_of_protein
            total_carbs += recipe_obj.percentage_of_carbs

        d_total_fat.append(total_fat)
        d_total_carbs.append(total_carbs)
        d_total_protein.append(total_protein)

    print d_total_fat
    print d_total_carbs
    print d_total_protein 

    # percentage_data = json.dumps(total_percentages)

    new_date_list = []
    for item in date_list:
        item = item.strftime('%m/%d')
        new_date_list.append(item)

    d_total_fat = json.dumps(d_total_fat)
    d_total_carbs = json.dumps(d_total_carbs)
    d_total_protein = json.dumps(d_total_protein)
    date_list = json.dumps(new_date_list)
    # return "<HTML><p>YAYAYAYAYAY</p></HTML>"


    return render_template("show_progress.html", d_total_fat=d_total_fat, d_total_carbs=d_total_carbs, d_total_protein=d_total_protein, date_list=date_list)


@app.route('/calculate-recipes/<recipe_date>', methods=['GET', 'POST'])
def calculate_recipes(recipe_date):
    # Filter out each recipe based on input name in the Caching Database 
    # Grab nutritional data from each recipe 
    # Add all of them up. 
    print "Here is my recipe_date: ", recipe_date
    total_fat = 0 
    total_carbs = 0 
    total_protein = 0 
    # Want to calculate the total percentages of fat, carbs and protein 
    recipe_inputs = Input.query.filter_by(eaten_at = recipe_date).all()
    print recipe_inputs
    for recipe in recipe_inputs:
        recipe = Recipe.query.filter_by(input_name=recipe.input_name).first()
        total_fat += recipe.percentage_of_fat
        total_carbs += recipe.percentage_of_carbs
        total_protein += recipe.percentage_of_protein

    recipe_totals = {}
    total_fat = "{0:.2f}".format(total_fat)
    recipe_totals['total_fat'] = total_fat
    total_carbs = "{0:.2f}".format(total_carbs)
    recipe_totals['total_carbs'] = total_carbs
    total_protein = "{0:.2f}".format(total_protein)
    recipe_totals['total_protein'] = total_protein



    recipe_totals = json.dumps(recipe_totals)




    return render_template("recipes_date.html", recipe_date=recipe_date, total_fat=total_fat, total_carbs=total_carbs,
                                             total_protein=total_protein, recipe_totals=recipe_totals)


    


@app.route('/')

@app.route('/recipe/input/<input_name>', methods=['GET'])
def process_recipe_info(input_name):
    """Make API call, store stuff for the ingredient."""
  
    # user_recipe = request.args.get('input_name')
    # grab input name and query database for it. 

    user_recipe_obj = Recipe.query.filter_by(input_name=input_name).first()
    # print "This is the user_recipe_obj: ", user_recipe_obj 

    #break down input_name into a list of words and then query for whatever matches the most, and ask, did you mean this?"
    #if user presses nope, move on to making the api call. 
    if user_recipe_obj:
        input_name = user_recipe_obj.input_name 
        percentage_of_fat = user_recipe_obj.percentage_of_fat
        percentage_of_carbs = user_recipe_obj.percentage_of_carbs
        percentage_of_protein = user_recipe_obj.percentage_of_protein

        #create a dictionary for chart.js 
        recipe_data = {}
        percentage_of_fat = "{0:.2f}".format(percentage_of_fat)
        recipe_data['percentage_of_fat'] = percentage_of_fat
        percentage_of_carbs = "{0:.2f}".format(percentage_of_carbs)
        recipe_data['percentage_of_carbs'] = percentage_of_carbs
        percentage_of_protein = "{0:.2f}".format(percentage_of_protein)
        recipe_data['percentage_of_protein'] = percentage_of_protein

        recipe_data = json.dumps(recipe_data)

    # search for the term within the database. 
    # if not there, call the api and search for the information within the api. 
    else:
        print input_name
        input_name = str(input_name)
        print input_name
        json_string = requests.get("https://api.edamam.com/search?q="+input_name+"&app_id=22a5c077&app_key=9e70212d2e504688b4f44ee2651a7769&health=vegan") 
        # import pdb; pdb.set_trace()
        print "json_string", json_string  
        json_dict = json_string.json() # converting this into a python dictionary.
        print "json_dict", json_dict


        json_recipe = json_dict['hits'][0]
        print "json_recipe", json_recipe 
        recipe = json_recipe['recipe']
        print "recipe", recipe 

        # grabbing serving of the recipe from json object. 
        serving = recipe['yield']

        # grabbing name of the recipe from json object. 
        recipe_name = recipe['label'].lower()

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

        stored_recipe = Recipe(input_name=input_name, percentage_of_protein=percentage_of_protein,
                                                percentage_of_fat=percentage_of_fat, percentage_of_carbs=percentage_of_carbs)

        db.session.add(stored_recipe)
        db.session.commit()

        #create a dictionary for chart.js 
        recipe_data = {}
        percentage_of_fat = "{0:.2f}".format(percentage_of_fat)
        recipe_data['percentage_of_fat'] = percentage_of_fat
        percentage_of_carbs = "{0:.2f}".format(percentage_of_carbs)
        recipe_data['percentage_of_carbs'] = percentage_of_carbs
        percentage_of_protein = "{0:.2f}".format(percentage_of_protein)
        recipe_data['percentage_of_protein'] = percentage_of_protein

        recipe_data = json.dumps(recipe_data)





    return render_template("recipe.html", input_name=input_name, percentage_of_fat=percentage_of_fat, percentage_of_carbs=percentage_of_carbs,
                                             percentage_of_protein=percentage_of_protein, data=recipe_data)


   
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
