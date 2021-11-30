from typing_extensions import Required
from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast
import xml.etree.ElementTree as et 
import numpy as np
from datetime import timedelta, datetime

#intitialize flask and api
app = Flask(__name__)
api = Api(app)

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
start = datetime(2021,11,17)

#set integer for days as T
x = now - start
x= x.days 
x = int(x)
T=x

#calculate product totals for milk and skins
def get_totals(T):
    global skins
    global milk

    herd_df['age'] = herd_df['age'] + (T*0.01)

    for n in herd_df['age_days']:
        milk = T * (50 - ((herd_df['age_days'])*0.03))
        herd_df['milk'] = milk
        milk = herd_df['milk'].sum()

    for n in herd_df['age_days']:
        if  n < 1000:
            if T%13 == 0:
                shaved = T/13 * 1
                herd_df['skins'] = shaved
                skins = herd_df['skins'].sum()

get_totals(T)

#create a totals nested dictionary for desired output format
totals = {}
for variable in ["milk", "skins"]:
    totals[variable] = eval(variable)

IDs = ['In Stock']
Defaults = totals
totals = dict.fromkeys(IDs, Defaults)

#only select necessary herd_df columns
herd_df = herd_df[['name', 'age', 'sex']]

#create a class for GET requests for input data to api
class Herd(Resource):
    def get(self):
        data = herd_df
        data = data.to_dict()
        IDs = ['Herd']
        Defaults = data
        data = dict.fromkeys(IDs, Defaults)
        data.update(totals)
        return{'data': data}, 200

#api.com/herd
api.add_resource(Herd, '/herd')

if __name__ == "__main__":
    app.run(debug=True)