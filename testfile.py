#Test python file

from bs4 import BeautifulSoup as bs
import numpy as np
import matplotlib.pyplot as plt


# generate set of students
def initializeClass(classSize):
    # Each student is a dictionary with name, positive pairs, negative pairs
    studentInfo = [{'Name':'', 'PositivePairs':[], 'NegativePairs':[], 'LocationPref':[]} for x in range(classSize+1)]

    return studentInfo

#populate class with 2 students each student shouldn't sit with
def populateStudentInfo(studentInfo, numPos = 2, numNeg = 1):

    s = 1
    for student in studentInfo[1:]:
        student['Name'] = "Student %d" % s
        negatives = np.random.random_integers(1, len(studentInfo), numNeg)
        positives = np.random.random_integers(1, len(studentInfo), numPos)
        while True:
            if (s in negatives) or (s in positives):
                negatives = np.random.random_integers(1, len(studentInfo), numNeg)
                positives = np.random.random_integers(1, len(studentInfo), numPos)
            else:
                student['NegativePairs'] = negatives
                student['PositivePairs'] = positives
                student['LocationPref'].append(getRandomLocationPref())
                s += 1
                break

    return studentInfo

def getRandomLocationPref():
    r = str(np.random.random_integers(0,2))
    key = {'0':'F', '1':'M', '2':'R'}
    return key[r]

# function that returns a matrix of students in groups
def assignSeats(studentInfo, numGroups, groupSize):
    seatingChart = np.zeros((numGroups,groupSize))
    assigned = np.zeros(len(studentInfo), dtype = bool)

    groupNum = 0
    seatNum = 0
    iterations = 0

    for student in range(1, len(studentInfo)):
        while True:
            n = np.random.random_integers(1, len(studentInfo)-1)
            iterations += 1
            badPairs = []
            if (not assigned[n]):
                for x in seatingChart[groupNum]:
                    for s in studentInfo[int(x)]['NegativePairs']:
                        badPairs.append(int(s))
                #print("badPairs for student %d is " % n + str(badPairs) + " and group %d is " %groupNum + str(seatingChart[groupNum]))
                if (n not in badPairs):
                    seatingChart[groupNum, seatNum] = n
                    assigned[n] = True
                    #print ("Student %d assigned to group %d, seat %d. " % (n, groupNum+1, seatNum+1))
                    if(groupNum == (numGroups-1)):
                        seatNum += 1
                        groupNum = 0
                    else:
                        groupNum += 1


                    break
                else:
                    #print("======= Invalid assignment. Construction new chart. =======")
                    return False, [0]
    #print ("%d iterations completed" % iterations)

    return True, seatingChart

#
def checkForConflicts(seatingChart, studentInfo, FMR):
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

            for loc in studentInfo[student]['LocationPref']:
                if (group+1) in FMR[loc]:
                    score += 1
                if ((loc == 'F') and ((group+1) in FMR['R'])) or ((loc == 'R') and ((group+1) in FMR['F'])):
                    score -= 2

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
    testClass = initializeClass(24)
    populatedClass = populateStudentInfo(testClass, 4, 2)

    for s in range(len(populatedClass)):
        print("Student %d works well with " % s + str(populatedClass[s]['PositivePairs']) + " but not well with " + str(populatedClass[s]['NegativePairs']) +
            " and likes to sit in the " + str(populatedClass[s]['LocationPref']))

    maxScore = 0
    bestSeats = np.zeros((3, 3))
    validCharts = 0
    attempts = 10000
    attemptsX = []
    attemptsY = []
    classArrangement = {'F':[1], 'M':[2,3,4,5], 'R':[6]}

    for n in range(attempts):
        success, seatsAssigned = assignSeats(populatedClass, 6, 4)
        while (not success):
            success, seatsAssigned = assignSeats(populatedClass, 6, 4)

        conflicts = checkForConflicts(seatsAssigned, populatedClass, classArrangement)
        attemptsX.append(n)
        if (n % 1000 == 0):
            print ("attempt %d completed " % n)
        if (conflicts > 0):
            validCharts += 1
            if (conflicts > maxScore):
                bestSeats = seatsAssigned
                maxScore = conflicts
        attemptsY.append(maxScore)

    print("Best conflict score = %d after %d valid seating charts out of %d " % (maxScore, validCharts, attempts))
    print("Best Seating Chart:" )
    print(str(bestSeats))

    plt.plot(attemptsX,attemptsY)
    plt.show()


testProgram()


#To do:
# Make generateValidSeats work!
# Add file IO
#
