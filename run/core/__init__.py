#!/usr/bin/env python3


import os

from flask import Flask

from core.controllers.featured import controller as featured
from core.controllers.general import controller as general


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

omnibus = Flask(__name__)

omnibus.register_blueprint(featured)
omnibus.register_blueprint(general)

# TODO: Write the following function.
keymaker(omnibus)
