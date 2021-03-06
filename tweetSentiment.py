import csv
import json
import datetime
import nltk
import nltk.classify.util as classUtil
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews, twitter_samples, comparative_sentences
from nltk.tokenize import TweetTokenizer, WordPunctTokenizer
import re
import pickle
import os
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import math

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
    fout = open('wordFeatures.json', "w+")
    fout.write(json.dumps(wordFeatures, indent=2))
    fout.close()


def twitterClass():
    global wordFeatures
    tknzr = TweetTokenizer(strip_handles=True)
    onlyWords = re.compile('^[a-zA-Z]+$')
    # print
    if not os.path.exists(os.path.join(os.getcwd(), 'semtiment_classifier.pickle')):
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
        classifier = pickle.load(f)  # type: nltk.classify.naivebayes.NaiveBayesClassifier
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
        classification = open('trumpClassified.json', 'w+')
        classification.write(json.dumps(tweets, indent=2))
        classification.close()
        tweets = []
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
        classification = open('clintonClassified.json', 'w+')
        classification.write(json.dumps(tweets, indent=2))
        classification.close()


def trainMovies():
    negids = movie_reviews.fileids('neg')
    print type(negids), negids
    posids = movie_reviews.fileids('pos')

    negfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'neg') for f in negids]
    posfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'pos') for f in posids]

    train = negfeats + posfeats

    classifier = NaiveBayesClassifier.train(train)

    f = open('movie_semtiment_classifier.pickle', 'wb')
    pickle.dump(classifier, f)
    f.close()


def moviesClass():
    tknzr = TweetTokenizer(strip_handles=True)
    onlyWords = re.compile('^[a-zA-Z]+$')

    f = open('movie_semtiment_classifier.pickle', 'rb')
    classifier = pickle.load(f)  # type: nltk.classify.naivebayes.NaiveBayesClassifier
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
            "classification": classifier.classify(word_feats(features))
        })
    classification = open('trumpClassifiedm.json', 'w+')
    classification.write(json.dumps(tweets, indent=2))
    classification.close()

    tweets = []
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
            "classification": classifier.classify(word_feats(features))
        })
    classification = open('clintonClassifiedm.json', 'w+')
    classification.write(json.dumps(tweets, indent=2))
    classification.close()


def trainMovieTwitter():
    negLabeled = []
    posLabeled = []
    negids = movie_reviews.fileids('neg')
    posids = movie_reviews.fileids('pos')
    for f in negids:
        negLabeled.append((word_feats(movie_reviews.words(fileids=[f])), 'neg'))
    # negfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'neg') ]

    for f in posids:
        posLabeled.append((word_feats(movie_reviews.words(fileids=[f])), 'pos'))
    # posfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'pos') ]

    # # train = negfeats + posfeats
    #
    tknzr = TweetTokenizer(strip_handles=True)
    onlyWords = re.compile('^[a-zA-Z]+$')
    labeledTweets = []

    for it in twitter_samples.docs('negative_tweets.json'):
        tokens = []
        for token in tknzr.tokenize(it['text']):
            if onlyWords.match(token) is not None:
                tokens.append(token.lower())
        negLabeled.append((word_feats(tokens), 'neg'))
        # print [token for token in tknzr.tokenize(it['text']) if onlyWords.match(token) is not None]

    for it in twitter_samples.docs('positive_tweets.json'):
        tokens = []
        for token in tknzr.tokenize(it['text']):
            if onlyWords.match(token) is not None:
                tokens.append(token.lower())
        posLabeled.append((word_feats(tokens), 'pos'))

    train = negLabeled + posLabeled

    classifier = NaiveBayesClassifier.train(train)

    f = open('movieTwitter_semtiment_classifier.pickle', 'wb')
    pickle.dump(classifier, f)
    f.close()


def bothTwitterAndMovie():
    tknzr = TweetTokenizer(strip_handles=True)
    onlyWords = re.compile('^[a-zA-Z]+$')

    f = open('movieTwitter_semtiment_classifier.pickle', 'rb')
    classifier = pickle.load(f)  # type: nltk.classify.naivebayes.NaiveBayesClassifier
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
            "classification": classifier.classify(word_feats(features))
        })
    classification = open('trumpClassified_both.json', 'w+')
    classification.write(json.dumps(tweets, indent=2))
    classification.close()

    tweets = []
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
            "classification": classifier.classify(word_feats(features))
        })
    classification = open('clintonClassified_both.json', 'w+')
    classification.write(json.dumps(tweets, indent=2))
    classification.close()


