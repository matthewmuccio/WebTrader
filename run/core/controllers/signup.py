#!/usr/bin/env python3

from flask import abort, Blueprint, redirect, render_template, request, session, url_for

from core.models import model

controller = Blueprint("signup", __name__, url_prefix="/")

@controller.route("/", methods=["GET", "POST"])
def show_signup():
	# In session (user signed in)
	if "username" in session:
			return redirect(url_for("dashboard.show_dashboard"))
	# Out of session (user not signed in)
	else:
		# GET request
		if request.method == "GET":
			return render_template("signup.html")
		# POST request
		else:
			# Accesses current form data (data transmitted in a POST request).
			username = request.form["username"]
			password1 = request.form["password1"]
			password2 = request.form["password2"]
			# If the passwords the user entered match.
			if password1 == password2:
				# Attempts to create an account with the entered username and password.
				response = model.create_account(username, password1)
				# If the user's account has been successfully created.
				if "Success" in response:
					session["username"] = username
					return redirect(url_for("dashboard.show_dashboard"))
				# If there was an issue creating the account (username already exists, account already exists, or username was invalid).
				else:
					return render_template("signup.html", response=response)
			# If the passowrds the user entered do not match.
			else:
				return render_template("signup.html", response=["Passwords did not match."])

# Handles page requests for non-existent pages (404 errors).
@controller.route("/<path:path>", methods=["GET"])
def show_404(path):
	if "username" in session:
		return redirect(url_for("dashboard.show_dashboard"))
	else:
		abort(404)

@controller.errorhandler(404)
def page_not_found(e):
	return render_template("404.html"), 404