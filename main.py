from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy




app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


@app.route("/")
def index():
    return render_template('index.html', title = "Please sign up")

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    username = ""
    username_error = ""
    password_error = ""
    verify_error = ""

    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        existing_user = User.query.filter_by(username = username).first()

        if len(username) < 3:
            username_error = "Usernames must be longer than 3 characters. Or they will not be accepted."
            if username == "":
                username_error = "Please enter a username."
      
        if password != verify:
            password_error = "Passwords must match."
            verify_error = "Passwords must match."
            
        if len(password) < 3:
            password_error = "Password must be longer than 3 characters. Or they will not be accepted."
            if password == "":
                password_error = "Please enter a valid password."

        if password != verify:
            password_error = "Passwords must match."
            verify_error = "Passwords must match."

        if not username_error and not password_error and not verify_error:
            if not existing_user:
                new_user = User(username, password)
                db.session.add(new_user)
                db.session.commit()
                session['username'] = username
                return redirect('/newpost')
            else:
                username_error = "Username is already claimed. Please try another username"

    return render_template('signup.html', username = username, username_error = username_error, password_error = password_error, verify_error = verify_error)


@app.route('/login', methods=['POST', 'GET'])
def login():
    username = ""
    username_error = ""
    password_error = ""

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username = username).first()

        if not user:
            username_error = "User does not exist."
            return redirect ('/homepage')
            if username == "":
                username_error = "Please enter your username."
                return redirect ('/welcomepage')

        if password == "":
            password_error = "Please enter your password."
            return redirect('/welcomepage')
   
        if user and user.password != password:
            password_error = "That is the wrong password."

        if user and user.password == password:
            session['username'] = username
            return redirect('/index')

    return render_template('welcomepage.html', username = username, username_error = username_error, password_error = password_error)

@app.route('/newpost', methods=['POST', 'GET'])
def create_new_post():
    blog_title = ""
    blog_content = ""
    title_error = ""
    content_error = ""

    if request.method == 'POST':
        blog_title = request.form['blog_title']
        blog_content = request.form['blog_content']

        if blog_title == "":
            title_error = "Please enter a title!"

        if blog_content == "":
            content_error = "Please enter a post!"

        if title_error == "" and content_error == "":
            new_post = Blog(blog_title, blog_content, owner)
            db.session.add(new_post)
            db.session.commit()
            blog_id = Blog.query.order_by(Blog.id.desc()).first()
            user = owner

            return redirect('/blog?id={}&user={}'.format(blog_id.id, user.username))

    return render_template('newpost.html', title = "Add a new post", blog_title = blog_title, blog_content = blog_content, title_error = title_error, content_error = content_error)


app.run()