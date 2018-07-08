#!/usr/bin/env python3


from flask import abort, Blueprint, redirect, render_template, request, session, url_for

from core.models import model


controller = Blueprint("admin", __name__, url_prefix="/admin")

@controller.route("/", methods=["GET"])
def show_admin_dashboard():
	# In session (user signed in) and username is admin
	if "username" in session and session["username"] == "admin":
		# TODO: CODE
		pass
	# Out of session (user not signed in)
	else:
		return redirect(url_for("signup.show_signup"))

@controller.route("/admin/balance", methods=["GET"])
def show_admin_balance():
	# In session (user signed in) and username is admin
	if "username" in session and session["username"] == "admin":
		# TODO: CODE
		pass
	# Out of session (user not signed in)
	else:
		return redirect(url_for("signup.show_signup"))

@controller.route("/admin/deposit", methods=["GET"])
def show_admin_deposit():
	# In session (user signed in) and username is admin
	if "username" in session and session["username"] == "admin":
		# TODO: CODE
		pass
	# Out of session (user not signed in)
	else:
		return redirect(url_for("signup.show_signup"))

@controller.route("/admin/withdraw", methods=["GET"])
def show_admin_withdraw():
	# In session (user signed in) and username is admin
	if "username" in session and session["username"] == "admin":
		# TODO: CODE
		pass
	# Out of session (user not signed in)
	else:
		return redirect(url_for("signup.show_signup"))

@controller.route("/admin/set", methods=["GET"])
def show_admin_set():
	# In session (user signed in) and username is admin
	if "username" in session and session["username"] == "admin":
		# TODO: CODE
		pass
	# Out of session (user not signed in)
	else:
		return redirect(url_for("signup.show_signup"))

@controller.route("/admin/portfolio", methods=["GET"])
def show_admin_portfolio():
	# In session (user signed in) and username is admin
	if "username" in session and session["username"] == "admin":
		# TODO: CODE
		pass
	# Out of session (user not signed in)
	else:
		return redirect(url_for("signup.show_signup"))

@controller.route("/admin/leaderboard", methods=["GET"])
def show_admin_leaderboard():
	# In session (user signed in) and username is admin
	if "username" in session and session["username"] == "admin":
		# TODO: CODE
		pass
	# Out of session (user not signed in)
	else:
		return redirect(url_for("signup.show_signup"))

@controller.route("/admin/users", methods=["GET"])
def show_admin_users():
	# In session (user signed in) and username is admin
	if "username" in session and session["username"] == "admin":
		# TODO: CODE
		pass
	# Out of session (user not signed in)
	else:
		return redirect(url_for("signup.show_signup"))