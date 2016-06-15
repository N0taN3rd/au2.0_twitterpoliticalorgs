import csv
import json

import nltk
import nltk.classify.util as classUtil
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews, twitter_samples, comparative_sentences
from nltk.tokenize import TweetTokenizer, WordPunctTokenizer
import re
import pickle
import  os



wordFeatures = None

def word_feats(words):
    return dict([(word, True) for word in words])


def posNegativeTweets():
    for it in twitter_samples.docs('negative_tweets.json'):
        print it

    for it in twitter_samples.docs('positive_tweets.json'):
        print it


def get_words_in_tweets(tweets):
    all_words = []
    for (words, sentiment) in tweets:
        all_words.extend(words)
    return all_words


def get_word_features(wordlist):
    wordlist = nltk.FreqDist(wordlist)
    word_features = wordlist.keys()
    return word_features


def extract_features(document):
    document_words = set(document)
    features = {}
    for word in wordFeatures:
        features['contains(%s)' % word] = (word in document_words)
    return features



def buildWordFeatures():
    tknzr = TweetTokenizer(strip_handles=True)
    onlyWords = re.compile('^[a-zA-Z]+$')
    labeledTweets = []
    for it in twitter_samples.docs('negative_tweets.json'):
        tokens = []
        for token in tknzr.tokenize(it['text']):
            if onlyWords.match(token) is not None:
                tokens.append(token.lower())
        labeledTweets.append((tokens, "negative"))
        # print [token for token in tknzr.tokenize(it['text']) if onlyWords.match(token) is not None]

    for it in twitter_samples.docs('positive_tweets.json'):
        tokens = []
        for token in tknzr.tokenize(it['text']):
            if onlyWords.match(token) is not None:
                tokens.append(token.lower())
        labeledTweets.append((tokens, "positive"))

    wordFeatures = get_word_features(get_words_in_tweets(labeledTweets))
    fout = open('wordFeatures.json',"w+")
    fout.write(json.dumps(wordFeatures,indent=2))
    fout.close()



if __name__ == '__main__':
    # buildWordFeatures()

    tknzr = TweetTokenizer(strip_handles=True)
    onlyWords = re.compile('^[a-zA-Z]+$')
    # print
    if not os.path.exists(os.path.join(os.getcwd(),'semtiment_classifier.pickle')):
        print twitter_samples.fileids()
        # print movie_reviews.fileids()
        # print

        tknzr = TweetTokenizer(strip_handles=True)
        onlyWords = re.compile('^[a-zA-Z]+$')
        labeledTweets = []

        for it in twitter_samples.docs('negative_tweets.json'):
            tokens = []
            for token in tknzr.tokenize(it['text']):
                if onlyWords.match(token) is not None:
                    tokens.append(token.lower())
            labeledTweets.append((tokens, "negative"))
                    # print [token for token in tknzr.tokenize(it['text']) if onlyWords.match(token) is not None]

        for it in twitter_samples.docs('positive_tweets.json'):
            tokens = []
            for token in tknzr.tokenize(it['text']):
                if onlyWords.match(token) is not None:
                    tokens.append(token.lower())
            labeledTweets.append((tokens, "positive"))

        # print  labeledTweets
        wordFeatures = get_word_features(get_words_in_tweets(labeledTweets))
        print "training"
        training = classUtil.apply_features(extract_features, labeledTweets)
        # print training

        sentimentClassifier = NaiveBayesClassifier.train(training)
        print "done training"
        f = open('semtiment_classifier.pickle', 'wb')
        pickle.dump(sentimentClassifier, f)
        f.close()
    else:
        fin = open('wordFeatures.json', "r")
        wordFeatures = json.load(fin)
        fin.close()
        print wordFeatures
        f = open('semtiment_classifier.pickle', 'rb')
        classifier = pickle.load(f) # type: nltk.classify.naivebayes.NaiveBayesClassifier
        f.close()
        # text,created_at
        tweets = []

        onlyWords = re.compile('^[a-zA-Z]+$')
        labeledTweets = []
        for row in csv.DictReader(open('datafiles/trump.csv')):
            text = row['text']
            features = []
            for token in tknzr.tokenize(text):
                if onlyWords.match(token) is not None:
                    features.append(token.lower())
            print row['created_at']
            tweets.append({
                "created_at": row['created_at'],
                "text": text,
                "classification": classifier.classify(extract_features(features))
            })
        classification = open('trumpClassified.json','w+')
        classification.write(json.dumps(tweets, indent=2))
        classification.close()

        labeledTweets = []
        for row in csv.DictReader(open('datafiles/clinton.csv')):
            text = row['text']
            features = []
            for token in tknzr.tokenize(text):
                if onlyWords.match(token) is not None:
                    features.append(token.lower())
            print row['created_at']
            tweets.append({
                "created_at": row['created_at'],
                "text": text,
                "classification": classifier.classify(extract_features(features))
            })
        classification = open('trumpClassified.json', 'w+')
        classification.write(json.dumps(tweets, indent=2))
        classification.close()

        # print classifier.labels()
    #
    #
    # print type(classifier)

    # print wordFeatures

    # for it in twitter_samples.docs():
    #     print it
    # negids = movie_reviews.fileids('neg')
    #
    # posids = movie_reviews.fileids('pos')
    # #
    # negfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'neg') for f in negids]
    # posfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'pos') for f in posids]
    #
    # print negfeats
    #
    # negcutoff = len(negfeats) * 3 / 4
    # poscutoff = len(posfeats) * 3 / 4
    #
    # trainfeats = negfeats[:negcutoff] + posfeats[:poscutoff]
    # testfeats = negfeats[negcutoff:] + posfeats[poscutoff:]
    # print 'train on %d instances, test on %d instances' % (len(trainfeats), len(testfeats))
    #
    # classifier = NaiveBayesClassifier.train(trainfeats)
    # print 'accuracy:', nltk.classify.util.accuracy(classifier, testfeats)
    # classifier.show_most_informative_features()
