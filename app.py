from flask import Flask, render_template, request, session, redirect, url_for
from flask_session import Session
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)


@app.route("/")
def index():
    if session.get("logged_in"):
        theme = session.get("theme", "light")
        return render_template("home.html", title="Home", body_class="home-body", theme=theme)

    return render_template("index.html", title="Login", body_class="login-body")


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    if username == "Demo_user" and password == "pass1234":
        session["logged_in"] = True
        session["theme"] = "light"  # default theme

        # If HTMX request → return partial
        if "HX-Request" in request.headers:
            return render_template("home_partial.html", theme="light", show_welcome=True)

        return render_template("home.html", theme="light", show_welcome=True)

    return render_template("index.html", error="Invalid username or password!")


@app.route("/toggle-theme", methods=["POST"])
def toggle_theme():
    if not session.get("logged_in"):#If someone tries to open POST /toggle-theme WITHOUT logging in…This line stops them:
        return "Not logged in", 401

    current_theme = session.get("theme", "light")
    new_theme = "dark" if current_theme == "light" else "light"
    session["theme"] = new_theme

    # Return updated partial view ONLY
    return render_template("home_partial.html", theme=new_theme)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
