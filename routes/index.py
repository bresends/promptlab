from pathlib import Path

from flask import flash, redirect, render_template, request, url_for

from app import db
from models.user import User
from prompts.prompt_manager import PromptManager


def list_prompts():
    """List all available prompt templates"""
    try:
        prompts_dir = Path(__file__).parent.parent / "prompts" / "blueprints"

        if not prompts_dir.exists():
            flash("Templates directory not found", "warning")
            return render_template("index.j2", templates=[])

        # Get all template files
        template_files = [f.stem for f in prompts_dir.glob("*.jinja2")]

        # Get template info for each
        templates_info = []
        for template_name in template_files:
            try:
                info = PromptManager.get_template_info(template_name)
                templates_info.append(info)
            except Exception as e:
                print(f"Error loading template {template_name}: {e}")

        return render_template("index.j2", templates=templates_info)
    except Exception as e:
        flash(f"Error loading templates: {str(e)}", "danger")
        return render_template("index.j2", templates=[])


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