def vader():
    tweets = []
    sid = SentimentIntensityAnalyzer()
    for row in csv.DictReader(open('datafiles/trump.csv')):
        text = row['text']
        features = []
        # for token in tknzr.tokenize(text):
        #     if onlyWords.match(token) is not None:
        #         features.append(token.lower())
        # print row['created_at']
        ss = sid.polarity_scores(text)
        tweets.append({
            "created_at": row['created_at'],
            "text": text,
            "classification": ss
        })
    classification = open('trumpClassifiedVader.json', 'w+')
    classification.write(json.dumps(tweets, indent=2))
    classification.close()
    tweets = []
    labeledTweets = []
    for row in csv.DictReader(open('datafiles/clinton.csv')):
        text = row['text']
        features = []
        # for token in tknzr.tokenize(text):
        #     if onlyWords.match(token) is not None:
        #         features.append(token.lower())
        # print row['created_at']
        ss = sid.polarity_scores(text)
        tweets.append({
            "created_at": row['created_at'],
            "text": text,
            "classification": ss
        })
    classification = open('clintonClassifiedVader.json', 'w+')
    classification.write(json.dumps(tweets, indent=2))
    classification.close()


def avg(list):
    sum = 0
    for elm in list:
        sum += elm
    return sum / (len(list) * 1.0)


if __name__ == '__main__':

    cvader = open('clintonClassifiedVader.json', "r")
    tvader = open('trumpClassifiedVader.json', "r")

    cScores = json.load(cvader)
    tScores = json.load(tvader)

    cvader.close()
    tvader.close()
    cGroup = {}
    for cScore in cScores:
        time = cScore['created_at'].split(' ')[0]
        clazz = cScore["classification"]
        neg = clazz['neg']
        pos = clazz['pos']
        neu = clazz['neu']
        data = cGroup.get(time, {})
        theMax = max(neg, max(pos, neu))
        if theMax == neg:
            val = data.get('neg', [])
            val.append(neg)
            data['neg'] = val
        elif theMax == pos:
            val = data.get('pos', [])
            val.append(pos)
            data['pos'] = val
        else:
            val = data.get('neu', [])
            val.append(neu)
            data['neu'] = val
        cGroup[time] = data

    cGroupOut = {}
    for k, v in cGroup.items():
        dout = {

        }
        total = 0

        for kk, vv in v.items():
            dout[kk] = avg(vv)

        cGroupOut[k] = dout



    tGroup = {}
    for tScore in tScores:
        time = tScore['created_at'].split(' ')[0]
        clazz = tScore["classification"]
        neg = clazz['neg']
        pos = clazz['pos']
        neu = clazz['neu']
        data = cGroup.get(time, {})
        theMax = max(neg, max(pos, neu))
        if theMax == neg:
            val = data.get('neg', [])
            val.append(neg)
            data['neg'] = val
        elif theMax == pos:
            val = data.get('pos', [])
            val.append(pos)
            data['pos'] = val
        else:
            val = data.get('neu', [])
            val.append(neu)
            data['neu'] = val
        tGroup[time] = data

    tGroupOut = {}
    for k, v in tGroup.items():
        dout = {

        }
        total = 0
        for it in v.values():
            total += len(it)
        for kk, vv in v.items():
            dout[kk] = avg(vv)
        tGroupOut[k] = dout

    cav = open('vaderClintonAv.json', 'w+')
    tav = open('vaderTrumpAv.json', 'w+')

    cOut = []
    tOut = []

    for k,v in cGroupOut.items():
        for kk in v.keys():

            cOut.append({"created_at":k,"name":kk,"value":v[kk]})

    for k, v in tGroupOut.items():
        for kk in v.keys():
            tOut.append({"created_at": k, "name": kk, "value": v[kk]})

    cav.write(json.dumps(cOut, sort_keys=True, indent=2))
    tav.write(json.dumps(tOut, sort_keys=True, indent=2))

    cav.close()
    tav.close()





# buildWordFeatures()
# twitterClass()

# nltk.download()

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
