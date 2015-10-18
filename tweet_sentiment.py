import sys
import json

sent_dict = {}
tweets = []

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

def get_sent_for_line(tweet,debug):
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

def give_text(tweet):
	if 'text' in tweet.keys():
		return tweet['text']
	else:
		return 'qqqqqqqqqq No text found'

def sent_per_line(tweets):
	spl = [(give_text(tweets[i]),get_sent_for_line(tweets[i],0)) for i in range(len(tweets))]
	#print len(spl)
	return spl

def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])

    load_dict(sent_file)
    load_tweets(tweet_file)
    #print len(tweets)
    #print len(sent_dict)
    #print tweets[0]['text']
    spl = sent_per_line(tweets)

    for x in spl:
    	print x[1]


if __name__ == '__main__':
    main()
