import os
import errno

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
