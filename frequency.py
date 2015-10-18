import sys
import json
import operator

debug=0

tweets = []
new_term = {}

def printdebug(func,text):
	print func,':',text

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

def get_term_frequency_from_text(text):
	if len(text) == 0:
		return
	words = []
	local_new_term = {}
	text_emotion=0
	if debug:
		print 'Input text',text
	words = text.strip().encode('utf-8').split(' ')
	
	for x in words:
		if x.isalpha():
			new_term[x]= new_term.get(x,0) + 1

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
	tweet_file = open(sys.argv[1])
	load_tweets(tweet_file)

	for i in tweets:
		get_term_frequency_from_text(remove_all_entities(i))
	total_terms=sum(new_term.values())

	for x in new_term: 
		print x,float(new_term[x])/total_terms

if __name__ == '__main__':
	main()
