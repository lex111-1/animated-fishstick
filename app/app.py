from flask import Flask, request, jsonify
import sqlite3
app = Flask(__name__)


def get_db():
	db = sqlite3.connect("matches.db")
	db.execute("""
		CREATE TABLE IF NOT EXISTS matches (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		hero TEXT,
		map TEXT,
		time INTEGER,
		date TEXT,
		outcome TEXT
	)""")
	return db

@app.route("/health")
def health():
	return "ok"

@app.route ("/")
def home():
	return  '<h1>Overwatch Tracker</h1><a href="/health">Check health</a>'
 	
if __name__ == "__main__":
    db = get_db()
    print(db.execute("SELECT name FROM sqlite_master").fetchall())