import argparse
from utils.fileProvider import getAllOutputFiles, getSimilarityData, appendToFile
import cv2
import os
import math
from operator import itemgetter

IMAGE_OFFSET = 20

ap = argparse.ArgumentParser()
ap.add_argument("-s", "--source", required=True,
	help="source directory with results from roamer")
ap.add_argument("-r", "--range", default=0.9,
	help="define up to which SSIM value images should be regarded as similar")
ap.add_argument("-d", "--displaysize", default=1.0,
	help="define scale factor for image display")
args = vars(ap.parse_args())

sourceDir = args["source"]
range = float(args["range"])
displaySize = int(args["displaysize"])

print "Loading Data"
similarityData = {}
[similarityData.update(getSimilarityData(outfile)) for outfile in getAllOutputFiles(sourceDir)]
print "Loaded " + str(len(similarityData)) + " images with " + str(sum([len(similarityData[x]) for x in similarityData])) + " similarity entries..."

filteredSimilarityData = {}
print "Filtering data by range"
for key, value in similarityData.iteritems():
    filteredSimilarityData[key] = [(similarityEntry[0], similarityEntry[1]) for similarityEntry in value if float(similarityEntry[0]) >= range]
print "Status after filtering: " + str(len(filteredSimilarityData)) + " images with " + str(sum([len(filteredSimilarityData[x]) for x in filteredSimilarityData])) + " similarity entries..."

def recursivelyMergeSimilarities(mergedSimilarityData, filteredSimilarityData, pkey, ckey, usedImagesList):
    if not filteredSimilarityData[ckey]:
        return mergedSimilarityData, usedImagesList
    for similarityEntry in filteredSimilarityData[ckey]:
        if similarityEntry[1] not in list(map(itemgetter(1), mergedSimilarityData[pkey])) and similarityEntry[1] not in usedImagesList:
            mergedSimilarityData[pkey].append(similarityEntry)
            usedImagesList.append(similarityEntry[1])
        return recursivelyMergeSimilarities(mergedSimilarityData, filteredSimilarityData, pkey, similarityEntry[1], usedImagesList)

mergedSimilarityData = {}
usedImagesList = []
print "Merging Similarity Data - setting up related data"
for key, value in filteredSimilarityData.iteritems():
    if len(value) < 1 or key in usedImagesList:
        continue
    mergedSimilarityData[key] = []
    usedImagesList.append(key)
    for similarityEntry in value:
        if not similarityEntry or similarityEntry[1] in list(map(itemgetter(1), mergedSimilarityData[key])) or similarityEntry[1] in usedImagesList:
            continue
        mergedSimilarityData[key].append(similarityEntry)
        usedImagesList.append(similarityEntry[1])
        mergedSimilarityData, usedImagesList = recursivelyMergeSimilarities(mergedSimilarityData, filteredSimilarityData, key, similarityEntry[1], usedImagesList)
print "Status " + str(len(mergedSimilarityData)) + " images including " + str(sum([len(mergedSimilarityData[x]) for x in mergedSimilarityData if mergedSimilarityData[x]])) + " similarity entries..."
print "Merging Similarity Data - setting up unrelated data"
for key, value in filteredSimilarityData.iteritems():
    if key not in usedImagesList:
        mergedSimilarityData[key] = []
print "Status " + str(len(mergedSimilarityData)) + " images including " + str(sum([len(mergedSimilarityData[x]) for x in mergedSimilarityData if mergedSimilarityData[x]])) + " similarity entries..."
print str(len([x for x in mergedSimilarityData if mergedSimilarityData[x]])) + " coices to make..." #TODO: FIXME
cont = raw_input("Continue? [y/n]: ")
favorizeFotosWithSubstring = raw_input("Favorize any Fotos? Provide Substring: ")
if not cont.startswith("y"):
    exit(0)

for key, value in mergedSimilarityData.iteritems():
    if len(value) < 1:
        appendToFile("./output2", key)
        continue
    elif favorizeFotosWithSubstring and len(value) == 1:
        if favorizeFotosWithSubstring in key:
            appendToFile("./output2", key)
            print "Favorized " + key + " over " + value[0][1]
            continue
        elif favorizeFotosWithSubstring in value[0][1]:
            appendToFile("./output2", value[0][1])
            print "Favorized " + value[0][1] + " over " + key
            continue
    loadedImages = [(cv2.imread(key), key)]
    loadedImages = loadedImages + [(cv2.imread(imgPath), imgPath) for (s,imgPath) in value]
    loadedImages = [(cv2.resize(image[0], (int(math.floor(image[0].shape[1] / displaySize)), int(math.floor(image[0].shape[0] / displaySize)))),image[1]) for image in loadedImages]
    print "Choice between:"
    for i, (image, path) in enumerate(loadedImages):
        cv2.imshow(str(i+1) + ": " + path, image)
        print path
        cv2.moveWindow(path, 50 + (i + 1) * IMAGE_OFFSET,(i + 1) * IMAGE_OFFSET);
    cv2.waitKey(1)
    choice = raw_input("Your Choice? [single number or multiple column seperated]: ")
    if not choice:
        cv2.destroyAllWindows()
        continue
    for index in choice.split(","):
        print "choosing " + loadedImages[int(index)-1][1]
        appendToFile("./output2", loadedImages[int(index)-1][1])
    cv2.destroyAllWindows()
