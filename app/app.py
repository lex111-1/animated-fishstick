from flask import Flask

app = Flask(__name__)

@app.route("/health")
def health():
	return "ok"

@app.route ("/")
def home():
	return  '<h1>Overwatch Tracker</h1><a href="/health">Check health</a>'
 	
