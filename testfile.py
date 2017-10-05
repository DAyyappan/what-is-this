#Test python file
from bs4 import BeautifulSoup as bs
import numpy as np

# generate set of students
def initializeClass(classSize):
    classIDs = np.zeros((classSize, 2))
    print("classIDs shape = " + str(classIDs.shape))

    return classIDs


def populateNegatives(classList, numNegs = 2):
    for student in range(len(classList)):
        negatives = np.random.random_integers(1, len(classList), numNegs)
        classList[student] = negatives

    return classList

print(populateNegatives(initializeClass(20)))
