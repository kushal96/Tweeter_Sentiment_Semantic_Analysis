#importing important libraries
import tweepy as tpi
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import re
import json
import csv



#tokens required to connect to twitter collected from twitter application[1][2]
consumer_api_key = 'OBGostRMOuYcdy1u8b6qqbeih'
consumer_secret_api_key = '8WjV4oArYEYS3LHmMKHJBn051G8lXCWlSgfth079Lp5M7k47os'
access_token = '1140654968736796672-wdtIatbv16sRqeZ2HyK7i0roRgRMtr'
access_secret_token = 'eKy6pvabClorY2LXZOaLEirQorZbS0qqRb2NOG0MSHSNz'

#opening text and JSON files storing raw tweets
live_tweet_file =open("streamedtweets.txt","a+")
jsonfile = open("streamedtweets._json","a")

#opening csv for inserting column titles
with open("streamedtweets.csv", "+a") as outfiletitle:
    writer = csv.writer(outfiletitle)
    writer.writerow(["Id", "Name", "Date(created_at)", "Tweet(text)", "User_id", "Screen_name", "Location"])

#function for data cleaning
def cleaning_stream_tweet(tweet_data) :
    tweet_data = re.sub(r"[^a-zA-Z0-9]+", ' ', tweet_data)  # removing special character[5]
    tweet_data = re.sub('_images/[A-Z-0-9a-z.jpg]+', ' ', tweet_data) # removing images
    tweet_data = re.sub(r"http\S+", "", tweet_data)#removing HTTP/HTTPS and URL[8][9]
    # removing emoticons, using this spaces between letters remains as it is.[7]
    emoticons_remove = re.compile(u"[^\U00000000-\U0000ffff]", flags=re.UNICODE)
    tweet_data = emoticons_remove.sub(r'', tweet_data)
    tweet_data = tweet_data.lower();  # useful for word count
    return tweet_data

#inbuilt library for fetching live streamed tweets[3][10][11]
class tweet_fetching (StreamListener):

    def on_data(self, fetched_tweets):

        try:
            live_tweet_file.write((fetched_tweets) + '\n')
            # self.jsonfile.append(json.loads(fetched_tweets))
            # jsonfile.write(str(fetched_tweets))
            fetched_json_live_tweets = json.loads(fetched_tweets)#[12]
            json.dump(fetched_json_live_tweets, jsonfile, indent=4)#[4]
            with open("streamedtweets.csv", "+a") as outfilecsv:
                writer = csv.writer(outfilecsv)#[6]
                # writes data into csv
                print(fetched_json_live_tweets)
                writer.writerow(
                    [ fetched_json_live_tweets["id"],fetched_json_live_tweets["user"]["name"],fetched_json_live_tweets["created_at"],cleaning_stream_tweet(fetched_json_live_tweets["text"]),
                     fetched_json_live_tweets["user"]["id"], fetched_json_live_tweets["user"]["screen_name"], fetched_json_live_tweets["user"]["location"]])

        except:
            pass

# code for authentication
authentication = OAuthHandler(consumer_api_key, consumer_secret_api_key)
authentication.set_access_token(access_token, access_secret_token)

#filters the tweet language and keyword
stream_tweet = Stream(authentication, tweet_fetching())#[11]
stream_tweet.filter(languages = ["en"], track=["Canada" ,"Canada import", "Canada export"])