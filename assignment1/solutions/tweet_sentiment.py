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
    #return not streaming_message["text"].startswith("RT") and not streaming_message["truncated"]


def score_tweet(tweet, scores):
    words = tweet["text"].lower().split()
    word_scores = [scores.get(word, 0) for word in words]

    return sum(word_scores)


def main():
    sent_filename = sys.argv[1]
    sent_scores = parse_afinn_file(sent_filename)
    
    tweets_filename = sys.argv[2]
    tweets_iterator = parsed_tweets_file_iterator(tweets_filename)

    for tweet in tweets_iterator:
        score = score_tweet(tweet, sent_scores)
        print score
        #print str(score) + "\t{{{ " + tweet["text"].encode("UTF-8") + " }}}"


if __name__ == '__main__':
    main()

