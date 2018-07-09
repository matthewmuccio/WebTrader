#!/usr/bin/env python3


from flask import abort, Blueprint, redirect, render_template, request, session, url_for

from core.models import model


controller = Blueprint("dashboard", __name__, url_prefix="/dashboard")

@controller.route("/", methods=["GET"])
def show_dashboard():
	# In session (user signed in)
	if "username" in session:
		# User
		if session["username"] != "admin":
			# Accesses last 10 stock purchases and sales from the database.
			buy_portfolio = model.get_orders_dataframe(session["username"], "buy", 10)
			sell_portfolio = model.get_orders_dataframe(session["username"], "sell", 10)
			return render_template("dashboard.html", \
									title="Home", \
									username=session["username"], \
									buy_portfolio=buy_portfolio, \
									sell_portfolio=sell_portfolio)
		# Admin
		else:
			return redirect(url_for("admin.show_dashboard"))
	# Out of session (user not signed in)
	else:
		return redirect(url_for("signup.show_signup"))

@controller.route("/balance", methods=["GET"])
def show_balance():
	# In session (user signed in)
	if "username" in session:
		# User
		if session["username"] != "admin":
			return render_template("balance.html", \
										title="Balance", \
										username=session["username"], \
										balance=format(model.get_balance(session["username"]), ".2f"))
		# Admin
		else:
			return redirect(url_for("admin.show_dashboard"))
	# Out of session (user not signed in)
	else:
		return redirect(url_for("signup.show_signup"))

@controller.route("/buy", methods=["GET", "POST"])
def show_buy():
	# In session (user signed in)
	if "username" in session:
		# User
		if session["username"] != "admin":
			# GET request
			if request.method == "GET":
				return render_template("buy.html", \
										title="Buy", \
										username=session["username"])
			# POST request
			else:
				# Accesses current form data (data transmitted in a POST request).
				ticker_symbol = request.form["ticker-symbol"]
				trade_volume = request.form["trade-volume"]
				# Attempts to purchase stock and stores the response.
				response = model.buy(ticker_symbol, trade_volume, session["username"])
				return render_template("buy.html", \
										title="Buy", \
										username=session["username"], \
										response=response)
		# Admin
		else:
			return redirect(url_for("admin.show_dashboard"))
	# Out of session (user not signed in)
	else:
		return redirect(url_for("signup.show_signup"))

@controller.route("/sell", methods=["GET", "POST"])
def show_sell():
	# In session (user signed in)
	if "username" in session:
		# User
		if session["username"] != "admin":
			# GET request
			if request.method == "GET":
				return render_template("sell.html", \
										title="Sell", \
										username=session["username"])
			# POST request
			else:
				# Accesses current form data (data transmitted in a POST request).
				ticker_symbol = request.form["ticker-symbol"]
				trade_volume = request.form["trade-volume"]
				# Attempts to sell stock and stores the response.
				response = model.sell(ticker_symbol, trade_volume, session["username"])
				return render_template("sell.html", \
										title="Sell", \
										username=session["username"], \
										response=response)
		# Admin
		else:
			return redirect(url_for("admin.show_dashboard"))
	# Out of session (user not signed in)
	else:
		return redirect(url_for("signup.show_signup"))

@controller.route("/lookup", methods=["GET", "POST"])
def show_lookup():
	# In session (user signed in)
	if "username" in session:
		# User
		if session["username"] != "admin":
			# GET request
			if request.method == "GET":
				return render_template("lookup.html", \
										title="Lookup", \
										username=session["username"])
			# POST request
			else:
				# Accesses current form data (data transmitted in a POST request).
				company_name = request.form["company-name"]
				# Attempts to lookup a ticker symbol for a given company name and stores the response.
				response = model.lookup(company_name)
				return render_template("lookup.html", \
										title="Lookup", \
										username=session["username"], \
										response=response)
		# Admin
		else:
			return redirect(url_for("admin.show_dashboard"))
	# Out of session (user not signed in)
	else:
		return redirect(url_for("signup.show_signup"))

@controller.route("/quote", methods=["GET", "POST"])
def show_quote():
	# In session (user signed in)
	if "username" in session:
		# User
		if session["username"] != "admin":
			# GET request
			if request.method == "GET":
				return render_template("quote.html", \
										title="Quote", \
										username=session["username"])
			# POST request
			else:
				# Accesses current form data (data transmitted in a POST request).
				ticker_symbol = request.form["ticker-symbol"]
				# Attempts to lookup a ticker symbol for a given company name and stores the response.
				response = model.quote(ticker_symbol)
				return render_template("quote.html", \
										title="Quote", \
										username=session["username"], \
										response=response)
		# Admin
		else:
			return redirect(url_for("admin.show_dashboard"))
	# Out of session (user not signed in)
	else:
		return redirect(url_for("signup.show_signup"))

@controller.route("/portfolio", methods=["GET"])
def show_portfolio():
	# In session (user signed in)
	if "username" in session:
		# User
		if session["username"] != "admin":
			balance = model.get_balance(session["username"])
			earnings = model.get_earnings(session["username"])
			total = float(balance) + float(earnings)
			portfolio = model.get_holdings_dataframe(session["username"])
			return render_template("portfolio.html", \
									title="Portfolio", \
									username=session["username"], \
									balance=format(balance, ".2f"), \
									earnings=format(earnings, ".2f"), \
									total=format(total, ".2f"), \
									portfolio=portfolio)
		# Admin
		else:
			return redirect(url_for("admin.show_dashboard"))
	# Out of session (user not signed in)
	else:
		return redirect(url_for("signup.show_signup"))

@controller.route("/signout", methods=["GET"])
def signout():
	# In session (user signed in)
	if "username" in session:
		session.pop("username", None)
		return redirect(url_for("login.show_login"))
	# Out of session (user not signed in)
	else:
		return redirect(url_for("signup.show_signup"))