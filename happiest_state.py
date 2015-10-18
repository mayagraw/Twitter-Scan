import sys
import json
import operator

sent_dict = {}
tweets = []
state_sentiment={}
debug =0

states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}


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

def clean_tweet_of_entities(tweet,delete_range):
	start=0
	text=give_text(tweet)
	outstr=''
	for i in range(len(delete_range)):
		outstr+=text[start:delete_range[i][0]]
		start=delete_range[i][1]
		if debug:
			print 'loop ',i,' data',outstr,' start=',start
	outstr+=text[start:]
	if debug:
		print 'func end',outstr
	return outstr

def remove_entity(tweet,entity,delete_range):
	values = tweet['entities'][str(entity)]
	
	for val in range(len(values)):
		tmp=tweet['entities'][str(entity)][val]['indices']
		if debug:
			print 'Entity',entity,'found with start as',tmp[0],'and end as',tmp[1]
		delete_range.append(tmp)

def remove_all_entities(tweet):
	
	if 'entities' not in tweet.keys():
		return ''
	delete_range = []
	entities = tweet['entities'].keys()
	if debug:
		print give_text(tweet)
	[remove_entity(tweet,x.encode('utf-8'),delete_range) for x in entities]
	#print len(delete_range)
	delete_range.sort(key=operator.itemgetter(0))
	txt=clean_tweet_of_entities(tweet,delete_range)
	if debug:
		print  'Original:',give_text(tweet),'\n Cleaned:',txt
	return txt


def get_sent_for_line(text):
	words = []
	total_sent = 0
	words = remove_all_entities(text).strip().encode('utf-8').split(' ')
	for x in words:
		if x in sent_dict:
			if debug:
				print "Sent for",x,"equals",int(sent_dict[x])
			total_sent += int(sent_dict[x])
	#print total_sent
	return total_sent

def get_place_data(tweet):
	if u'place' in tweet.keys():
			if tweet[u'place']:
				return tweet[u'place']
	return False

def is_US_state(placejson):
	if placejson:
		if u'country' in placejson.keys():
			if placejson[u'country'] == u'United States':
				return True
	return False

def get_US_state_code(tweet):
	placejson = get_place_data(tweet)
	if placejson == False:
		return False
	if is_US_state(placejson) == False:
		return False
	if placejson[u'place_type'] == u'city':
		state_code = str(placejson[u'full_name']).split(',')[1].strip()
		if state_code in states.keys():
			return state_code
	return False

def map_tweet_sentiment_to_US_state(tweet):
	if is_a_tweet(tweet) == False:
		return

	tweet_state_code = get_US_state_code(tweet)
	if tweet_state_code == False:
		return

	tweet_sentiment = get_sent_for_line(tweet)
	state_sentiment[tweet_state_code] = state_sentiment.get(tweet_state_code,0) + tweet_sentiment
	


def main():
	sent_file = open(sys.argv[1])
	tweet_file = open(sys.argv[2])

	load_dict(sent_file)
	load_tweets(tweet_file)

	for x in tweets:
		map_tweet_sentiment_to_US_state(x)

	sorted_state_list = sorted(state_sentiment.items(), key=operator.itemgetter(1),reverse=True)

	print sorted_state_list[0][0]

if __name__ == '__main__':
	main()
