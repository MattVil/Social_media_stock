import csv
import os

numOfEntries = 0

rawTweetFileExists = os.path.isfile('./rawTweetFile.csv')
if rawTweetFileExists:

    rawTweetFileForReading = open("rawTweetFile.csv", 'r')
    csvReader = csv.reader(rawTweetFileForReading)
    # record all tweet id's in local list to check future tweets for uniqueness
    for line in csvReader:
        numOfEntries += 1

    rawTweetFileForReading.close()

    print(numOfEntries)

else:
    print("File doesn't exist")