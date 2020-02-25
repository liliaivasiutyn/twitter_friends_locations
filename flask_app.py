from flask import Flask, render_template, request, url_for, redirect
import friends_location


app = Flask(__name__)


def before_request():
    app.jinja_env.cache = {}


app.before_request(before_request)


@app.route("/", methods=["GET", "POST"])
def index():
    print("INDEX")
    if request.method == "GET":
        print("GET")
        return render_template("main.html")

    if request.method == "POST":
        print("POST")
        try:
            friends_location.map_creation(request.form['contents'])
            return redirect(url_for('map'))
        except:
            return redirect(url_for('err'))


@app.route("/map", methods=["GET"])
def map():
    return render_template("Map.html")


@app.route("/err", methods=["GET"])
def err():
    return render_template("Error.html")
