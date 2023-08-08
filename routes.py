from flask import Flask, render_template, request, redirect
import sqlite3


app = Flask(__name__)
conn = sqlite3.connect('song.db')
conn = sqlite3.connect('song.db', check_same_thread=False)
cur = conn.cursor()


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/all_songs')
def all_songs():
    cur.execute('SELECT name, artist, album FROM song')
    results = cur.fetchall()
    print(results)
    return render_template("all_songs.html", results=results)


@app.post('/add_a_song')
def add_a_song():
    sql = ('INSERT INTO song (name, artist, album) VALUES (?,?,?)')
    cur.execute(sql, (request.form['name'], request.form['artist'], request.form['album']))
    conn.commit()
    results = cur.fetchall()
    print(results)
    return redirect("all_songs")


@app.route('/edit_a_song/<int:id>', methods=['POST', 'GET'])
def edit_a_song(id):
    song_to_update = all_songs.query(id)
    if request.method == "POST":
        song_to_update.name = request.form['name']
        song_to_update.name = request.form['artist']
        song_to_update.name = request.form['album']
        sql = ('INSERT INTO song (name, artist, album) VALUES (?,?,?)')
        cur.execute(sql, (request.form['name'], request.form['artist'], request.form['album'],))
        cur.session.commit()
    else: 
        print("")
    return render_template('edit_song.html', song_to_update=song_to_update)


    #sql = ('INSERT INTO song (name, artist, album) VALUES (?,?,?)')
    #cur.execute(sql, (request.form['name'], request.form['artist'], request.form['album']))
    #conn.commit()
    #results = cur.fetchall()
    #print(results)
    #return redirect("all_songs")


@app.post('/delete_song')
def delete_song():
    sql = "DELETE FROM song WHERE id = ?"
    cur.execute(sql, (request.form['song_id']))
    conn.commit()
    return redirect("all_songs")


if __name__ == "__main__":
    app.run(debug=True)
