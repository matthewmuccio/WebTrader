#!/usr/bin/env python3


from operator import itemgetter
from math import isclose

from core.models import mapper
from core.models import wrapper


### User
# Buy
def buy(ticker_symbol, trade_volume, username):
	last_price = wrapper.get_last_price(ticker_symbol)
	# Error handling: if the user enters a ticker symbol that does not exist.
	if last_price == "exit":
		return ["Sorry, the ticker symbol you entered does not exist."]
	balance = mapper.get_balance(username)
	brokerage_fee = 6.95
	# Error handling: if the user enters a trade volume that is not a number.
	try:
		transaction_cost = last_price * float(trade_volume) + brokerage_fee
	except ValueError:
		return ["Sorry, the trade volume you entered is invalid."]
	# Error handling: if the user enters a trade volume that is negative or 0.
	if float(trade_volume) <= 0:
		return ["Sorry, the trade volume you entered is invalid."]
	# If the user has enough money in their account to execute the trade.
	if transaction_cost < balance:
		ticker_symbols = mapper.get_ticker_symbols(ticker_symbol, username)
		# If the user does not hold any stock from company with ticker_symbol.
		if len(ticker_symbols) == 0:
			new_balance = balance - transaction_cost
			# Updates the user's balance in the users database table.
			mapper.update_balance(new_balance, username)
			# Inserts a new row to the holdings database table after buying the stock.
			mapper.insert_holdings_row(ticker_symbol, trade_volume, last_price, username)
			# Inserts a new row to the orders database table after buying the stock.
			mapper.insert_orders_row("buy", ticker_symbol, trade_volume, last_price, username)
			# Returns the success message depending on how much stock the user bought (one or multiple).
			if isclose(float(trade_volume), 1):
				return ["Success! The trade was executed.", "You bought {0} share of {1} stock.".format(trade_volume, ticker_symbol.upper())]
			else:
				return ["Success! The trade was executed.", "You bought {0} shares of {1} stock.".format(trade_volume, ticker_symbol.upper())]
		# If the user holds some stock from company with ticker_symbol.
		else:
			# Gets the number of shares from holdings database table for the company with ticker_symbol.
			curr_number_of_shares = mapper.get_number_of_shares(ticker_symbol, username)
			new_number_of_shares = curr_number_of_shares + float(trade_volume)
			# Gets the last price stored in the holdings database table for a given ticker_symbol.
			curr_price = mapper.get_last_price(ticker_symbol, username)
			# Calculates the new VWAP based on the current values in the database table and the most recent (last) prices.
			new_vwap = calculate_vwap(curr_price, curr_number_of_shares, last_price, trade_volume)
			# Updates the VWAP in the holdings database table with a new value.
			mapper.update_volume_weighted_average_price(new_vwap, ticker_symbol, username)
			# Updates the holdings database table with the new number of shares after buying stock.
			mapper.update_number_of_shares(new_number_of_shares, ticker_symbol, username)
			# Inserts a new row to the orders database table after buying the stock.
			mapper.insert_orders_row("buy", ticker_symbol, trade_volume, last_price, username)
			# Returns the success message depending on how much stock the user bought (one or multiple).
			if isclose(float(trade_volume), 1):
				return ["Success! The trade was executed.", "You bought {0} share of {1} stock.".format(trade_volume, ticker_symbol.upper())]
			else:
				return ["Success! The trade was executed.", "You bought {0} shares of {1} stock.".format(trade_volume, ticker_symbol.upper())]
	else:
		# Returns error response.
		return ["Sorry, you do not have the balance necessary to execute that trade."]

# Sell
def sell(ticker_symbol, trade_volume, username):
	last_price = wrapper.get_last_price(ticker_symbol)
	# Error handling: if the user enters a ticker symbol that does not exist.
	if last_price == "exit":
		return ["Sorry, the ticker symbol you entered does not exist."]
	brokerage_fee = 6.95
	# Error handling: if the user enters a trade volume that is not a number.
	try:
		balance_to_add = last_price * float(trade_volume) - brokerage_fee
	except ValueError:
		return ["Sorry, the trade volume you entered is invalid."]
	# Error handling: if the user enters a trade volume that is negative or 0.
	if float(trade_volume) <= 0:
		return ["Sorry, the trade volume you entered is invalid."]
	# Checks if the user holds any stock from the company with ticker_symbol.
	ticker_symbols = mapper.get_ticker_symbols(ticker_symbol, username)
	if len(ticker_symbols) == 0:
		return ["Sorry, you do not hold any shares from that company."]
	# Gets needed values from the user and holdings database tables.
	balance = mapper.get_balance(username)
	number_of_shares = mapper.get_number_of_shares(ticker_symbol, username)
	new_number_of_shares = number_of_shares - float(trade_volume)
	# If the user holds enough shares to complete their trade.
	if float(trade_volume) <= number_of_shares:
		# Gets the last price stored in the holdings database table for a given ticker_symbol.
		curr_price = mapper.get_last_price(ticker_symbol, username)
		# Gets the number of shares from holdings database table for the company with ticker_symbol.
		curr_number_of_shares = mapper.get_number_of_shares(ticker_symbol, username)
		# Calculates the new VWAP based on old values in the database table.
		new_vwap = calculate_vwap(curr_price, curr_number_of_shares, last_price, trade_volume)
		# Updates the VWAP in the holdings database table with a new value.
		mapper.update_volume_weighted_average_price(new_vwap, ticker_symbol, username)
		# Updates users database table with the new balance after selling the stock.
		new_balance = balance + balance_to_add
		mapper.update_balance(new_balance, username)
		# If the new number of shares would be 0 after the user sells their shares.
		if new_number_of_shares == 0:
			# Deletes the row from holdings database table for company with ticker_symbol.
			mapper.delete_holdings_row(ticker_symbol)
		else:
			# Updates holdings database table with the new number of shares.
			mapper.update_number_of_shares(new_number_of_shares, ticker_symbol, username)
		# Inserts a new row to the orders database table after selling the stock.
		mapper.insert_orders_row("sell", ticker_symbol, trade_volume, last_price, username)
		# Returns the success message depending on how much stock the user bought (one or multiple).
		if isclose(float(trade_volume), 1):
			return ["Success! The trade was executed.", "You sold {0} share of {1} stock.".format(trade_volume, ticker_symbol.upper())]
		else:
			return ["Success! The trade was executed.", "You sold {0} shares of {1} stock.".format(trade_volume, ticker_symbol.upper())]
	else:
		# Returns error response.
		return ["Sorry, you do not have the shares necessary to execute that trade."]
	
