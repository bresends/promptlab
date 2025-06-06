from flask import render_template, session, request, redirect, url_for, flash
from models.user import User
from app import db


def index():
    """Main index page"""
    return render_template("index.j2", message="Hello, World!")


def set_data():
    """Set data in session"""
    session["name"] = "Mike"
    return render_template("index.j2", message="Data has been set in the session!")


def get_data():
    """Get data from session"""
    name = session.get("name", "No data found in session")
    return render_template("index.j2", message=f"Session data: {name}")


def clear_data():
    """Clear data from session"""
    session.pop("name", None)
    return render_template("index.j2", message="Session data has been cleared!")


def show_users():
    """Display all users from the database"""
    try:
        users = User.query.all()
        return render_template("users.j2", users=users)
    except Exception as e:
        flash(f"Error retrieving users: {str(e)}")
        return redirect(url_for("index"))


def create_user():
    """Create a new user"""
    if request.method == "POST":
        try:
            username = request.form.get("username")
            email = request.form.get("email")
            password = request.form.get("password")

            if not username or not email or not password:
                flash("All fields are required!")
                return redirect(url_for("index"))

            new_user = User()
            new_user.username = username
            new_user.email = email
            new_user.password = password

            db.session.add(new_user)
            db.session.commit()
            flash(f"User {username} created successfully!")
            return redirect(url_for("index"))

        except Exception as e:
            db.session.rollback()
            flash(f"Error creating user: {str(e)}")
            return redirect(url_for("index"))

    # For GET requests, show the create user form
    return render_template("create_user.j2")
