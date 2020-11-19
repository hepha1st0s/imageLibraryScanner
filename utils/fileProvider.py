import os
import errno
from collections import namedtuple

def getNumFilesInFolderOfType(folderPath, type):
    return sum([len([file for file in files if file.endswith(type)]) for r, d, files in os.walk(folderPath)])

def getAllFilesOfType(folderPath, type):
    numFilesTotal = getNumFilesInFolderOfType(folderPath, type)
    print "found " + str(numFilesTotal) + " files in directory " + folderPath
    return [f for i in [[os.path.join(r,file) for file in files if file.endswith(type)] for r, d, files in os.walk(folderPath)] for f in i]

def appendToFile(file, text):
    if not os.path.exists(os.path.dirname(file)):
        try:
            os.makedirs(os.path.dirname(file))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise
    with open(file, "a") as f:
        f.write(text)
        f.write("\n")

def getAllOutputFiles(folderPath):
    return [f for i in [[os.path.join(r,file) for file in files if file.isdigit()] for r, d, files in os.walk(folderPath)] for f in i]

def getSimilarityData(file):
    similarityData = {}
    key = None
    with open(file, "r") as file:
        for line in file:
            if not line:
                return imageSimilarityData
            if key is None:
                key = line.replace("\n", "")
                similarityData[key] = []
            else:
                similarityData[key].append((line.replace("\n", "").split(":")))
    return similarityData
