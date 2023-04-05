from flask import Flask, render_template, request
from CreateLoginTable import CreateLoginTable

aws_access_key_id = "ASIASEPGD37DX2M43UHA"
aws_secret_access_key = "WIWF9TlbzxDOeCa+tfkZ2Qghst0v6SgJe1VLebVa"
aws_session_token = "FwoGZXIvYXdzEDIaDH/OYLTkluz23QUO7iLNAd1kOELMaU5wR+oXClY6Y5Bc2vSmC19DvZq81H00Hf5jPebEWDG0pWQkXmaIOypyBI3JG1mNyTk8PZ+z6xFyA1uiZrmFnFSf2nnFqRpwkap9qAC/WyNRiJuzNT9dTt6ZLbrkF5DLXUNehRMuW/yOhsonWWaSXDF+2F4eghoLiY9wCGbyUu51zqpvVyyteMd+10CnVmb+SURwMKNIsuVUqTMayt48r49cm6kStuyMmbTBShM1WOvWEdG69pToOPW7MbzCDYCD+w/wKtEcLtwog/myoQYyLYDWUUzHSbRxpumU9jze0EXVBFeSUf2mycCeGK9AdF1AtsOdBEDoOBKYgbjiHw=="
region_name = "us-east-1"

app = Flask(__name__)

createLoginTable = CreateLoginTable(
    aws_access_key_id, aws_secret_access_key, aws_session_token, region_name)
createLoginTable.createTable()


@ app.route("/")
def index():
    return render_template("index.html")

# TODO: Create a route for /checkLogin


@ app.route("/checkLogin", methods=["POST"])
def checkLogin():
    email = request.form.get("email")


if __name__ == "__main__":
    app.run(debug=True)
