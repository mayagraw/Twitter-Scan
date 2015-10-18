import sys
import json
import operator

debug=0

sent_dict = {}
tweets = []
new_term = {}

def printdebug(func,text):
	print func,':',text

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

def get_sentiment_for_text(text):
	if len(text) == 0:
		return
	words = []
	total_sent = 0
	local_new_term = {}
	text_emotion=0
	if debug:
		print 'Input text',text
	words = text.strip().encode('utf-8').split(' ')
	for x in words:
		if x in sent_dict:
			if debug:
				print "Sentiment for",x,"equals",int(sent_dict[x])
			total_sent += int(sent_dict[x])
		else:
			if debug:
				print 'Term',x,' not found, adding as a new local entry'
			if x.isalpha():
				local_new_term[x]=0
	if debug:
		print total_sent
	
	if total_sent>0:
		text_emotion=1
	elif total_sent<0:
		text_emotion=-1

	for i in local_new_term.keys():
		if i in new_term:
			new_term[i]+=text_emotion
		else:
			new_term[i]=text_emotion
	if debug:
		print new_term
	return total_sent

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

def main():
	sent_file = open(sys.argv[1])
	tweet_file = open(sys.argv[2])

	load_dict(sent_file)
	load_tweets(tweet_file)
	#print tweets[0]['entities']
	for i in tweets:
		#print '-'*30
		get_sentiment_for_text(remove_all_entities(i))
	for x in new_term.keys():
		print x,new_term[x]
if __name__ == '__main__':
	main()
