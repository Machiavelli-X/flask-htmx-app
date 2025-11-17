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
        return render_template("home.html", title="Home", body_class="home-body")

    return render_template("index.html", title="Login", body_class="login-body")


@app.route("/login", methods=["GET", "POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    if username == "Demo_user" and password == "pass1234":
        session["logged_in"] = True

        
        if "HX-Request" in request.headers:
            return render_template("home_partial.html", show_welcome=True)

        
        return render_template(
            "home.html",
            show_welcome=True,
            title="Home",
            body_class="home-body",
        )

    
    return render_template(
        "index.html",
        error="Invalid username or password!",
        title="Login",
        body_class="login-body",
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


# ------------------- MAIN APP RUNNER -------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
