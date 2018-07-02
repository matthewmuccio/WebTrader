#!/usr/bin/env python3


from flask import Blueprint, render_template


controller = Blueprint("dashboard", __name__, url_prefix="/dashboard")

@controller.route("/", methods=["GET"])
def show_dashboard():
	return render_template("dashboard.html")

@controller.route("/balance", methods=["GET"])
def show_balance():
	return render_template("balance.html")

@controller.route("/buy", methods=["GET"])
def show_buy():
	return render_template("buy.html")

@controller.route("/sell", methods=["GET"])
def show_sell():
	return render_template("sell.html")

@controller.route("/lookup", methods=["GET"])
def show_lookup():
	return render_template("lookup.html")

@controller.route("/quote", methods=["GET"])
def show_quote():
	return render_template("quote.html")

@controller.route("/portfolio", methods=["GET"])
def show_portfolio():
	return render_template("portfolio.html")

@controller.route("/<text>", methods=["GET"])
def show_dash(text):
	return render_template("dashboard.html")