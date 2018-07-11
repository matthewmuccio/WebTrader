#!/usr/bin/env python3


import sqlite3


connection = sqlite3.connect("master.db", check_same_thread=False)
cursor = connection.cursor()

# Create users table
cursor.execute(
	"""CREATE TABLE users(
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		username VARCHAR(16) UNIQUE NOT NULL,
		password VARCHAR(128) NOT NULL,
		balance FLOAT NOT NULL,
		account_created DATETIME NOT NULL,
		last_login DATETIME NOT NULL
	);"""
)

# Create portfolio/holdings table
cursor.execute(
	"""CREATE TABLE holdings(
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		ticker_symbol VARCHAR(5) NOT NULL,
		number_of_shares INTEGER NOT NULL,
		volume_weighted_average_price FLOAT NOT NULL,
		username VARCHAR(16) NOT NULL,
		FOREIGN KEY(username) REFERENCES users(username)
	);"""
)

# Create orders/transactions table
cursor.execute(
	"""CREATE TABLE orders(
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		unix_time FLOAT NOT NULL
		transaction_type VARCHAR(4) NOT NULL,
		ticker_symbol VARCHAR(5) NOT NULL,
		trade_volume INTEGER NOT NULL,
		last_price FLOAT NOT NULL,
		username VARCHAR(16) NOT NULL,
		FOREIGN KEY(username) REFERENCES users(username)
	);"""
)

cursor.close()
connection.close()