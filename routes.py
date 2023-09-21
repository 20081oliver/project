from flask import Flask, render_template, request, redirect, flash
import sqlite3


app = Flask(__name__)
app.secret_key = "flash"  # used for flashing
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
    # Gets the name, artist, and album from the song table
    # to get displayed onto the all songs page
    results = cur.fetchall()
    print(results)
    return render_template("all_songs.html", results=results)


# adding a song code


@app.post('/add_a_song')
def add_a_song():
    sql = ('INSERT INTO song (name, artist, album) VALUES (?,?,?)')
    # values from the input field gets inserted to the corresponding data
    cur.execute(sql, (request.form['name'], request.form['artist'],
                request.form['album']))
    conn.commit()
    # after requesting and getting the user input the database will commit
    results = cur.fetchall()
    print(results)
    flash('Song submitted!')  # flashes the message onto the page
    return redirect("all_songs")


# delelte code


@app.route('/delete/<name>')
def delete_song(name):
    conn = sqlite3.connect("song.db")
    cur.execute("DELETE FROM song WHERE name = ?", (name,))
    # finds the name of the song and deletes it
    conn.commit()
    print("name")
    return redirect("/admin_all_songs")


# admin login system


password = "1234"  # password to access admin
typed = False  # password has not been typed yet


@app.route("/admin/login", methods=['GET', 'POST'])
def adminLogin():
    global password
    global typed
    if request.method == 'POST':
        formRequest = request.form['password']
        if formRequest == password:
            typed = True  # typed will equal true if password is correct
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
    global typed
    if typed == False:
        # if the user puts in the "admin_all_songs" link into the url bar,
        # the user will be redirected to the login page since
        # they haven't typed the correct password.
        return redirect("/admin/login")
    else:
        cur.execute('SELECT name, artist, album FROM song')
        # Gets the name, artist, and album from the song table
        # to get displayed onto the all songs page
        results = cur.fetchall()
        print(results)
        return render_template("admin_all_songs.html", results=results)


# Error handling

@app.errorhandler(404)
def error404(error):
    errorCode = 404
    app.logger.debug(errorCode)
    return render_template('errorpage.html', errorCode=errorCode)


if __name__ == "__main__":
    app.run(debug=True)
