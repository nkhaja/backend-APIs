import bcrypt
from remindersAPI_classes import Task, TodoList
from flask import Flask, request, jsonify, json
from flask_pymongo import PyMongo
from pymongo import MongoClient
from bson import ObjectId

#Todo:
## makes all names consistent, camel or underscores
## Setup Auth, getting relevant lists or tasks with auth

# dbSetup
client = MongoClient()
db = client.database

allLists = db.lists
allTasks = db.tasks
allUsers = db.users

#used when operation is on object itself
# ie. use selfId when looking for a lists' id
# but use list_id when looking for task associated with that list
# MongoDb automatically inserts an ID into each uploaded object

selfId = '_id'

#user
name = 'name'
password = 'password'
phone_number = 'phone_number'

#list
title = 'title'
user_id = 'user_id' #task
secure_id = "secure_id"

#task
list_id = 'list_id'
completed = 'completed'
due_date = 'due_date'
text = 'text'

## Errors

te400 = {"error": "400 -- Error, you are missing a _id, user_id, list_id or text field"}
te404 = {'error':'404 -- No task with given id found, or no id given'}
te409 = {"error": "409 -- there is already a task stored with this id"}
le400 = {"error": "400 -- Error, you are missing a _id, user_id, or title field"}
le404 = {'error':'404 -- No list with given id found, or no list given'}
le409 = {"error": "409 -- there is already a list stored with this name"}
ue400 = {"error": "400 -- Error, you are missing an _id, phone_number, or name"}
ue404 = {'error':'404 -- No user with given id found, or no user given'}
ue409 = {"error": "409 -- there is already a user with this name"}
authError = {"error" : "Your credentials do not match any stored in the database"}


app = Flask(__name__)


##authenticated

def authenticated(request_headers):
    someUserId = request.headers['uid']
    password = request.headers['password'].encode('utf-8')
    someUser = allUsers.find_one({selfId:ObjectId(someUserId)})
    if someUser:
        hashed_pw = someUser[secure_id].encode('utf-8')
        if bcrypt.hashpw(password, hashed_pw) == hashed_pw:
            return True
    return False

### TASK FUNCTIONS
def getTasksForUser(someUserId):
    allTasksArray = list(allTasks.find({user_id:someUserId}))
    return allTasksArray

def getTasksForList(someListId):
    tasks = allTasks.find({list_id:someListId})
    if tasks:
        return list(tasks)
    else:
        return []

def getTaskWithId(someTaskId):
    task = allTasks.find_one({selfId:ObjectId(someTaskId)})
    if task:
        return task
    else:
        return te404

def deleteTask(someTaskId):
    task = allTasks.find_one({selfId:ObjectId(someTaskId)})
    allTasks.delete_one({selfId:ObjectId(someTaskId)})
    if task:
        return task
    else:
        return te404

def addTask(taskDic):
    if allTasks.find_one({selfId:ObjectId(taskDic[selfId])}) == None:
        return allTasks.insert_one(taskDic).inserted_id
    else:
        raise ValueError

def updateTask(task_id, newTask):
    task = allTasks.find_one({selfId:ObjectId(someTaskId)})
    if task:
        allTasks.update_one({selfId:someTaskId}, {'$set':newTask})
        return task
    else:
        return te404

def validTaskDic(taskDic):
    try:
        id = tasksDic[selfId]
        uid = taskDic[user_id]
        lid = taskDic[list_id]
        text = taskDic[text]
        dueDate = task[due_date]
        # due_date is an optional field
    except:
        raise ValueError



### LIST FUNCTIONS


def addList(listDic):
    exists = allLists.find_one({name:listDic['title']})
    try:
        someId = listDic[selfId]
    except:
        if exists == None:
            return str(allLists.insert_one(listDic).inserted_id)
        else:
            raise ValueError
    raise ValueError


def deletList(someListId, someUserId):
    checkForList = allLists.find_one({selfId:ObjectId(someListId)})
    if checkForList:
        allLists.delete_one({list_id:someListId})
        allTasks.delete({list_id:someListId, user_id:someUserId})
        return checkForList
    else:
        return le404

