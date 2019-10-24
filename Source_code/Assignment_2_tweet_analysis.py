#importing important libraries
import tweepy as tpi
from tweepy import OAuthHandler
import re
import json
import csv


# tokens required to connect to twitter collected from twitter application[1][2]
consumer_api_key = 'OBGostRMOuYcdy1u8b6qqbeih'
consumer_secret_api_key = '8WjV4oArYEYS3LHmMKHJBn051G8lXCWlSgfth079Lp5M7k47os'
access_token = '1140654968736796672-wdtIatbv16sRqeZ2HyK7i0roRgRMtr'
access_secret_token = 'eKy6pvabClorY2LXZOaLEirQorZbS0qqRb2NOG0MSHSNz'

# code for authentication
authentication = OAuthHandler(consumer_api_key, consumer_secret_api_key)
authentication.set_access_token(access_token, access_secret_token)

# fetching API
api=tpi.API(authentication,wait_on_rate_limit=True,wait_on_rate_limit_notify= True ,compression=True)

# creating and storing raw tweets in text file
tweet_stored_file =open("searchedtweets.txt","a+")

for tweets in tpi.Cursor(api.search, q='Canada , Canada import, Canada export', lang = "en").items(1200):#[13]
    print(tweets)
    try:
        tweet_stored_file.write(str(tweets._json) + '\n')
    except:
        pass

# creating and storing raw tweets in JSON file
tweets_in_json = api.search(["Canada", "Canada import" , "Canada export"], count=1200)#[13]

jsonfile = open("searchedtweets._json","+a")
#[4]
for item in tweets_in_json:
    json.dump(tweets._json, jsonfile, indent=4)

#data cleaning function
def cleaning_tweet(tweet_data) :
    tweet_data = re.sub(r"[^a-zA-Z0-9]+", ' ', tweet_data)  # removing special character[5]
    tweet_data = re.sub('_images/[A-Z-0-9a-z.jpg]+', ' ', tweet_data) # removing images
    tweet_data = re.sub(r"http\S+", "", tweet_data)#removing HTTP/HTTPS and URL[8][9]
    # removing emoticons, using this spaces between letters remains as it is.[7]
    emoticons_remove = re.compile(u"[^\U00000000-\U0000ffff]", flags=re.UNICODE)
    tweet_data = emoticons_remove.sub(r'', tweet_data)
    tweet_data = tweet_data.lower(); #lowering the tweet alphabets which is useful for word count
    return tweet_data

# for storing into csv
results_for_csv = api.search(["Canada" , "Canada import" , "Canada export"],"en",count=1200)#[13]

#opening csv for inserting column titles
with open("searchedtweets.csv", "+a") as outfiletitle:
    writer = csv.writer(outfiletitle)
    writer.writerow(["Id", "Name", "Date(created_at)", "Tweet(text)", "User_id", "Screen_name", "Location"])

for item_tweets in results_for_csv:

    try:

        # opening csv for inserting fetched tweet data into columns
        with open("searchedtweets.csv", "+a") as outfilecsv:
            writer = csv.writer(outfilecsv)#[6]
            writer.writerow([item_tweets.id, item_tweets.user.name,item_tweets.created_at, cleaning_tweet(item_tweets.text),item_tweets.user.id, item_tweets.user.screen_name,item_tweets.user.location])

    except:
        pass

