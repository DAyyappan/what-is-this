#Test python file

from bs4 import BeautifulSoup as bs
import numpy as np

# generate set of students
def initializeClass(classSize):
    # Each student is a dictionary with name, positive pairs, negative pairs
    studentInfo = [{'Name':'', 'PositivePairs':[], 'NegativePairs':[]} for x in range(classSize)]

    return studentInfo

#populate class with 2 students each student shouldn't sit with
def populateStudentInfo(studentInfo, numPos = 2, numNeg = 1):

    s = 0
    for student in studentInfo:
        student['Name'] = "Student %d" % s
        negatives = np.random.random_integers(0, len(studentInfo)-1, numNeg)
        positives = np.random.random_integers(0, len(studentInfo)-1, numPos)
        while True:
            if (s in negatives) or (s in positives):
                negatives = np.random.random_integers(0, len(studentInfo)-1, numNeg)
                positives = np.random.random_integers(0, len(studentInfo)-1, numPos)
            else:
                student['NegativePairs'] = negatives
                student['PositivePairs'] = positives
                s += 1
                break

    return studentInfo


# function that returns a matrix of students in groups
def assignSeats(studentInfo, numGroups, groupSize):
    seatingChart = np.zeros((numGroups,groupSize))
    assigned = np.zeros(len(studentInfo), dtype = bool)

    groupNum = -1
    seatNum = 0
    iterations = 0

    for student in range(0, len(studentInfo)):
        while True:
            n = np.random.random_integers(0, len(studentInfo)-1)
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
def checkForConflicts(seatingChart, studentInfo):
    score = 0
    for group in range(len(seatingChart)):

        for seat in range(len(seatingChart[0])):

            student = int(seatingChart[group][seat])

            for neg in studentInfo[student]['NegativePairs']:
                if neg in seatingChart[group]:
                    return -1

            for pos in studentInfo[student]['PositivePairs']:
                if pos in seatingChart[group]:
                    score += 1

    return score

def generateValidSeats(classSize, numGroups, groupSize):
    testClass = initializeClass(classSize)
    print("class Initialized")

    studentsPopulated = populateStudentInfo(testClass)
    print("Student Info populated")
    print(str(studentsPopulated))

    seatsAssigned = assignSeats(studentsPopulated, numGroups, groupSize)
    attempt = 0

    while True:
        conflicts = checkForConflicts(seatsAssigned, studentsPopulated)
        if (conflicts <= 0):
            attempt += 1
            if (attempt % 100 == 0):
                print("Attempt no. %d failed" % attempt)
            seatsAssigned = assignSeats(studentsPopulated, numGroups, groupSize)
        else:
            print("Attempt no. %d succeeded! " % attempt)
            print("Seating chart score = %d" & conflicts)
            break

    return studentsPopulated, seatsAssigned


def testProgramComplete():
    studentInfo, seatsAssigned = generateValidSeats(12, 4, 3)
    print("studentInfo: ")
    print(str(studentInfo))
    print("Seating Chart: ")
    print(str(seatsAssigned))

def testProgram():
    testClass = initializeClass(22)
    populatedClass = populateStudentInfo(testClass, 3, 1)

    for s in range(len(populatedClass)):
        print("Student %d works well with " % s + str(populatedClass[s]['PositivePairs']) + " but not well with " + str(populatedClass[s]['NegativePairs']))

    maxScore = 0
    bestSeats = np.zeros((3, 3))
    for n in range(1000):
        seatsAssigned = assignSeats(populatedClass, 6, 4)
        conflicts = checkForConflicts(seatsAssigned, populatedClass)

        if (conflicts > maxScore):
            bestSeats = seatsAssigned
            maxScore = conflicts

    print("Best conflict score = %d" % maxScore)
    print("Best Seating Chart:" )
    print(str(bestSeats))


testProgram()


#To do:
# Add zero as an empty student (to fill in empty seats)
# Make generateValidSeats work!
# Add file IO
#
