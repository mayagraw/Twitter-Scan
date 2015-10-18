import sys
import json
import requests
import operator

sent_dict = {}
tweets = []
state_sentiment={}
debug =0

def load_dict(sent_file):
	for entry in sent_file:
		entry_split = entry.strip().split('\t')
		sent_dict[entry_split[0]]=entry_split[1]

def load_tweets(tweet_file):
	for line in tweet_file:
		try:
			tweets.append(json.loads(line))
		except:
			pass

def give_text(tweet):
	if 'text' in tweet.keys():
		return tweet['text']
	else:
		return 'qqqqqqqqqq No text found'

def is_a_tweet(tweet):
	if 'text' in tweet.keys():
		return True
	else :
		return False

def get_sent_for_line(tweet):
	if 'text' in tweet.keys(): 
		text = tweet['text']
		if debug:
			print 'Text found in the tweet'
	else:
		if debug:
			'qqqqqqqqqq No text found'
		return 0
	words = []
	total_sent = 0
	words = text.strip().encode('utf-8').split(' ')
	for x in words:
		if x in sent_dict:
			if debug:
				print "Sent for",x,"equals",int(sent_dict[x])
			total_sent += int(sent_dict[x])
	#print total_sent
	return total_sent

def get_US_state_code(tweet):
	if 'coordinates' in tweet.keys():
			if tweet['coordinates']:
				geojson = tweet['coordinates']
				lon = geojson['coordinates'][0]
				lat = geojson['coordinates'][1]
				url = "http://data.fcc.gov/api/block/find?format=json&latitude="+str(lat)+"&longitude="+str(lon)+"&showall=true"
				res = requests.get(url)
				if res.json()[u'State'][u'code']:
					#print '@'
					return str(res.json()[u'State'][u'code'])
	return ''

def map_tweet_sentiment_to_US_state(tweet):
	if is_a_tweet(tweet) == False:
		return

	tweet_sentiment = get_sent_for_line(tweet)
	tweet_state_code = get_US_state_code(tweet)
	if tweet_state_code:
		state_sentiment[tweet_state_code] = state_sentiment.get(tweet_state_code,0) + tweet_sentiment

def main():
	sent_file = open(sys.argv[1])
	tweet_file = open(sys.argv[2])

	load_dict(sent_file)
	load_tweets(tweet_file)

	#print 'Working...'
	for x in tweets:
		map_tweet_sentiment_to_US_state(x)
	#print 'Sorting...'
	sorted_state_list = sorted(state_sentiment.items(), key=operator.itemgetter(1),reverse=True)

	sorted_state_list[0][0]

if __name__ == '__main__':
	main()
