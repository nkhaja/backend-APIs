from flask import Flask, request, jsonify, json
from flask_pymongo import PyMongo
from pymongo import MongoClient

client = MongoClient()
db = client.database
collection = db.collection

app = Flask(__name__)
petDict = {}
@app.route('/hello')
@app.route("/hello/<name>")
def hello(name=None):
    if name != None:
        return 'Hello, ' + name + '!'

    return "Hello World!"


storage = []
@app.route("/pets", methods=['GET', 'POST'])
def storePets():
    dic = request.form.to_dict()
    result = request.form
    jsonResponse = jsonify(result)

    if request.method == 'POST':
        # args = request.args
        # print(args)
        # print(type(args))
        try:
            name = dic["name"]
            age = dic["age"]
            species = dic["species"]

        except KeyError:
            return jsonify({"error": "400 Error, you are missing one of name, age, or species"})


        for pet in storage:
            if pet["name"] == dic["name"]:
                return jsonify({"error": "409 -- there is already a pet stored with this name"})
            else:
                return jsonResponse

    else:
        return jsonify(storage)

    collection_id = collection.insert_one(dic).inserted_id
    storage.append(dic)
    db.collection_names(include_system_collections=False)
    print(collection.find_one())
    return jsonResponse




@app.route("/pets/<name>", methods=['GET', 'PUT'])
def findPet(name):

    for pet in storage:
        print pet["name"]
        if pet["name"] == name:
            return jsonify(pet)

    return jsonify({"error": "404 Pet not found"})


@app.route("/fizzbuzz", methods=['GET', 'POST'])
def fizzBuzz():
    num = int(request.args.get("q"))

    if num % 3 == 0 and num % 5 == 0 :
        return "fizz buzz"

    elif num % 3 == 0:
        return "fizz"

    elif num % 5 == 0:
        return "buzz"

    else:
        return "%s" % num


if __name__ == "__main__":
    app.run()
