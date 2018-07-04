#!/usr/bin/env python3


from core.models import model

from flask import Blueprint, redirect, render_template, request, session, url_for


controller = Blueprint("login", __name__, url_prefix="/login")

@controller.route("/", methods=["GET", "POST"])
def show_login():
	if "username" in session:
		return redirect(url_for("dashboard.show_dashboard"))
	else:
		if request.method == "GET":
			return render_template("login.html")
		# Assumes it is a POST request.
		else:
			username = request.form["username"]
			password = request.form["password"]
			# Attempts to log in to the account with the entered username and password.
			response = model.login(username, password)
			# If the user has successfully logged in to their account.
			if "Success!" in response:
				session["username"] = username
				return redirect(url_for("dashboard.show_dashboard"))
			# If there was an issue with logging in to the account (username or account does not exist).
			else:
				return render_template("login.html", response=response)