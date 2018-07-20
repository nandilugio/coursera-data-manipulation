# Data Manipulation at Scale: Systems and Algorithms

## Assignment 1: Twitter Sentiment Analysis

### Bootstrap

```bash
cp example.env .env
# vim .env  # add twitter credentials

# Install python 2.7 and pipenv
pipenv shell
pipenv install -d
```

### Running solutions

```bash
# Problem 1
time python twitterstream.py > tweets_apachekafka.jsonl
head -n 20 tweets_apachekafka.jsonl > problem_1_submission.txt

# Problem 2
python solutions/tweet_sentiment.py materials/AFINN-111.txt materials/three_minutes_tweets.json
python solutions/tweet_sentiment.py materials/AFINN-111.txt tweets_apachekafka_1min_2019-01-18.jsonl

# Problem 3
python solutions/term_sentiment.py materials/AFINN-111.txt materials/three_minutes_tweets.json
python solutions/term_sentiment.py materials/AFINN-111.txt tweets_apachekafka_1min_2019-01-18.jsonl

# Problem 4
python solutions/frequency.py materials/three_minutes_tweets.json
python solutions/frequency.py tweets_apachekafka_1min_2019-01-18.jsonl

# Problem 5
python solutions/happiest_state.py materials/AFINN-111.txt materials/three_minutes_tweets.json
python solutions/happiest_state.py materials/AFINN-111.txt tweets_apachekafka_1min_2019-01-18.jsonl

# Problem 6
python solutions/top_ten.py materials/three_minutes_tweets.json
python solutions/top_ten.py tweets_apachekafka_1min_2019-01-18.jsonl
```

