#!/usr/bin/env python3


import datetime
import hashlib
import re
import sqlite3
import time

import pandas as pd


# Encrypt a plaintext string (password) with SHA-512 cryptographic hash function.
def encrypt_password(password):
	return hashlib.sha512(str.encode(password)).hexdigest()

# Creates an account in users database table.
def create_account(username, password):
	if account_exists(username, password):
		return ["Sorry, an account with that username and password already exists.", "Log in with those credentials to access your account."]
	elif username_exists(username):
		return ["Sorry, the username you entered is already taken."]
	elif not valid_username(username):
		return ["Sorry, the username you entered is invalid.", "Usernames must contain between 3 and 20 characters.", "They can only contain lowercase letters, numbers, and underscores."]
	elif not valid_password(password):
		return ["Sorry, the password you entered is invalid.", "Passwords must contain between 8 and 50 characters."]
	password = encrypt_password(password)
	default_balance = 100000.00
	first_login = datetime.datetime.now()
	last_login = first_login
	connection = sqlite3.connect("master.db", check_same_thread=False)
	cursor = connection.cursor()
	cursor.execute(
		"""INSERT INTO users(
			username,
			password,
			balance,
			first_login,
			last_login
			) VALUES(?,?,?,?,?);
		""", (username, password, default_balance, first_login, last_login,)
	)
	connection.commit()
	cursor.close()
	connection.close()
	return ["Success", "User"]

# Logs in to account in users database table.
def login(username, password):
	if not username_exists(username):
		return ["Sorry, no account exists with that username.", "Please sign up for a Web Trader account to log in."]
	elif not account_exists(username, password):
		return ["Sorry, the password you entered was incorrect."]
	elif is_admin(username, password):
		return ["Success", "Admin"]
	password = encrypt_password(password)
	connection = sqlite3.connect("master.db", check_same_thread=False)
	cursor = connection.cursor()
	cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password,))
	result = len(cursor.fetchall()) == 1
	cursor.close()
	connection.close()
	if result:
		return ["Success", "User"]

### SELECT (GET)

# Checks if a username exists in a row in the users database table.
def username_exists(username):
	connection = sqlite3.connect("master.db", check_same_thread=False)
	cursor = connection.cursor()
	cursor.execute("SELECT * FROM users WHERE username=?", (username,))
	result = len(cursor.fetchall()) == 1
	cursor.close()
	connection.close()
	return result

# Checks if an account (username and password) exists in a row in the users database table.
def account_exists(username, password):
	password = encrypt_password(password)
	connection = sqlite3.connect("master.db", check_same_thread=False)
	cursor = connection.cursor()
	cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password,))
	result = len(cursor.fetchall()) == 1
	cursor.close()
	connection.close()
	return result

# Checks if an account (username and password) is the admin account.
def is_admin(username, password):
	return username == "admin" and account_exists(username, password)

# Checks if a username is valid.
def valid_username(username):
	return re.search(r"\A[a-z0-9_]{3,20}\Z", username)
 
# Checks if a password is valid.
def valid_password(password):
	regex = r"\A[A-Za-z0-9\"\^\-\]\\~`!@#$%&*()_+=|{}[:;'<>,.?/]{8,50}\Z"
	return re.search(regex, password)

# Gets the balance value from the row in the users database table for the given username.
def get_balance(username):
	connection = sqlite3.connect("master.db", check_same_thread=False)
	cursor = connection.cursor()
	cursor.execute("SELECT balance FROM users WHERE username=?", (username,))
	# Error handling for an unknown username.
	try:
		balance = cursor.fetchall()[0][0]
	except IndexError:
		balance = ["Sorry, no account exists with that username."]
	cursor.close()
	connection.close()
	return balance

# Gets the ticker symbols of the holdings of the user with the given username.
def get_ticker_symbols(ticker_symbol, username):
	connection = sqlite3.connect("master.db", check_same_thread=False)
	cursor = connection.cursor()
	cursor.execute("SELECT ticker_symbol FROM holdings WHERE ticker_symbol=? AND username=?", (ticker_symbol.upper(), username,))
	ticker_symbols = cursor.fetchall()
	cursor.close()
	connection.close()
	return ticker_symbols

# Gets the number of shares for the given username from holdings database table.
def get_number_of_shares(ticker_symbol, username):
	connection = sqlite3.connect("master.db", check_same_thread=False)
	cursor = connection.cursor()
	cursor.execute("SELECT number_of_shares FROM holdings WHERE ticker_symbol=? AND username=?", (ticker_symbol.upper(), username,))
	number_of_shares = cursor.fetchall()[0][0]
	cursor.close()
	connection.close()
	return number_of_shares

# Gets the last price stored in the holdings database table for a given ticker_symbol.
def get_last_price(ticker_symbol, username):
	connection = sqlite3.connect("master.db", check_same_thread=False)
	cursor = connection.cursor()
	cursor.execute("SELECT volume_weighted_average_price FROM holdings WHERE ticker_symbol=? AND username=?", (ticker_symbol.upper(), username,))
	last_price = cursor.fetchall()[0][0]
	cursor.close()
	connection.close()
	return last_price

