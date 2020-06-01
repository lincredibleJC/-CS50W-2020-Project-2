import os

from flask import Flask, session, render_template, request, redirect, url_for, flash
from flask_socketio import SocketIO, emit

from helpers import login_required 

app = Flask(__name__)

# app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SECRET_KEY"] = "tempKey"
socketio = SocketIO(app)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"

users = []
logged_in = []

@app.route("/")
@login_required
def index():
	return render_template("index.html")

@app.route("/login", methods=['GET','POST'])
def login():

	if request.method == "POST":
		username = request.form.get("username")

		if not username.replace(" ", "").isalpha():
			flash("Your username is not valid")
			return redirect("login.html")

		if username in users:
			if username in logged_in:
				flash("This name is currently being used")
				return redirect("login.html")	
			else:
				flash("You have successfully logged in")
				logged_in.append(username)
				session['username'] = username
				return redirect("/")
		else:
			users.append(username)
			flash("User created")
			logged_in.append(username)
			session['username'] = username
			flash("You have successfully logged in")
			return redirect("/")
	else:
		return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
	logged_in.remove(session.get("username"))
	session.clear()
	return redirect("/")
