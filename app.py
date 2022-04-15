from flask import Flask, jsonify, request
from flask import render_template
import time
from pymongo import MongoClient
import pymongo
import json

app = Flask(__name__)

def get_mongo_database():
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = "mongodb+srv://mongo:Rahin2702@cluster0.8uh2v.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(CONNECTION_STRING)

    # Create the database for our example (we swill use the same database throughout the tutorial
    return client["final_project"]["final_project"]


def get_all_data():
    get_client = get_mongo_database()
    get_data = get_client.find({})
    return get_data

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/barGraph')
def barGraph():
    data = get_all_data()
    Positive=0
    VPositive=0
    Mixed=0
    Other=0
    for i in data:
        if (i["steamRatingText"] == "Mostly Positive"):
            Positive += 1
        elif (i["steamRatingText"] == "Very Positive"):
            VPositive += 1
        elif (i["steamRatingText"] == "Mixed"):
            Mixed += 1
        else:
            Other += 1
    labels = ["Very Positive","Positive","Mixed","Others"]
    values = [VPositive,Positive,Mixed,Other]
    return render_template("barGraph.html",labels=labels,values=values)


@app.route('/pieChart')
def pieChart():
    data = get_all_data()
    title = []
    values = []
    for i in data:
        title.append(i["title"])
        values.append(i["salePrice"])
    return render_template("pieChart.html",labels=title,values=values)
    

@app.route('/lineChart')
def lineChart():
    data = get_all_data()
    labels=[]
    salePrice=[]
    normalPrice=[]
    for i in data:
        labels.append(i["title"])
        salePrice.append(i["salePrice"])
        normalPrice.append(i["normalPrice"])
    return render_template("lineGraph.html",labels=labels,salePrice=salePrice,normalPrice=normalPrice)

# BONUS
@app.route('/getAll', methods=['GET'])
def get_item_by_id():
    data = get_all_data()
    response = []
    for document in data:
        document['_id'] = str(document['_id'])
        response.append(document)
    return json.dumps(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
