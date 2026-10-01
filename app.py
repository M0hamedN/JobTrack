import os
from dotenv import load_dotenv
from flask import Flask, flash, render_template, request, session, redirect
from flask_session import Session
from cs50 import SQL
from helpers import *
from werkzeug.security import check_password_hash, generate_password_hash
from flask_wtf import CSRFProtect

load_dotenv()

app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY")
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

csrf = CSRFProtect(app)

db = SQL("sqlite:///jobtrack.db")


@app.route('/', methods=["POST", "GET"])
@login_required
def main():

    if request.method == "POST":
        if "notes" in request.form:
            

            return redirect("/")

        elif "application_id" in request.form:
            application_id = request.form.get("application_id")

            db.execute(
                "DELETE FROM applications WHERE id = ? AND user_id = ?",
                application_id,
                session["user_id"]
            )

            return redirect("/")

    if request.method == "GET":
        user = db.execute(
            "SELECT username, id FROM users WHERE id = ?",
            session["user_id"]
        )[0]

        applications = db.execute(
            "SELECT id, job_title, job_url, location, status, applied_date, notes "
            "FROM applications WHERE user_id = ?",
            session["user_id"]
        )

        companies = db.execute(
            "SELECT name, url FROM companies "
            "WHERE id IN "
            "(SELECT company_id FROM applications WHERE user_id = ?)",
            session["user_id"]
        )

        return render_template(
            "main.html",
            applications=applications,
            username=user["username"],
            user_id=user["id"],
            companies=companies
        )

    return render_template("main.html")


@app.route('/account')
@login_required
def account():
    user = db.execute("SELECT email, username, created_at FROM users WHERE id == ?", session["user_id"])
    job_titles = db.execute("SELECT job_title FROM applications WHERE user_id = ?", session["user_id"])
    applications_count = len(job_titles)
    companies = db.execute("SELECT companies.name FROM applications JOIN companies ON applications.company_id = companies.id WHERE applications.user_id = ? GROUP BY companies.name", session["user_id"])
    print(companies)
    return render_template("account.html", user=user[0], job_titles=job_titles, count=applications_count, companies=companies)

@app.route('/delete_account')
@login_required
def delete_account():
    db.execute("DELETE FROM users WHERE id = ?", session["user_id"])
    session.clear()
    return redirect('/login')

@app.route('/change_password', methods=["POST"])
@login_required
def change_password():
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm-password')
    print(new_password, confirm_password)

    if new_password != confirm_password:
        flash("Confirm password does not match")
        return redirect('/Account')

    new_password_hash = generate_password_hash(new_password)

    db.execute("UPDATE users SET password_hash = ? WHERE id = ?", new_password_hash, session["user_id"])
    return redirect('/logout')


@app.route('/update_status', methods=["POST"])
@login_required
def update_status():
    new_status = request.form.get('status')
    application_id = request.form.get('application_id')
    if not new_status:
        flash('No changes were made')
        return redirect('/')

    try:
        db.execute('UPDATE applications SET status = ? WHERE user_id == ? AND id == ?', new_status, session["user_id"], application_id)
        if new_status == 'accepted':
            flash('Congratulations on getting accepted!!!')
    except IndexError:
        flash('No changes were made')
        return redirect('/')
    
    return redirect('/')

@app.route('/update_notes', methods=["POST"])
@login_required
def update_notes():
    application_id = request.form.get("id")
    new_notes = request.form.get("notes")

    db.execute(
        "UPDATE applications SET notes = ? WHERE id = ? AND user_id = ?",
        new_notes,
        application_id,
        session["user_id"]
    )
    return redirect('/')

@app.route('/add_application', methods=["POST"])
@login_required
def add_application():
    job_title = request.form.get("job_title")
    job_url = request.form.get("job_url")
    company = request.form.get("company")
    company_url = request.form.get("company_url")
    location = request.form.get("location")
    status = request.form.get("status")
    notes = request.form.get("notes")

    if not job_title or not location or not status or not company:
        flash("Missing information for application. Required fields: (Job title, Location, Status, Company)")
        return redirect("/")

    try:
        company_id = db.execute(
            "SELECT id FROM companies WHERE name = ?", company
        )[0]["id"]

    except IndexError:
        db.execute(
            "INSERT INTO companies(name, url) VALUES(?, ?)",
            company,
            company_url
        )

        company_id = db.execute(
            "SELECT id FROM companies WHERE name = ?", company
        )[0]["id"]

    db.execute(
        "INSERT INTO applications(user_id, company_id, job_title, job_url, location, status, notes) VALUES(?, ?, ?, ?, ?, ?, ?)",
        session["user_id"],
        company_id,
        job_title,
        job_url,
        location,
        status,
        notes
    )
    return redirect('/')


@app.route('/delete_application', methods=["POST"])
@login_required
def delete_application():
    application_id = request.form.get("application_id")

    db.execute(
        "DELETE FROM applications WHERE id = ? AND user_id = ?",
        application_id,
        session["user_id"]
    )

    return redirect('/')


@app.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect('/login')


@app.route('/login', methods=["GET", "POST"])
def login():

    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        userorE = request.form.get("email-or-username")

        # stands for username or email
        if not userorE or not request.form.get("password"):
            flash("Invalid input")
            return redirect("/login")

        rows = db.execute(
            "SELECT * FROM users WHERE username = ? OR email = ?",
            userorE,
            userorE
        )

        if len(rows) != 1 or not check_password_hash(
            rows[0]["password_hash"],
            request.form.get("password")
        ):
            flash("Invalid login")
            return redirect("/login")

        # log user in
        session["user_id"] = rows[0]["id"]

        return redirect("/")

    flash("Login successful!")
    return render_template("login.html")


@app.route('/register', methods=["GET", "POST"])
def register():

    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm-password")

        if not email or not username or not password or not confirm_password:
            flash("Invalid input")
            return redirect("/register")

        if not is_valid_email(email):
            flash("Invalid email")
            return redirect("/register")

        if password != confirm_password:
            flash("Password does not match confirmation")
            return redirect("/register")

        if db.execute(
            "SELECT * FROM users WHERE username = ? OR email = ?",
            username,
            email
        ):
            flash("User already exists.")
            return redirect("/register")

        password_hash = generate_password_hash(password)

        db.execute(
            "INSERT INTO users(email, username, password_hash) VALUES(?, ?, ?)",
            email,
            username,
            password_hash
        )

        flash("Account successfully registered")
        return redirect("/login")



if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)