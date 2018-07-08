#!/usr/bin/env python3


import os

from flask import Flask, render_template

from core.controllers.signup import controller as signup
from core.controllers.login import controller as login
from core.controllers.admin import controller as admin
from core.controllers.dashboard import controller as dashboard
from core.controllers.search import controller as search


def keymaker(omnibus, filename="secret_key"):
	pathname = os.path.join(omnibus.instance_path, filename)
	try:
		print("Trying to find a directory labelled \"instance.\"")
		print("Trying to find a file labelled \"secret_key.\"")
		omnibus.config["SECRET_KEY"] = open(pathname, "rb").read()
		print("Found a directory labelled \"instance.\"")
		print("Found a file labelled \"secret_key.\"")
	except IOError:
		parent_directory = os.path.dirname(pathname)
		if not os.path.isdir(parent_directory):
			print("Cannot find a directory called labelled \"instance.\"")
			print("Making a directory labelled \"instance.\"")
			os.system("mkdir -p {0}".format(parent_directory))
		print("Writing to a file labelled \"secret_key.\"")
		os.system("head -c 24 /dev/urandom > {0}".format(pathname))
		omnibus.config["SECRET_KEY"] = open(pathname, "rb").read()

# Creates a new app.
omnibus = Flask(__name__)

# Registers blueprints of the controllers for the app.
omnibus.register_blueprint(signup)
omnibus.register_blueprint(login)
omnibus.register_blueprint(admin)
omnibus.register_blueprint(dashboard)
omnibus.register_blueprint(search)

# Enables debug mode.
omnibus.config["DEBUG"] = True

# Creates a private key for the user.
keymaker(omnibus)