def updateListWithId(someListId, updatedList):
    checkForList = allLists.find_one({selfId:ObjectId(someListId)})
    if checkForList:
        allLists.update_one({selfId:someListId}, {'$set':updatedList})
        return updatedList
    else:
        return le404


def getListsForUser(someUserId):
    lists = list(allLists.find({user_id:someUserId}))

    for l in lists:
        l['tasks'] = getTasksForList(l[selfId])
    return lists

def getListWithId(someListId):
    someList = allLists.find({selfId:someListId})
    if someList:
        return someList
    else:
        return le404

def getAllListNames(someUserId):
    one = allLists.find_one({user_id:ObjectId(someUserId)})
    print(one)
    everything = allLists.find({user_id:someUserId},{title: 1})
    print list(everything)
    output = []
    for i in everything:
        print('entered the loop')
        output.append(i[title])
    else:
        return output

def validListDic(listDic, new_list):
    try:
        someTitle = listDic[title]
        uid = listDic[user_id]
        print('uid settled')
        if new_list:
            print('checking for id')
            id = listDic[selfId]
        print('returning')
        return
    except:
        print('reading error')
        return KeyError


### USER FUNCTIONS
def getTasksForUser(someUserId):
    tasks = list(allTasks.find({user_id:someUserId}))
    if tasks:
        return tasks
    else:
        return []


def createUser(userDic):

    unhashed_pw = userDic[secure_id].encode('utf-8')
    hashed_pw = bcrypt.hashpw(unhashed_pw, bcrypt.gensalt())
    if allUsers.find_one({name:userDic[name]}) == None:
        userDic[secure_id] = hashed_pw
        return str(allUsers.insert_one(userDic).inserted_id)
    else:
        raise ValueError

def getUserWithId(someUserId):
    user = allUsers.find_one({selfId:ObjectId(someUserId)})
    user[selfId] = str(user[selfId])
    if user:
        return user
    else:
        return ue404

def getUserWithName(someUserName):
    user = allUsers.find_one({selfId:ObjectId(someUserId)})
    if user:
        return user
    else:
        return ue404


def deleteUser(someUserId):
    exists = allUsers.find_one({selfId: ObjectId(someUserId)})
    if exists:
        allUsers.delete_one({selfId:ObjectId(someUserId)})
        allTasks.delete_many({user_id:someUserId})
        allLists.delete_many({user_id:someUserId})
        exists[selfId] = str(exists[selfId])

        return exists
    else:
        return ue404

# id in newUserDic must much someUserId
def updateUser(updatedUserDic):
    someUserId = updatedUserDic[selfId]
    someUser = allUsers.find_one({selfId:ObjectId(someUserId)})
    samePass = updatedUserDic[secure_id] == someUser[secure_id]
    if someUser and samePass:
        allUsers.update_one({selfId:ObjectId(someUserId)}, {'$set':updatedUserDic})
        return updatedUserDic
    else:
        return ue404

def validUserDic(userDic, new_user):
    try:
        if new_user:
            someSecureId = userDic[secure_id]
            userName = userDic[name]
            return
        else:

            secureId = userDic[password]
            userName = userDic[name]
            userid = userDic[selfId]
            return
        #Phone number is optional feature
    except:
        raise KeyError



#########

@app.route('/')
def index(item=None):
    if item == None:
        return "Welcome!"

### TASKS

#Look into how UID affects this process
@app.route('/tasks', methods = ['GET', 'POST'])
def manageAllTasks():

    if not authenticated(request.headers):
        return jsonify(authError)

    requestAsDic = request.form.to_dict()
    requestAsDic[completed] = False
    GET = request.method == 'GET'
    POST = request.method == 'POST'


    if GET:
        return jsonify(getTasksForUser(uid))

    elif POST:
        try:
            validTaskDic(requestAsDic)
            addedTaskId = addTask(requestAsDic)
            #user must update local object with this id
            return addedTaskId
        except KeyError:
            return jsonify(te400)
        except ValueError:
            return jsonify(te409)


@app.route('/tasks/<someTaskId>', methods = ['GET', 'DELETE'])
def manageSpecificTask(someTaskId=None):

    if not authenticated(request.headers):
        return jsonify(authError)

    GET = request.method == 'GET'
    DELETE = request.method == 'DELETE'

    if GET and someTaskId != None:
        return jsonify(getTaskWithId(someTaskId))

    elif DELETE and someTaskId != None:
        return jsonify(deleteTask(someTaskId))
    else:
        return jsonify(te404)


