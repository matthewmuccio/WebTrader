#!/usr/bin/env python3


from flask import Blueprint, render_template, request, redirect


controller = Blueprint("login", __name__, url_prefix="/login")

@controller.route("/", methods=["GET", "POST"])
def show_login():
	if request.method == "GET":
		return render_template("login.html")
	# Assumes it is a POST request.
	else:
		email = request.form["email"]
		password = request.form["password"]
		if email == "me@matthewmuccio.com" and password == "password":
			return redirect("/dashboard")
		else:
			return redirect("/login")