# Gets a list of all Terminal Traders users in the users database table.
def get_users():
	connection = sqlite3.connect("master.db", check_same_thread=False)
	cursor = connection.cursor()
	cursor.execute("SELECT username FROM users WHERE username NOT LIKE 'admin'")
	users = cursor.fetchall() # List of tuples
	users_list = [str(user[0]) for user in users] # List of strings
	cursor.close()
	connection.close()
	return users_list

# Gets all the ticker symbols in a given user's portfolio.
def get_ticker_symbols_from_user(username):
	connection = sqlite3.connect("master.db", check_same_thread=False)
	cursor = connection.cursor()
	cursor.execute("SELECT ticker_symbol FROM holdings WHERE username=?", (username,))
	ticker_symbols = cursor.fetchall() # List of tuples
	ticker_symbols_list = [str(t[0]) for t in ticker_symbols]
	cursor.close()
	connection.close()
	return ticker_symbols_list

# Creates a new pandas DataFrame that contains the rows in holdings database table for the given user.
def get_holdings_dataframe(username):
	connection = sqlite3.connect("master.db", check_same_thread=False)
	df1 = pd.read_sql_query("SELECT * FROM holdings WHERE username=?", connection, params=[username])
	if df1.empty:
		return "empty"
	df2 = df1[df1.columns.difference(["id", "username"])]
	df3 = df2.to_html().replace('<tr>', '<tr style="text-align: center;">')
	return df3

# Creates a new pandas DataFrame that contains the last 10 trades (in the orders database table) for the given user.
def get_orders_dataframe(username, transaction_type, num):
	connection = sqlite3.connect("master.db", check_same_thread=False)
	df1 = pd.read_sql_query("SELECT * FROM orders WHERE username=? AND transaction_type=? ORDER BY transaction_time DESC LIMIT ?", connection, params=[username, transaction_type, num])
	if df1.empty:
		return "empty"
	df2 = df1[df1.columns.difference(["id", "username"])]
	df3 = df2.to_html().replace('<tr>', '<tr style="text-align: center;">')
	if transaction_type == "buy":
		df4 = df3.replace('<table border="1" class="dataframe">', '<h4>Stock Purchases</h4> <table border="1" class="dataframe" style="display: inline-block;">')
	else:
		df4 = df3.replace('<table border="1" class="dataframe">', '<h4>Stock Sales</h4> <table border="1" class="dataframe" style="display: inline-block;">')
	return df4

### UPDATE / INSERT

# Updates the user's balance in the users database table.
def update_balance(new_balance, username):
	if new_balance != "exit":
		connection = sqlite3.connect("master.db", check_same_thread=False)
		cursor = connection.cursor()
		cursor.execute("UPDATE users SET balance=? WHERE username=?", (new_balance, username,))
		connection.commit()
		cursor.close()
		connection.close()

# Updates the number of shares in the holdings database table with a new number of shares.
def update_number_of_shares(new_number_of_shares, ticker_symbol, username):
	connection = sqlite3.connect("master.db", check_same_thread=False)
	cursor = connection.cursor()
	cursor.execute("UPDATE holdings SET number_of_shares=? WHERE ticker_symbol=? AND username=?", (new_number_of_shares, ticker_symbol.upper(), username,))
	connection.commit()
	cursor.close()
	connection.close()

# Updates the volume weighted average price in the holdings database table with a new value.
def update_volume_weighted_average_price(new_vwap, ticker_symbol, username):
	connection = sqlite3.connect("master.db", check_same_thread=False)
	cursor = connection.cursor()
	cursor.execute("UPDATE holdings SET volume_weighted_average_price=? WHERE ticker_symbol=? AND username=?", (new_vwap, ticker_symbol.upper(), username,))
	connection.commit()
	cursor.close()
	connection.close()

# Inserts a new row in the holdings database table.
def insert_holdings_row(ticker_symbol, trade_volume, price, username):
	connection = sqlite3.connect("master.db", check_same_thread=False)
	cursor = connection.cursor()
	cursor.execute("""INSERT INTO holdings(
				ticker_symbol,
				number_of_shares,
				volume_weighted_average_price,
				username
			) VALUES(?,?,?,?);""", (ticker_symbol.upper(), trade_volume, price, username,)
	)
	connection.commit()
	cursor.close()
	connection.close()

# Inserts a new row in the orders database table.
def insert_orders_row(transaction_type, ticker_symbol, trade_volume, price, username):
	connection = sqlite3.connect("master.db", check_same_thread=False)
	cursor = connection.cursor()
	unix_time = round(time.time(), 2)
	cursor.execute("""INSERT INTO orders(
				unix_time,
				transaction_type,
				ticker_symbol,
				trade_volume,
				last_price,
				username
			) VALUES(?,?,?,?,?,?);""", (unix_time, transaction_type, ticker_symbol.upper(), trade_volume, price, username,)
	)
	connection.commit()
	cursor.close()
	connection.close()

### DELETE

# Deletes the row from holdings database table that contains a given ticker symbol.
def delete_holdings_row(ticker_symbol):
	connection = sqlite3.connect("master.db", check_same_thread=False)
	cursor = connection.cursor()
	cursor.execute("DELETE FROM holdings WHERE ticker_symbol=?", (ticker_symbol.upper(),))
	connection.commit()
	cursor.close()
	connection.close()