from remindersAPI_classes import Task, TodoList

dic = {}
dic["id"] = "cheese"
dic["text"] = "tsldjflasdkjflkasdjf"
dic["list_id"] = "fsdf"
dic["completed"] = "True"

dic2 = {}
dic2["id"] = "cheese2"
dic2["text"] = "tsldjflasdkjflkasdjf"
dic2["list_id"] = "fsdf"
dic2["completed"] = "True"

dic3 = {}
dic3["id"] = "cheese2"
dic3["text"] = "tsldjflasdkjflkasdjf"
dic3["list_id"] = "fsdf"
dic3["completed"] = "True"

json = [dic, dic2, dic3]



def main():
    newTask = Task("cheese")
    newTask.text = "dkjhfkjadsfa"
    newTask.completed = True
    newTask.list_id = "kjkdsf"
    newDic = newTask.taskToDict()
    secondTask = Task(None, dic2)
    # print newTask.id
    # print secondTask.id
    # print secondTask.text
    # print secondTask.list_id
    # print secondTask.completed
    print newDic

    newList = TodoList("1","cool")
    print newList.title
    newList.addTask(newTask)
    print len(newList.tasks)
    newList.addTask(newTask)
    print len(newList.tasks)
    newList.addTask(secondTask)
    print len(newList.tasks)
    thirdTask = Task(None, dic3)
    newList.addTask(thirdTask)
    print len(newList.tasks)

    print "all tasks " , newList.listAllTasks()
    print  "task with id " , newList.getTaskWithId("cheese")
    newList.removeTaskWithId("cheese")
    print "all tasks removed cheese " , newList.listAllTasks()
    # print "all tasks to dic " , newList.allTasksToDict()
    print "toDict " , newList.toDict()
    newList.removeAllTasks()
    print "remove all tasks " , newList.listAllTasks()
    newList.allTasksFromJson(json)
    print newList.tasks

main()
