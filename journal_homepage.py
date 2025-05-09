from flask import Flask, request, render_template
import sqlite3

DB = "journal.db"

## DATABASES
with sqlite3.connect(DB) as conn:
        conn.execute(f"""CREATE TABLE IF NOT EXISTS journal(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            date TEXT,
            entry TEXT
        )""")

with sqlite3.connect(DB) as con:
    con.execute(f"""CREATE TABLE IF NOT EXISTS account(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                forename TEXT,
                surname TEXT,
                email TEXT,
                username TEXT,
                password TEXT
                )""")

## FLASK PAGES
app = Flask(__name__)


# Home page
@app.route("/")
def home():
    return render_template("home.html")


# Login page
@app.route("/login")
def log_in():
    return render_template("login.html")


# Create account confirmation
@app.route("/confirm")
def confirm():
    return("confirm.html")


# Create account page
@app.route("/createaccount", methods=["GET", "POST"])
def make_account():
    if request.method == "POST":
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")

        with sqlite3.connect(DB) as con:
            con.execute("""INSERT INTO account (forename, surname, email,
                        username, password) VALUES (?, ?, ?, ?, ?)
                        """, (fname, lname, email, username, password))
        return render_template("confirm.html")
    return render_template("create_account.html")    


# Journal entry page
@app.route("/user", methods=["GET", "POST"])
def user_page():
    if request.method == "POST":
        name = request.form.get("name")
        date = request.form.get("date")
        entry = request.form.get("entry")
        with sqlite3.connect(DB) as conn:
            conn.execute(f"INSERT INTO journal (name, date, entry) VALUES (?, ?, ?)", (name, date, entry))

    with sqlite3.connect(DB) as conn:
        entries = conn.execute(f"SELECT date, entry FROM journal").fetchall()
    return render_template("user.html", entries=entries)


# Connecting to server
if __name__ == "__main__":    
    app.run(debug=True)    

