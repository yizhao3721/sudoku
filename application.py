import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from solve import solveDoku, validate_input
from helpers import apology, login_required


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///puzzles.db")


# basic home screen
@app.route("/", methods=["GET"])
@login_required
def index():
    # get a list of the different puzzles in collection that are under the user's ID
    myPuzzles = db.execute("SELECT puzzle_id, complete, puzzle_name, date, time FROM collection WHERE user_id = :user_id",
                        user_id=session["user_id"])
    # use them in a template that displays "completeness," name, and date/time created
    return render_template("index.html", puzzles=myPuzzles)


# allows the user to create sudoku puzzles from our interactive grid
@app.route("/create", methods=["GET", "POST"])
@login_required
def create():
    # return the blank grid page
    if request.method == "GET":
        return render_template("create.html")
    # else, store all the information and add the formalities of the puzzle tothe database
    else:
        # add a puzzle into the collection under the user's name
        add = db.execute("INSERT INTO collection (user_id, puzzle_name) VALUES (:user_id, :puzzle_name)",
                        user_id=session["user_id"], puzzle_name=request.form.get("puzzle_name"))
        # find the puzzle_id of the puzzle you just created (the id being currP)
        currP = db.execute("SELECT puzzle_id FROM collection WHERE user_id = :user_id",
                        user_id=session["user_id"])
        currP = currP[len(currP)-1]["puzzle_id"]
        # get the list of values inputted from the form
        for x in range(9):
            for y in range(9):
                value = request.form.get(str(x*9+y))
                # orig is True if the value is part of the puzzle itself, an "original" value
                orig = 1
                if not value:
                    # if there is no input, set value=0 and orig=False
                    value = 0
                    orig = 0
                # input all values along with their information into the grid database
                point = db.execute("INSERT INTO grid (puzzle_id, orig, value, row, col) VALUES (:puzzle_id, :orig, :value, :row, :col)",
                        puzzle_id=currP, orig=orig, value=value, row=x, col=y)
        #return to home screen
        return redirect("/")


# the solve page, which is where the user can solve their puzzles or the pre-loaded puzzles (as well as obtain a solution)
@app.route("/solve", methods=["GET", "POST"])
@login_required
def solve():
    if request.method == "GET":
        # get the id of the puzzle
        puzzle_id = int(request.args.get("puzzle_id"))
        # update the field "currPID" in users (it tells the id of the puzzle the user is currently working on)
        act = db.execute("UPDATE users SET currPID = :puzzle_id WHERE username = :username",
                        puzzle_id=puzzle_id, username=session["user_id"])
        # get all the values of the puzzle from the grid database and convert it into a 9x9 array
        myPuzzle = db.execute("SELECT * FROM grid WHERE puzzle_id = :puzzle_id", puzzle_id=puzzle_id)
        myPuzzle = convert(myPuzzle)
        name = (db.execute("SELECT puzzle_name FROM collection WHERE puzzle_id = :puzzle_id", puzzle_id=puzzle_id))[0]["puzzle_name"]
        return render_template("solve.html", puzzles=myPuzzle, name=name, congratz=False, puzzle_id=puzzle_id)
    else:
        # check the thingy
        puzzle_id = request.form.get("puzzle_id")
        name = (db.execute("SELECT puzzle_name FROM collection WHERE puzzle_id = :puzzle_id", puzzle_id=puzzle_id))[0]["puzzle_name"]
        req = request.form.get("choice")
        print(req=="check")
        if (req == "check" or req == "save"):
            # get the list from the form and update the database
            isEmpty = False
            for x in range(9):
                for y in range(9):
                    value = request.form.get(str(x*9+y))
                    if not value:
                        value = 0
                        isEmpty = True
                    print(value)
                    # updating the database
                    point = db.execute("UPDATE grid SET value = :value WHERE puzzle_id = :puzzle_id AND row = :row AND col = :col", value=value, puzzle_id=puzzle_id, row=x, col=y)

            # get the list from the database
            origPuzzle = db.execute("SELECT * FROM grid WHERE puzzle_id = :puzzle_id", puzzle_id=puzzle_id)
            # convert into a 9x9 list of dictionaries
            myPuzzle = convert(origPuzzle)
            purePuzzle = convertValues(origPuzzle, False)
            # if checking and the result is correct
            if req == "check" and validate_input(purePuzzle):
                # update the puzzle to be complete
                print(validate_input(purePuzzle))
                complete = db.execute("UPDATE collection SET complete = 1 WHERE puzzle_id = :puzzle_id", puzzle_id=puzzle_id)
                return render_template("solve.html", congratz=True, puzzles=myPuzzle, name=name, puzzle_id=puzzle_id)
            # elif you're checking and result is incorrect
            elif req == "check":
                return render_template("solve.html", error=True, message="Your solution does not work.", puzzles=myPuzzle, name=name, puzzle_id=puzzle_id)
            # else you're just saving
            else:
                return render_template("solve.html", puzzles=myPuzzle, name=name, puzzle_id=puzzle_id)
        # else you're trying to get the solution
        elif req == "solve":
            # redirect to /solved
            return redirect("/solved?puzzle_id="+str(puzzle_id))


