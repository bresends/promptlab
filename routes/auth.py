from flask import render_template, request, session, flash, redirect, url_for


def login():
    """Handle user login"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == "admin" and password == "password":
            session["logged_in"] = True
            session["username"] = username
            flash("Login successful!")
            return redirect(url_for("list_prompts"))
        else:
            flash("Invalid username or password!")

    return render_template("login.j2")
