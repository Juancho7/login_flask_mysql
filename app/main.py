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
            sql = "SELECT * FROM login WHERE username = %s AND password = %s"
            cursor.execute(sql, (username, password))
            account = cursor.fetchone()
            if account:
                session["loggedin"] = True
                session["id"] = account["id"]
                session["username"] = account["username"]
                msg = "Logged in succesfully"
                return render_template("index.html", message=msg)
            else:
                msg = "Incorrect user / password"
        except Exception as e:
            raise e
    return render_template("login.html", message=msg)


@app.route("/register", methods=["POST", "GET"])
def register():
    msg = ""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        cursor = mysql.connection.cursor(DictCursor)
        sql = "SELECT * FROM login WHERE username = %s OR email = %s"
        cursor.execute(sql, (username, email))
        account = cursor.fetchone()
        if account:
            msg = "This account already exists!"
        else:
            sql = "INSERT INTO login (username, password, email) VALUES (%s, %s, %s)"
            cursor.execute(sql, (username, password, email))
            mysql.connection.commit()
            msg = "Registered succesfully"
        return render_template("register.html", message=msg)
    return render_template("register.html", message=msg)


if __name__ == "__main__":
    app.run(debug=True)
