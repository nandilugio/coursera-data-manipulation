from __future__ import division

import collections
import json
import sys


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
    tweets_filename = sys.argv[1]
    tweets_iterator = parsed_tweets_file_iterator(tweets_filename)

    word_counts = collections.defaultdict(int)
    total_words = 0

    for tweet in tweets_iterator:
        tokens = tweet["text"].lower().split()
        words = [token for token in tokens if is_word(token)]

        for word in words:
            word_counts[word] += 1
            total_words += 1

    sorted_word_counts = sorted(word_counts.iteritems(), key=lambda (k,v): v, reverse=True)

    for (word, count) in sorted_word_counts:
        print word.encode("UTF-8"), str(count / total_words)


if __name__ == '__main__':
    main()

