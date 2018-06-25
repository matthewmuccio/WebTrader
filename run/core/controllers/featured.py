#!/usr/bin/env python3


from flask import Blueprint, render_template


controller = Blueprint("featured", __name__, url_prefix="/featured")

@controller.route("/", methods=["GET"])
def show_featured():
	return render_template("featured.html")