### LISTS
@app.route('/lists', methods = ['GET', 'POST'])
def manageAllLists():

    if not authenticated(request.headers):
        return jsonify(authError)

    requestAsDic = request.form.to_dict()
    uid = request.headers['uid']
    requestAsDic[user_id] = uid
    print(requestAsDic[user_id])


    GET = request.method == 'GET'
    POST = request.method == 'POST'

    if GET:
        return jsonify(getAllListNames(uid))

    elif POST:
        try:
            validListDic(requestAsDic, False)
            newListId = (addList(requestAsDic))
            return jsonify(newListId)
        except KeyError:
            print('getting this error')
            return jsonify(le400)
        except ValueError:
            return jsonify(le404)

@app.route('/lists/<someListId>', methods = ['GET', 'PUT', 'DELETE'])
def manageSpecificList(someListId=None):

    if not authenticated(request.headers):
        return jsonify(authError)

    requestAsDic = request.form.to_dict()
    GET = request.method == 'GET'
    PUT = request.method == 'PUT'
    DELETE = request.method == 'DELETE'

    uid = request.headers['uid']

    if GET and someListId:
        return jsonify(getListWithId(someListId))

    elif PUT and someListId:
        return jsonify(updateListWithId(someListId))

    elif DELETE and someListId:
        return deleteList(someListId,uid)

@app.route('/lists/<someListId>/tasks', methods = ['GET', 'POST'])
def manageTasksOfList(someListId):

    if not authenticated(request.headers):
        return jsonify(authError)

    requestAsDic = request.form.to_dict()
    requestAsDic[completed] = False
    GET = request.method == 'GET'
    POST = request.method == 'POST'

    if GET:
        #currently returns empty list if id doesn't match, change to error?
        return getTasksForList(someListId)

    elif POST:
        try:
            validTaskDic(requestAsDic)
            return jsonify(addTask(requestAsDic))
        except KeyError:
            return jsonify(te400)
        except ValueError:
            return jsonify(te409)

    return jsonfy ({'response:this request is not supported'})

## Todo Verify that this is a redundant route if all tasks have lists?
@app.route('/lists/<someListId>/tasks/<someTaskId>', methods = ['GET', 'PUT', 'DELETE'])
def manageSpecificTasksOfLists(someListId, someTaskId=None):
    if not authenticated(request.headers):
        return jsonify(authError)

    requestAsDic = request.form.to_dict()
    GET = request.method == 'GET'
    PUT = request.method == 'PUT'
    DELETE = request.method == 'DELETE'

    if someTaskId:

        if GET:
            return jsonify(getTaskWithId(someTaskId))

        elif PUT:
            try:
                validTaskDic(requestAsDic)
                return updateTask(someTaskId,requestAsDic)
            except KeyError:
                return jsonify(te400)

        elif DELETE:
            return jsonify(deleteTask(someTaskId))
    return


### USERS
@app.route('/users', methods = ['POST'])
def addUser():
    requestAsDic = request.form.to_dict()
    POST = request.method == 'POST'
    if  POST:
        try:
            validUserDic(requestAsDic, True)
            return jsonify(createUser(requestAsDic))
        except KeyError:
            return jsonify(ue400)
        except ValueError:
            return jsonify(ue409)

@app.route('/users/<someUserId>', methods = ['GET','PUT', 'DELETE'])
def manageUser(someUserId=None):

    requestAsDic = request.form.to_dict()
    GET = request.method == 'GET'
    PUT = request.method == 'PUT'
    DELETE = request.method == 'DELETE'

    if not authenticated(request.headers):
        return jsonify(authError)

    if someUserId:
        if GET:
            return jsonify(getUserWithId(someUserId))

        elif PUT:
            try:
                validUserDic(requestAsDic, False)
                return jsonify(updateUser(requestAsDic))
            except KeyError:
                return jsonify(ue400)

        elif DELETE:
            return jsonify(deleteUser(someUserId))



if __name__ == "__main__":
    app.run()
