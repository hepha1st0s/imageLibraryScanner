import argparse
import ntpath
import cv2
import os
import math

ap = argparse.ArgumentParser()
ap.add_argument("-s", "--source", required=True,
	help="source file with results from extractor")
ap.add_argument("-d", "--destination", required=True,
	help="destination folder")
ap.add_argument("-r", "--reduction", default=1.0,
	help="factor to reduce image size by (0.01 - 1.0)")
args = vars(ap.parse_args())

sourceFile = args["source"]
destinationFolder = args["destination"]
reduction = float(args["reduction"])

if not os.path.exists(destinationFolder):
    os.makedirs(destinationFolder)
print "Processing images..."
with open(sourceFile, "r") as file:
    for line in file:
        if not line:
            continue
        line = line.replace("\n", "")
        loadedImage = cv2.imread(line)
        if reduction > 0 and reduction < 1:
            loadedImage = cv2.resize(loadedImage, (int(math.floor(loadedImage.shape[1] * reduction)), int(math.floor(loadedImage.shape[0] * reduction))))
            cv2.imwrite(destinationFolder + "/" + ntpath.basename(line), loadedImage)
print "Done..."
