from nltk.tag import StanfordNERTagger
from nltk.tokenize import TweetTokenizer
import csv

download = True
if download:
    import nltk
    nltk.download()


if __name__ == '__main__':
    print "hi"
    tweetToke = TweetTokenizer()
    o = open('datafiles/clinton.csv')
    st = StanfordNERTagger('english.all.3class.distsim.crf.ser.gz')
    for row in csv.DictReader(o):
        #
        print row['text']
        print st.tag(tweetToke.tokenize(row['text']))
        print '\n'
    # tagger = StanfordNERTagger('datafile/clinton.csv')