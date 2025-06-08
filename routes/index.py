from pathlib import Path

from flask import flash, redirect, render_template, request, url_for, session

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
        
        # Check if this is a multi-step template
        if template_info.get("is_multi_step"):
            return render_multi_step_prompt(template_path, template_info)

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


def render_multi_step_prompt(template_path, template_info):
    """Handle multi-step prompt rendering"""
    try:
        # Get current step from query parameter, default to first step
        current_step_id = request.args.get('step', template_info['steps'][0]['id'])
        
        # Get step responses from session
        session_key = f"multistep_{template_path.replace('/', '_')}"
        step_responses = session.get(session_key, {})
        
        # Find current step info
        current_step = None
        step_index = 0
        for i, step in enumerate(template_info['steps']):
            if step['id'] == current_step_id:
                current_step = step
                step_index = i
                break
        
        if not current_step:
            flash(f"Step {current_step_id} not found", "danger")
            return redirect(url_for("list_prompts"))
        
        rendered_step = ""
        
        # Handle POST request (step submission)
        if request.method == "POST":
            # Handle form variables for current step
            step_variables = {}
            for var in current_step.get('variables', []):
                value = request.form.get(var, '').strip()
                if value:
                    step_variables[var] = value
            
            # Save step variables
            step_responses[current_step_id] = step_variables
            
            # Handle LLM output if provided
            llm_output = request.form.get('llm_output', '').strip()
            if llm_output:
                # Save LLM output for this step
                llm_outputs_key = f"{session_key}_llm_outputs"
                llm_outputs = session.get(llm_outputs_key, {})
                llm_outputs[current_step_id] = llm_output
                session[llm_outputs_key] = llm_outputs
                
                # Move to next step if there are more steps
                next_step_index = step_index + 1
                if next_step_index < len(template_info['steps']):
                    next_step_id = template_info['steps'][next_step_index]['id']
                    session[session_key] = step_responses
                    return redirect(url_for('render_prompt', template_path=template_path, step=next_step_id))
                else:
                    # All steps completed
                    session[session_key] = step_responses
                    flash("Workflow completed successfully!", "success")
                    return redirect(url_for('list_prompts'))
            
            # If no LLM output provided, just save variables and stay on current step
            session[session_key] = step_responses
        
        # Get LLM outputs for context
        llm_outputs_key = f"{session_key}_llm_outputs"
        llm_outputs = session.get(llm_outputs_key, {})
        
        # Render current step
        try:
            rendered_step = PromptManager.render_step(
                template_path, current_step_id, step_responses, llm_outputs
            )
        except Exception as e:
            rendered_step = f"Error rendering step: {str(e)}"
        
        return render_template(
            "prompts/multi_step.j2",
            template_name=template_info["name"],
            template_path=template_path,
            template_info=template_info,
            current_step=current_step,
            current_step_index=step_index,
            total_steps=len(template_info['steps']),
            rendered_step=rendered_step,
            step_responses=step_responses,
        )
        
    except Exception as e:
        flash(f"Error rendering multi-step template {template_path}: {str(e)}", "danger")
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
