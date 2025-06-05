import os
from flask import Flask, render_template, session, flash, request, redirect, url_for
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__, template_folder="templates", static_folder="static")

app.secret_key = os.getenv("SECRET_KEY")


@app.route("/")
def index():
    return render_template("index.j2", message="Hello, World!")


@app.route("/set_data")
def set_data():
    session["name"] = "Mike"
    return render_template("index.j2", message="Data has been set in the session!")


@app.route("/get_data")
def get_data():
    name = session.get("name", "No data found in session")
    return render_template("index.j2", message=f"Session data: {name}")


@app.route("/clear_data")
def clear_data():
    session.pop("name", None)
    return render_template("index.j2", message="Session data has been cleared!")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == "admin" and password == "password":
            session["logged_in"] = True
            session["username"] = username
            flash("Login successful!")
            return redirect(url_for("index"))
        else:
            flash("Invalid username or password!")

    return render_template("login.j2")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
