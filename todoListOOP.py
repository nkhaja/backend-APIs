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

def getTasksForList(someListId, someUserId):
    tasks = allTasks.find({list_id:someListId, user_id:someUserId})
    if tasks:
        return list(tasks)
    else:
        return []

def getTaskWithId(someTaskId, someUserId):
    task = allTasks.find_one({selfId:ObjectId(someTaskId), user_id:someUserId})
    if task:
        print(task)
        task[selfId] = str(task[selfId])
        return task
    else:
        return te404

def deleteTask(someTaskId, someUserId):
    task = allTasks.find_one({selfId:ObjectId(someTaskId), user_id:someUserId})
    allTasks.delete_one({selfId:ObjectId(someTaskId)})
    if task:
        task[selfId] = str(task[selfId])
        return task
    else:
        return te404

def addTask(taskDic):
    try:
        someId = taskDic[selfId]
    except:
        return str(allTasks.insert_one(taskDic).inserted_id)
    raise ValueError


def updateTask(someTaskId, someUserId, newTask):
    task = allTasks.find_one({selfId:ObjectId(someTaskId), user_id:someUserId})
    #make sure user can't change objectID (screw themeselves)
    #newTask.pop(selfid) ## think about possibly re-introducing this
    if task:
        print task
        print('got inside task')
        allTasks.update_one({selfId:ObjectId(someTaskId)}, {'$set':newTask})
        #TODO protect against failed write on DB
        print('updated task')
        return newTask
    else:
        print('reading t404')
        return te404

def validTaskDic(taskDic, new_task):
    try:
        # if not new_task:
        #     print('task is not new')
        #     id = tasksDic[selfId]

        print('checking user id')
        uid = taskDic[user_id]
        print('checking list id')
        lid = taskDic[list_id]
        print('checking text')
        text = taskDic['text']
        print('returning from function')
        return
        # dueDate = task[due_date]
        # due_date is an optional field
    except:
        print('task not valid')
        raise ValueError




### LIST FUNCTIONS

def addList(listDic):
    try:
        someId = listDic[selfId]
    except:
        return str(allLists.insert_one(listDic).inserted_id)
    raise ValueError


def deleteList(someListId, someUserId):
    checkForList = allLists.find_one({selfId:ObjectId(someListId), user_id:someUserId})
    if checkForList:
        allLists.delete_one({selfId:ObjectId(someListId)})
        allTasks.delete_many({list_id:someListId, user_id:someUserId})
        checkForList[selfId] = str(checkForList[selfId])
        return checkForList
    else:
        return le404

def updateListWithId(someListId, someUserId,  updatedList):
    checkForList = allLists.find_one({selfId:ObjectId(someListId), user_id:someUserId})
    theList = allLists.find_one({selfId:ObjectId(someListId)})
    print(theList)
    if checkForList:
        print('list was found')
        allLists.update_one({selfId:ObjectId(someListId)}, {'$set':updatedList})
        print('returning with updated list')
        return updatedList
    else:
        return le404


def getListsForUser(someUserId):
    lists = list(allLists.find({user_id:someUserId}))
    id_as_string(lists)
    for l in lists:
        l['tasks'] = getTasksForList(l[selfId], someUserId)
    return lists

def getListWithId(someListId, someUserId):
    everyList = allLists.find({selfId:ObjectId(someListId),user_id:someUserId})

    if everyList:
        everyList = list(everyList)

        id_as_string(everyList)
        return everyList
    else:
        return le404

def getAllListNames(someUserId):
    everything = list(allLists.find({user_id:someUserId},{title: 1}))
    return [item['title'] for item in everything]


def validListDic(listDic, new_list):
    try:
        someTitle = listDic[title]
        uid = listDic[user_id]
        return
    except:
        return KeyError


### USER FUNCTIONS
def getTasksForUser(someUserId):
    tasks = list(allTasks.find({user_id:someUserId}))
    id_as_string(tasks)
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

def id_as_string(someList):
    for item in someList:
        item[selfId] = str(item[selfId])



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
    requestAsDic[user_id] = request.headers['uid']
    uid = request.headers['uid']

    GET = request.method == 'GET'
    POST = request.method == 'POST'


    if GET:
        return jsonify(getTasksForUser(uid))

    elif POST:
        try:
            validTaskDic(requestAsDic, True)
            addedTaskId = addTask(requestAsDic)
            #user must update local object with this id
            return jsonify(addedTaskId)
        except KeyError:
            return jsonify(te400)
        except ValueError:
            return jsonify(te409)

    return jsonify ({'response:this request is not supported'})



@app.route('/tasks/<someTaskId>', methods = ['GET', 'DELETE','PUT'])
def manageSpecificTask(someTaskId=None):

    if not authenticated(request.headers):
        return jsonify(authError)

    GET = request.method == 'GET'
    PUT = request.method == 'PUT'
    DELETE = request.method == 'DELETE'

    requestAsDic = request.form.to_dict()
    uid = request.headers['uid']


    if GET and someTaskId:
        return jsonify(getTaskWithId(someTaskId, uid))

    elif PUT and someTaskId:
        try:
            validTaskDic(requestAsDic, False)
            return jsonify(updateTask(someTaskId, uid, requestAsDic))
        except:
            print('reading outside error')
            return jsonify(te400)

    elif DELETE and someTaskId:
        return jsonify(deleteTask(someTaskId, uid))
    else:
        return jsonify(te404)

    return jsonify ({'response:this request is not supported'})

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

    return jsonify ({'response:this request is not supported'})


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
        return jsonify(getListWithId(someListId, uid))

    elif PUT and someListId:
        try:
            validListDic(requestAsDic, False)
            return jsonify(updateListWithId(someListId, uid, requestAsDic))
        except KeyError:
            return le400

    elif DELETE and someListId:
        return jsonify(deleteList(someListId,uid))

    return jsonify ({'response:this request is not supported'})


@app.route('/lists/<someListId>/tasks', methods = ['GET', 'POST'])
def manageTasksOfList(someListId):

    if not authenticated(request.headers):
        return jsonify(authError)

    requestAsDic = request.form.to_dict()
    requestAsDic[completed] = False
    uid = request.headers['uid']
    GET = request.method == 'GET'
    POST = request.method == 'POST'

    if GET:
        #currently returns empty list if id doesn't match, change to error?
        return jsonify(getTasksForList(someListId,uid))

    elif POST:
        try:
            validTaskDic(requestAsDic, True)
            return jsonify(addTask(requestAsDic))
        except KeyError:
            return jsonify(te400)
        except ValueError:
            return jsonify(te409)

    return jsonify ({'response: this request is not supported'})

## Todo Verify that this is a redundant route if all tasks have lists?
@app.route('/lists/<someListId>/tasks/<someTaskId>', methods = ['GET', 'PUT', 'DELETE'])
def manageSpecificTasksOfLists(someListId, someTaskId=None):
    if not authenticated(request.headers):
        return jsonify(authError)

    requestAsDic = request.form.to_dict()
    uid = request.headers['uid']
    GET = request.method == 'GET'
    PUT = request.method == 'PUT'
    DELETE = request.method == 'DELETE'

    if someTaskId:

        if GET:
            return jsonify(getTaskWithId(someTaskId, uid))

        elif PUT:
            try:
                validTaskDic(requestAsDic, False)
                print('got back from function')
                return jsonify(updateTask(someTaskId, uid, requestAsDic))
            except KeyError:
                return jsonify(te400)

        elif DELETE:
            return jsonify(deleteTask(someTaskId, uid))
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
