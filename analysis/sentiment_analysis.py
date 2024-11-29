from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def analyze_sentiment(text):
    # Usando TextBlob
    blob = TextBlob(text)
    sentiment_textblob = blob.sentiment.polarity

    # Usando VADER
    analyzer = SentimentIntensityAnalyzer()
    sentiment_vader = analyzer.polarity_scores(text)

    return {
        'textblob': sentiment_textblob,
        'vader': sentiment_vader['compound']
    }