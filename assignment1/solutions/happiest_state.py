from __future__ import division

import collections
import json
import math
import string
import sys


###############################################################################
# Tweets


def parsed_tweets_file_iterator(filename):
    for line in open(filename):
        streaming_message = json.loads(line)
        if is_tweet(streaming_message):
            yield streaming_message


def is_tweet(streaming_message):
    return streaming_message.get("text") is not None


###############################################################################
# Tweet Geolocation


def us_state_from_tweet_coords(tweet):
    latitude, longitude = None, None
    if tweet["coordinates"]:
        [longitude, latitude] = tweet["coordinates"]["coordinates"]
    elif tweet["geo"]:
        [latitude, longitude] = tweet["geo"]["coordinates"]

    if not (latitude and longitude):
        return None

    return us_state_from_coords(latitude, longitude)


def us_state_from_tweet_place(tweet):
    if not tweet["place"] or tweet["place"]["country_code"] != "US":
        return None

    place = tweet["place"]
    if not place["place_type"] == "city":
        return None

    state_code = place["full_name"].split(", ")[-1]

    return us_state_from_code(state_code)


def us_state_from_tweet_user_location(tweet):
    user_location = tweet["user"]["location"].strip()
    ul_tokens = user_location.split(", ")
    ul_last_token = ul_tokens[-1].strip()

    if len(ul_tokens) != 2 or len(ul_last_token) != 2 or not ul_last_token.isupper():
        return None

    state_code = ul_last_token

    return us_state_from_code(state_code)


def tweet_us_state(tweet):
    return us_state_from_tweet_coords(tweet) or \
        us_state_from_tweet_place(tweet) or \
        us_state_from_tweet_user_location(tweet)


###############################################################################
# Geolocation

def distance(lat1, lon1, lat2, lon2):
    return math.sqrt( ((lat1-lat2)**2) + ((lon1-lon2)**2) )


def us_state_from_coords(latitude, longitude):
    # http://en.wikipedia.org/wiki/Extreme_points_of_the_United_States
    northmost = 49.3457868
    western = -124.7844079
    eastern = -66.9513812
    southmost =  24.7433195

    within_us_borders = southmost <= latitude <= northmost and western <= longitude <= eastern

    if not within_us_borders:
        return None

    distances_to_state_centroids = [
        (state, distance(latitude, longitude, state["latitude"], state["longitude"]))
        for state in us_states()
    ]

    nearest_state = sorted(
        distances_to_state_centroids,
        key=lambda (k,v): v,
    )[0][0]

    return nearest_state


def us_state_from_code(code):
    for state in us_states():
        if state["code"] == string.upper(code.strip()):
            return state

    return None


_us_states = []
def us_states():
    if not _us_states:
        for line in US_STATES_RAW_DATA.split("\n"):
            tokens = line.strip().split("\t")
            clean_tokens = [token.strip() for token in tokens]
            _us_states.append({
                "name": clean_tokens[0],
                "code": string.upper(clean_tokens[1]),
                "latitude": float(clean_tokens[2]),
                "longitude": float(clean_tokens[3]),
            })

    return _us_states

# Tab separated: Name, Code, Coords:Lat, Coords:Long
# From: https://www.census.gov/geo/reference/state-area.html
#  and: https://en.wikipedia.org/wiki/List_of_U.S._state_abbreviations
US_STATES_RAW_DATA = '''
Alabama	AL	32.7396323	-86.8434593
Alaska	AK	63.346191	-152.8370679
Arizona	AZ	34.2099643	-111.602401
Arkansas	AR	34.8955256	-92.4446262
California	CA	37.148573	-119.5406515
Colorado	CO	38.9935752	-105.5077737
Connecticut	CT	41.5797842	-72.7466666
Delaware	DE	38.9935501	-75.4473739
District of Columbia	DC	38.9041485	-77.0170942
Florida	FL	28.4574302	-82.4091478
Georgia	GA	32.629384	-83.4232125
Hawaii	HI	19.809767	-155.5061027
Idaho	ID	44.3020948	-114.5956254
Illinois	IL	40.1028754	-89.1526108
Indiana	IN	39.9030256	-86.2839503
Iowa	IA	42.0700243	-93.4933473
Kansas	KS	38.4985464	-98.3834298
Kentucky	KY	37.5336807	-85.2929841
Louisiana	LA	30.8577705	-91.803273
Maine	ME	45.3906022	-68.6574869
Maryland	MD	38.9466584	-76.6744939
Massachusetts	MA	42.1565196	-71.4895915
Michigan	MI	44.8410835	-85.6593197
Minnesota	MN	46.3161343	-94.1994801
Mississippi	MS	32.6864655	-89.6561493
Missouri	MO	38.35075	-92.4567826
Montana	MT	47.0511771	-109.6348174
Nebraska	NE	41.5438105	-99.8123253
Nevada	NV	39.3310928	-116.6151469
New Hampshire	NH	43.6708595	-71.5811278
New Jersey	NJ	40.1072744	-74.6652012
New Mexico	NM	34.4391265	-106.1261511
New York	NY	42.9133974	-75.5962723
North Carolina	NC	35.53971	-79.1308636
North Dakota	ND	47.4569538	-100.4619304
Ohio	OH	40.4149297	-82.7119975
Oklahoma	OK	35.5894185	-97.4868683
Oregon	OR	43.9715225	-120.6226269
Pennsylvania	PA	40.9042486	-77.8280624
Rhode Island	RI	41.5978358	-71.5252895
South Carolina	SC	33.8741769	-80.8542699
South Dakota	SD	44.4467957	-100.2381762
Tennessee	TN	35.8585639	-86.3493573
Texas	TX	31.4347032	-99.2818238
Utah	UT	39.3349735	-111.6563633
Vermont	VT	44.0605475	-72.673354
Virginia	VA	37.5222512	-78.6681938
Washington	WA	47.4162296	-120.5996231
West Virginia	WV	38.6472854	-80.6183274
Wisconsin	WI	44.628484	-89.7119299
Wyoming	WY	42.9918024	-107.5419255
'''.strip()


###############################################################################
# Tweet Sentiment


def tweet_sentiment(tweet, scores):
    words = tweet["text"].lower().split()
    word_scores = [scores.get(word, 0) for word in words]

    return sum(word_scores)


###############################################################################
# Sentiment


def parse_afinn_file(filename):
    scores = {}
    for line in open(filename):
        term, score  = line.split("\t")
        scores[term] = int(score)

    return scores


###############################################################################


def main():
    sentiment_filename = sys.argv[1]
    sentiment_scores = parse_afinn_file(sentiment_filename)

    tweets_filename = sys.argv[2]
    tweets_iterator = parsed_tweets_file_iterator(tweets_filename)

    state_accumulated_sentiment = collections.defaultdict(int)
    for tweet in tweets_iterator:
        us_state = tweet_us_state(tweet)

        if not us_state:
            continue

        sentiment = tweet_sentiment(tweet, sentiment_scores)

        state_accumulated_sentiment[us_state["name"]] += sentiment

    sorted_state_accumulated_sentiment = sorted(
        state_accumulated_sentiment.iteritems(),
        key=lambda (k,v): v,
        reverse=True
    )

    for state_name, accumulated_sentiment in sorted_state_accumulated_sentiment:
        print state_name, accumulated_sentiment


if __name__ == '__main__':
    main()

