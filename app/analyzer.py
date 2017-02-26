import json
import urllib

import requests

from chiedza.settings import TONE_ANALYZER
from .apis._twitter import get_tweets

def analyze(req):


    tweets = get_tweets(req)

    most_positive = None
    most_negative = None    

    twitter_average = 0
    positive_average = 0
    anger_average = 0
    sadness_average = 0
    disgust_average = 0

    negative_count = 0

    positvie_count = 0

    tweet_count = 0
    top = []
    for tweet in tweets:
        tweet_count += 1
        if(tweet_count <= 3):
            top.append(tweet._json)
        tones = TONE_ANALYZER.tone(text=tweet.text, tones='emotion')
        positive_tone = list(filter(lambda x: x.get('tone_id') == 'joy', tones.get('document_tone').get('tone_categories')[0].get('tones')))
        positive_percent = positive_tone[0].get('score')
        positive_average += positive_percent

        anger_tone = list(filter(lambda x: x.get('tone_id') == 'anger', tones.get('document_tone').get('tone_categories')[0].get('tones')))
        negativePercent = anger_tone[0].get('score')
        anger_average += anger_tone[0].get('score')

        sadness_tone = list(filter(lambda x: x.get('tone_id') == 'sadness', tones.get('document_tone').get('tone_categories')[0].get('tones')))
        negativePercent += sadness_tone[0].get('score')
        sadness_average += sadness_tone[0].get('score')

        disgust_tone = list(filter(lambda x: x.get('tone_id') == 'disgust', tones.get('document_tone').get('tone_categories')[0].get('tones')))
        negativePercent += disgust_tone[0].get('score')
        disgust_average += disgust_tone[0].get('score')

        score = positive_percent * 5
        twitter_average += score

        if(positive_percent >= 0.5):
            positvie_count += 1


    twitter_average /= tweet_count
    positive_average /= tweet_count
    anger_average /= tweet_count
    sadness_average /= tweet_count
    disgust_average /= tweet_count

    positvie_count /= tweet_count
    negative_count = 1 - positvie_count

    top_tweets = []
    for tweet in top:
        uri = {'url' : 'https://twitter.com/%s/status/%s' % (tweet.get('user').get('screen_name'), tweet.get('id_str')), 'omit_script': True }
        encoded = urllib.parse.urlencode(uri)
        r = requests.get('https://publish.twitter.com/oembed?=%s' % encoded)
        top_tweets.append(r.json().get('html'))

    results = {
        'twitter_average' : twitter_average,
        'positive' : positive_average,
        'anger' : anger_average,
        'sadness' : sadness_average,
        'disgust' : disgust_average,
        'top_tweets' : top_tweets,
        'percent_positive' : positvie_count,
        'percent_negative' : negative_count
    }

    return results
