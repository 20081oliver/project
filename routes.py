from flask import Flask, render_template, request, redirect, flash
import sqlite3


app = Flask(__name__)
app.secret_key = "flash"  # used for flasking
conn = sqlite3.connect('song.db')
conn = sqlite3.connect('song.db', check_same_thread=False)
cur = conn.cursor()

# home tab


@app.route('/')
def home():
    return render_template("home.html")

# about tab


@app.route('/about')
def about():
    return render_template("about.html")

# route that displays all the songs added


@app.route('/all_songs')
def all_songs():
    cur.execute('SELECT name, artist, album FROM song')
    results = cur.fetchall()
    print(results)
    return render_template("all_songs.html", results=results)

# adding a song code


@app.post('/add_a_song')
def add_a_song():
    sql = ('INSERT INTO song (name, artist, album) VALUES (?,?,?)')
    cur.execute(sql, (request.form['name'], request.form['artist'],
                request.form['album']))
    conn.commit()
    results = cur.fetchall()
    print(results)
    flash('Song submitted!')
    return redirect("all_songs")


# delelte code


@app.route('/delete/<name>')
def delete_song(name):
    conn = sqlite3.connect("song.db")
    cur.execute("DELETE FROM song WHERE name = ?", (name,))
    conn.commit()
    print("name")
    return redirect("/admin_all_songs")

# admin login page


password = "1234"  # password to access admin
typed = False


@app.route("/admin/login", methods=['GET', 'POST'])
def adminLogin():
    global password
    global typed
    if request.method == 'POST':
        formRequest = request.form['password']
        if formRequest == password:
            typed = True
            flash("Login successful!")
            # if the password is correct, the user will be redirected to
            # "admin_all_songs" and get flashed with "Login successfull!"
            return redirect("/admin_all_songs") 
        else:
            flash('Incorrect password')  # if the password is incorrect a
            #  message will flash "Incorrect Password"
            return redirect("/admin/login")
    return render_template("login.html")

# how admins view every song


@app.route('/admin_all_songs')
def adminSongs():
    cur.execute('SELECT name, artist, album FROM song')
    results = cur.fetchall()
    print(results)
    return render_template("admin_all_songs.html", results=results)


if __name__ == "__main__":
    app.run(debug=True)
