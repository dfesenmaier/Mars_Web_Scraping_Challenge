from flask import Flask, jsonify, request, render_template, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from scrape_mars import scrape, read_scrape

app = Flask(__name__)

@app.route("/")
def index():
    return send_from_directory("", "index.html")

@app.route("/landing")
def landing():
	return render_template("home.html", data=read_scrape())

@app.route("/scrape")
def scrape_data():
	scrape()
	return render_template("home.html", data=read_scrape())

if __name__ == "__main__":
    app.run(debug=True)