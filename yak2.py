from typing_extensions import Required
from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast
import xml.etree.ElementTree as et 

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

herd_df.head()

#/herd
class Herd(Resource):
    def get(self):
        data = herd_df
        data = data.to_dict()
        return{'data': data}, 200

#api.com/herd
api.add_resource(Herd, '/herd')

if __name__ == "__main__":
    app.run(debug=True)