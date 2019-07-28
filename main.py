from flask import Flask, request, redirect, render_template ,url_for, flash
import cgi
import os 

app = Flask(__name__)
app.config['DEBUG'] = True 


@app.route("/")
def index():
    return render_template("welcomepage.html", title = "Welcome Page!")

#need this in order to test the @ symbol, periods and spaces for the email
def email_address_is_valid(email_address):
    if len(email_address) <3 or len (email_address) >20:
        return False

    the_at_symbol = "@"
    the_at_symbol_count = email_address.count(the_at_symbol)
    if the_at_symbol !=1:
        return False 

    the_period = "."
    the_period_count = email_address.count(the_period)
    if the_period != 1:
        return False 

    cant_have_a_space = " "
    cant_have_a_space_count = email_address(cant_have_a_space)
    if cant_have_a_space != 0:
        return False

    else:
        return True


@app.route("/welcomepage", methods = ['POST'])
def welcomepage():

    username_error = ""
    password_erorr = ""
    verify_error = ""
    email_error = ""

    username = request.form['username']
    password = request.form['password']
    verify = request.form['verify']
    email = request.form['email']

    #validating the user and username
    if len(username) < 3 or len(username) >20:
        username_error = "The username you have typed does not fit the criteria. The username must be between 3 and 20 characters."
        password = ""
        verify = ""

    #validating the password
    if len(password) < 3 or len(password) >20:
        password_error = "The password you have typed does not fit the criteria. The password must be between 3 and 20 characters long."
        password = ""
        verify = ""

    #passwords don't match
    if verify !=password:
        verify_error ="Your passwords do not match. Please try again."
        password =""
        verify = ""

    #validating the email
    if len(email) != 0:
        if email_address_is_valid == False:
            email_error = "Please enter a valid email. A valid email includes: 3-20 characters, no spaces, a @ symbol and one period. "
            password = ""
            verify = ""

    if not username_error and not password_error and not email_error and not verify_error:
        username = request.form['username']
        return redirect (url_for('/welcomepage?username ={0}'.format(username)))

    #make it look nice to show the render template at the end
    else:
        return render_template(welcomepage.html, title = "Welcome Page!",
        username = username, username_error = username_erorr,
        password = password, password_error = password_error,
        verify = verify, verify_error = verify_error,
        email_address = email_address, email_error = email_error)



@app.route("/homepage")
def homepage():
        my_user = request.args.get(username)
        return render_template("/homepage", my_user = my_user)

app.run()