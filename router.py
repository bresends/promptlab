from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from routes.index import index, set_data, get_data, clear_data, show_users, create_user
from routes.auth import login


def register_routes(app: Flask, db: SQLAlchemy):
    app.add_url_rule("/", view_func=index)
    app.add_url_rule("/set_data", view_func=set_data)
    app.add_url_rule("/get_data", view_func=get_data)
    app.add_url_rule("/clear_data", view_func=clear_data)
    app.add_url_rule("/users", view_func=show_users)
    app.add_url_rule("/users/new", view_func=create_user, methods=["GET", "POST"])
    app.add_url_rule("/login", view_func=login, methods=["GET", "POST"])
