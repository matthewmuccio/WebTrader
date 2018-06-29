#!/usr/bin/env python3


from flask import Blueprint, render_template, request, redirect


controller = Blueprint("login", __name__, url_prefix="/login")

@controller.route("/", methods=["GET", "POST"])
def show_login():
	if request.method == "GET":
		return render_template("login.html")
	# Assumes it is a POST request.
	else:
		username = request.form["username"]
		password = request.form["password"]
		if username == "matthewmuccio" and password == "password":
			return render_template("dashboard.html")
		else:
			return render_template("login.html")