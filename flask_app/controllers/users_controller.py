from flask import render_template, request, redirect, session
from flask_app import app
from flask_app.models.users_model import User

@app.route( "/", methods=["GET"] )
def display_login_registration():
    return render_template( "index.html" )

@app.route( "/user/new", methods=["POST"] )
def create_user():
    if User.validate_user( request.form ) == False:
        return redirect( "/" )
    encrypted_password = User.encrypt_string( request.form["password"] )
    data = {
        **request.form,
        "password" : encrypted_password
    }
    user_id = User.create_one( data )
    session["user_id"] = user_id
    return redirect( "/user/welcome" )

@app.route( "/user/welcome", methods=["GET"] )
def display_welcome_page():
    return render_template( "welcome_page.html" )

@app.route( "/user/login", methods=["POST"] )
def login():
    current_user = User.get_one( request.form )
    if current_user == None:
        flash( "Email not found!", "error_login_email" )
        return redirect( "/" )
    if User.validate_password( request.form["password"], current_user.password ) == False:
        return redirect( "/" )
    session["user_id"] = current_user.id
    session["first_name"] = current_user.first_name
    return redirect( "/user/welcome" )

@app.route("/user/logout")
def logout_user():
    session.clear()
    return redirect("/")