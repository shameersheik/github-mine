#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 23 21:15:29 2019

@author: sham
"""

from textblob.classifiers import NaiveBayesClassifier
train = [
     ('This is a bug', 'pos'),
     ('This is not a bug', 'neg'),
     ('This is a api issue', 'pos'),
     ('This is not an api issue', 'neg'),
     ('This is a documentation issue', 'pos'),
     ('This is not a documentation issue', 'neg')
     ]
nbClassifier = NaiveBayesClassifier(train)



def getTextBasedClassification(text):
    return nbClassifier.classify(text)
