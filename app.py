from flask import render_template, Flask, render_template, flash, request, redirect, url_for, session
from conection import engine
import connexion
import user as sheduled_user
import event as sheduled_event

app = connexion.App(__name__, specification_dir="./")
app.add_api("swagger.yml")


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
        msg = msg + "Ei po"
        email, password = request.form["usuario"], request.form["senha"]
        with engine.connect() as conn:
            connection = conn.connect("./DB/schedule.db")
            msg = msg + "Vai Tu"
            if user[3] == email and user[4] == password:
                session["email"] = user[3]
                session["password"] = user[4]
                session["First_name"] = user[0]
                session["Last_name"] = user[1]
                return render_template("login.html")
        return render_template("homepage.html", msg=msg)


@app.route("/Perfil")
def perfill():
    return render_template("myperfil.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    

    return render_template("register.html")


@app.route("/Events")
def perfil():
    return render_template("myevents.html")



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
