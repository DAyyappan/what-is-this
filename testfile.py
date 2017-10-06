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
        classList[student] = negatives

    return classList


# function that returns a matrix of students in groups
def assignSeats(classList, numGroups, groupSize):
    seatingChart = np.zeros((numGroups+1,groupSize+1))
    assigned = np.zeros(len(classList), dtype = bool)

    groupNum = 0
    seatNum = 1
    iterations = 0
    print ("empty seatching chart looks like this: " + str(seatingChart))

    for student in range(1, len(classList)):
        while True:
            n = np.random.random_integers(1, len(classList)-1)
            iterations += 1
            if (not assigned[n]):
                if(groupNum == numGroups):
                    seatNum += 1
                    groupNum = 1
                else:
                    groupNum += 1
                seatingChart[groupNum, seatNum] = n
                print ("Student %s assigned to group %d, seat %d. " % (n, groupNum, seatNum))
                assigned[n] = True
                break

    print ("%d iterations completed" % iterations)

    return seatingChart





print(str(assignSeats(populateNegatives(initializeClass(30)), 6, 5)))
