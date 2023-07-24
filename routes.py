from flask import Flask, render_template, request, redirect
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


@app.post('/add_a_song')
def add_a_song():
    conn = sqlite3.connect('song.db')
    cur = conn.cursor()
    sql = ('INSERT INTO song (name, artist, album) VALUES (?,?,?)')
    cur.execute(sql, (request.form['name'], request.form['artist'], request.form['album']))
    conn.commit()
    results = cur.fetchall()
    print(results)
    return redirect("all_songs")


# @app.route('/delete/<int:id>')

@app.route('/add_song', methods=['POST', 'GET'])
def add_song():
    return render_template("add_song.html")


if __name__ == "__main__":
    app.run(debug=True)
