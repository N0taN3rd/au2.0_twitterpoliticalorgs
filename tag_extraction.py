from nltk.tag import StanfordNERTagger
from nltk.tokenize import TweetTokenizer, WordPunctTokenizer
import csv
import os

# download = True
# if download:
#     import nltk
#     nltk.download()


if __name__ == '__main__':
    print "hi"
    tweetToke = TweetTokenizer()
    wordToke = WordPunctTokenizer()
    o = open('datafiles/clinton.csv')

    st = StanfordNERTagger(os.path.join(os.getcwd(), 'stanfordModel/classifiers/english.all.3class.distsim.crf.ser.gz'),
                           os.path.join(os.getcwd(), 'stanfordModel/stanford-ner-3.6.0.jar'))
    # 'create_at', 'twitter_id', 'hashtags', 'twitter_url','person','organization'
    taggedFile = open('taggedClinton.csv', 'w+')
    headers = ['create_at', 'twitter_id', 'hashtags', 'twitter_url', 'person', 'organization']
    tweetWriter = csv.DictWriter(taggedFile, headers)
    tweetWriter.writeheader()
    for row in csv.DictReader(o):
        #
        print row['text']
        csvrow = {
                  'create_at': row['created_at'],
                  'twitter_id': row['twitter_id'],
                  'hashtags': row['hashtags'],
                  'twitter_url': row['twitter_url']
                  }
        for tagged in st.tag(wordToke.tokenize(row['text'])):
            org = []
            person = []

            wasOrg = False
            wasPerson = False
            if tagged[1] == 'ORGANIZATION':
                csvrow['organization'] = tagged[0]
                wasOrg = True
                print wasOrg

            if tagged[1] == 'PERSON':
                csvrow['person'] = tagged[0]
                wasPerson = True
                print wasPerson

            if wasOrg or wasPerson:
                tweetWriter.writerow(csvrow)
        print '\n'
        # tagger = StanfordNERTagger('datafile/clinton.csv')
