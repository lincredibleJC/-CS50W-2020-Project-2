import os

from flask import Flask, session, render_template, request, redirect, url_for, flash
from flask_socketio import SocketIO, emit, join_room, leave_room

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
channels = dict()


@app.route("/")
@login_required
def index():

	session.pop("channel_name", None)
	return render_template("index.html", channels=channels)

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
	if session.get("username") in logged_in:
		logged_in.remove(session.get("username"))
	session.clear()
	return redirect("/")

@app.route("/create_channel", methods=['POST'])
@login_required
def create_channel():
	channel_name = request.form.get("channel_name")

	if not channel_name.replace(" ", "").isalpha():
		flash("This channel name is not valid")
		return redirect("/")

	if channel_name in channels:
		flash("A channel with the same name already exists.")
		session["channel_name"] = channel_name
		return redirect("/channel/"+channel_name)
	
	channels[channel_name] = {"name": channel_name, "messages": []}
	flash("Channel created")
	return redirect("/")

@app.route("/channel/<string:channel_name>")
@login_required
def channel(channel_name):
	if channel_name not in channels:
		flash("Channel does not exist")
		return redirect(index)
	
	session["channel_name"] = channel_name
	
	channel_data = channels[channel_name]

	return render_template("channel.html", channel_data=channel_data)

@socketio.on("send message")
def send_message(message, timestamp):
	username = session.get("username")
	channel_name = session.get('channel_name')

	channels[channel_name]["messages"].append({"username": username, "message": message, "timestamp": timestamp})
	print(channels[channel_name])

	emit("announce message", {"username": username,
							 "message": message,
							 "timestamp": timestamp},
							 room=channel_name)

@socketio.on('join')
def on_join():
    room = session.get("channel_name")
    join_room(room)

    username = session.get("username")
    emit("announce join", {"username": username}, room=room)

@socketio.on('leave')
def on_leave():
    room = session.get("channel_name")
    leave_room(room)
    print(room)
    username = session.get("username")
    emit("announce leave", {"username": username}, room=room)
