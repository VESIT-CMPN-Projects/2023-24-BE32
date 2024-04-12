from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
from django.shortcuts import render
from django.conf import settings
from .models import PollingData
from dashboard.models import History
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer


def get_instagram_user_info(username):
    url = f"https://instagram-2024-new.p.rapidapi.com/api/instagram/users/info/{username}/username"

    headers = {
        # "X-RapidAPI-Key": "2f8e44311msh4cc20224a3df5fap15bc31jsnb430596ce1e2",
	    # "X-RapidAPI-Host": "instagram-2024-new.p.rapidapi.com",
        # "X-RapidAPI-Key": "2f8e4431a1msh4cc20224a3df5fap15bc31jsnb430596ce1e2",
       "X-RapidAPI-Key": "98544df8bfmsh0477d0edeb89c70p1890c6jsnf0abc33340de",
	   "X-RapidAPI-Host": "instagram-2024-new.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    if 'user' in data:
        user_data = data['user']
        return {
            'username': user_data['username'],
            'full_name': user_data['full_name'],
            'follower_count': user_data['follower_count'],
            'following_count': user_data['following_count'],
            'media_count': user_data['media_count'],
        }
    else:
        return {
            'error': f"Error occurred while fetching user data for {username}."
        }

def get_twitter_user_info(user_id, endpoint):
    # url = f"https://twitter154.p.rapidapi.com/user/{endpoint}"
    url ="https://twitter154.p.rapidapi.com/user/followers"
    querystring = {"user_id": user_id, "limit": "10"}

    headers = {
        # "X-RapidAPI-Key": "2f8e441a1msh4cc20224a3df5fap15bc31jsnb430596ce1e2",
        # # "X-RapidAPI-Key": "2f8e4431a1msh4cc20224a3df5fap15bc31jsnb430596ce1e2",
	    # "X-RapidAPI-Host": "twitter154.p.rapidapi.com"

        # "X-RapidAPI-Key": "2f8e4431a1msh4cc20224a3df5fap15bc31jsnb430596ce1e2",
	    # "X-RapidAPI-Host": "twitter154.p.rapidapi.com"

        "X-RapidAPI-Key": "98544df8bfmsh0477d0edeb89c70p1890c6jsnf0abc33340de",
	    "X-RapidAPI-Host": "twitter154.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()

    if response.status_code == 200:
        return data
    else:
        return {'error': f"Error occurred while fetching {endpoint} data for user {user_id}."}

from textblob import TextBlob
import requests
import csv

import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Initialize VADER sentiment analyzer
sid = SentimentIntensityAnalyzer()

# Function to perform sentiment analysis using VADER
def get_sentiment(text):
    sentiment_score = sid.polarity_scores(text)
    if sentiment_score['compound'] > 0:
        return 'Positive'
    elif sentiment_score['compound'] == 0:
        return 'Neutral'
    else:
        return 'Negative'

def fetch_tweets(hashtags):
    tweets_data = []
    sentiment_counts = {'Neutral': 0, 'Positive': 0, 'Negative': 0}

    for hashtag in hashtags:
        url = "https://twitter154.p.rapidapi.com/hashtag/hashtag"
        querystring = {"hashtag": hashtag, "limit": "20", "section": "top"}
        headers = {
            "X-RapidAPI-Key": "98544df8bfmsh0477d0edeb89c70p1890c6jsnf0abc33340de",
	        "X-RapidAPI-Host": "twitter154.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()

        if 'results' in data:
            for result in data['results']:
                sentiment = get_sentiment(result['text'])
                tweets_data.append({'text': result['text'], 'sentiment': sentiment})
                sentiment_counts[sentiment] += 1
        else:
            print(f"No results found for hashtag: {hashtag}")

    return tweets_data, sentiment_counts['Positive'], sentiment_counts['Neutral'], sentiment_counts['Negative'] 


# Function to analyze sentiment of YouTube comments
def analyze_youtube_sentiment(video_ids):
    # Implementation of this function is assumed but not provided in the current context
    pass



sid = SentimentIntensityAnalyzer()

def get_sentiment(text):
    sentiment_score = sid.polarity_scores(text)
    if sentiment_score['compound'] > 0:
        return 'Positive'
    elif sentiment_score['compound'] == 0:
        return 'Neutral'
    else:
        return 'Negative'


    
from django.shortcuts import render
from textblob import TextBlob
import requests


def fetch_comments(video_ids):
    comments = []

    for video_id in video_ids:
        url = "https://yt-api.p.rapidapi.com/comments"
        params = {"id": video_id}  # Change "v" to "id"
        headers = {
            'X-RapidAPI-Key': '98544df8bfmsh0477d0edeb89c70p1890c6jsnf0abc33340de',
            'X-RapidAPI-Host': 'yt-api.p.rapidapi.com'
        }

        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()  # Raise exception for 4xx or 5xx status codes
            data = response.json()
            
            if 'data' in data:
                for item in data['data']:
                    comment = item['textDisplay']
                    comments.append(comment)
            else:
                print(f"No comments found for video ID: {video_id}")
        
        except requests.HTTPError as e:
            print(f"HTTP error occurred: {e.response.status_code} {e.response.reason}")
        except Exception as e:
            print(f"An error occurred: {e}")
    
    return comments


# Initialize VADER sentiment analyzer
sid = SentimentIntensityAnalyzer()

# Function to perform sentiment analysis using VADER
def get_sentiment(text):
    sentiment_score = sid.polarity_scores(text)
    if sentiment_score['compound'] > 0:
        return 'Positive'
    elif sentiment_score['compound'] == 0:
        return 'Neutral'
    else:
        return 'Negative'

# Function to fetch comments from YouTube API with pagination
def fetch_comments(video_ids):
    comments = []

    for video_id in video_ids:
        # Your fetch_comments function implementation goes here
        url = "https://yt-api.p.rapidapi.com/comments"
        params = {"id": video_id}  # Change "v" to "id"
        headers = {
            # "X-RapidAPI-Key": "2f8e4431a1msh4cc20224a3df5fap15bc31jsnb430596ce1e2",
	        # "X-RapidAPI-Host": "yt-api.p.rapidapi.com"
            'X-RapidAPI-Key': '98544df8bfmsh0477d0edeb89c70p1890c6jsnf0abc33340de',
            'X-RapidAPI-Host': 'yt-api.p.rapidapi.com'
        }

        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()  # Raise exception for 4xx or 5xx status codes
            data = response.json()
            
            if 'data' in data:
                for item in data['data']:
                    comment = item['textDisplay']
                    comments.append(comment)
            else:
                print(f"No comments found for video ID: {video_id}")
        
        except requests.HTTPError as e:
            print(f"HTTP error occurred: {e.response.status_code} {e.response.reason}")
        except Exception as e:
            print(f"An error occurred: {e}")
        pass  # Placeholder until you implement this function

    return comments

# Function to analyze sentiment of YouTube comments
def analyze_youtube_sentiment(video_ids):
    comments = fetch_comments(video_ids)
    sentiments = [get_sentiment(comment) for comment in comments]
    sentiment_counts = {
        'Positive': sentiments.count('Positive'),
        'Neutral': sentiments.count('Neutral'),
        'Negative': sentiments.count('Negative')
    }
    return sentiment_counts

# Your social view function
def social(request):
    # Fetch data from multiple URLs (Instagram, Twitter)
    # Fetch data from multiple URLs
    bjp4india_data = get_instagram_user_info('bjp4india')
    incindia_data = get_instagram_user_info('incindia')
    aap_data = get_instagram_user_info('aamaadmiparty')
    bsp_data = get_instagram_user_info('bsp4india_')

    # Fetch data from Twitter for followers and following for both BJP and INCIndia
    bjp4india_followers_data = get_twitter_user_info('BJP4India', 'followers')
    bjp4india_following_data = get_twitter_user_info('BJP4India', 'following')
    
    incindia_followers_data = get_twitter_user_info('INCIndia', 'followers')
    incindia_following_data = get_twitter_user_info('INCIndia', 'following')

    aap_followers_data = get_twitter_user_info('AamAadmiParty', 'followers')
    aap_following_data = get_twitter_user_info('AamAadmiParty', 'following')

    bsp_followers_data = get_twitter_user_info('bspindia', 'followers')
    bsp_following_data = get_twitter_user_info('bspindia', 'following')


    # List of hashtags for different parties
    congress_hashtags = ["#congress", "#rahulgandhi", "#voteforcongress", "#INC", "#SoniaGandhi", "#CongressParty", "#IndianNationalCongress", "#CongressForIndia", "#PriyankaGandhi", "#rahulgandhi", "#CongressManifesto"]
    bjp_hashtags = ["#NarendraModi", "#BJP", "#Modi", "#bjpgovt", "#votebjp", "#voteforbjp", "#yogiadityanath", "#bjpindia", "#bharatiyajanataparty", "#pmmodi", "#JPNadda"]
    aap_hashtags = ["#AAP", "#ArvindKejriwal", "#AamAadmiParty", "#kejriwal", "#aapgovt", "#voteaap", "#dilipkpandey", "#AAP_का_सच", "#AAPReducesElectricityRates", "#AAP_सरकार_जनता_की_सरकार"]
    bsp_hashtags = ["#BSP", "#Mayawati", "#BahujanSamajParty", "#Dalit", "#BSPGovt", "#votebsp", "#dalits", "#BSPMissionUP", "#BSPRocks", "#BSP_संग_गठबंधन"]

    # Fetch tweets and sentiments for each party
    congress_tweets, congress_positive_count, congress_neutral_count, congress_negative_count = fetch_tweets(congress_hashtags)
    bjp_tweets, bjp_positive_count, bjp_neutral_count, bjp_negative_count = fetch_tweets(bjp_hashtags)
    aap_tweets, aap_positive_count, aap_neutral_count, aap_negative_count = fetch_tweets(aap_hashtags)
    bsp_tweets, bsp_positive_count, bsp_neutral_count, bsp_negative_count = fetch_tweets(bsp_hashtags)

    # Calculate total comments for each party (similar to YouTube sentiment analysis)
    congress_total_comments = len(congress_tweets)
    bjp_total_comments = len(bjp_tweets)
    aap_total_comments = len(aap_tweets)
    bsp_total_comments = len(bsp_tweets)


    congress_video_ids = ["tCoubnfvqvs", "2WYJ-HkswKg", "NHo-S6vEu1c", "FegYDz2yZto", "Lm4Qv6YAtKI", "ajLwBlo8qQ8"]
    congress_sentiment = analyze_youtube_sentiment(congress_video_ids)

    # List of video IDs for another party
    # Modify the video IDs accordingly
    bjp_video_ids = ["J-8yUaJCz9g", "5DzI96OGfxQ", "FwXql4khb-8", "crHhiZ3g2Fo", "mIUvBnbz1II", "uNvUx884-tE&t=4s",
                    "H-UbncTACFM", "87vvl39nsvg", "Lqfpiu6cjFs", "Ya8kdtfw4CM", "FSdZb32Dmv4", "z6k5WyBRvcw",
                    "vAbiXkSRLzU", "5LsLz9b29lg"]
    bjp_sentiment = analyze_youtube_sentiment(bjp_video_ids)

    aap_video_ids = ["GUOncTZdYho", "CepAJM8eVic", "JwAU_97ugkw", "1z9HVWD_TbA", "o6_eAkPLz3c", "U12b5Jsrs_s"]
    aap_sentiment = analyze_youtube_sentiment(aap_video_ids)

    bsp_video_ids = ["U-QrtgfJiL0", "rdgAFogMBoo", "zQDpDrdFMnE", "xPda7MAXSdE", "KqLHP5wX18s", "rYH7rp5p7Zk",
                    "nbvq-BborGY", "1f-RQYiE6es", "2uH3fg8ZksE", "00AYVVgjkOM"]
    bsp_sentiment = analyze_youtube_sentiment(bsp_video_ids)

    # Determine the winning party based on sentiment counts (similar to YouTube sentiment analysis)
    party_sentiments = {
        'BJP': {'Positive': bjp_positive_count, 'Neutral': bjp_neutral_count, 'Negative': bjp_negative_count},
        'Congress': {'Positive': congress_positive_count, 'Neutral': congress_neutral_count, 'Negative': congress_negative_count},
        'AAP': {'Positive': aap_positive_count, 'Neutral': aap_neutral_count, 'Negative': aap_negative_count},
        'BSP': {'Positive': bsp_positive_count, 'Neutral': bsp_neutral_count, 'Negative': bsp_negative_count}
    }
    winning_party = max(party_sentiments, key=lambda x: sum(party_sentiments[x].values()))

    # Merge data into a single context dictionary (similar to existing context merging)
    context = {
        # Existing context data...
        'congress_tweets': congress_tweets,
        'bjp_tweets': bjp_tweets,
        'aap_tweets': aap_tweets,
        'bsp_tweets': bsp_tweets,
        'congress_positive_count': congress_positive_count,
        'congress_neutral_count': congress_neutral_count,
        'congress_negative_count': congress_negative_count,
        'bjp_positive_count': bjp_positive_count,
        'bjp_neutral_count': bjp_neutral_count,
        'bjp_negative_count': bjp_negative_count,
        'aap_positive_count': aap_positive_count,
        'aap_neutral_count': aap_neutral_count,
        'aap_negative_count': aap_negative_count,
        'bsp_positive_count': bsp_positive_count,
        'bsp_neutral_count': bsp_neutral_count,
        'bsp_negative_count': bsp_negative_count,
        'congress_total_comments': congress_total_comments,
        'bjp_total_comments': bjp_total_comments,
        'aap_total_comments': aap_total_comments,
        'bsp_total_comments': bsp_total_comments,
        'party_sentiments': party_sentiments,
        'winning_party': winning_party,
        # New data for Instagram and Twitter
        'bjp4india_data': bjp4india_data,
        'incindia_data': incindia_data,
        'aap_data': aap_data,
        'bsp_data': bsp_data,
        'bjp4india_followers_data': bjp4india_followers_data,
        'bjp4india_following_data': bjp4india_following_data,
        'incindia_followers_data': incindia_followers_data,
        'incindia_following_data': incindia_following_data,
        'aap_followers_data': aap_followers_data,
        'aap_following_data': aap_following_data,
        'bsp_followers_data': bsp_followers_data,
        'bsp_following_data': bsp_following_data,
        'congress_sentiment': congress_sentiment,
        'bjp_sentiment': bjp_sentiment,
        'aap_sentiment': aap_sentiment,
        'bsp_sentiment': bsp_sentiment,
    }

    return render(request, 'dashboard/socialmedia.html', context)



# Your social view function
# def social(request):
#     # Fetch data from multiple URLs
#     bjp4india_data = get_instagram_user_info('bjp4india')
#     incindia_data = get_instagram_user_info('incindia')
#     aap_data = get_instagram_user_info('aamaadmiparty')
#     bsp_data = get_instagram_user_info('bsp4india_')

#     # Fetch data from Twitter for followers and following for both BJP and INCIndia
#     bjp4india_followers_data = get_twitter_user_info('BJP4India', 'followers')
#     bjp4india_following_data = get_twitter_user_info('BJP4India', 'following')
    
#     incindia_followers_data = get_twitter_user_info('INCIndia', 'followers')
#     incindia_following_data = get_twitter_user_info('INCIndia', 'following')

#     aap_followers_data = get_twitter_user_info('AamAadmiParty', 'followers')
#     aap_following_data = get_twitter_user_info('AamAadmiParty', 'following')

#     bsp_followers_data = get_twitter_user_info('bspindia', 'followers')
#     bsp_following_data = get_twitter_user_info('bspindia', 'following')

#     congress_hashtags = ["#congress", "#rahulgandhi", "#voteforcongress", "#INC", "#SoniaGandhi", "#CongressParty", "#IndianNationalCongress", "#CongressForIndia", "#PriyankaGandhi", "#rahulgandhi", "#CongressManifesto"]
#     bjp_hashtags = ["#NarendraModi", "#BJP", "#Modi", "#bjpgovt", "#votebjp", "#voteforbjp", "#yogiadityanath", "#bjpindia", "#bharatiyajanataparty", "#pmmodi", "#JPNadda"]
#     # List of hashtags for AAP party
#     aap_hashtags = ["#AAP", "#ArvindKejriwal", "#AamAadmiParty", "#kejriwal", "#aapgovt", "#voteaap", "#dilipkpandey", "#AAP_का_सच", "#AAPReducesElectricityRates", "#AAP_सरकार_जनता_की_सरकार"]

# # List of hashtags for BSP party
#     bsp_hashtags = ["#BSP", "#Mayawati", "#BahujanSamajParty", "#Dalit", "#BSPGovt", "#votebsp", "#dalits", "#BSPMissionUP", "#BSPRocks", "#BSP_संग_गठबंधन"]


#     # Fetch tweets for Congress and BJP
#     congress_tweets = fetch_tweets(congress_hashtags)
#     bjp_tweets = fetch_tweets(bjp_hashtags)

#     tweets = congress_tweets + bjp_tweets

#     # List of video IDs for Congress
#     congress_video_ids = ["tCoubnfvqvs", "2WYJ-HkswKg", "NHo-S6vEu1c", "FegYDz2yZto", "Lm4Qv6YAtKI", "ajLwBlo8qQ8"]
#     congress_sentiment = analyze_youtube_sentiment(congress_video_ids)

#     # List of video IDs for another party
#     # Modify the video IDs accordingly
#     bjp_video_ids = ["J-8yUaJCz9g", "5DzI96OGfxQ", "FwXql4khb-8", "crHhiZ3g2Fo", "mIUvBnbz1II", "uNvUx884-tE&t=4s",
#                     "H-UbncTACFM", "87vvl39nsvg", "Lqfpiu6cjFs", "Ya8kdtfw4CM", "FSdZb32Dmv4", "z6k5WyBRvcw",
#                     "vAbiXkSRLzU", "5LsLz9b29lg"]
#     bjp_sentiment = analyze_youtube_sentiment(bjp_video_ids)

#     aap_video_ids = ["GUOncTZdYho", "CepAJM8eVic", "JwAU_97ugkw", "1z9HVWD_TbA", "o6_eAkPLz3c", "U12b5Jsrs_s"]
#     aap_sentiment = analyze_youtube_sentiment(aap_video_ids)

#     bsp_video_ids = ["U-QrtgfJiL0", "rdgAFogMBoo", "zQDpDrdFMnE", "xPda7MAXSdE", "KqLHP5wX18s", "rYH7rp5p7Zk",
#                     "nbvq-BborGY", "1f-RQYiE6es", "2uH3fg8ZksE", "00AYVVgjkOM"]
#     bsp_sentiment = analyze_youtube_sentiment(bsp_video_ids)

#     congress_hashtags = ["#congress", "#rahulgandhi", "#voteforcongress", "#INC", "#SoniaGandhi", "#CongressParty", "#IndianNationalCongress", "#CongressForIndia", "#PriyankaGandhi", "#rahulgandhi", "#CongressManifesto"]
#     bjp_hashtags = ["#NarendraModi", "#BJP", "#Modi", "#bjpgovt", "#votebjp", "#voteforbjp", "#yogiadityanath", "#bjpindia", "#bharatiyajanataparty", "#pmmodi", "#JPNadda"]

#     congress_tweets, congress_positive_count, congress_neutral_count, congress_negative_count = fetch_tweets(congress_hashtags)
#     bjp_tweets, bjp_positive_count, bjp_neutral_count, bjp_negative_count = fetch_tweets(bjp_hashtags)

#     # Calculate total comments for each party
#     congress_total_comments = len(congress_tweets)
#     bjp_total_comments = len(bjp_tweets)

#     # Determine the winning party based on sentiment counts
#     party_sentiments = { 'BJP': bjp_sentiment, 'Congress': congress_sentiment, 'AAP': aap_sentiment, 'BSP': bsp_sentiment }
#     winning_party = max(party_sentiments, key=lambda x: sum(party_sentiments[x].values()))

#     # Merge data into a single context dictionary
#     context = {
#         'bjp4india_data': bjp4india_data,
#         'incindia_data': incindia_data,
#         'aap_data': aap_data,
#         'bsp_data': bsp_data,
#         'bjp4india_followers_data': bjp4india_followers_data,
#         'bjp4india_following_data': bjp4india_following_data,
#         'incindia_followers_data': incindia_followers_data,
#         'incindia_following_data': incindia_following_data,
#         'aap_followers_data': aap_followers_data,
#         'aap_following_data': aap_following_data,
#         'bsp_followers_data': bsp_followers_data,
#         'bsp_following_data': bsp_following_data,
#         'tweets': tweets,
#         'congress_sentiment': congress_sentiment,
#         'bjp_sentiment': bjp_sentiment,
#         'aap_sentiment': aap_sentiment,
#         'bsp_sentiment': bsp_sentiment,
#         'congress_tweets': congress_tweets,
#         'bjp_tweets': bjp_tweets,
#         'congress_positive_count': congress_positive_count,
#         'congress_neutral_count': congress_neutral_count,
#         'congress_negative_count': congress_negative_count,
#         'bjp_positive_count': bjp_positive_count,
#         'bjp_neutral_count': bjp_neutral_count,
#         'bjp_negative_count': bjp_negative_count,
#         'party_sentiments': party_sentiments,
#         'winning_party': winning_party
#     }

#     return render(request, 'dashboard/socialmedia.html', context)


# def fetch_wikipedia_data():
#     # URL of the Wikipedia page
#     url = "https://en.wikipedia.org/wiki/Opinion_polling_for_the_2024_Indian_general_election"

#     # Fetch the HTML content of the page
#     response = requests.get(url)
#     html_content = response.text

#     # Parse the HTML content using BeautifulSoup
#     soup = BeautifulSoup(html_content, "html.parser")

#     # Find all tables on the page
#     tables = soup.find_all("table", {"class": "wikitable"})

#     # Custom column headings for each table
#     column_headings = [
#         ['Polling agency', 'Date published', 'Sample size', 'Margin of Error', 'NDA', 'I.N.D.I.A.', 'Others', 'Lead'],
#         ['Polling agency', 'Date published', 'Sample size', 'Margin of Error', 'NDA', 'I.N.D.I.A.', 'Others', 'Lead']
#     ]

#     # Table headings
#     table_headings = ['Vote Share Projections', 'Seat Projections']

#     # Prepare data to be returned
#     data = []

#     for index, (table, headings, table_heading) in enumerate(zip(tables[:2], column_headings, table_headings), 1):
#         table_data = {'table_heading': table_heading, 'headings': headings, 'data': []}

#         # Print column headings only if they haven't been printed already
#         if index == 1:
#             table_data['headings_printed'] = True
#         else:
#             table_data['headings_printed'] = False

#         # Print table data
#         rows = table.find_all("tr")
#         for i, row in enumerate(rows):
#             cells = row.find_all(["th", "td"])
#             row_data = [cell.get_text(strip=True) for cell in cells]

#             # Skip two rows after printing headings
#             if i < 2:
#                 continue

#             table_data['data'].append(row_data)

#         data.append(table_data)

#     return data

# def home_view(request):
#     grand_total_data = PollingData.objects.filter(state='GRAND TOTAL').first()
#     gwomen_column = grand_total_data.gwomen if grand_total_data else None
#     gmen_column = grand_total_data.gmen if grand_total_data else None
#     gthird_column = grand_total_data.gthird if grand_total_data else None
#     gtotal_column = grand_total_data.gtotal if grand_total_data else None

#     general_men_count = grand_total_data.gmen if grand_total_data else None
#     general_women_count = grand_total_data.gwomen if grand_total_data else None
#     general_third_count = grand_total_data.gthird if grand_total_data else None

#     overseas_men_count = grand_total_data.omen if grand_total_data else None
#     overseas_women_count = grand_total_data.owomen if grand_total_data else None
#     overseas_third_count = grand_total_data.othird if grand_total_data else None

#     service_men_count = grand_total_data.smen if grand_total_data else None
#     service_women_count = grand_total_data.swomen if grand_total_data else None

#     general_men_ratio = (grand_total_data.gmen / grand_total_data.gtotal) * 100 if grand_total_data and grand_total_data.gtotal != 0 else 0
#     general_women_ratio = (grand_total_data.gwomen / grand_total_data.gtotal) * 100 if grand_total_data and grand_total_data.gtotal != 0 else 0
#     general_third_ratio = (grand_total_data.gthird / grand_total_data.gtotal) * 100 if grand_total_data and grand_total_data.gtotal != 0 else 0

#     overseas_men_ratio = (grand_total_data.omen / grand_total_data.ototal) * 100 if grand_total_data and grand_total_data.ototal != 0 else 0
#     overseas_women_ratio = (grand_total_data.owomen / grand_total_data.ototal) * 100 if grand_total_data and grand_total_data.ototal != 0 else 0
#     overseas_third_ratio = (grand_total_data.othird / grand_total_data.ototal) * 100 if grand_total_data and grand_total_data.ototal != 0 else 0

#     service_men_ratio = (grand_total_data.smen / grand_total_data.stotal) * 100 if grand_total_data and grand_total_data.stotal != 0 else 0
#     service_women_ratio = (grand_total_data.swomen / grand_total_data.stotal) * 100 if grand_total_data and grand_total_data.stotal != 0 else 0

#     polling_data = PollingData.objects.all()

#     labels = [data.polling_station for data in polling_data]
#     gmens = [data.gmen for data in polling_data]
#     gwomen = [data.gwomen for data in polling_data]
#     gthird = [data.gthird for data in polling_data]

#     wikipedia_data = fetch_wikipedia_data()


    

#     context = {
#         'gwomen_column': gwomen_column,
#         'gmen_column': gmen_column,
#         'gthird_column': gthird_column,
#         'gtotal_column': gtotal_column,
#         'general_men_count': general_men_count,
#         'general_women_count': general_women_count,
#         'general_third_count': general_third_count,
#         'overseas_men_count': overseas_men_count,
#         'overseas_women_count': overseas_women_count,
#         'overseas_third_count': overseas_third_count,
#         'service_men_count': service_men_count,
#         'service_women_count': service_women_count,
#         'general_men_ratio': general_men_ratio,
#         'general_women_ratio': general_women_ratio,
#         'general_third_ratio': general_third_ratio,
#         'overseas_men_ratio': overseas_men_ratio,
#         'overseas_women_ratio': overseas_women_ratio,
#         'overseas_third_ratio': overseas_third_ratio,
#         'service_men_ratio': service_men_ratio,
#         'service_women_ratio': service_women_ratio,
#         'labels': labels,
#         'gmens': gmens,
#         'gwomen': gwomen,
#         'gthird': gthird,
#         'wikipedia_data': wikipedia_data,
        
#     }

#     return render(request, 'dashboard/home.html', context)


# def history_search(request):
#     if request.method == 'GET':
#         # Retrieve distinct states and years
#         states = History.objects.values_list('state', flat=True).distinct()
#         years = History.objects.values_list('year', flat=True).distinct()
#         selected_state = request.GET.get('state')
#         selected_year = request.GET.get('year')

#         # Define NDA and UPA party lists
#         nda_parties = ["Bharatiya Janata Party", "Shiv Sena", "Janata Dal (United)", "Lok Janshakti Party"]
#         upa_parties = ["Indian National Congress", "Nationalist Congress Party", "Dravida Munnetra Kazhagam"]

#         # Initialize context with states and years
#         context = {
#             'states': states,
#             'years': years,
#             'selected_state': selected_state,
#             'selected_year': selected_year,
#             'party_stats': None,  # Initialize party_stats to None by default
#             'punjab_election_data': None,  # Initialize punjab_election_data to None by default
#             'election_data': None,  # Initialize election_data to None by default
#             'upa_seats': 0,
#             'upa_votes_percent': 0,
#             'upa_contested_voteshare': 0,
#             'nda_seats': 0,
#             'nda_votes_percent': 0,
#         }

#         if selected_state and selected_year:
#             # Filter election data based on selected state and year
#             election_data = History.objects.filter(state=selected_state, year=selected_year)

#             # Calculate party statistics
#             party_stats = {}
#             upa_seats = 0
#             upa_votes = 0
#             nda_seats = 0
#             nda_votes = 0
#             for record in election_data:
#                 party = record.party
#                 seats = party_stats.get(party, {'seats': 0, 'votes': 0})
#                 seats['seats'] += 1
#                 seats['votes'] += record.votes
#                 party_stats[party] = seats

#                 if party in upa_parties:
#                     upa_seats += 1
#                     upa_votes += record.votes
#                 elif party in nda_parties:
#                     nda_seats += 1
#                     nda_votes += record.votes

#             # Calculate total votes
#             total_votes = sum(record.votes for record in election_data)

#             # Calculate votes percentage per party
#             for party, stats in party_stats.items():
#                 stats['votes_percent'] = (stats['votes'] / total_votes) * 100

#             # Calculate UPA and NDA votes percentage
#             total_votes = sum(record.votes for record in election_data)
#             upa_votes_percent = (upa_votes / total_votes) * 100
#             nda_votes_percent = (nda_votes / total_votes) * 100

#             # Update context with party statistics
#             context['party_stats'] = party_stats

#             # Update context with election statistics
#             context['upa_seats'] = upa_seats
#             context['upa_votes_percent'] = upa_votes_percent
#             context['nda_seats'] = nda_seats
#             context['nda_votes_percent'] = nda_votes_percent

#             electors_total = sum(record.electors for record in election_data)
#             votes_polled_total = sum(record.votes for record in election_data)
#             num_pc = election_data.count()
#             num_general = election_data.filter(type='GEN').count()
#             num_sc = election_data.filter(type='SC').count()
#             num_bye_election = election_data.filter(type='Bye Election').count()
#             context.update({
#                 'electors_total': electors_total,
#                 'votes_polled_total': votes_polled_total,
#                 'turnout_average': votes_polled_total / electors_total * 100 if electors_total != 0 else 0,
#                 'num_pc': num_pc,
#                 'num_general': num_general,
#                 'num_sc': num_sc,
#                 'num_bye_election': num_bye_election,
#             })

#             # Fetch election data for Punjab
#             punjab_election_data = election_data.filter(state='Punjab')

#             context['punjab_election_data'] = punjab_election_data

#             # Update context with election data for the selected state
#             context['election_data'] = election_data

#             # Add NDA and UPA parties to the party stats
#             for party, stats in party_stats.items():
#                 if party in nda_parties:
#                     stats['alliance'] = 'NDA'
#                 elif party in upa_parties:
#                     stats['alliance'] = 'UPA'
#                 else:
#                     stats['alliance'] = 'Others'

#         return render(request, 'dashboard/history_election.html', context)
#     else:
#         return render(request, 'dashboard/history_election.html')
    


# def state_data(request):
#     # Retrieve state-wise election data from the database
#     states = History.objects.values('state').distinct()

#     state_data = []
#     for state in states:
#         state_name = state['state']
#         data = History.objects.filter(state=state_name).values('party', 'margin')
#         party_counts = {}
#         party_margin_percentage = {}
#         total_margin = 0
#         for row in data:
#             party = row['party']
#             margin = row['margin']
#             total_margin += margin
#             if party in party_counts:
#                 party_counts[party] += 1
#             else:
#                 party_counts[party] = 1
#         # Calculate the margin percentage for each party
#         for party, count in party_counts.items():
#             party_margin_percentage[party] = (party_counts[party] / total_margin) * 100
#         state_data.append({'state_name': state_name, 'party_counts': party_counts, 'party_margin_percentage': party_margin_percentage})

#     return render(request, 'dashboard/state.html', {'state_data': state_data})


# def about_us(request):

#     return render(request, 'dashboard/about_us.html')

# def feedback(request):

#     return render(request, 'dashboard/feedback.html')

def news_list(request):
    url = "https://real-time-news-data.p.rapidapi.com/search"
    querystring = {"query": "BJP", "country": "IN", "lang": "en", "time_published": "7d"}
    headers = {
        # "X-RapidAPI-Key": "2f8e4431a1msh4c20224a3df5fap15bc31jsnb430596ce1e2",
        # "X-RapidAPI-Key": "2f8e4431a1msh4cc20224a3df5fap15bc31jsnb430596ce1e2",
        # "X-RapidAPI-Host": "real-time-news-data.p.rapidapi.com",
        # "X-RapidAPI-Key": "2f8e4431a1msh4cc20224a3df5fap15bc31jsnb430596ce1e2",
        "X-RapidAPI-Key": "98544df8bfmsh0477d0edeb89c70p1890c6jsnf0abc33340de",
	"X-RapidAPI-Host": "real-time-news-data.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()
    articles = []
    if 'status' in data and data['status'] == "OK" and 'data' in data:
        count = 0
        for article in data['data']:
            articles.append({
                'title': article['title'],
                'published_date': article['published_datetime_utc']
            })
            count += 1
            if count == 30:  # Limiting to top 30 articles
                break


    url = "https://real-time-news-data.p.rapidapi.com/search"
    querystring = {"query": "Congress", "country": "IN", "lang": "en", "time_published": "7d"}
    headers = {
        # "X-RapidAPI-Key": "2f8e4431a1msh4cc20224a3df5fap15bc31snb430596ce1e2",
        # "X-RapidAPI-Host": "real-time-news-data.p.rapidapi.com",
        # "X-RapidAPI-Key": "2f8e4431a1msh4cc20224a3df5fap15bc31jsnb430596ce1e2",
        "X-RapidAPI-Key": "98544df8bfmsh0477d0edeb89c70p1890c6jsnf0abc33340de",
	"X-RapidAPI-Host": "real-time-news-data.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()
    articles_congress = []
    if 'status' in data and data['status'] == "OK" and 'data' in data:
        count = 0
        for article in data['data']:
            articles_congress.append({
                'title': article['title'],
                'published_date': article['published_datetime_utc']
            })
            count += 1
            if count == 30:  # Limiting to top 30 articles
                break

    
    url = "https://real-time-news-data.p.rapidapi.com/search"
    querystring = {"query":"AAP", "country": "IN", "lang": "en", "time_published": "7d"}
    headers = {
        # "X-RapidAPI-Key": "2f8e4431a1msh4c20224a3df5fap15bc31jsnb430596ce1e2",
        # "X-RapidAPI-Key": "2f8e4431a1msh4cc20224a3df5fap15bc31jsnb430596ce1e2",
        # "X-RapidAPI-Host": "real-time-news-data.p.rapidapi.com"
        # "X-RapidAPI-Key": "2f8e4431a1msh4cc20224a3df5fap15bc31jsnb430596ce1e2",
        "X-RapidAPI-Key": "98544df8bfmsh0477d0edeb89c70p1890c6jsnf0abc33340de",
	"X-RapidAPI-Host": "real-time-news-data.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()
    articles_aap = []
    if 'status' in data and data['status'] == "OK" and 'data' in data:
        count = 0
        for article in data['data']:
            articles_aap.append({
                'title': article['title'],
                'published_date': article['published_datetime_utc']
            })
            count += 1
            if count == 30:  # Limiting to top 30 articles
                break

    url = "https://real-time-news-data.p.rapidapi.com/search"
    querystring = {"query": "BSP", "country": "IN", "lang": "en", "time_published": "7d"}
    headers = {
        # "X-RapidAPI-Key": "2f8e4431a1msh4cc20224a3df5fap15bc31snb430596ce1e2",
        # "X-RapidAPI-Host": "real-time-news-data.p.rapidapi.com",
        # "X-RapidAPI-Key": "2f8e4431a1msh4cc20224a3df5fap15bc31jsnb430596ce1e2",
        "X-RapidAPI-Key": "98544df8bfmsh0477d0edeb89c70p1890c6jsnf0abc33340de",
	    "X-RapidAPI-Host": "real-time-news-data.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()
    articles_bsp = []
    if 'status' in data and data['status'] == "OK" and 'data' in data:
        count = 0
        for article in data['data']:
            articles_bsp.append({
                'title': article['title'],
                'published_date': article['published_datetime_utc']
            })
            count += 1
            if count == 30:  # Limiting to top 30 articles
                break
    
    # Merge data into a single context dictionary
    context = {
        'articles': articles,
        'articles_congress' : articles_congress,
        'articles_aap' : articles_aap,
        'articles_bsp' : articles_bsp,
    }

    return render(request, 'dashboard/news.html', context)
def fetch_wikipedia_data():
    # URL of the Wikipedia page
    url = "https://en.wikipedia.org/wiki/Opinion_polling_for_the_2024_Indian_general_election"

    # Fetch the HTML content of the page
    response = requests.get(url)
    html_content = response.text

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Find all tables on the page
    tables = soup.find_all("table", {"class": "wikitable"})

    # Custom column headings for each table
    column_headings = [
        ['Polling agency', 'Date published', 'Sample size', 'Margin of Error', 'NDA', 'I.N.D.I.A.', 'Others', 'Lead'],
        ['Polling agency', 'Date published', 'Sample size', 'Margin of Error', 'NDA', 'I.N.D.I.A.', 'Others', 'Lead']
    ]

    # Table headings
    table_headings = ['Vote Share Projections', 'Seat Projections']

    # Prepare data to be returned
    data = []

    for index, (table, headings, table_heading) in enumerate(zip(tables[:2], column_headings, table_headings), 1):
        table_data = {'table_heading': table_heading, 'headings': headings, 'data': []}

        # Print column headings only if they haven't been printed already
        if index == 1:
            table_data['headings_printed'] = True
        else:
            table_data['headings_printed'] = False

        # Print table data
        rows = table.find_all("tr")
        for i, row in enumerate(rows):
            cells = row.find_all(["th", "td"])
            row_data = [cell.get_text(strip=True) for cell in cells]

            # Skip two rows after printing headings
            if i < 2:
                continue

            table_data['data'].append(row_data)

        data.append(table_data)

    return data

def exitpoll_view(request):
    wikipedia_data = fetch_wikipedia_data()

    context = {
        'wikipedia_data': wikipedia_data,
    }

    return render(request, 'dashboard/exitpoll.html', context)

def index_view(request):
    grand_total_data = PollingData.objects.filter(state='GRAND TOTAL').first()
    gwomen_column = grand_total_data.gwomen if grand_total_data else None
    gmen_column = grand_total_data.gmen if grand_total_data else None
    gthird_column = grand_total_data.gthird if grand_total_data else None
    gtotal_column = grand_total_data.gtotal if grand_total_data else None

    general_men_count = grand_total_data.gmen if grand_total_data else None
    general_women_count = grand_total_data.gwomen if grand_total_data else None
    general_third_count = grand_total_data.gthird if grand_total_data else None

    overseas_men_count = grand_total_data.omen if grand_total_data else None
    overseas_women_count = grand_total_data.owomen if grand_total_data else None
    overseas_third_count = grand_total_data.othird if grand_total_data else None

    service_men_count = grand_total_data.smen if grand_total_data else None
    service_women_count = grand_total_data.swomen if grand_total_data else None

    general_men_ratio = (grand_total_data.gmen / grand_total_data.gtotal) * 100 if grand_total_data and grand_total_data.gtotal != 0 else 0
    general_women_ratio = (grand_total_data.gwomen / grand_total_data.gtotal) * 100 if grand_total_data and grand_total_data.gtotal != 0 else 0
    general_third_ratio = (grand_total_data.gthird / grand_total_data.gtotal) * 100 if grand_total_data and grand_total_data.gtotal != 0 else 0

    overseas_men_ratio = (grand_total_data.omen / grand_total_data.ototal) * 100 if grand_total_data and grand_total_data.ototal != 0 else 0
    overseas_women_ratio = (grand_total_data.owomen / grand_total_data.ototal) * 100 if grand_total_data and grand_total_data.ototal != 0 else 0
    overseas_third_ratio = (grand_total_data.othird / grand_total_data.ototal) * 100 if grand_total_data and grand_total_data.ototal != 0 else 0

    service_men_ratio = (grand_total_data.smen / grand_total_data.stotal) * 100 if grand_total_data and grand_total_data.stotal != 0 else 0
    service_women_ratio = (grand_total_data.swomen / grand_total_data.stotal) * 100 if grand_total_data and grand_total_data.stotal != 0 else 0

    polling_data = PollingData.objects.all()

    labels = [data.polling_station for data in polling_data]
    gmens = [data.gmen for data in polling_data]
    gwomen = [data.gwomen for data in polling_data]
    gthird = [data.gthird for data in polling_data]

    context = {
        'gwomen_column': gwomen_column,
        'gmen_column': gmen_column,
        'gthird_column': gthird_column,
        'gtotal_column': gtotal_column,
        'general_men_count': general_men_count,
        'general_women_count': general_women_count,
        'general_third_count': general_third_count,
        'overseas_men_count': overseas_men_count,
        'overseas_women_count': overseas_women_count,
        'overseas_third_count': overseas_third_count,
        'service_men_count': service_men_count,
        'service_women_count': service_women_count,
        'general_men_ratio': general_men_ratio,
        'general_women_ratio': general_women_ratio,
        'general_third_ratio': general_third_ratio,
        'overseas_men_ratio': overseas_men_ratio,
        'overseas_women_ratio': overseas_women_ratio,
        'overseas_third_ratio': overseas_third_ratio,
        'service_men_ratio': service_men_ratio,
        'service_women_ratio': service_women_ratio,
        'labels': labels,
        'gmens': gmens,
        'gwomen': gwomen,
        'gthird': gthird,
    }

    return render(request, 'dashboard/index.html', context)

def history_search(request):
    if request.method == 'GET':
        # Retrieve distinct states and years
        states = History.objects.values_list('state', flat=True).distinct()
        years = History.objects.values_list('year', flat=True).distinct()
        selected_state = request.GET.get('state')
        selected_year = request.GET.get('year')

        # Define NDA and UPA party lists
        nda_parties = ["Bharatiya Janata Party", "Shiv Sena", "Janata Dal (United)", "Lok Janshakti Party"]
        upa_parties = ["Indian National Congress", "Nationalist Congress Party", "Dravida Munnetra Kazhagam"]

        # Initialize context with states and years
        context = {
            'states': states,
            'years': years,
            'selected_state': selected_state,
            'selected_year': selected_year,
            'party_stats': None,  # Initialize party_stats to None by default
            'punjab_election_data': None,  # Initialize punjab_election_data to None by default
            'election_data': None,  # Initialize election_data to None by default
            'upa_seats': 0,
            'upa_votes_percent': 0,
            'upa_contested_voteshare': 0,
            'nda_seats': 0,
            'nda_votes_percent': 0,
        }

        if selected_state and selected_year:
            # Filter election data based on selected state and year
            election_data = History.objects.filter(state=selected_state, year=selected_year)

            # Calculate party statistics
            party_stats = {}
            upa_seats = 0
            upa_votes = 0
            nda_seats = 0
            nda_votes = 0
            for record in election_data:
                party = record.party
                seats = party_stats.get(party, {'seats': 0, 'votes': 0})
                seats['seats'] += 1
                seats['votes'] += record.votes
                party_stats[party] = seats

                if party in upa_parties:
                    upa_seats += 1
                    upa_votes += record.votes
                elif party in nda_parties:
                    nda_seats += 1
                    nda_votes += record.votes

            # Calculate total votes
            total_votes = sum(record.votes for record in election_data)

            # Calculate votes percentage per party
            for party, stats in party_stats.items():
                stats['votes_percent'] = (stats['votes'] / total_votes) * 100

            # Calculate UPA and NDA votes percentage
            total_votes = sum(record.votes for record in election_data)
            upa_votes_percent = (upa_votes / total_votes) * 100
            nda_votes_percent = (nda_votes / total_votes) * 100

            # Update context with party statistics
            context['party_stats'] = party_stats

            # Update context with election statistics
            context['upa_seats'] = upa_seats
            context['upa_votes_percent'] = upa_votes_percent
            context['nda_seats'] = nda_seats
            context['nda_votes_percent'] = nda_votes_percent

            electors_total = sum(record.electors for record in election_data)
            votes_polled_total = sum(record.votes for record in election_data)
            num_pc = election_data.count()
            num_general = election_data.filter(type='GEN').count()
            num_sc = election_data.filter(type='SC').count()
            num_bye_election = election_data.filter(type='Bye Election').count()
            context.update({
                'electors_total': electors_total,
                'votes_polled_total': votes_polled_total,
                'turnout_average': votes_polled_total / electors_total * 100 if electors_total != 0 else 0,
                'num_pc': num_pc,
                'num_general': num_general,
                'num_sc': num_sc,
                'num_bye_election': num_bye_election,
            })

            # Fetch election data for Punjab
            punjab_election_data = election_data.filter(state='Punjab')

            context['punjab_election_data'] = punjab_election_data

            # Update context with election data for the selected state
            context['election_data'] = election_data

            # Add NDA and UPA parties to the party stats
            for party, stats in party_stats.items():
                if party in nda_parties:
                    stats['alliance'] = 'NDA'
                elif party in upa_parties:
                    stats['alliance'] = 'UPA'
                else:
                    stats['alliance'] = 'Others'

        return render(request, 'dashboard/history.html', context)
    else:
        return render(request, 'dashboard/history.html')
    


def state_data(request):
    # Retrieve state-wise election data from the database
    states = History.objects.values('state').distinct()

    state_data = []
    for state in states:
        state_name = state['state']
        data = History.objects.filter(state=state_name).values('party', 'margin')
        party_counts = {}
        party_margin_percentage = {}
        total_margin = 0
        for row in data:
            party = row['party']
            margin = row['margin']
            total_margin += margin
            if party in party_counts:
                party_counts[party] += 1
            else:
                party_counts[party] = 1
        # Calculate the margin percentage for each party
        for party, count in party_counts.items():
            party_margin_percentage[party] = (party_counts[party] / total_margin) * 100
        state_data.append({'state_name': state_name, 'party_counts': party_counts, 'party_margin_percentage': party_margin_percentage})

    return render(request, 'dashboard/state.html', {'state_data': state_data})

def aboutus(request):
    return render(request, 'dashboard/about.html')

def feedback(request):
    return render(request, 'dashboard/feedback.html')

def predict(request):
    # URL of the webpage containing the tables
    url = "https://en.wikipedia.org/wiki/Opinion_polling_for_the_2024_Indian_general_election"

    # List of table indexes
    table_indexes = [2, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 44, 45, 46, 48, 50, 51, 53, 55, 56, 58, 60, 61, 63, 65]

    # List of heading strings (corresponding to table indexes)
    heading_strings = ["Andaman and Nicobar Islands", "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chandigarh",
                      "Chhattisgarh", "Dadra and Nagar Haveli and Daman and Diu", "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jammu and Kashmir",
                      "Jharkhand", "Karnataka", "Kerala", "Ladakh", "Lakshadweep", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya",
                      "Mizoram", "Nagaland", "NCT of Delhi", "Odisha", "Puducherry", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana",
                      "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal"]

    # Target row number (change to 3 for the third row)
    row_number = 3

    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all tables on the webpage
    tables = soup.find_all('table', {'class': 'wikitable'})

    # Ensure table indexes and heading strings have the same length
    if len(table_indexes) != len(heading_strings):
        error_message = "Error: Table indexes and heading strings must have the same length."
        return render(request, 'your_app/error.html', {'error_message': error_message})

    # Create an empty list to store table data
    table_data = []

    # Iterate over each table index and corresponding heading
    for table_index, heading in zip(table_indexes, heading_strings):
        # Check if the table index is within the range of available tables
        if table_index < len(tables):
            # Extract the table corresponding to the index
            table = tables[table_index]

            # Extract the rows from the table
            rows = table.find_all('tr')

            # Validate the requested row number (ensure it's within range)
            if row_number < 1 or row_number > len(rows):
                error_message = f"Invalid row number: {row_number} (Table has {len(rows)} rows)"
                return render(request, 'your_app/error.html', {'error_message': error_message})

            # Access the requested row (excluding header row)
            target_row = rows[row_number - 1]  # Adjust index for zero-based indexing

            # Extract the last column value from the target row (assuming winner)
            target_row_cells = target_row.find_all(['th', 'td'])
            if target_row_cells:
                last_column_value = target_row_cells[-1].get_text(strip=True)
                table_data.append({"State": heading, "Winner": last_column_value})
            else:
                no_data_message = f"No data available in row {row_number}"
                return render(request, 'dashboard/predict.html', {'error_message': no_data_message})
        else:
            out_of_range_message = f"Table index {table_index} out of range."
            return render(request, 'dashboard/predict.html', {'error_message': out_of_range_message})

    # Render the table data in the template
    return render(request, 'dashboard/predict.html', {'table_data': table_data})

def tweets(request):

    congress_hashtags = ["#congress", "#rahulgandhi", "#voteforcongress", "#INC", "#SoniaGandhi", "#CongressParty", "#IndianNationalCongress", "#CongressForIndia", "#PriyankaGandhi", "#rahulgandhi", "#CongressManifesto"]
    bjp_hashtags = ["#NarendraModi", "#BJP", "#Modi", "#bjpgovt", "#votebjp", "#voteforbjp", "#yogiadityanath", "#bjpindia", "#bharatiyajanataparty", "#pmmodi", "#JPNadda"]

    congress_tweets = fetch_tweets(congress_hashtags)
    bjp_tweets = fetch_tweets(bjp_hashtags)

    tweets = congress_tweets + bjp_tweets
    
    # Merge data into a single context dictionary
    context = {
        'tweets': tweets,
    }

    return render(request, 'dashboard/tweets.html', context)
