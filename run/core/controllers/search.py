#!/usr/bin/env python3


from flask import Blueprint, render_template, request, redirect


controller = Blueprint("search", __name__, url_prefix="/search")

@controller.route("/", methods=["GET", "POST"])
def show_login():
    if request.method == "POST":
        return render_template("search.html")