from config import consumer_api_key, consumer_api_secret_key, access_token, access_token_secret

import csv
import tweepy
import os

# twitter authorization stuff
auth = tweepy.OAuthHandler(consumer_api_key, consumer_api_secret_key)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# these are our search terms
companiesTracked = ["Tesla", "Google", "Apple", "CVS Health", "Verizon", "Facebook", "Amazon", "General Motors",
                    "Chevron", "J.P. Morgan Chase"]

currentlyRecordedTweetsById = []
numOfTweetsRecorded = 0

rawTweetFileExists = os.path.isfile('./rawTweetFile.csv')

if rawTweetFileExists:

    rawTweetFileForReading = open("rawTweetFile.csv", 'r')
    csvReader = csv.reader(rawTweetFileForReading)
    # record all tweet id's in local list to check future tweets for uniqueness
    for line in csvReader:
        currentlyRecordedTweetsById.append(line[1])

    rawTweetFileForReading.close()

# csv file will track all our raw data
rawTweetFile = open("rawTweetFile.csv", 'a+')
csvWriter = csv.writer(rawTweetFile)


try:
    # searches for tweets related to each corporation we're tracking
    for company in companiesTracked:

        searchTerm = company

        # records raw tweets and other data in our rawTweetFile
        for tweet in tweepy.Cursor(api.search, q=searchTerm + " -filter:retweets", tweet_mode='extended',
                                   lang='en').items(80):
            # makes sure a tweet isn't a reply to some other tweet and that the tweet isn't a duplicate
            if tweet.in_reply_to_status_id is None and tweet.id not in currentlyRecordedTweetsById:
                csvWriter.writerow([searchTerm, tweet.id, tweet.user.screen_name, tweet.user.followers_count,
                                    tweet.created_at, tweet.full_text])
                # add tweet id to our list to make sure we don't record the same tweet twice
                currentlyRecordedTweetsById.append(tweet.id)
                numOfTweetsRecorded += 1
except Exception as e:
    with open("logFile.txt", 'a+') as logFile:
        logFile.write("\n" + str(e))


rawTweetFile.close()

# used to keep track of how many tweets we're getting each time this is run
logFile = open("logFile.txt", 'a+')
logFile.write("\n" + str(numOfTweetsRecorded))
logFile.close()