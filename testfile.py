#Test python file

from bs4 import BeautifulSoup as bs
import numpy as np

# generate set of students
def initializeClass(classSize):
    # Each student is a dictionary with name, positive pairs, negative pairs
    studentInfo = [{'Name':'', 'PositivePairs':[], 'NegativePairs':[]} for x in range(classSize+1)]
    #print("Student Info shape = " + str(studentInfo.shape))

    return studentInfo

#populate class with 2 students each student shouldn't sit with
def populateStudentInfo(studentInfo, numPos = 2, numNeg = 1):

    s = 0
    i = 1
    for student in studentInfo:
        student['Name'] = "Student %d" % s
        negatives = np.random.random_integers(1, len(studentInfo)-1, numNeg)
        positives = np.random.random_integers(1, len(studentInfo)-1, numPos)
        while True:
            if (s in negatives) or (s in positives):
                negatives = np.random.random_integers(1, len(studentInfo)-1, numNeg)
                positives = np.random.random_integers(1, len(studentInfo)-1, numPos)
                i += 1
            else:
                student['NegativePairs'] = negatives
                student['PositivePairs'] = positives
                s += 1
                break

    return studentInfo


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


def testProgramComplete():
    classList, seatsAssigned = generateValidSeats(30, 6, 5)
    print("Classlist: ")
    print(str(classList))
    print("Seating Chart: ")
    print(str(seatsAssigned))

def testProgram():
    testClass = initializeClass(5)
    populatedClass = populateStudentInfo(testClass, 5, 2)

    for s in range(len(populatedClass)):
        print("Student %d works well with " % s + str(populatedClass[s]['PositivePairs']) + " but not well with " + str(populatedClass[s]['NegativePairs']))

testProgram()
