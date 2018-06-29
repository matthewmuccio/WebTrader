#!/usr/bin/env python3


from flask import Blueprint, render_template, request, redirect


controller = Blueprint("signup", __name__, url_prefix="/")

@controller.route("/", methods=["GET", "POST"])
def show_signup():
	if request.method == "GET":
		return render_template("signup.html")
	# Assumes it is a POST request.
	else:
		email = request.form["email"]
		password1 = request.form["password1"]
		password2 = request.form["password2"]
		if email == "me@matthewmuccio.com" and password1 == password2:
			return render_template("dashboard.html")
		else:
			return render_template("signup.html")