from flask import Flask, render_template
import sqlite3


app = Flask(__name__)


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/all_songs')
def all_songs():
    conn = sqlite3.connect('song.db')
    cur = conn.cursor()
    cur.execute('SELECT name, artist FROM song')
    results = cur.fetchall()
    print(results)
    return render_template("all_songs.html", results=results)


if __name__ == "__main__":
    app.run(debug = True)