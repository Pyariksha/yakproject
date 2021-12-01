from flask import Flask, render_template, request, flash
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.secret_key = "labyak1"

@app.route("/hello")
def index():
    flash("What would you like to order?")
    return render_template("index.html")

@app.route("/input", methods=['GET', 'POST'])
def input():
    flash("Hi! Order for " + str(request.form["num_input"]) + " is received") 
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
