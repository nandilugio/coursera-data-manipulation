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


def main():
    tweets_filename = sys.argv[1]
    tweets_iterator = parsed_tweets_file_iterator(tweets_filename)

    hashtag_counts = collections.defaultdict(int)

    for tweet in tweets_iterator:
        hashtag_objects = tweet["entities"]["hashtags"]

        for hashtag_object in hashtag_objects:
            hashtag_counts[hashtag_object["text"]] += 1

    sorted_hashtag_counts = sorted(hashtag_counts.iteritems(), key=lambda (k,v): v, reverse=True)

    for (hashtag, count) in sorted_hashtag_counts:
        print hashtag.encode("UTF-8"), str(count)


if __name__ == '__main__':
    main()

