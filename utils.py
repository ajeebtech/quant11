from nltk.corpus import stopdocument
import nltk
from transformers import pipeline


def sentiment(document):
    nltk.download("stopwords")
    stop_words = set(stopdocument.document("english"))
    document = [word for word in document if word.lower() not in stop_words]
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