# the route taken after the user presses the "solve" button on the Solve Page ("/solve")
@app.route("/solved", methods=["GET"])
@login_required
def solved():
    # obtains some commonly used variables like the puzzle_id and the name of the puzzle
    puzzle_id = request.args.get("puzzle_id")
    name = (db.execute("SELECT puzzle_name FROM collection WHERE puzzle_id = :puzzle_id", puzzle_id=puzzle_id))[0]["puzzle_name"]
    # obtain a list of all the terms from the database
    myPuzzle = db.execute("SELECT * FROM grid WHERE puzzle_id = :puzzle_id", puzzle_id=puzzle_id)
    # and convert it into a 9x9 matrix of only the original values (we don't want user values changing our results)
    result = solveDoku(convertValues(myPuzzle, True))
    # if there is a result that is not false
    if result:
        # obtain the solved list and display it
        myPuzzle = result[1]
        return render_template("solved.html", lst=myPuzzle, name=name)
    # else, there is no solution and take them back to the "solve" page wiht an error message
    else:
        return render_template("solve.html", error=True, message="The puzzle ["+name+"] is unsolveable.", puzzles=convert(myPuzzle), name=name, puzzle_id=puzzle_id)


# logs the user in
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("login.html", error=True)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


# logs the user out
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
    rows = db.execute("SELECT username FROM users WHERE username=:username", username=request.args.get("username"))
    if len(rows) > 0:
        return jsonify(False)
    return jsonify(True)


# registers the user, making sure that the username is not taken
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        """Register user"""
        # get the username, password, and password confirmation from the form (sending errors if not correctly filled)
        name = request.form.get("username")
        if not name:
            return apology("Missing username!")
        pwd = request.form.get("password")
        pwd2 = request.form.get("confirmation")
        if not pwd or not pwd2:
            return apology("Missing password/password confirmation!")
        elif pwd != pwd2:
            return apology("Passwords don't match!")

        # make sure password has at least one number and at least one letter
        letters, numbers = 0, 0
        for character in request.form.get("password"):
            if character.isalpha():
                letters += 1
            if character.isdigit():
                numbers += 1
        if letters == 0 or numbers == 0:
            return apology("Password must have at least one letter and one number")

        # add the user to the users database
        result = db.execute("INSERT INTO users (username, hash) VALUES (:username, :password)",
                            username=request.form.get("username"), password=generate_password_hash(
                                request.form.get("password"), method='pbkdf2:sha256', salt_length=8))
        if not result:
            return apology("Username already exists.")

        # obtain the user_id of the user you just added and save it
        user_id = db.execute("SELECT id FROM users WHERE username = :username", username=request.form.get("username"))
        session["user_id"] = user_id[0]["id"]

        # make copies of the three sample puzzles under the user's name (where the sample puzzles are puzzle_id 1:3 and under user_id=0)
        # first get a list of the puzzles from the collection where user_id = 0
        sampleList = db.execute("SELECT * FROM collection WHERE user_id = 0")
        for sample in sampleList:
            # get the sample puzzle's puzzle_id
            oldP = sample["puzzle_id"]
            # first add a new puzzle into the collection database under our user's user_id and store that new puzzle_id as currP
            add = db.execute("INSERT INTO collection (user_id, puzzle_name) VALUES (:user_id, :puzzle_name)",
                            user_id=session["user_id"], puzzle_name=sample["puzzle_name"])
            currP = db.execute("SELECT puzzle_id FROM collection WHERE user_id = :user_id",
                            user_id=session["user_id"])
            currP = currP[len(currP)-1]["puzzle_id"]

            # obtain all the cells from the grid database where the puzzle_id is the same as the sample one's
            myPuzzle = db.execute("SELECT * FROM grid WHERE puzzle_id = :puzzle_id", puzzle_id=oldP)
            # convert into a 9x9 array of dictionaries
            myPuzzle = convert(myPuzzle)
            # make a copy of that puzzle and store all values into the grid database but under the new puzzle_id
            for x in range(9):
                for y in range(9):
                    value = myPuzzle[x][y]["value"]
                    orig = myPuzzle[x][y]["orig"]
                    point = db.execute("INSERT INTO grid (puzzle_id, orig, value, row, col) VALUES (:puzzle_id, :orig, :value, :row, :col)",
                                    puzzle_id=currP, orig=orig, value=value, row=x, col=y)
        # lead them to the home page
        return redirect("/")


# changes the password
@app.route("/change", methods=["GET", "POST"])
@login_required
def change():
    """Change password."""
    if request.method == "GET":
        return render_template("change.html")
    else:
        # get the two passwords from the form and check if they are filled and are equal
        pwd = request.form.get("password")
        pwd2 = request.form.get("confirmation")
        if not pwd or not pwd2:
            return apology("Missing password/password confirmation!")
        elif pwd != pwd2:
            return apology("Passwords don't match!")
        db.execute("UPDATE users SET hash = :password WHERE id = :user_id", password=generate_password_hash(
            request.form.get("password"), method='pbkdf2:sha256', salt_length=8), user_id=session["user_id"])
        return redirect("/")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

# converts a list of dictionaries into a 9x9 list of dictionaries
def convert(lst):
    # lst = each cell in lst has cell["orig"] cell["row"] cell["col"] cell["value"] cell["puzzle_id"] #
    result = []
    temp = []
    for cell in lst:
        temp.append(cell)
        # end the temp list and create a new one every 9 values added
        if (cell["col"] == 8):
            result.append(temp)
            temp = []
    return result


# does much the same as convert() except that 1) it returns a 9x9 array of values only and
# 2) if keepO = True, then it only takes values where orig = True, and sets value = 0 otherwise, else if keepO = False, keep everything
def convertValues(lst, keepO):
    # lst = each cell in lst has cell["orig"] cell["row"] cell["col"] cell["value"] cell["puzzle_id"]
    result = []
    temp = []
    for cell in lst:
        value = cell["value"]
        orig = cell["orig"]
        # when keepO is true, only add the value if it is original value
        if keepO and not orig:
            temp.append(0)
        # else, either keepO is false, or it's the original value, in either case, add the value to the list
        else:
            temp.append(cell["value"])
        # every 9 values added, end the temp list and begin a new one to build a 9x9 array
        if (cell["col"] == 8):
            result.append(temp)
            temp = []
    return result