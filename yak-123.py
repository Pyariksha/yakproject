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
from app import index

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
#start = datetime(2021,11,16)
day = 14
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

#restore T to x
T=x

#print out desired output
pd.options.mode.chained_assignment = None  # default='warn'
print_herd = herd_df[['name','age']]
print_herd['age'] = print_herd['age'].astype(str) + ' years old'
print_herd = print_herd.to_string(header=False, index= False)

print('In stock:')
print(' ' + str(milk) + ' litres of milk')
print(' ' + str(skins) + ' skins of wool')

print('Herd:')
print(herd_df)

#create a totals dictionary for desired output format
totals = {}
for variable in ["milk", "skins"]:
    totals[variable] = eval(variable)

#only select necessary herd_df columns
herd_df_get = herd_df[['name', 'age', 'sex']]

#create a class for GET requests for stock
class Stock(Resource):
    def get(self):
        data = totals
        return{'data': data}, 200

#create a class for GET requests for herd
api.add_resource(Stock, f'/yak-shop/stock/{T}')

class Herd(Resource):
    def get(self):
        data = herd_df_get
        data = data.to_dict()
        return{'data': data}, 200

#api.com/herd
api.add_resource(Herd, f'/yak-shop/herd/{T}')

#create a orders data
orderdata = {'customer':[],
        'milk':[],
        'skins': []}

order_df = pd.DataFrame(orderdata)
order_df['customer'].astype(str)
order_df['milk'].astype(int)
order_df['skins'].astype(int)
print(order_df)

class Post(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('customer', required=True) #create args
        parser.add_argument('milk', required=True, type = int)
        parser.add_argument('skins', required=True, type = int)
        args = parser.parse_args()  # parse arguments to dictionary
        #test in insomnia
        #return {
           #'cust': args['customer'],
          # 'milk': args['milk'],
          # 'skins': args['skins']
        #}, 200

        if args['milk'] > int(milk) and args['skins'] <= int(skins): #requirements
            return{
            'customer': args['customer'],
            'skins': args['skins']}, 206

        elif args['milk'] > int(milk) and args['skins'] > int(skins): #requirements
            return{
                'message': "404 not found - not in stock"
            }, 404
        else:
            return{
            'customer': args['customer'],
            'milk': args['milk'],
            'skins': args['skins']}, 201

#api.com/herd
api.add_resource(Post, f'/yak-shop/order/{T}')
    
if __name__ == "__main__":
    app.run(debug=True)
    