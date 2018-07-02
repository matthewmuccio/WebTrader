#!/usr/bin/env python3


from flask import abort, Blueprint, redirect, render_template, request, session, url_for


controller = Blueprint("signup", __name__, url_prefix="/")

@controller.route("", methods=["GET", "POST"])
def show_signup():
	if "username" in session:
		return redirect(url_for("dashboard.show_dashboard"))
	else:
		if request.method == "GET":
			return render_template("signup.html")
		# Assumes it is a POST request.
		else:
			username = request.form["username"]
			session["username"] = username
			password1 = request.form["password1"]
			password2 = request.form["password2"]
			if username == "matthewmuccio" and password1 == password2:
				return redirect(url_for("dashboard.show_dashboard"))
			else:
				return render_template("signup.html")

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