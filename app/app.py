from flask import Flask, request, jsonify, render_template
import sqlite3
app = Flask(__name__)


def get_db():
	db = sqlite3.connect("matches.db")
	db.execute("""
		CREATE TABLE IF NOT EXISTS matches (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		hero TEXT,
		map_name TEXT,
		time INTEGER,
		date TEXT,
		outcome TEXT
	)""")
	return db

@app.route("/matches", methods=["POST"])
def add_match():
    data = request.get_json()
    hero = data["hero"]
    map_name = data["map"]
    time = data["time"]
    date = data["date"]
    outcome = data["outcome"]
    db = get_db()
    db.execute("INSERT INTO matches (hero, map_name, time, date, outcome) VALUES (?, ?, ?, ?, ?)", (hero, map_name, time, date, outcome))
    db.commit()
    return jsonify({"status": "added"}), 201

@app.route("/matches")
def list_matches():
	db = get_db()
	db.row_factory = sqlite3.Row
	rows = db.execute("SELECT * FROM matches").fetchall()
	return jsonify([dict(row) for row in rows])

@app.route("/stats")
def get_stats():
	db = get_db()
	db.row_factory = sqlite3.Row
	stats = db.execute("""
	SELECT hero,
	 	COUNT(*) AS games, 
	 	SUM(CASE WHEN outcome = 'win' THEN 1 ELSE 0 END) AS wins
	 FROM matches 
	 GROUP BY hero 
	 ORDER BY games DESC
	 				  """).fetchall()


	
	lines = []
	for row in stats:
		winrate = row['wins'] / row['games'] * 100
		lines.append(f"Hero: {row['hero']}<br>Games: {row['games']}<br>WR: {round(winrate)}%<br>")
	return "<br>".join(lines)

@app.route("/stats/view") # New view page created by claude code, my code is in the pure /stats page
def stats_view():
	# Same query as /stats: one row per hero with games played and wins.
	db = get_db()
	db.row_factory = sqlite3.Row
	rows = db.execute("""
		SELECT hero,
			COUNT(*) AS games,
			SUM(CASE WHEN outcome = 'win' THEN 1 ELSE 0 END) AS wins
		FROM matches
		GROUP BY hero
		ORDER BY games DESC
	""").fetchall()

	# Turn each database row into a plain dict and add the win rate,
	# so the template only has to display values, not calculate them.
	heroes = []
	for row in rows:
		heroes.append({
			"hero": row["hero"],
			"games": row["games"],
			"wins": row["wins"],
			"winrate": round(row["wins"] / row["games"] * 100),
		})

	# Flask looks for this file in the templates/ folder and fills it in
	# with the "heroes" list.
	return render_template("stats.html", heroes=heroes)

@app.route("/health")
def health():
	return "ok"

@app.route ("/")
def home():
	return  '<h1>Overwatch Tracker</h1><a href="/health">Check health</a> | <a href="/stats/view">View stats</a>'
 	
if __name__ == "__main__":
    db = get_db()
    print(db.execute("SELECT name FROM sqlite_master").fetchall())