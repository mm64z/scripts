#!/usr/bin/python
# clock in and out. maybe comments too

import time
import datetime

startTime = 0
currentComment = ""

def printState():
    if startTime == 0:
        print "You are currently clocked out"
    else:
        print "You are clocked in " + \
          ("on \"" + currentComment + "\"" if currentComment != "" else \
               "(please enter comment)")

def clockIn(incComment):
    # for real python
    global startTime
    # start a new current task
    if len(incComment) != 0:
        comment(incComment)
    startTime = time.localtime()
    print "Clocked in" + \
          (" on \"" + currentComment + "\"" if currentComment != "" else "" ) + \
          " at " + time.strftime("%H:%M", startTime)
    return startTime

def clockOut(maybeComment):
    global startTime
    global currentComment
    # clock out of the current task
    if len(maybeComment) != 0:
        comment(maybeComment)

    endTime = time.localtime()
    print "Clocked out at " + time.strftime("%H:%M", endTime)
    timeSpent = datetime.timedelta(seconds = time.mktime(endTime)-time.mktime(startTime))
    print "Spent " + \
       str(timeSpent.seconds//3600) + ":" + str(timeSpent.seconds//60%60) +\
      " on " + currentComment
    startTime = 0
    currentComment

def comment(incComment):
    global currentComment
    # add a comment to the current task
    currentComment = " ".join(incComment)

options = {
    "ci" : clockIn,
    "co" : clockOut,
    "m"  : comment,
}

def main():
    # Loop through
    keepGoing = True
    while (keepGoing):
        printState()
        userInput = raw_input("ci, co, m, ? : ")
        inputList = userInput.split(" ")
        options[inputList[0]](inputList[1:])
        

if __name__ == "__main__":
    import sys
    main()
