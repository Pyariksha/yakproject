from typing_extensions import Required
from flask import Flask, render_template, request, flash
from flask_cors import CORS
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast
import xml.etree.ElementTree as et 
import numpy as np
from datetime import timedelta, datetime
from flask_cors import CORS
#from app import index

#get input xml
users_path = r'C:\Users\pya.tiluk\yakproject\inputherd.xml'

#parse input xml
xtree = et.parse(users_path)
xroot = xtree.getroot()

df_cols = ["name", "age", "sex"]
rows = []

for child in xroot:
    name = child.attrib.get("name")
    age = child.attrib.get('age')
    sex = child.attrib.get('sex')

    rows.append({"name": name, "age": age, 
                 "sex": sex})

#save to herd_df
herd_df = pd.DataFrame(rows, columns = df_cols)

#get age as days and add as column
herd_df["age"] = herd_df["age"].astype(float)
herd_df['age_days'] = herd_df["age"]*100

#define start of project (testing for 13 days)
now = datetime.now()
day = 13
delta = now - timedelta(day)
start = delta

#set integer for days as T
x = now - start
x= x.days 
x = int(x)
T=x

#calculate product totals for milk and skins
def get_totals(T):
    global skins
    global milk

    herd_df['age'] = round(herd_df['age'] + (T*0.01), 2)

    for n in herd_df['age_days']:
        milk = round(T * (50 - ((herd_df['age_days'])*0.03)), 2)
        herd_df['milk'] = milk
        milk = herd_df['milk'].sum()

    for n in herd_df['age_days']:
        if  n < 1000:
            if T%13 == 0:
                shaved = T/13 * 1
                herd_df['skins'] = shaved
                skins = herd_df['skins'].sum()
            elif (T - 13) < 13:
                T = T - (T-13)
                shaved = T/13 * 1
                herd_df['skins'] = shaved
                skins = herd_df['skins'].sum()

get_totals(T)

app = Flask(__name__)
CORS(app)

app.secret_key = "labyak1"

@app.route("/hello")
def index():
    flash("Hi! Or should we say Mooo?? What would you like to order?")
    return render_template("index.html")

@app.route("/reply", methods=['GET', 'POST'])
def reply():
   #milk = 20
    #skins = 10
    if int(request.form['1_input']) > milk and int(request.form['2_input'])<= skins:
        flash("Partial order available - milk not in stock but " + str(request.form['2_input']) + " skins ordered")
    elif int(request.form['1_input']) <= milk and int(request.form['2_input']) > skins:
        flash("Partial order available - skins not in stock but " + str(request.form['1_input']) + " litres of milk ordered")
    elif int(request.form['1_input']) > milk and int(request.form['2_input']) > skins:
        flash("Requested milk and skins not in stock")
    else:
        flash("Order for " + str(request.form['1_input']) + " litres of milk "  + " and " + str(request.form['2_input']) + " skins " + " is successful") 
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