# Lookup
def lookup(company_name):
	response = wrapper.get_ticker_symbol(company_name)
	if response == "exit":
		return ["Sorry, the company name you entered does not have a ticker symbol."]
	else:
		return ["Company name: {0}".format(company_name.lower().capitalize()), "Ticker symbol: {0}".format(response)]

# Quote
def quote(ticker_symbol):
	response = wrapper.get_last_price(ticker_symbol)
	if response == "exit":
		return ["Sorry, the ticker symbol you entered does not exist."]
	else:
		return ["Ticker symbol: {0}".format(ticker_symbol.upper()), "Current stock price: {0} USD".format(response)]

# Calculates the new volume weighted average to update the holdings database table.
def calculate_vwap(curr_price, curr_num_shares, new_price, new_num_shares):
	old = float(curr_price) * float(curr_num_shares)
	new = float(new_price) * float(new_num_shares)
	total_volume = float(curr_num_shares) + float(new_num_shares)
	return (old + new) / total_volume

### Admin
# Calculates new deposit, and handles errors.
def calculate_new_deposit(balance, balance_to_add):
	errors = ["Sorry, the amount you entered is invalid."]
	try:
		# If the balance to add is over 1,000,000,000,000,000,000 (10^15 or one quadrillion), add error message to list, and throw an error.
		if float(balance_to_add) > 10 ** 15:
			errors.append("You cannot deposit more than a quadrillion (10^15) dollars into a user's account balance.")
			raise ValueError
		# If the balance to add is negative or 0, add error message to list, and throw an error.
		if float(balance_to_add) <= 0:
			errors.append("You cannot deposit a non-positive value ($0 or less) into a user's account balance.")
			raise ValueError
		# Otherwise return the sum of the old balance and the balance to add.
		return balance + float(balance_to_add)
	except (ValueError, TypeError):
		return errors

# Calculates new withdraw, and handles errors.
def calculate_new_withdraw(balance, balance_to_subtract):
	errors = ["Sorry, the amount you entered is invalid."]
	try:
		# If the balance to subtract would result in a negative balance, add error message to list, and throw an error.
		if float(balance_to_subtract) > balance:
			errors.append("You cannot withdraw more than the user's account balance.")
			raise ValueError
		# If the balance to subtract is negative or 0, add error message to list, and throw an error.
		if float(balance_to_subtract) <= 0:
			errors.append("You cannot withdraw a non-positive value ($0 or less) from a user's account balance.")
			raise ValueError
		# Otherwise return the difference of the old balance and the balance to subtract.
		return balance - float(balance_to_subtract)
	except (ValueError, TypeError):
		return errors

# Calculates the new balance to set, and handles errors.
def calculate_new_set(balance, balance_to_set):
	try:
		# If the new balance is negative, throw an error.
		if float(balance_to_set) < 0:
			raise ValueError
		# Otherwise return the balance to set as a float.
		return float(balance_to_set)
	except (ValueError, TypeError):
		return ["Sorry, the balance you entered is invalid."]

# Gets the portfolio earnings for a given username.
def get_earnings(username):
	user_ticker_symbols = mapper.get_ticker_symbols_from_user(username)
	earnings = 0.0
	for t in user_ticker_symbols:
		last_price = wrapper.get_last_price(t) # Current market price
		user_num_shares = mapper.get_number_of_shares(t, username)
		if last_price == "exit":
			earnings += 0.0
		else:
			earnings += float(last_price) * user_num_shares
	return earnings

# Gets a sorted dictionary representing the leaderboard where the key is the username and the value is their earnings.
def get_leaderboard():
	leaderboard = {}
	users = get_users()
	for user in users:
		earnings = get_earnings(user)
		leaderboard[user] = earnings
	sorted_leaderboard = sorted(leaderboard.items(), key=itemgetter(1), reverse=True)
	return sorted_leaderboard

### Wrapper
def get_ticker_symbol(company_name):
	return wrapper.get_ticker_symbol(company_name)

def get_last_price(ticker_symbol):
	return wrapper.get_last_price(ticker_symbol)

### Mapper
def create_account(username, password):
	return mapper.create_account(username, password)

def login(username, password):
	return mapper.login(username, password)

def get_balance(username):
	return mapper.get_balance(username)

def get_holdings_dataframe(username):
	return mapper.get_holdings_dataframe(username)

def get_orders_dataframe(username, num, transaction_type):
	return mapper.get_orders_dataframe(username, num, transaction_type)

def update_balance(new_balance, username):
	return mapper.update_balance(new_balance, username)

### Admin
def get_users():
	return mapper.get_users()