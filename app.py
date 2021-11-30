from flask import Flask, render_template, request, flash

app = Flask(__name__)

@app.route("/hello")
def index():
    flash("What would you like to order?")
    return render_template("index.html")

@app.route("/input", methods = ['POST', 'GET'])
def input():
    flash("Hi! Order for" + str(request.form['num_input']) + "is received") 
    return render_template("index.html")

if __name__ == "__main__":
    app.run()
