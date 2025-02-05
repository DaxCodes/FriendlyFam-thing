import sqlite3 as sql
import flask
from flask import *

app = Flask(__name__)
app.secret_key = "ajshdfuoahsdfusfdhfisf"

conn = sql.connect("friendlyfam.db")
cur = conn.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY, host VARCHAR(255), description VARCHAR(255), day VARCHAR(255), time VARCHAR(255), status VARCHAR(255))")
cur.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, username VARCHAR(255), password VARCHAR(255))")
conn.commit()
@app.route('/')
def index():
    if "username" in session:
        return redirect("/home")
    else:
        return render_template('index.html')

@app.route('/myevents')
def events():
    if "username" in session:
        usernamern = session["username"]
        myeventslol = cur.execute(f"SELECT * FROM events WHERE host='{usernamern}';").fetchall()
        return render_template("myevents.html", username=session["username"], list=myeventslol)
    else:
        return render_template('index.html')

@app.route('/add', methods=["POST", "GET"])
def addevent():
    if "username" in session:
        if request.method == "POST":
            newDesc = request.form["description"]
            newTime = request.form["time"]
            newDay = request.form["day"]
            usernamern = session["username"]
            cur.execute(f"INSERT INTO events (host, description, day, time, status) VALUES ('{usernamern}', '{newDesc}', '{newDay}', '{newTime}', 'Active');")
            conn.commit()
            
            return redirect("/home")
        else:
            return render_template("add.html", username=session["username"])
    else:
        return render_template('index.html')

@app.route('/update/<id>', methods=["POST", "GET"])
def editevent(id):
    if "username" in session:
        if request.method == "POST":
            usernamern = session["username"]
            newDesc = request.form["description"]
            newDay = request.form["day"]
            newTime = request.form["time"]
            newStatus = request.form["status"] # option thingy
            cur.execute(f"UPDATE events SET host = '{usernamern}',  description = '{newDesc}', day = '{newDay}', time = '{newTime}', status = '{newStatus}' WHERE id = {id};")
            conn.commit()
            
            #description VARCHAR(255), day VARCHAR(255), time VARCHAR(255), status VARCHAR(255))
            return redirect("/home")
        else:
            #newId = int(id)
            getEvent = cur.execute(f"SELECT * FROM events WHERE id={id};").fetchone()
            return render_template("edit.html", username=session["username"], event=getEvent)
    else:
        return render_template('index.html')

@app.route('/cancel/<id>', methods=["POST", "GET"])
def cancelEvent(id):
    if "username" in session:
        cur.execute(f"DELETE FROM events WHERE id={id};")
        conn.commit()

        #description VARCHAR(255), day VARCHAR(255), time VARCHAR(255), status VARCHAR(255))
        return redirect("/home")
    else:
        return render_template('index.html')
@app.route('/home')
def home():
    events = cur.execute(f"SELECT * FROM events").fetchall()
    return render_template('home.html', username=session["username"], list=events)

@app.route('/signup', methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        newUsername = request.form["username"]
        newPassword = request.form["password"]
        cur.execute(f"INSERT INTO users (username, password) VALUES ('{newUsername}', '{newPassword}');")
        conn.commit()
        return render_template('index.html')
    else:
        return render_template('signup.html')

@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        getUsername = request.form["username"]
        getPassword = request.form["password"]
        usr = cur.execute(f"SELECT * FROM users WHERE username='{getUsername}' AND password='{getPassword}';").fetchone()
        print(usr)
        try:
            if usr[1] == getUsername and usr[2] == getPassword:
                session['username'] = request.form["username"]
                
                return redirect("/home")
        except:
            print('incorrect credentials')


    else:
        return render_template('index.html')

@app.route('/logout')
def logout():
    session.pop('username', None)

    return render_template('index.html')

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=True)
