#index file for accessing util functions

import populatedb

print ("Create SQL Tables")
populatedb.createTables()
print ("Mine and Populate Necessary data from github repos")
populatedb.populateCommitTables()
populatedb.populateIssueTables()

import commitModifiedFilesUtil
print ("Number of files touched by bugs is as follows")
commitModifiedFilesUtil.getNumberofFilesTouchedForBugs()

print ("Number of files touched by features is as follows")
commitModifiedFilesUtil.getNumberofFilesTouchedForFeature()

print ("Number of files touched for each label")
commitModifiedFilesUtil.getNumberOfFilesTouchedByAllLabels()

print ("get Distinct labels in the repository for issues")
commitModifiedFilesUtil.getDistinctLabels()

print ("get files touched issue having a label")
commitModifiedFilesUtil.getNumberofFilesTouched("api")

import frequency

print("Frequency of commits")
frequency.getCommitFrequency()

print ("Frequency of issue closure for each label")
frequency.getIssueClosureFrequencyForAllLabels()

print ("Frequency of issue creation for each label")
frequency.getIssueCreationFrequencyForAllLabels()

print ("Frequency of issue closed segregated by label")
frequency.getIssueFrequencyForLabelsClosed()

print ("Frequency of bugs created")
frequency.getIssueFrequency()

print("Frequency of issues created with respect to labels")
frequency.getIssueFrequencyForLabelsCreation("api")

import excelexport

print("save data list to an excel file")
excelexport.saveExcel([],"samplefilename")

import initializeConnections

print("get sql connection object")
initializeConnections.getConnectionMySql()

print("get github connection object")
initializeConnections.getConnectionGitHub()

import issuelabelUtil

print("get number of issues with respect to label")
issuelabelUtil.getNumberofIssuewrtLabel()

import subscribers

print("gets subscribers data for the repository")
subscribers.getSubscribersData()

import userinfo

print(" gets number of commits by a user")
userinfo.getNoOfCommitsByUsers()

print("get number of issues for a label by a user")
userinfo.getNoOfIssueByLabel("api")

print("get number of issues segregated by label for a user")
userinfo.getNoOfIssueForAllLabels()


