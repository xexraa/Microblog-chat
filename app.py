import datetime
import os
from flask import Flask, render_template, request
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    client = MongoClient(os.getenv("MONGODB_URI"))
    app.db = client.Microblog


    @app.route("/", methods=["GET", "POST"])
    def home():
        if request.method == "POST":
            entryContent = request.form.get("content")
            date = datetime.datetime.today().strftime("%Y-%m-%d")
            time = datetime.datetime.today().strftime("%H-%M") 
            app.db.entries.insert_one({"content": entryContent, "date": date, "time": time})
            
        entriesWithDate = [
            (
            entry["content"],
            entry["date"],
            datetime.datetime.strptime(entry["date"],"%Y-%m-%d").strftime("%b %d"),
            datetime.datetime.strptime(entry["time"],"%H-%M").strftime("%H:%M") 
            ) for entry in app.db.entries.find({})
            ]
        return render_template("home.html", entries=entriesWithDate)
    
    
    @app.route("/meeting", methods=["GET", "POST"])
    def meeting():
        if request.method == "POST":
            content = request.form.get("meetContent")
            time = datetime.datetime.today().strftime("%H-%M") 
            app.db.meetings.insert_one({"meetContent": content, "time": time})
            
        meets = [(entry["meetContent"], datetime.datetime.strptime(entry["time"],"%H-%M").strftime("%H:%M"))for entry in app.db.meetings.find({})]
            
        return render_template("meeting.html", meets=meets)
    
    
    return app