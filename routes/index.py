from flask import render_template, session
from models.user import User

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
        if users:
            user_list = [f"ID: {user.id}, Username: {user.username}, Email: {user.email}" for user in users]
            message = "Users in database:<br>" + "<br>".join(user_list)
        else:
            message = "No users found in the database."
    except Exception as e:
        message = f"Error retrieving users: {str(e)}"
    
    return render_template("index.j2", message=message)


