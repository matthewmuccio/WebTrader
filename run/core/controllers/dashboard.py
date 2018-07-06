#!/usr/bin/env python3


from flask import abort, Blueprint, redirect, render_template, request, session, url_for

from core.models import model


controller = Blueprint("dashboard", __name__, url_prefix="/dashboard")

@controller.route("/", methods=["GET"])
def show_dashboard():
	if "username" in session:
		portfolio = model.get_orders_dataframe(session["username"], 15)
		return render_template("dashboard.html", \
								title="Home", \
								username=session["username"],
								portfolio=portfolio)
	else:
		return redirect(url_for("signup.show_signup"))

@controller.route("/balance", methods=["GET"])
def show_balance():
	if "username" in session:
		return render_template("balance.html", \
								title="Balance", \
								username=session["username"], \
								balance=format(model.get_balance(session["username"]), ".2f"))
	else:
		return redirect(url_for("signup.show_signup"))

@controller.route("/buy", methods=["GET", "POST"])
def show_buy():
	if "username" in session:
		if request.method == "GET":
			return render_template("buy.html", \
									title="Buy", \
									username=session["username"])
		else:
			ticker_symbol = request.form["ticker-symbol"]
			trade_volume = request.form["trade-volume"]
			# Attempts to purchase stock and stores the response.
			response = model.buy(ticker_symbol, trade_volume, session["username"])
			return render_template("buy.html", \
									title="Buy", \
									username=session["username"], \
									response=response)
	else:
		return redirect(url_for("signup.show_signup"))

@controller.route("/sell", methods=["GET", "POST"])
def show_sell():
	if "username" in session:
		if request.method == "GET":
			return render_template("sell.html", \
									title="Sell", \
									username=session["username"])
		else:
			ticker_symbol = request.form["ticker-symbol"]
			trade_volume = request.form["trade-volume"]
			# Attempts to sell stock and stores the response.
			response = model.sell(ticker_symbol, trade_volume, session["username"])
			return render_template("sell.html", \
									title="Sell", \
									username=session["username"], \
									response=response)
	else:
		return redirect(url_for("signup.show_signup"))

@controller.route("/lookup", methods=["GET", "POST"])
def show_lookup():
	if "username" in session:
		if request.method == "GET":
			return render_template("lookup.html", \
									title="Lookup", \
									username=session["username"])
		else:
			company_name = request.form["company-name"]
			# Attempts to lookup a ticker symbol for a given company name and stores the response.
			response = model.lookup(company_name)
			return render_template("lookup.html", \
									title="Lookup", \
									username=session["username"], \
									response=response)
	else:
		return redirect(url_for("signup.show_signup"))

@controller.route("/quote", methods=["GET", "POST"])
def show_quote():
	if "username" in session:
		if request.method == "GET":
			return render_template("quote.html", \
									title="Quote", \
									username=session["username"])
		else:
			ticker_symbol = request.form["ticker-symbol"]
			# Attempts to lookup a ticker symbol for a given company name and stores the response.
			response = model.quote(ticker_symbol)
			return render_template("quote.html", \
									title="Quote", \
									username=session["username"], \
									response=response)
	else:
		return redirect(url_for("signup.show_signup"))

@controller.route("/portfolio", methods=["GET"])
def show_portfolio():
	if "username" in session:
		portfolio = model.get_holdings_dataframe(session["username"])
		return render_template("portfolio.html", \
								title="Portfolio", \
								username=session["username"], \
								balance=format(model.get_balance(session["username"]), ".2f"), \
								earnings=format(model.get_earnings(session["username"]), ".2f"), \
								portfolio=portfolio)
	else:
		return redirect(url_for("signup.show_signup"))

@controller.route("/signout", methods=["GET"])
def signout():
	if "username" in session:
		session.pop("username", None)
		return redirect(url_for("login.show_login"))
	else:
		return redirect(url_for("signup.show_signup"))