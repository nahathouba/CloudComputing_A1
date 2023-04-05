from flask import Flask, render_template, request
from Utils import tableExists, createLogInTable, createMusicTable

app = Flask(__name__)


isTableExist = tableExists('login')
if not isTableExist:
    # Create the login table and load the users
    createLogInTable()

isTableExist = tableExists('music')
if not isTableExist:
    # Create the music table and load the music
    createMusicTable()


@ app.route("/")
def index():
    return render_template("index.html")

# TODO: Create a route for /checkLogin


@ app.route("/checkLogin", methods=["POST"])
def checkLogin():
    email = request.form.get("email")


if __name__ == "__main__":
    app.run(debug=True)
