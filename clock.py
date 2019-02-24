#!/usr/bin/python
# clock in and out. maybe comments too

import time
import datetime

dayTime = 0
startTime = 0
currentComment = ""
timePerTask = {}

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
    global dayTime
    # clock out of the current task
    if startTime == 0:
        print "Please clock in first"
        return
    if len(maybeComment) != 0:
        comment(maybeComment)

    endTime = time.localtime()
    print "Clocked out at " + time.strftime("%H:%M", endTime)
    timeSpent = datetime.timedelta(seconds = time.mktime(endTime)-time.mktime(startTime))
    print "Spent " + \
       str(timeSpent.seconds//3600) + ":" + str(timeSpent.seconds//60%60) +\
      " on " + currentComment
    dayTime += timeSpent.seconds
    timePerTask[currentComment] = timePerTask.get(currentComment, 0) + timeSpent.seconds
    startTime = 0
    currentComment = ""

def formatTime(seconds):
    return str(seconds//3600) + ":" + str(seconds//60%60)

def clockOutDay(ignoreComment):
    global dayTime
    if startTime != 0:
        clockOut(ignoreComment)
    print "For this day, total of " +  \
        str(dayTime//3600) + ":" + str(dayTime//60%60)
    for key, value in timePerTask.iteritems():
        print key + " : " + formatTime(value)
    print ""
    dayTime = 0
    

def comment(incComment):
    global currentComment
    # add a comment to the current task
    currentComment = " ".join(incComment)

def helpLine(ignoreComment):
    # add a comment to the current task
    print "  ci <comment> - check in with optional comment"
    print "  m  <comment> - add a comment, replacing an existing"
    print "  co <comment> - check out with optional comment"
    print "  coo          - check out for the day"
    print "  ?            - print this message"

options = {
    "ci" : clockIn,
    "co" : clockOut,
    "coo": clockOutDay,
    "m"  : comment,
    "?"  : helpLine,
}

def main():
    # Loop through
    keepGoing = True
    while (keepGoing):
        printState()
        userInput = raw_input("ci, co, coo, m, ? : ")
        inputList = userInput.split(" ")
        options.get(inputList[0], helpLine)(inputList[1:])
        

if __name__ == "__main__":
    import sys
    main()
