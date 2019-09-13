#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 23 21:15:29 2019

@author: sham
"""

from textblob.classifiers import NaiveBayesClassifier
train = [
     ('This is a bug', 1),
     ('This is not a bug', -1),
     ('This is a api issue', 1),
     ('This is not an api issue', -1),
     ('This is a documentation issue', 1),
     ('This is not a documentation issue', -1)
     ]
nbClassifier = NaiveBayesClassifier(train)



def getTextBasedClassification(text):
    return nbClassifier.classify(text)
