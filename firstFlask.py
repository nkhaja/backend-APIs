from flask import Flask, request, jsonify, json

app = Flask(__name__)
petDict = {}

@app.route("/hello", methods=['GET', 'POST'])
def hello():
    return "Hello World!"


storage = []
@app.route("/pets", methods=['GET', 'POST'])
def storePets():
    dic = request.form.to_dict()
    result = request.form
    jsonResponse = jsonify(result)

    if request.method == 'POST':
        try:
            name = dic["name"]
            age = dic["age"]
            species = dic["species"]
            storage.append(dic)
        except KeyError:
            return jsonify({"error": "400 Error, you are missing one of name, age, or species"})

        return jsonResponse

    else:
        return jsonify(storage)

@app.route("/pets/<name>", methods=['GET'])
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
