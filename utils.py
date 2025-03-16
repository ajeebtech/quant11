from nltk.corpus import stopwords
import nltk
from transformers import pipeline
import requests
from bs4 import BeautifulSoup
import random
import os
import json

class Player:
    def __init__(self,name,team):
        self.name = name
        self.team = team

    def teamcode(self):
        self.team = twt_ids[self.team]


xrapidapikey = os.getenv("x-rapidapi-key")
twt_ids = {'csk':'117407834','dc':'176888549','rcb':'70931004','mi':'106345557',
           'srh':'989137039','pbks':'30631766','kkr':'23592970','gt':'1476438846988427265',
           'lsg':'4824087681','rr':'17082958'}
def sentiment(document,subject):     # do this for twitter as well
    nltk.download("stopwords")
    stop_words = set(stopwords.words("english"))
    url = "https://twitter241.p.rapidapi.com/user-tweets"

    querystring = {"user":subject.team,"count":"5"}

    headers = {
        "x-rapidapi-key": xrapidapikey,
        "x-rapidapi-host": "twitter241.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    full_texts = []

    for instruction in response:
        if "entries" in instruction:
            for entry in instruction["entries"]:
                if "full_text" in entry:
                    subject_words = subject.split()
                    if all(word in entry["full_text"] for word in subject_words):
                        full_texts.append(entry["full_text"])
    document = [word for word in document+f' {full_texts}' if word.lower() not in stop_words]

    with open('twt.json', 'w') as f:
        json.dump(response.json(),f,indent=4)
    print(response.json())
    classifier = pipeline("sentiment-analysis", model="distilbert/distilbert-base-uncased-finetuned-sst-2-english")
    results = classifier(document)
    total_score = 0
    positive_count = 0
    negative_count = 0

    for word, result in zip(document, results):
        label = result['label']
        score = result['score']
        
        total_score += score if label == "POSITIVE" else -score
        if label == "POSITIVE":
            positive_count += 1
        else:
            negative_count += 1

    avg_score = total_score / len(document)

    if avg_score > 0.5:
        overall_sentiment = "OVERALL POSITIVE"
    elif avg_score < -0.5:
        overall_sentiment = "OVERALL NEGATIVE"
    else:
        overall_sentiment = "MIXED/NEUTRAL"

    return [avg_score,overall_sentiment]

def load_cookies_from_file(driver, file_path):
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('#') or not line.strip():
                continue
                
            try:
                fields = line.strip().split('\t')
                if len(fields) >= 7:
                    cookie = {
                        'domain': fields[0],
                        'path': fields[2],
                        'name': fields[5],
                        'value': fields[6],
                        'secure': fields[3] == 'TRUE',
                    }
                    if fields[4].isdigit():
                        cookie['expiry'] = int(fields[4])
                    try:
                        driver.add_cookie(cookie)
                        print(f"Added cookie: {cookie['name']}")
                    except Exception as e:
                        print(f"Failed to add cookie {cookie['name']}: {e}")
            except Exception as e:
                print(f"Error processing line: {line.strip()}")
                print(f"Error: {e}")

def plyrvsplyr(player1, player2):
    pass

def player_to_json(player):
    pass

def newscheck(subject):
    pass

def getplayers(match_link):
    # get all the playing xi
    pass

def making_changes():
    pass

def weather():
    pass

