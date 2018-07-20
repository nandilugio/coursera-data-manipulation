from __future__ import division

import collections
import json
import sys


def parse_afinn_file(filename):
    scores = {}
    for line in open(filename):
        term, score  = line.split("\t")
        scores[term] = int(score)

    return scores


def parsed_tweets_file_iterator(filename):
    for line in open(filename):
        streaming_message = json.loads(line)
        if is_tweet(streaming_message):
            yield streaming_message


def is_tweet(streaming_message):
    return streaming_message.get("text") is not None


def is_word(token):
    return all(char.isalpha() for char in token)


def main():
    sentiment_filename = sys.argv[1]
    sentiment_scores = parse_afinn_file(sentiment_filename)

    tweets_filename = sys.argv[2]
    tweets_iterator = parsed_tweets_file_iterator(tweets_filename)

    unscored_words_rolling_avgs = collections.defaultdict(lambda: {"avg": 0.0, "count": 0})

    for tweet in tweets_iterator:
        tokens = tweet["text"].lower().split()
        scored_words = [token for token in tokens if type(sentiment_scores.get(token, False)) is int]
        scored_word_count = len(scored_words)

        if scored_word_count == 0:
            continue

        unscored_tokens = [token for token in tokens if type(sentiment_scores.get(token, False)) is not int]
        unscored_words = [token for token in unscored_tokens if is_word(token)]
        unscored_word_count = len(unscored_words)

        if unscored_word_count == 0:
            continue

        scores = [sentiment_scores[word] for word in scored_words]
        avg_score = sum(scores) / scored_word_count

        for word in unscored_words:
            prev = unscored_words_rolling_avgs[word]
            unscored_words_rolling_avgs[word]["avg"] = \
                ((prev["avg"] * prev["count"]) + avg_score) / (prev["count"] + 1)
            unscored_words_rolling_avgs[word]["count"] += 1

    new_word_scores = {}
    for word, rolling_avg in unscored_words_rolling_avgs.iteritems():
        score = rolling_avg["avg"]
        new_word_scores[word] = score
        print word.encode("UTF-8"), str(score)


if __name__ == '__main__':
    main()

