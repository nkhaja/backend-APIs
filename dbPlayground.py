from flask import Flask, request, jsonify, json
from flask_pymongo import PyMongo
from pymongo import MongoClient
import bcrypt
from bson import ObjectId
# from bson.objectid import ObjectId


if __name__ == "__main__":
    client = MongoClient()
    db = client.database
    stuff = db.stuff

    stuff.insert_one({'name':'Nabil', 'age':23, 'id': "31232342"})
    stuff.insert_one({'name':'Snoop', 'age':25, 'id': "32423423"})
    stuff.insert_one({'name':'shoop', 'age': 55})

    # db = con.test_database
    # people = db.people
    # people.insert({'name':'Nabil', 'age':23})

    output = stuff.find_one()
    print output
    print dict(output)
    print output['age']
    print output['name']
    # print output['id']
    print output['_id']

for s in stuff.find():
    print s

print stuff.find_one({'name':"Nabil"})
print stuff.find_one({'name':"charlie"})
print stuff.find_one({'name':'shoop'})
print "BREAK"
print stuff.find_one({"_id": "5844edb53ef5cfa3336d3f6e"})
print stuff.find_one({"_id": ObjectId("5844edb53ef5cfa3336d3f6e")})

stuff.update_one({'name':"shoop"},{'$set':{'name':'jones', 'age':65}})
print stuff.find_one({'name':'shoop'})
print stuff.find_one({'name':'jones'})


password = "cheese"
hashed = bcrypt.hashpw(password, bcrypt.gensalt())

print hashed
hashed2 = bcrypt.hashpw(password, bcrypt.gensalt())
print hashed2
