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
								username="Admin")
	# Out of session (user not signed in)
	else:
		return redirect(url_for("signup.show_signup"))

@controller.route("/balance", methods=["GET", "POST"])
def show_balance():
	# In session (user signed in) and username is admin
	if "username" in session and session["username"] == "admin":
		# GET request
		if request.method == "GET":
			return render_template("admin-balance.html", \
									title="Balance", \
									username="Admin")
		# POST request
		else:
			# Accesses current form data (data transmitted in a POST request).
			username = request.form["username"]
			# Attempts to get the balance of the user with the given username.
			balance = model.get_balance(username)
			# If balance is a float.
			if type(balance) == type(0.0):
				response = [format(balance, ".2f")]
			# If balance is an error message.
			else:
				response = balance
			return render_template("admin-balance.html", \
									title="Balance", \
									username="Admin", \
									user=username, \
									response=response)
	# Out of session (user not signed in)
	else:
		return redirect(url_for("signup.show_signup"))

@controller.route("/deposit", methods=["GET", "POST"])
def show_deposit():
	# In session (user signed in) and username is admin
	if "username" in session and session["username"] == "admin":
		return render_template("admin-deposit.html", \
                                title="Deposit", \
								username="Admin")
	# Out of session (user not signed in)
	else:
		return redirect(url_for("signup.show_signup"))

@controller.route("/withdraw", methods=["GET", "POST"])
def show_withdraw():
	# In session (user signed in) and username is admin
	if "username" in session and session["username"] == "admin":
		return render_template("admin-withdraw.html", \
                                title="Withdraw", \
								username="Admin")
	# Out of session (user not signed in)
	else:
		return redirect(url_for("signup.show_signup"))

@controller.route("/set", methods=["GET", "POST"])
def show_set():
	# In session (user signed in) and username is admin
	if "username" in session and session["username"] == "admin":
		return render_template("admin-set.html", \
                                title="Set Balance", \
								username="Admin")
	# Out of session (user not signed in)
	else:
		return redirect(url_for("signup.show_signup"))

@controller.route("/portfolio", methods=["GET", "POST"])
def show_portfolio():
	# In session (user signed in) and username is admin
	if "username" in session and session["username"] == "admin":
		return render_template("admin-portfolio.html", \
                                title="Portfolio", \
								username="Admin")
	# Out of session (user not signed in)
	else:
		return redirect(url_for("signup.show_signup"))

@controller.route("/leaderboard", methods=["GET"])
def show_leaderboard():
	# In session (user signed in) and username is admin
	if "username" in session and session["username"] == "admin":
		return render_template("admin-leaderboard.html", \
                                title="Leaderboard", \
								username="Admin")
	# Out of session (user not signed in)
	else:
		return redirect(url_for("signup.show_signup"))

@controller.route("/users", methods=["GET"])
def show_users():
	# In session (user signed in) and username is admin
	if "username" in session and session["username"] == "admin":
		return render_template("admin-users.html", \
                                title="Users", \
								username="Admin")
	# Out of session (user not signed in)
	else:
		return redirect(url_for("signup.show_signup"))