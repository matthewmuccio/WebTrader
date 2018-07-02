#!/usr/bin/env python3


from flask import Blueprint, redirect, render_template, session, url_for


controller = Blueprint("dashboard", __name__, url_prefix="/dashboard")

@controller.route("/", methods=["GET"])
def show_dashboard():
	if "username" in session:
		return render_template("dashboard.html", title="Home")
	else:
		return redirect(url_for("signup.show_signup"))

@controller.route("/balance", methods=["GET"])
def show_balance():
	if "username" in session:
		return render_template("balance.html", title="Balance")
	else:
		return redirect(url_for("signup.show_signup"))

@controller.route("/buy", methods=["GET"])
def show_buy():
	if "username" in session:
		return render_template("buy.html", title="Buy")
	else:
		return redirect(url_for("signup.show_signup"))

@controller.route("/sell", methods=["GET"])
def show_sell():
	if "username" in session:
		return render_template("sell.html", title="Sell")
	else:
		return redirect(url_for("signup.show_signup"))

@controller.route("/lookup", methods=["GET"])
def show_lookup():
	if "username" in session:
		return render_template("lookup.html", title="Lookup")
	else:
		return redirect(url_for("signup.show_signup"))

@controller.route("/quote", methods=["GET"])
def show_quote():
	if "username" in session:
		return render_template("quote.html", title="Quote")
	else:
		return redirect(url_for("signup.show_signup"))

@controller.route("/portfolio", methods=["GET"])
def show_portfolio():
	if "username" in session:
		return render_template("portfolio.html", title="Portfolio")
	else:
		return redirect(url_for("signup.show_signup"))

@controller.route("/signout", methods=["GET"])
def signout():
	session.pop("username", None)
	return redirect(url_for("login.show_login"))

@controller.route("/<text>", methods=["GET"])
def show_dash(text):
	if "username" in session:
		return redirect(url_for("dashboard.show_dashboard"))
	else:
		return redirect(url_for("signup.show_signup"))