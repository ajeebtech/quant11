from nltk.corpus import stopwords
import nltk
from transformers import pipeline
import requests
from bs4 import BeautifulSoup
import random
import os
import json
import re
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
options = Options()
options.headless = True

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
team_ids = {'csk':'58','dc':'61','rcb':'59','mi':'62','srh':'255','pbks':'65',
            'kkr':'63','gt':'971','lsg':'966','rr':'64'}               # for cricbuzz

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

def load_cookies_from_json(driver, file_path):
    with open(file_path, "r") as f:
        cookies = json.load(f)
    
    for cookie in cookies:
        driver.add_cookie(cookie)
    
    print("✅ Cookies loaded successfully!")

def plyrvsplyr(player1, player2):
    pass


def newscheck(subject):
    pass

def getplayers(team1,team2,matchid):
    url = "https://unofficial-cricbuzz.p.rapidapi.com/matches/get-team"
    headers = {
        "x-rapidapi-key": "177d2b042emsh8c4f4a1cfc76311p144f8fjsn1f1e347b1c89",
        "x-rapidapi-host": "unofficial-cricbuzz.p.rapidapi.com"
    }

    match_id = matchid
    team_ids = [team_ids[team1], team_ids[team2]]

    playing_xi = {}

    for team_id in team_ids:
        querystring = {"matchId": match_id, "teamId": team_id}
        response = requests.get(url, headers=headers, params=querystring)

        if response.status_code == 200:
            playing_xi[team_id] = response.json()
        else:
            print(f"Error fetching data for team {team_id}: {response.status_code}")
        pass
    team1xi = playing_xi[team_ids][0]["player"][0]["player"][:11] 
    team2xi = playing_xi[team_ids][1]["player"][0]["player"][:11]
    team1xi = [player["name"] for player in team1xi]
    team2xi = [player["name"] for player in team2xi]
    return team1xi,team2xi

def making_changes():
    pass

def weather():          # selenium
    pass

def dbupdate():
    with open('db.json', 'w') as f:
        data = json.load(f)
    for player in data:
        driver = webdriver.Chrome(options=options)
        options.add_argument('--headless')
        driver.get('https://stats.espncricinfo.com/ci/engine/stats/index.html')
        driver.maximize_window()
        search_box = driver.find_element(By.NAME, "search")
        player_name = player
        print(player_name)
        search_query = player_name
        search_box.send_keys(search_query.strip())
        search_box.send_keys(Keys.RETURN)
        link = driver.find_element(By.XPATH, "//a[starts-with(text(), 'Players and Officials')]")
        link.click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "gurusearch_player")))
        table = driver.find_element(By.ID, "gurusearch_player")
        max_matches = 0
        link_to_click = None
        rows = table.find_elements(By.XPATH, ".//table/tbody/tr[@valign='top']")
        for row in rows:
            try:
                match_links = row.find_elements(By.XPATH, ".//td[3]/a[contains(text(), 'Twenty20 matches player')]")
                
                for link in match_links:
                    parent_text = link.find_element(By.XPATH, "./..").text
                    match = re.search(r"(\d+) matches", parent_text)
                    
                    if match:
                        matches_count = int(match.group(1))
                        if matches_count > max_matches:
                            max_matches = matches_count
                            data[player]['matches'] = matches_count
                            print(data[player]['matches'])
                            link_to_click = link
            except Exception:
                continue
        try:
            link_to_click.click()
        except Exception as e:
            return
        menu_url = driver.current_url
        radio_button = driver.find_element(By.XPATH, "//input[@type='radio' and @value='bowling']")
        radio_button.click()
        submit_button = driver.find_element(By.XPATH, "//input[@type='submit' and @value='Submit query']")
        submit_button.click()
        row = driver.find_element(By.XPATH, "//tr[@class='data1']")
        cells = row.find_elements(By.TAG_NAME, "td")
        try:
            wickets = int(cells[7].text)
            data[player]['wickets'] = wickets
        except Exception:
            data[player]['wickets'] = None
        try:
            bowling_average = float(cells[9].text)
            data[player]['bowling_average'] = bowling_average
        except Exception:
            data[player]['bowling_average'] = None
        try:
            economy = float(cells[10].text)
            data[player]['economy_rate'] = economy
        except Exception:
            data[player]['economy_rate'] = None
        try:
            print(f"Wickets: {wickets}, Bowling Average: {bowling_average}, Economy: {economy}")
        except Exception:
            pass
        driver.get(menu_url)
        radio_button = driver.find_element(By.XPATH, "//input[@type='radio' and @value='batting']")
        radio_button.click()
        submit_button = driver.find_element(By.XPATH, "//input[@type='submit' and @value='Submit query']")
        submit_button.click()
        table_row = driver.find_element(By.CLASS_NAME, "data1")
        cells = table_row.find_elements(By.TAG_NAME, "td")
        try:
            runs = int(cells[5].text)
            data[player]['runs_made'] = runs
        except Exception:
            data[player]['runs_made'] = None
        try:
            batting_average = float(cells[7].text)
            data[player]['batting_average'] = batting_average
        except Exception:
            data[player]['batting_average'] = None
        try:
            strike_rate = float(cells[9].text)
            data[player]['strike_rate'] = strike_rate
        except Exception:
            data[player]['strike_rate'] = None
        try:
            print(f"Runs: {runs}, Batting Average: {batting_average}, Strike Rate: {strike_rate}")
        except:
            pass
        with open("db.json", "w") as file:
            json.dump(data, file, indent=4)
    
def convert_netscape_to_json(netscape_file, json_file):
    cookies = []
    with open(netscape_file, "r") as f:
        for line in f:
            if line.startswith("#") or line.strip() == "":
                continue  
            parts = line.strip().split("\t")
            if len(parts) < 7:
                continue  
            expiry = parts[4]
            expiry = int(expiry) if expiry.isdigit() and int(expiry) > 0 else None

            cookie = {
                "domain": parts[0],
                "httpOnly": parts[1].upper() == "TRUE",
                "path": parts[2],
                "secure": parts[3].upper() == "TRUE",
                "name": parts[5],
                "value": parts[6]
            }
            if expiry:
                cookie["expiry"] = expiry

            cookies.append(cookie)

    with open(json_file, "w") as f:
        json.dump(cookies, f, indent=4)

    print(f"✅ Converted Netscape cookies to JSON: {json_file}")

