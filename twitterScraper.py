import tweepy

from key import API_KEY, SECRET_API_KEY, ACCESS_TOKEN, SECRET_ACCESS_TOKEN
from utils import COMPANIES

def setTwitterAuth():
    """
    obtains authorization from twitter API
    """
    # sets the auth tokens for twitter using tweepy
    auth = tweepy.OAuthHandler(API_KEY, SECRET_API_KEY)
    auth.set_access_token(ACCESS_TOKEN, SECRET_ACCESS_TOKEN)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    return api

def searchTweet(api, searchTerm):
    """
    gets 100 search results of the string, search, and returns them as a list
    of tweet objects
    """


    searchResults = [status for status in tweepy.Cursor(api.search,
                                                        q=searchTerm,
                                                        tweet_mode='extended',
                                                        lang="en",
                                                        ).items(10)]
    return searchResults


def main():
    api = setTwitterAuth()
    searchResults = searchTweet(api, " Tesla ")
    print(len(searchResults))
    print(searchResults[0].user.name)
    print(searchResults[0].full_text)
    print(searchResults[0].author.followers_count)
    print(searchResults[0].created_at)
    print(searchResults[0].id)
    print(dir(searchResults[0]))


if __name__ == '__main__':
    main()
