class Task():
    def __init__(self,id=None, dic=None):
        if dic == None:
            self.id = id
            self.list_id = None
            self.text = ""
            self.completed = False
        else:
            self.id = dic["id"]
            self.list_id = dic["list_id"]
            self.text = dic["text"]
            self.completed = bool(dic["completed"])

    def taskToDict(self):
        dic = {}
        dic["id"] = self.id
        dic["list_id"] = self.list_id
        dic["text"] = self.text
        dic["completed"] = self.completed
        return dic


class TodoList():
    # only one of title or dic can be None
    # otherwise how will it know which is which?

    def __init__(self, id, title, dic=None):
        if dic == None:
            self.id = id
            self.title = title
            self.tasks = []

        else:
            self.id = dic["id"]
            self.title = dic["title"]
            self.tasks = dic["tasks"]


    def addTask(self, task):
        for t in self.tasks:
            if t.id == task.id:
                return None

        task.list_id = self.id
        self.tasks.append(task)

    def removeTaskWithId(self, taskId):
        for t in self.tasks:
            if taskId == t.id:
                self.tasks.remove(t)

    def getTaskWithId(self, id):
        for t in self.tasks:
            if t.id == id:
                return t


    def listAllTasks(self):
        return self.tasks

    def removeAllTasks(self):
        self.tasks = []

    # def allTasksToDict(tasks):
    #     taskArray = []
    #     for t in self.tasks:
    #         taskArray.append(t.taskToDict())
    #     return taskArray

    def allTasksFromJson(self, arrayOfJson):
        for a in arrayOfJson:
            self.tasks.append(Task(None,a))


    def toDict(self):
        dic = {}
        dic["id"] = self.id
        dic["title"] = self.title
        taskArray = []
        for t in self.tasks:
            newTaskDic = t.taskToDict()
            taskArray.append(newTaskDic)
        dic["tasks"] = taskArray
        return dic
