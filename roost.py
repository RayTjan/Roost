import json
import csv
import tweepy
import re
import io

# Enter your twitter credentials here
consumer_key = 'PrlTaQUDVkEVVgcI9DsQk350Q'
consumer_secret = 'NbyP2mDZrJ0E6iYCeT2wrhrsiAiNbGSS0tuD8pVlGMaEf2GfLX'

access_token = '1310256451659603969-d5kItqGLMyR3d59tNOi0XFzlgAHJuQ'
access_token_secret = 'e2iyx8eRW5iSD3hPWySZDA1Ns3Zx9kwuGfL8rzIha7M0Q'
search_terms = 'life OR fuck OR feel OR school OR know OR think OR pain OR way OR thought OR die'
search_try = 'life'
search_list = ['life', 'fuck', 'feel', 'school', 'know', 'think', 'pain', 'way', 'thought','die']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True)
LAST_SEEN_FILE = 'last_seen.txt'
LAST_SUB_FILE = 'last_sub.txt'
subscribeList = ['1085785224363962368']

def read_last_seen(FILE_NAME):
    file_read = open(FILE_NAME, 'r')
    last_seen_id = int(file_read.read().strip())
    file_read.close()
    return last_seen_id

def store_last_seen(FILE_NAME, last_seen_id):
    file_write = open(FILE_NAME, 'w')
    file_write.write(str(last_seen_id))
    file_write.close()
    return

def get_user_list(list_of_user) :
    tweets = tweepy.Cursor(api.search_tweets, q="#RoostMeDM",
                           since_id = read_last_seen(LAST_SUB_FILE), tweet_mode='extended').items(100)
    for tweet in tweets :
        list_of_user.append(tweet.user.id)
        store_last_seen(LAST_SUB_FILE, tweet.id)
    return list_of_user
        

def create_dataset(search_terms, list_of_user):
    # Name of csv file to be created
    # fname = "Tweet"
    
    # # Open the spreadsheet
    # with open('%s.csv' % (fname), 'w', encoding="utf-8") as file:
    #     w = csv.writer(file)
        
    #     # Write header row (feature column names of your choice)
    #     w.writerow(['timestamp', 'tweet_text', 'username', 'all_hashtags', 'location', 
    #                 'followers_count', 'retweet_count', 'favorite_count'])

    keep_post_id = 0
    for name in list_of_user :
        print(name)
        for tweet in tweepy.Cursor(api.user_timeline, user_id=name, since_id = read_last_seen(LAST_SEEN_FILE), tweet_mode='extended').items(100):
            # w.writerow([tweet.created_at, 
            #             tweet.full_text.replace('\n',' '), 
            #             tweet.user.screen_name, 
            #             tweet.user.location  
            #            ])
            print("RAW :" + tweet.full_text)
            for tag in search_list :
                found = False
                for word in tweet.full_text.lower().split():
                    if tag == word and found == False :
                        print("filtered :" + tweet.full_text)
                        found = True
                        break

            if keep_post_id < tweet.id :
                print("waht")
                keep_post_id = tweet.id
    if keep_post_id != 0 :
        store_last_seen(LAST_SEEN_FILE, keep_post_id)

if __name__ == '__main__':
    # create_dataset(search_terms)
    #  get_user_list(subscribeList)
    # subscribeList = get_user_list(subscribeList)
    create_dataset(search_terms,subscribeList)
    print(subscribeList)

#how to post
# api.update_status('Updating using OAuth authentication via Tweepy!')
#how to reply
# api.update_status(status = "@" + tweet.user.screen_name + " Auto Reply, Like & Retweet works.", in_reply_to_status_id = tweet.id)
