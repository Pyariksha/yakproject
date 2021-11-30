from datetime import datetime
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

users_path = r'C:\Users\pya.tiluk\yakproject\inputherd.xml'

xtree = et.parse(users_path)
xroot = xtree.getroot()

xroot.tag
xroot.attrib

df_cols = ["name", "age", "sex"]
rows = []

for child in xroot:
    name = child.attrib.get("name")
    age = child.attrib.get('age')
    sex = child.attrib.get('sex')

    rows.append({"name": name, "age": age, 
                 "sex": sex})

herd_df = pd.DataFrame(rows, columns = df_cols)

#get age as days
herd_df["age"] = herd_df["age"].astype(float)
herd_df['age_days'] = herd_df["age"]*100
herd_df

#define start of project
now = datetime.now()
start = datetime(2021,11,17)
print(start)

#delta = start + timedelta(-26)
#print(delta)

#get integer for days as T
x = now - start
x= x.days 
x = int(x)
T=x
print(T)

#calculate product totals for milk and skins
def get_totals(T):
    global total_shaved
    global total_milk
    for n in herd_df['age_days']:
        milk = T * (50 - ((herd_df['age_days'])*0.03))
        herd_df['milk'] = milk
        total_milk = herd_df['milk'].sum()

    for n in herd_df['age_days']:
        if  n < 1000:
            if T%13 == 0:
                shaved = T/13 * 1
                herd_df['shaved'] = shaved
                total_shaved = herd_df['shaved'].sum()

get_totals(T)
herd_df 
print(total_milk)          
print(total_shaved)

herd_df = herd_df[['name', 'age', 'sex']]

#/herd
class Herd(Resource):
    def get(self):
        data = herd_df
        data = data.to_dict()
        return{'data': data}, 200

    def post(self):
        parser = reqparse.RequestParser()  # initialize

        parser.add_argument('name', required=True)  # add arguments
        parser.add_argument('age', required=True)
        parser.add_argument('sex', required=True)

        args = parser.parse_args()

        new_data = pd.DataFrame({
            'name': args['name'],
            'age': args['age'],
            'sex': args['sex']
        })

        data1 = pd.read_csv('')

#api.com/herd
api.add_resource(Herd, '/herd')

if __name__ == "__main__":
    app.run(debug=True)