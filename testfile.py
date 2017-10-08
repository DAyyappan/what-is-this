#Test python file

from bs4 import BeautifulSoup as bs
import numpy as np

# generate set of students
def initializeClass(classSize):
    classIDs = np.zeros((classSize+1, 2))
    print("classIDs shape = " + str(classIDs.shape))

    return classIDs

#populate class with 2 students each student shouldn't sit with
def populateNegatives(classList, numNegs = 2):
    for student in range(len(classList)):
        negatives = np.random.random_integers(1, len(classList+1), numNegs)
        while True:
            if int(student) in negatives:
                negatives = np.random.random_integers(1, len(classList+1), numNegs)
            else:
                classList[student] = negatives
                break

    return classList


# function that returns a matrix of students in groups
def assignSeats(classList, numGroups, groupSize):
    seatingChart = np.zeros((numGroups,groupSize))
    assigned = np.zeros(len(classList), dtype = bool)

    groupNum = -1
    seatNum = 0
    iterations = 0
    #print ("empty seatching chart looks like this: " + str(seatingChart))

    for student in range(1, len(classList)):
        while True:
            n = np.random.random_integers(1, len(classList)-1)
            iterations += 1
            if (not assigned[n]):
                if(groupNum == (numGroups-1)):
                    seatNum += 1
                    groupNum = 0
                else:
                    groupNum += 1
                seatingChart[groupNum, seatNum] = n
                #print ("Student %s assigned to group %d, seat %d. " % (n, groupNum+1, seatNum+1))
                assigned[n] = True
                break

    #print ("%d iterations completed" % iterations)

    return seatingChart

#
def checkForConflicts(seatingChart, classList):
    for group in range(len(seatingChart)):
        for seat in range(len(seatingChart[0])):
            student = int(seatingChart[group][seat])
            #print("Checking student %d" % student)
            #print("Student %d shouldn't sit with " % student + str(classList[student]))
            for i in range(len(classList[student])):
                if classList[student][i] in seatingChart[group]:
                    #print("check for conflicts failed because student %d" % student + " can't sit with " + str(classList[student][i]) + "but their group is " + str(seatingChart[group]) )
                    return True

    return False

def generateValidSeats(classSize, numGroups, groupSize):
    testClass = initializeClass(classSize)
    print("class Initialized")

    negativesPopulated = populateNegatives(testClass)
    print("negatives populated")
    print(str(negativesPopulated))

    seatsAssigned = assignSeats(negativesPopulated, numGroups, groupSize)
    attempt = 0

    while True:
        if (checkForConflicts(seatsAssigned, negativesPopulated)):
            attempt += 1
            if (attempt % 100 == 0):
                print("Attempt no. %d failed" % attempt)
            seatsAssigned = assignSeats(negativesPopulated, numGroups, groupSize)
        else:
            print("Attempt no. %d succeeded! " % attempt)
            break

    return negativesPopulated, seatsAssigned


classList, seatsAssigned = generateValidSeats(30, 6, 5)
print("Classlist: ")
print(str(classList))
print("Seating Chart: ")
print(str(seatsAssigned))
