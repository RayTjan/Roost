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
    tweets = tweepy.Cursor(api.search, q="#RoostMeDM",
                           since_id = read_last_seen(LAST_SUB_FILE), tweet_mode='extended').items(100)
    for tweet in tweets :  
      list_of_user.append(tweet.user.id)
      store_last_seen(LAST_SUB_FILE, tweet.id)
      send_reply(tweet.user.screen_name, " Thank you for consenting to Roost", tweet.id)
    return list_of_user
  

def create_dataset(search_terms, list_of_user):
    # Name of csv file to be created
    new_dataset_name = "tweet"
    keep_post_id = 0
    # # Open the spreadsheet
    with open('%s.csv' % (new_dataset_name), 'w', encoding="utf-8") as file:
        w = csv.writer(file)

    #     # Write header row (feature column names of your choice)
        w.writerow(['timestamp', 'tweet_text', 'username', 'location'])
        for name in list_of_user :
          # print(name)
          # tweets = tweepy.Cursor(api.user_timeline, user_id=name, since_id = read_last_seen(LAST_SEEN_FILE), tweet_mode='extended').items(1)
          for tweet in tweepy.Cursor(api.user_timeline, q=search_terms, user_id=name, since_id = read_last_seen(LAST_SEEN_FILE), tweet_mode='extended').items(1):
              w.writerow([tweet.created_at, 
                          tweet.full_text.replace('\n',' ') + ' + ' + str(tweet.id) + ' + ' + str(tweet.user.screen_name), 
                          tweet.user.screen_name, 
                          tweet.user.location,
                          ])
              for tag in search_list :
                  found = False
                  for word in tweet.full_text.lower().split():
                      if tag == word and found == False :
                          print("filtered :" + tweet.full_text)
                          found = True
                          break

              if keep_post_id < tweet.id :
                  keep_post_id = tweet.id
    if keep_post_id != 0 :
        store_last_seen(LAST_SEEN_FILE, keep_post_id)

def send_reply(username, text_reply, tweet_id):
  api.update_status(status = "@" + username + text_reply , in_reply_to_status_id = tweet_id)



# create_dataset(search_terms)
# get_user_list(subscribeList)
# subscribeList = get_user_list(subscribeList)
# create_csv()
create_dataset(search_terms,subscribeList)
# testing_tweepy(search_terms, subscribeList)
# print(subscribeList)

#how to post
# api.update_status('Updating using OAuth authentication via Tweepy!')
#how to reply
# api.update_status(status = "@" + tweet.user.screen_name + " Auto Reply, Like & Retweet works.", in_reply_to_status_id = tweet.id)

dataset_scraped = pd.read_csv('tweet.csv')
# dataset_scraped.head()
one_gram_svm_scraped = one_gram_svm_text.predict(dataset_scraped['tweet_text'])
for doc, category in zip(dataset_scraped['tweet_text'], one_gram_svm_prediction):
    splitted_doc = doc.split(' + ')
    print(splitted_doc[1])
    print('%r => %s' % (splitted_doc[0], category))
    if category != 0:
      # send DM
      # api.send_direct_message(splitted_doc[1], "this is a test")
      send_reply(splitted_doc[2], " Your post showed unsettling signs of destructive behavior, please contact your local hotline for help", splitted_doc[1])
      # api.update_status(status = "@" + splitted_doc[2] + " Your post showed unsettling signs of destructive behavior, please contact your local hotline for help", in_reply_to_status_id = splitted_doc[1])

# #1 suicide
# #0 non suicide