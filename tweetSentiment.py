import nltk
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews, twitter_samples,comparative_sentences


def word_feats(words):
    return dict([(word, True) for word in words])


def posNegativeTweets():
    for it in twitter_samples.docs('negative_tweets.json'):
        print it

    for it in twitter_samples.docs('positive_tweets.json'):
        print it

if __name__ == '__main__':
    print twitter_samples.fileids()
    # print movie_reviews.fileids()
    # print
    #

    # for it in twitter_samples.docs():
    #     print it
    negids = movie_reviews.fileids('neg')

    posids = movie_reviews.fileids('pos')
    #
    negfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'neg') for f in negids]
    posfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'pos') for f in posids]

    print negfeats
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

