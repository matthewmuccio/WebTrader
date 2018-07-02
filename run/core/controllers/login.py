#!/usr/bin/env python3


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
			session["username"] = username
			password = request.form["password"]
			if username == "matthewmuccio" and password == "password":
				return redirect(url_for("dashboard.show_dashboard"))
			else:
				return render_template("login.html")