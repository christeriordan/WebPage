#Webpage

from appDB import *
from flask import Flask, render_template, request, redirect, url_for, session, g
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.debug = True
app.secret_key = 'some_secret'

DATABASE = "Webpage.db"

#Connection to the database

def get_db():
    if not hasattr(g, "_database"):
        g._database = sqlite3.connect(DATABASE)
    return g._database

@app.teardown_appcontext
def teardown_db(error):
    db = getattr(g, '_database',None)
    if db is not None:
        db.close()

# check if login credentials are valid

def valid_login(username,password):
    conn = get_db()

    hash = get_hash_for_login(conn, username)
    if hash != None:
        return check_password_hash(hash, password)
    return False

#Error messages
@app.route("/check_username")
def check_username():
    conn = get_db()
    username = request.args.get("username", None)
    user_check = get_user_by_name(conn, username)

    if user_check['userID'] == None:
        return "", 401
    else:
        return "Username is already in use", 200

@app.route("/check_password")
def check_password():
    password = request.args.get("password", None)

    if password:
        if len(password) < 4:
            return "Password needs to be atleast 4 characters long"
        else:
            return "",401

@app.route("/check_login")
def check_login():
    conn = get_db()
    username = request.args.get("username", None)
    user_check = get_user_by_name(conn, username)
    if user_check['userID'] != None:
        return "", 400
    else:
        return "Invalid username or password", 200

# Edit page
@app.route("/edit")
def edit():
    beer_ID = request.args.get("beerID",None)
    conn = get_db()
    beer = get_beer(conn, beer_ID)

    return render_template("edit.html", beer=beer)

@app.route("/update_beer")
def update_beer():
    conn = get_db()
    name = request.args.get("beer_name",None)
    style = request.args.get("beer_style",None)
    brewery_name = request.args.get("brewery_name",None)
    beerID = request.args.get("beerID",None)

    id = update_info(conn,name,style,brewery_name,beerID)
    if id == 0:
        return "",401
    else:
        return "", 200



# Delete page
@app.route("/delete")
def delete():
    beer_ID = request.args.get("beerID", None)
    conn = get_db()
    beer = get_beer(conn, beer_ID)

    return render_template("delete.html", beer = beer)

@app.route("/delete_beer")
def delete_beer():
    conn = get_db()
    beerID = request.args.get("beerID", None)
    delete = delete_beer_by_id(conn,beerID)

    if delete == 1:
        return "",200
    else:
        return "",401



#Register page



@app.route("/register", methods=["GET","POST"])
def register():

    username = request.args.get("user","").strip()
    if username == "":
        return render_template("register.html",username=session.get("username", None), role=session.get("role", None))
    if len(username) < 4:
        return render_template("register.html",username=session.get("username", None), role=session.get("role", None))

    pw = request.args.get("password","")
    if pw == "":
        return render_template("register.html",username=session.get("username", None), role=session.get("role", None))
    if len(pw) < 4:
        return render_template("register.html",username=session.get("username", None), role=session.get("role", None))
    hash = generate_password_hash(pw)

    conn = get_db()
    id = add_user(conn, username, hash)
    if id == -1:
        return render_template("login.html")

    return redirect(url_for("index"))

#Login page

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if valid_login(request.form["username"], request.form["password"]):
            conn = get_db()
            user = get_user_by_name(conn, request.form["username"])
            session["username"] = user["username"]
            session["role"] = user["role"]
            return redirect(url_for("index"))
        else:
            ""

    return render_template("login.html",username=session.get("username", None), role=session.get("role", None))

#Beer page

@app.route("/beer", methods=["GET","POST"])
def beer():
    db = get_db()
    cur = db.cursor()
    cur2 = db.cursor()
    try:
        beers = []
        breweries = []

        if request.method == "POST" and session.get("role",None) != None:
            beer_name = request.form["beerName"]
            if beer_name == "":
                return "error1"
            if beer_name in beers:
                return "Error 10"
            beer_style = request.form["style"]
            if beer_style == "":
                return "error2"
            beer_id = request.form["brewery"]
            print(beer_id)
            if beer_id == "":
                return "error3"
            breweryID = request.args.get("breweryID", None)


            conn = get_db()
            add_beer(conn,beer_name, beer_style, breweryID)


        cur.execute("SELECT beerID, beerName, Style FROM Beer")
        cur2.execute("SELECT breweryID, breweryName FROM Brewery")
        for (beerID, beerName, style) in cur:
            beers.append({
                "beerID" : beerID,
                "beerName" : beerName,
                "style" : style

            })

        for (breweryID, breweryName) in cur2:
            breweries.append({
                "breweryID" : breweryID,
                "breweryName" : breweryName
            })
        return render_template("beer.html",  username=session.get("username", None), role=session.get("role", None), beers = beers,breweries = breweries)
    except sqlite3.Error as err:
        return ("Error {}".format(err))
    finally:
        cur.close()

# Logout session

@app.route("/logout")
def logout():
    session.pop("username")
    session.pop("role")
    return render_template("index.html", username=session.get("username", None), role=session.get("role", None))

#Index page

@app.route("/")
def index():
        return render_template("index.html", username=session.get("username", None), role=session.get("role", None))


if __name__ == "__main__":
    app.run(port="10000")

