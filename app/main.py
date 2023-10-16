from flask import Flask, request, session, render_template, redirect, url_for
from flask_mysqldb import MySQL
from MySQLdb.cursors import DictCursor

app = Flask(__name__)

app.secret_key = "your secret key"

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "flask_basics"

mysql = MySQL(app)


@app.route("/")
def empty():
    return redirect(url_for("login"))


@app.route("/login", methods=["POST", "GET"])
def login():
    msg = ""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        try:
            cursor = mysql.connection.cursor(DictCursor)
            sql = f"SELECT * FROM login WHERE (username = '{username}' AND password = '{password}') OR (email = '{username}' AND password = '{password}')"
            cursor.execute(sql)
            account = cursor.fetchone()
            print(account)
            if account:
                user = account["username"]
                session["loggedin"] = True
                session["id"] = account["id"]
                session["username"] = user
                msg = "Logged in succesfully"
                return render_template("index.html", message=msg, user=user)
            else:
                msg = "Incorrect user / password"
        except Exception as e:
            raise e
    return render_template("login.html", message=msg)


@app.route("/logout")
def logout():
    session.pop("loggedin", None)
    session.pop("id", None)
    session.pop("username", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
