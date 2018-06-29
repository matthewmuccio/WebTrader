#!/usr/bin/env python3


from flask import Blueprint, render_template


controller = Blueprint("dashboard", __name__, url_prefix="/dashboard")

@controller.route("/", methods=["GET"])
def show_featured():
	return render_template("dashboard.html")

@controller.route("/<username>", methods=["GET", "POST"])
def show_dashboard(username):
	return render_template("dashboard.html")