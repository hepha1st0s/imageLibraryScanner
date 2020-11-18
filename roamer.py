import argparse
import cv2
from skimage.measure import compare_ssim
from utils.fileProvider import getAllFilesOfType, appendToFile

DEFAULT_SOURCE_FILE_TYPE = ".jpg"

ap = argparse.ArgumentParser()
ap.add_argument("-s", "--source", required=True,
	help="source directory with input images")
ap.add_argument("-d", "--dimension", default=100,
	help="scale image to dimension x dimension pixels")
ap.add_argument("-t", "--type", default=DEFAULT_SOURCE_FILE_TYPE,
	help="file type extension to look for")
args = vars(ap.parse_args())

sourceDir = args["source"]
dimension = int(args["dimension"])
fileType = args["type"]

images = getAllFilesOfType(sourceDir, fileType)
print "Loading Images..."
loadedImages = [(image, cv2.resize(cv2.imread(image), (dimension,dimension))) for image in images]
print "Comparing Images..."

for i in range(0, len(loadedImages)):
    appendToFile("./output/" + str(i), loadedImages[i][0])
    for e in range(i+1, len(loadedImages)):
        try:
            score = compare_ssim(cv2.cvtColor(loadedImages[i][1], cv2.COLOR_BGR2GRAY), cv2.cvtColor(loadedImages[e][1], cv2.COLOR_BGR2GRAY))
            appendToFile("./output/" + str(i), str(score) + ":" + loadedImages[e][0])
        except:
            print "failed to compare " + loadedImages[i][0] + " with " + loadedImages[e][0]
print("DONE")
