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


@app.route('/delete/<name>')
def delete_song(name):
    conn = sqlite3.connect("song.db")

    cur.execute("DELETE FROM song WHERE name = ?", (name,))
    conn.commit()
    print("name")
    return redirect("/admin_all_songs")


password = "1234"
typed = False


@app.route("/admin/login", methods=['GET', 'POST'])
def adminLogin():
    global password
    global typed
    if request.method == 'POST':
        formRequest = request.form['password']
        if formRequest == password:
            typed = True
            return redirect("/admin_all_songs")
        else:
            return redirect("/admin/login")
    return render_template("login.html")


@app.route('/admin_all_songs')
def adminSongs():
    cur.execute('SELECT name, artist, album FROM song')
    results = cur.fetchall()
    print(results)
    return render_template("admin_all_songs.html", results=results)


if __name__ == "__main__":
    app.run(debug=True)
