import numpy as np
import matplotlib.pyplot as plt
import random
import math
import json


# Monte Carlo Method

class Person:
    def __init__(self, number, isInAction):
        self.number = number
        self.isInAction = isInAction
        self.row = math.ceil(number/4)
        self.seat = number-self.row*4+4
        self.seated = False
        self.timer = 0
        self.color = list(np.random.choice(range(256), size=3))
        if(self.number < 10):
            self.numberForJson = "00" + str(self.number)
        elif(self.number<100):
            self.numberForJson = "0" + str(self.number)
        else:
            self.numberForJson = str(self.number)
        
        # because the seat rows have a distance of 1m
        self.rowInPlane = self.row+self.row-1
        if(number == -1):
            self.seat = -1
            self.row = -1
            self.rowInPlane = -1
            self.color = [0, 0, 0]
            self.numberForJson = "000"

    def setIsInAction(self, boolean):
        self.isInAction = boolean

    def setSeated(self, seated):
        self.seated = seated

    def setTimer(self, timer):
        self.timer = timer

    def getTimer(self):
        return self.timer


# create Array
# space consumed by single components in 0,5m:
queue = 100
gateToPlane = 50
rowsInPlane = 50

queue = [Person(-1, False)]*(queue+gateToPlane+rowsInPlane)
#queue = [Person(-1,False)]*4
# create People / numbers from 1 to 100

numbers1To100 = [0]*100
for i in range(100):
    numbers1To100[i] = i+1

random.shuffle(numbers1To100)

for i in range(100):
    queue[i] = Person(numbers1To100[i], False)
# queue[0]=Person(1,False)
# queue[1]=Person(5,False)

# create Rows
rows = ["OOOO"]*25


# output for json
fiveRowsWithPersons = [[] for i in range(200)]
# initialize
for i in range(200):
    test = fiveRowsWithPersons[i]
    for j in range(5):
        test.append(Person(-1, False))


def updateJsonOutput():
    for i in range(200):
        fiveRowsWithPersons[i][2] = queue[i]


updateJsonOutput()

# create Functions
global time
time = 0


def startingPosition():
    global time
    time = 0
    for i in range(len(rows)):
        rows[i] = "OOOO"
    random.shuffle(numbers1To100)
    for i in range(100):
        queue[i] = Person(numbers1To100[i], False)


# checks whether the person can move 0.5m forward
def stepIsPossible(i):
    if(i < len(queue)-1 and queue[i+1].number == -1 and queue[i].isInAction == False):
        return True
    else:
        return False

# checks whether the person, sitting at the window has to change with a person, already sitting on the aisle seat
def seatInterference(person):
    seat = person.seat
    row = person.row-1
    if(seat == 2 or seat == 3):
        return False
    # Window Seat left
    elif seat == 1:
        aisleSeat = rows[row][1]
        if(aisleSeat == "X"):
            return True
        else:
            return False
    # Window Seat right
    elif seat == 4:
        aisleSeat = rows[row][3]
        if(aisleSeat == "X"):
            return True
        else:
            return False

# The person puts their luggage into the storage and sits down, possible seat interference also considered


def sitDown(i):  # put luggage into storage takes 30s
    person = queue[i]
    # put luggage in storage
    # first second in the row
    if(person.seated == False):
        # Seat Interference takes 15s
        if(seatInterference(person)):
            person.setTimer(45)
        else:
            person.setTimer(30)
        person.setSeated(True)
        person.setIsInAction(True)
    # all other seconds
    elif(person.seated == True):
        person.setTimer(person.getTimer()-1)
    # person has finished with luggage and seat Interference
    if(person.getTimer() == 0):
        person.setIsInAction(False)
        # set the seat to be occupied
        stringIndex = person.seat-1
        rows[person.row-1] = rows[person.row-1][:stringIndex] + \
            "X" + rows[person.row-1][stringIndex+1:]
        # print(rows[person.row-1])
        queue[i] = Person(-1, False)

        # fill new array Not necessary for the exercise
        newPersonSeat = -1
        if(person.seat < 3):
            newPersonSeat = person.seat-1
        else:
            newPersonSeat = person.seat
        fiveRowsWithPersons[200-person.rowInPlane][newPersonSeat] = person

#json output data
everyStep =[]

# Simulates one second
def oneStep():
    global time
    temporaryArray = queue
    for j in range(len(queue)):
        # i goes from the end to the beginning of the array
        i = len(queue)-j-1
        # if we have a person
        if(queue[i].number != -1):
            # if person is in the right row
            if(queue[i].rowInPlane == j+1):  # row between 1 and 25
                sitDown(i)
            # if person can move
            if(stepIsPossible(i)):
                # move Person to new location
                queue[i+1] = temporaryArray[i]
                # delete Person from old location
                queue[i] = Person(-1, False)
    time = time + 1
    # not necessary for the exercise
    updateJsonOutput()

    jsonString = [""]*200
    for i in range(200):
        jsonString[i] = fiveRowsWithPersons[i][0].numberForJson + fiveRowsWithPersons[i][1].numberForJson + fiveRowsWithPersons[i][2].numberForJson + fiveRowsWithPersons[i][3].numberForJson + fiveRowsWithPersons[i][4].numberForJson
    
    everyStep.append(jsonString)
    

    


# checks wheter all people have boarded successfully
def isNotFinished():
    for i in rows:
        if(i != "XXXX"):
            return True
    return False


boardingTries = 1
output = [0]*boardingTries

# Simulate until everyone has boarded successfully and tells the time


def simulate(boardingTries):
    for i in range(boardingTries):
        global time
        startingPosition()
        while isNotFinished():
            oneStep()
        output[i] = time
    print(output)


simulate(boardingTries)

mean = np.mean(output)
std = np.std(output)

# print(output)
# print("mean: ", mean)
# print("std: ", std)

plt.hist(output, bins=50, label="Histogram", density=True)

plt.title("Times of Boarding an Embraer E190 / 100tries")
plt.ylabel("Percentage")
plt.xlabel("Time in s")

plt.legend(loc='upper right')
# plt.show()

#color = list(np.random.choice(range(256), size=3))


# export to json
data = {"everyStep":everyStep}
with open("./output2.json", "w") as f:
    json.dump(data, f)

#for i in range(200):
    #print(fiveRowsWithPersons[i][0].number, " ", fiveRowsWithPersons[i][1].number, " ", fiveRowsWithPersons[i][2].number, " ", fiveRowsWithPersons[i][3].number, " ", fiveRowsWithPersons[i][4].number)



#print(everyStep)
# print(cedric is very cool yes i want a good grade)
# for i in queue:
#   print(i.color)
