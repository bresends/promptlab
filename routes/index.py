from pathlib import Path

from flask import flash, redirect, render_template, request, url_for

from app import db
from models.user import User
from prompts.prompt_manager import PromptManager


def list_prompts():
    """List all available prompt templates organized by category"""
    try:
        prompts_by_category = PromptManager.get_all_prompts()

        if not prompts_by_category:
            flash("No templates found", "warning")

        return render_template("index.j2", prompts_by_category=prompts_by_category)
    except Exception as e:
        flash(f"Error loading templates: {str(e)}", "danger")
        return render_template("index.j2", prompts_by_category={})


def render_prompt(template_path):
    """Render prompt template with interactive form using path (e.g., 'youtube/compare_videos')"""
    try:
        template_info = PromptManager.get_template_info(template_path)

        # Initialize template data
        template_data = {}
        rendered_prompt = ""

        # If this is a POST request, process the form data
        if request.method == "POST":
            # Handle form variables
            for key, value in request.form.items():
                if key in template_info["variables"] and value.strip():
                    template_data[key] = value

            # Try to render the prompt with current data
            try:
                rendered_prompt = PromptManager.get_prompt(
                    template_path, **template_data
                )
            except Exception as e:
                # If rendering fails (missing variables), show partial render
                rendered_prompt = f"Error rendering prompt: {str(e)}"
        else:
            # For GET requests, try to render with empty values to show template structure
            try:
                # Create empty values for all variables
                empty_data = {
                    var: f"[{var.upper()}]" for var in template_info["variables"]
                }
                rendered_prompt = PromptManager.get_prompt(template_path, **empty_data)
            except Exception:
                rendered_prompt = "Fill in the variables to see the rendered prompt."

        return render_template(
            "prompts/interactive.j2",
            template_name=template_info["name"],
            template_path=template_path,
            template_info=template_info,
            template_data=template_data,
            rendered_prompt=rendered_prompt,
        )

    except Exception as e:
        flash(f"Error loading template {template_path}: {str(e)}", "danger")
        return redirect(url_for("list_prompts"))


def show_users():
    """Display all users from the database"""
    try:
        users = User.query.all()
        return render_template("users.j2", users=users)
    except Exception as e:
        flash(f"Error retrieving users: {str(e)}")
        return redirect(url_for("list_prompts"))


def create_user():
    """Create a new user"""
    if request.method == "POST":
        try:
            username = request.form.get("username")
            email = request.form.get("email")
            password = request.form.get("password")

            if not username or not email or not password:
                flash("All fields are required!")
                return redirect(url_for("list_prompts"))

            new_user = User()
            new_user.username = username
            new_user.email = email
            new_user.password = password

            db.session.add(new_user)
            db.session.commit()
            flash(f"User {username} created successfully!")
            return redirect(url_for("list_prompts"))

        except Exception as e:
            db.session.rollback()
            flash(f"Error creating user: {str(e)}")
            return redirect(url_for("list_prompts"))

    # For GET requests, show the create user form
    return render_template("create_user.j2")
