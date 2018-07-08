#!/usr/bin/env python3


from flask import abort, Blueprint, redirect, render_template, request, session, url_for

from core.models import model


controller = Blueprint("admin", __name__, url_prefix="/admin")

@controller.route("/", methods=["GET"])
def show_dashboard():
	# In session (user signed in) and username is admin
	if "username" in session and session["username"] == "admin":
		return render_template("admin.html", \
                                title="Home", \
								username="admin")
	# Out of session (user not signed in)
	else:
		return redirect(url_for("signup.show_signup"))

@controller.route("/balance", methods=["GET"])
def show_balance():
	# In session (user signed in) and username is admin
	if "username" in session and session["username"] == "admin":
		return render_template("admin.html", \
                                title="Home", \
								username="admin")
	# Out of session (user not signed in)
	else:
		return redirect(url_for("signup.show_signup"))

@controller.route("/deposit", methods=["GET"])
def show_deposit():
	# In session (user signed in) and username is admin
	if "username" in session and session["username"] == "admin":
		return render_template("admin.html", \
                                title="Home", \
								username="admin")
	# Out of session (user not signed in)
	else:
		return redirect(url_for("signup.show_signup"))

@controller.route("/withdraw", methods=["GET"])
def show_withdraw():
	# In session (user signed in) and username is admin
	if "username" in session and session["username"] == "admin":
		return render_template("admin.html", \
                                title="Home", \
								username="admin")
	# Out of session (user not signed in)
	else:
		return redirect(url_for("signup.show_signup"))

@controller.route("/set", methods=["GET"])
def show_set():
	# In session (user signed in) and username is admin
	if "username" in session and session["username"] == "admin":
		return render_template("admin.html", \
                                title="Home", \
								username="admin")
	# Out of session (user not signed in)
	else:
		return redirect(url_for("signup.show_signup"))

@controller.route("/portfolio", methods=["GET"])
def show_portfolio():
	# In session (user signed in) and username is admin
	if "username" in session and session["username"] == "admin":
		return render_template("admin.html", \
                                title="Home", \
								username="admin")
	# Out of session (user not signed in)
	else:
		return redirect(url_for("signup.show_signup"))

@controller.route("/leaderboard", methods=["GET"])
def show_leaderboard():
	# In session (user signed in) and username is admin
	if "username" in session and session["username"] == "admin":
		return render_template("admin.html", \
                                title="Home", \
								username="admin")
	# Out of session (user not signed in)
	else:
		return redirect(url_for("signup.show_signup"))

@controller.route("/users", methods=["GET"])
def show_users():
	# In session (user signed in) and username is admin
	if "username" in session and session["username"] == "admin":
		return render_template("admin.html", \
                                title="Home", \
								username="admin")
	# Out of session (user not signed in)
	else:
		return redirect(url_for("signup.show_signup"))