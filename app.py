from flask import Flask, render_template, request, session, abort
import pyrebase
import os

firebaseConfig = {
    "apiKey": "AIzaSyCADqv8fYiPERrQpfgQpg7NjJymPaYrmek",
    "authDomain": "verkefni-5-m.firebaseapp.com",
    "databaseURL": "https://verkefni-5-m.firebaseio.com",
    "projectId": "verkefni-5-m",
    "storageBucket": "verkefni-5-m.appspot.com",
    "messagingSenderId": "685894801282",
    "appId": "1:685894801282:web:8f9a3e4b9a6609681fa19b"
}

app = Flask(__name__)
app.secret_key = os.urandom(42)
fb = pyrebase.initialize_app(firebaseConfig)
db = fb.database()


def generate_context(title):
    context = {
        "title": title
    }
    if "username" in session and session["username"] != None:
        context["username"] = session["username"]
    return context


def render(template, title):
    return render_template(template, context=generate_context(title))


@app.route("/")
def route_index():
    return render("index.html", "Home")


@app.route("/login")
def route_login():
    return render("login.html", "Log in")


@app.route("/logout")
def route_logout():
    if "username" in session:
        session.pop("username")
        return "You have been logged out<script>window.setTimeout(function(){ window.location.href = '/'; }, 2000);</script>"
    return "<script>window.setTimeout(function(){ window.location.href = '/'; }, 2000);</script>"


@app.route("/register")
def route_register():
    return render("register.html", "Register")


@app.route("/secured")
def route_secured():
    if "username" in session:
        return render("secure.html", "Secured page")
    else:
        abort(401)


@app.route("/api/login", methods=["POST"])
def route_api_login():
    username = request.form["username"]
    password = request.form["password"]
    if not username or not password:
        return "Login failed.<script>window.setTimeout(function(){ window.location.href = '/login'; }, 2000);</script>"
    if db.child("users").child(username).shallow().get().val():
        userPassword = db.child("users").child(
            username).child("password").shallow().get().val()
        if password == userPassword:
            session["username"] = username
    return "<script>window.setTimeout(function(){ window.location.href = '/'; }, 2000);</script>"


@app.route("/api/register", methods=["POST"])
def route_api_register():
    username = request.form["username"]
    password = request.form["password"]
    if not username or not password:
        return "<script>window.setTimeout(function(){ window.location.href = '/'; }, 2000);</script>"
    ret = ""
    if db.child("users").child(username).shallow().get().val():
        ret = "Username is taken"
    else:
        db.child("users").child(username).set({"password": password})
        ret = "Registered %s and %s" % (username, password)
    return ret+"<script>window.setTimeout(function(){ window.location.href = '/'; }, 2000);</script>"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
