#!/usr/bin/env python3


import datetime
import sqlite3


connection = sqlite3.connect("master.db", check_same_thread=False)
cursor = connection.cursor()

username = "admin"
password = "836bc6397d06de5f635683cff01822564683b57c5298c38bd389628685d9ce9d74cba952fc80ac305a6dd1d122bb041dfa93377880d478f27b99da3fafc05bf6"
balance = 0.0
first_login = datetime.datetime.now()
last_login = datetime.datetime.now()

cursor.execute(
	"""INSERT INTO users(
		username,
		password,
		balance,
		first_login,
		last_login
	) VALUES(?,?,?,?,?);""", (username, password, balance, first_login, last_login,)
)

connection.commit()
cursor.close()
connection.close()