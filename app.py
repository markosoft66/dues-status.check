from flask import Flask, request, redirect, url_for, render_template, session
from data_handler import get_combined_data, get_cached_data
from datetime import timedelta
from dotenv import load_dotenv
import os
import time

# Load env variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

# Session Config
app.permanent_session_lifetime = timedelta(minutes=10)

@app.before_request
def session_management():
    session.permanent = True

@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Get credentials from .env
        env_user = os.getenv("ADMIN_USERNAME")
        env_pass = os.getenv("ADMIN_PASSWORD")

        if username == env_user and password == env_pass:
            session.clear()
            session["user"] = username
            return redirect(url_for("search"))
        else:
            # Brute Force Protection: Slow down failed attempts
            time.sleep(2) 
            return render_template("login.html", error="Invalid Username or Password")
            
    return render_template("login.html")

@app.route("/search", methods=["GET", "POST"])
def search():
    if "user" not in session:
        return redirect(url_for("login"))
    
    record = None
    search_query = None
    df, last_updated = get_cached_data()

    if request.method == "POST":
        search_query = request.form.get("search_value", "").strip()
        
        if search_query:
            df, last_updated = get_combined_data()
            # Check if columns exist before searching to prevent errors
            if 'ID' in df.columns and 'NAME' in df.columns:
                mask = (
                    df['ID'].astype(str).str.contains(search_query, case=False, na=False) |
                    df['NAME'].astype(str).str.contains(search_query, case=False, na=False)
                )
                record = df[mask].to_dict(orient="records")

    if last_updated is None:
        last_updated = "N/A"
            
    return render_template("search.html", 
                           record=record, 
                           search_value=search_query, 
                           last_updated=last_updated)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)

# Vercel looks for the 'app' variable
app = app 

if __name__ == "__main__":
    app.run()