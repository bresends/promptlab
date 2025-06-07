from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from routes.index import list_prompts, show_users, create_user, render_prompt
from routes.auth import login


def register_routes(app: Flask, db: SQLAlchemy):
    app.add_url_rule("/", endpoint="list_prompts", view_func=list_prompts)

    app.add_url_rule(
        "/<template_name>/",
        endpoint="render_prompt",
        view_func=render_prompt,
        methods=["GET", "POST"]
    )
    app.add_url_rule("/users", endpoint="users", view_func=show_users)
    app.add_url_rule(
        "/users/new",
        endpoint="create_user",
        view_func=create_user,
        methods=["GET", "POST"],
    )
    app.add_url_rule(
        "/login", endpoint="login", view_func=login, methods=["GET", "POST"]
    )
