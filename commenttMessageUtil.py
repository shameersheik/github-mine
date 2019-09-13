#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 21:26:07 2019

@author: sham
"""
import initializeConnections
import commitModifiedFilesUtil
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from bs4 import BeautifulSoup

def mineCommits():
    labels = commitModifiedFilesUtil.getDistinctLabels()
    print(str(labels))
    repos = initializeConnections.getConnectionGitHub()
    issue_minedlabel = {}
    print("mine open issues")
    for repo_issue in repos.issues(state='closed'):
        print(repo_issue.number)
        if (repo_issue.number < 1203) :
            mined_labels = []
            for issue_comment in repo_issue.comments():
                print ("getting tokens")
                tokens = getTokens(issue_comment.body_text)
                print ("got tokens")
                for label in labels :
                    if ((label in tokens) and (label not in mined_labels)):
                        mined_labels.append(label)
            if(len(mined_labels)>0) :
                issue_minedlabel[repo_issue.number] = mined_labels
                    
    db = initializeConnections.getConnectionMySql()
    cursor = db.cursor()
    
#    print("clearing data in commentminedlabels table")
#    clearDataSQL = "DELETE FROM commentminedlabels"
#    cursor.execute(clearDataSQL)
#    db.commit()
    
    placeholders= ', '.join(['%s']*2)
    insertCommentminedlabelsSQLQuery = "INSERT INTO commentminedlabels VALUES ({})".format(placeholders)
    
    print("populating commentminedlabels issue table")
    for (issue_number,mined_labelinfo) in issue_minedlabel.items():
        for label in mined_labelinfo:
            print (str(issue_number))
            print (str(label))
            if issue_number != '':
                cursor.execute(insertCommentminedlabelsSQLQuery,[issue_number,label])
                
    db.commit()  
                
            
def getTokens(text):
    soup = BeautifulSoup(text,"html.parser")
    text = soup.get_text(strip=True)
    tokens = word_tokenize(text)
    clean_tokens = tokens[:]
    sr = stopwords.words('english')
    sr.append("'")
    sr.append(".")
    sr.append("`")
    for token in tokens:
        if token in sr or len(token) < 2:
            clean_tokens.remove(token)
    return clean_tokens