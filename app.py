import datetime
import os
from flask import Flask, render_template, request
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
client = MongoClient(os.getenv("MONGODB_URI")) #reprezentacja klastra mongoDB
#db = client.microblog to łączy się z database mongo
app.db = client.Microblog #wystarczy dodać app. żeby połączyć z naszą appką


@app.route("/", methods=["GET", "POST"])
def home():
    print([e for e in app.db.entries.find({})])
    if request.method == "POST":
        entryContent = request.form.get("content") #metoda na odbieranie danych ze strony, 'content' jest to name z home.html
        date = datetime.datetime.today().strftime("%Y-%m-%d")
        app.db.entries.insert_one({"content": entryContent, "date": date})
        
    entriesWithDate = [(entry["content"], entry["date"], datetime.datetime.strptime(entry["date"],
                            "%Y-%m-%d").strftime("%b %d")) for entry in app.db.entries.find({})]
    #entriesWithDate = [e for e in app.db.entries.find({})] opcja bezpośrednio z dictionary
    return render_template("home.html", entries=entriesWithDate)