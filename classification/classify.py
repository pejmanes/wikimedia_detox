# coding: utf-8

import sys, os

from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from preprocessing import preprocessing as pr


class CLassifier:
    def __init__(self):
        self.df = pr.get_df()

    def create_train_test(self):
        # shuffle data frame
        self.df = self.df.sample(frac=1)
        # take 10% of the data for evaluation
        eval_size = int(self.df.shape[0] * .1)
        test_df = self.df.iloc[:eval_size, :]
        train_df = self.df.iloc[eval_size:, :]
        return train_df, test_df

    def get_classifier(self, classifier_choise):
        if classifier_choise == "LogisticRegression":
            return LogisticRegression()
        elif classifier_choise == "LinearSVC":
            return LinearSVC()

    def cross_validate(self, dataset, max_features, analyzer, mingram, maxgram, cv_folds, classifier_choice):
        clf = Pipeline([
            ('vect', CountVectorizer(max_features=max_features, analyzer=analyzer, ngram_range=(mingram, maxgram))),
            ('tfidf', TfidfTransformer(norm='l2')),
            ('clf', self.get_classifier(classifier_choice)),
        ])
        df = self.df.sample(frac=1)
        scores = cross_val_score(clf, df["comment"], df[dataset], cv=cv_folds)
        return scores

    def train(self, dataset, max_features, analyzer, mingram, maxgram, classifier_choice):
        clf = Pipeline([
            ('vect', CountVectorizer(max_features=max_features, analyzer=analyzer, ngram_range=(mingram, maxgram))),
            ('tfidf', TfidfTransformer(norm='l2')),
            ('clf', self.get_classifier(classifier_choice)),
        ])
        df = self.df.sample(frac=1)
        clf = clf.fit(df["comment"], df[dataset])
        return clf
