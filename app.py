from flask import render_template, Flask, render_template, flash, request, redirect, url_for, session
from conection import engine
import connexion
import user as sheduled_user
import event as sheduled_event

app = connexion.App(__name__, specification_dir="./")
app.add_api("swagger.yml")
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_hereAAAAAAAAAAAAASDWSDAWZXCSAWD'
app.secret_key = "your_secret_key_hereAAAAAAAAAAAAASDWSDAWZXCSAWD"


@app.route("/user")
def user():
    user = sheduled_user.read_all()
    event = sheduled_event.read_all()
    return render_template("home.html", user=user, event=event)


@app.route("/")
def home():
    return render_template("homepage.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    msg = ""
    if request.method == "POST":
        email, password = request.form["usuario"], request.form["senha"]
        users = sheduled_user.read_all()
        with engine.connect() as conn:
            for user in users:
                if user["user_email"] == email and user["user_password"] == password:
                    session["user_email"] = user["user_email"]
                    session["user_password"] = user["user_password"]
                    session["user_name"] = user["user_name"]
                    session["user_id"] = user["user_id"]
                    session["user_status"] = user["user_status"]
                    return render_template("login.html")
        return render_template("homepage.html", msg=msg)


@app.route("/Perfil")
def perfill():
    return render_template("myperfil.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    msg = ""
    if request.method == "POST":
        first_name, email, password = request.form["first_name"], request.form["email"], request.form["senha"]
        users = sheduled_user.read_all()
        with engine.connect() as conn:
            user_verification = sheduled_user.read_one(2)
            for user in users:
                if user_verification["user_email"] == email:
                    return render_template("register.html")
            
            user_dict = {
                    'user_email': email,
                    'user_name': first_name,
                    'user_password': password,
                    'user_status': 0
            }
            create_user = sheduled_user.create(user_dict)
            if(create_user):
                return render_template("login.html")
            else:
                return render_template("register.html")
            
    return render_template("register.html")


@app.route("/Events")
def perfil():
    return render_template("myevents.html")



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
