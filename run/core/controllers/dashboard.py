#!/usr/bin/env python3


from flask import abort, Blueprint, redirect, render_template, session, url_for


controller = Blueprint("dashboard", __name__, url_prefix="/dashboard")

@controller.route("/", methods=["GET"])
def show_dashboard():
	if "username" in session:
		return render_template("dashboard.html", title="Home", username=session["username"])
	else:
		return redirect(url_for("signup.show_signup"))

@controller.route("/balance", methods=["GET"])
def show_balance():
	if "username" in session:
		return render_template("balance.html", title="Balance", username=session["username"])
	else:
		return redirect(url_for("signup.show_signup"))

@controller.route("/buy", methods=["GET"])
def show_buy():
	if "username" in session:
		return render_template("buy.html", title="Buy", username=session["username"])
	else:
		return redirect(url_for("signup.show_signup"))

@controller.route("/sell", methods=["GET"])
def show_sell():
	if "username" in session:
		return render_template("sell.html", title="Sell", username=session["username"])
	else:
		return redirect(url_for("signup.show_signup"))

@controller.route("/lookup", methods=["GET"])
def show_lookup():
	if "username" in session:
		return render_template("lookup.html", title="Lookup", username=session["username"])
	else:
		return redirect(url_for("signup.show_signup"))

@controller.route("/quote", methods=["GET"])
def show_quote():
	if "username" in session:
		return render_template("quote.html", title="Quote", username=session["username"])
	else:
		return redirect(url_for("signup.show_signup"))

@controller.route("/portfolio", methods=["GET"])
def show_portfolio():
	if "username" in session:
		return render_template("portfolio.html", title="Portfolio", username=session["username"])
	else:
		return redirect(url_for("signup.show_signup"))

@controller.route("/signout", methods=["GET"])
def signout():
	if "username" in session:
		session.pop("username", None)
		return redirect(url_for("login.show_login"))
	else:
		return redirect(url_for("signup.show_signup"))