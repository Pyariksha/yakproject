from flask import Flask, render_template, request, flash
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.secret_key = "labyak1"

@app.route("/hello")
def index():
    flash("What would you like to order?")
    return render_template("index.html")

@app.route("/reply", methods=['GET', 'POST'])
def reply():
    flash("Hi! Order for " + str(request.form['1_input']) + " litres of milk is received") 
    flash("Hi! Order for " + str(request.form['2_input']) + " packs of skins is received") 
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
