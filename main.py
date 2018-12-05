from flask import Flask, render_template, send_from_directory, request, url_for, redirect
from database_handler import *
from UserInput_handler import mk_account
import datetime

""" SPENDBOSS WEBSITE - Main.py
    This is the main file for the website to run and handling the user interaction with the server only.
    Flask is integrated for the redirection and passing of variables.
    Database handling and input validation are on different Python file.
    
    This file needs to be running to access the website properly.
    DON'T OPEN THE HTML FILE ITSELF (references will not work)

    version: 0.3
    since: 10 March 2017
"""

app = Flask(__name__)
db_create()


@app.route('/', methods=['GET', 'POST'])
def index():
    """ Index/Home Page function
    This is the first function that will be called when a user connect to the server 
    IP Address (e.g. 127.0.0.1:5000). GET and POST are used for communication with the 
    user input with request form.
    
    IF user login with correct credentials
        :return: call flask function redirect to dashboard function with name and email parameter
    else
        :return: call flask function render_template to template_index.html
    """
    if request.method == "POST":
        attempted_email = request.form['email']
        attempted_password = request.form['password']

        acc_verify = db_query("email, fname, password", "user_base", "email='%s' AND password='%s'" % (attempted_email, attempted_password))
        if acc_verify:
            print("Success.")
            print(acc_verify[1])
            print(acc_verify[0])
            return redirect(url_for('dashboard', name=acc_verify[1], email=acc_verify[0]))
        else:
            # flash will be implemented in the future
            print("Invalid credentials. Try again.")

    return render_template('template_index.html')


@app.route('/signup', methods=['GET', 'POST', 'LOGIN'])
def signup():
    """ Signup/CreateAccount Page function
    This function will render a template for signing up to the site. GET and POST are 
    used for communication with the user input to be submitted to the database.
    
    IF user input has @ in email && password == passwordConfirmation
        database will insert email, firstName, surname, status, password and dateToday
        :return: call flask function redirect to dashboard function with name and email parameter
    else
        :return: call flask function render_template to template_signup.html
    """
    if request.method == "POST":
        mk_name = request.form['mk_fullname']
        mk_email = request.form['mk_email']
        mk_password = request.form['mk_password']
        mk_confirm_pass = request.form['mk_confirm_password']

        user_data = mk_account(mk_name, mk_email, mk_password, mk_confirm_pass)
        if not user_data:
            return render_template('template_signup.html')
        else:
            today = datetime.date.today()
            today_input = "%s-%s-%s" % (today.year, today.month, today.day)
            db_insert("userbase", [user_data[2], user_data[0], user_data[1], user_data[3], "personal", today_input])
            return redirect(url_for('dashboard', name=user_data[0], email=user_data[2]))

    return render_template('template_signup.html')


@app.route('/dashboard-<name>-<email>')
def dashboard(name, email):
    """ Direct to dashboard
    Second validation of account will be implemented in later updates.
    
    :param name: string name of user
    :param email: string email of user
    :return: call flask function render_template to dashboard.html with two variables for the name and email """
    return render_template('dashboard.html', name=name, email=email)


@app.route('/<path:path>')
def send_static2(path):
    """ used to capture a path to a file """
    return send_from_directory('static', path)


# From here below will be error handling functions
@app.errorhandler(404)
def page_not_found(e):
    try:
        return render_template("400err.html")
    except Exception as e:
        return "Spendboss did not know what just happened..\n\n%e" % e


@app.errorhandler(405)
def page_not_found(e):
    try:
        return render_template("400err.html")
    except Exception as e:
        return "Spendboss did not know what just happened..\n\n%e" % e

if __name__ == "__main__":
    app.run(debug=True)




