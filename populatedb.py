# contains functions for populating related databases

import initializeConnections

def getCreateTablesSQL():
    createCommitSQL = "CREATE TABLE `Commits` (`HASH` varchar(255) NOT NULL,`EMAIL` varchar(320) DEFAULT NULL,`COMMITEDDATE` datetime DEFAULT NULL,`ISMERGE` tinyint(4) DEFAULT NULL,`ISMAINBRANCH` tinyint(4) DEFAULT NULL,`MODIFIEDFILES` int(11) DEFAULT NULL,PRIMARY KEY (`HASH`))"
    createIssueSQL = "CREATE TABLE `Issues` (`ID` int(11) NOT NULL,`NUMBER` int(11) NOT NULL,`COMMENTSCOUNT` int(11) DEFAULT NULL,`COMMENTSURL` text,`ISCLOSED` tinyint(4) DEFAULT NULL,`CLOSEDAT` datetime DEFAULT NULL,`HTMLURL` text,`STATE` text,`USERLOGIN` text,`LASTMODIFIED` datetime DEFAULT NULL,`CREATEDATE` datetime DEFAULT NULL,PRIMARY KEY (`ID`))"
    createCommitIssueMappingSQL = "CREATE TABLE `CommitIssueMapping` (`COMMIT` varchar(255) NOT NULL,`ISSUE` int(11) NOT NULL)"
    createCommitModifiedFilesSQL = "CREATE TABLE `CommitModifiedFilesMapping` (`COMMIT` varchar(255) NOT NULL,`FILENAME` varchar(255) NOT NULL,`FILEPATH` varchar(255) DEFAULT NULL,`CHANGETYPE` varchar(45) DEFAULT NULL,`ADDEDLINES` int(11) DEFAULT NULL,`REMOVEDLINES` int(11) DEFAULT NULL)"
    createIssueLabelSQL = "CREATE TABLE `IssueLabelMapping` (`Issue` int(11) NOT NULL,`Labels` varchar(255) NOT NULL)"
    createSubscribersSQL = "CREATE TABLE `minegithub`.`subscribers` (`loginName` VARCHAR(255) NOT NULL,`subscribeddate` DATETIME NOT NULL);"
    return [createCommitSQL,createIssueSQL,createCommitIssueMappingSQL,createCommitModifiedFilesSQL,createIssueLabelSQL,createSubscribersSQL]

def createTables() :
    db = initializeConnections.getConnectionMySql()
    cursor = db.cursor()
    createTablesSQL = getCreateTablesSQL()
    for createSQL in createTablesSQL :        
        cursor.execute(createSQL)
    db.commit()
    db.close()

def populateCommitTables() :
    from pydriller import RepositoryMining
    import config
    import re
    
    print("mining commits in repository")
    commit_row = []
    commit_issue_map = []
    modified_files = []
    for commit in RepositoryMining(config.repositoryname).traverse_commits():
        commit_row.append([commit.hash,commit.author.email,commit.committer_date,commit.merge,commit.in_main_branch,len(commit.modifications)])
        issue_numbers = re.findall("#[0-9]*",commit.msg)
        if(len(issue_numbers) > 0):
            issue_numbers_alone = re.sub("[^0-9,]","",str(issue_numbers)).split(",")
            commit_issue_map.append({commit.hash : issue_numbers_alone})
        for commit_modified_files in commit.modifications:
            modified_files.append([commit.hash,commit_modified_files.filename,commit_modified_files.new_path,commit_modified_files.change_type.name,commit_modified_files.added,commit_modified_files.removed])
    
    db = initializeConnections.getConnectionMySql()
    cursor = db.cursor()
    
    print("clearing data in commit table")
    clearDataSQL = "DELETE FROM Commits"
    cursor.execute(clearDataSQL)
    db.commit()
    
    placeholders= ', '.join(['%s']*len(commit_row[0]))
    insertCommitSQLQuery = "INSERT INTO Commits VALUES ({})".format(placeholders)
    
    print("populating commit table")
    for repo_commit in commit_row:
        print (str(repo_commit))
        cursor.execute(insertCommitSQLQuery,repo_commit)    
    db.commit()
    
    print("clearing commit issue table")
    clearData = "DELETE FROM CommitIssueMapping"
    cursor.execute(clearData)
    db.commit()
    
    placeholders= ', '.join(['%s']*2)
    insertCommitIssueSQLQuery = "INSERT INTO CommitIssueMapping VALUES ({})".format(placeholders)
    
    print("populating commit issue table")
    for commit_info in commit_issue_map:
        for (commit_id,issues_ids) in commit_info.items():
            for issue_id in issues_ids:
                print (str(issue_id))
                if issue_id != '':
                    cursor.execute(insertCommitIssueSQLQuery,[commit_id,issue_id])
                
    db.commit()  
    
    print("clearing commit modified table")
    clearData = "DELETE FROM CommitModifiedFilesMapping"
    cursor.execute(clearData)
    db.commit()
    
    placeholders= ', '.join(['%s']*len(modified_files[0]))
    insertCommitSQLQuery = "INSERT INTO CommitModifiedFilesMapping VALUES ({})".format(placeholders)
    
    print("populating commit modified table")
    for commitmodified_row in modified_files:
        print (str(commitmodified_row))
        cursor.execute(insertCommitSQLQuery,commitmodified_row)
    
    db.commit()
    db.close()

def populateIssueTables() :
    repos = initializeConnections.getConnectionGitHub()
    
    issue_table_row = []
    issue_label_map = []
    
    print("mine open issues")
    for repo_issue in repos.issues(state='open'):
        issue_table_row.append([repo_issue.id,repo_issue.number,repo_issue.comments_count,repo_issue.comments_url,repo_issue.is_closed(),repo_issue.closed_at,repo_issue.html_url,repo_issue.state,repo_issue.user.login,repo_issue.updated_at,repo_issue.created_at])
        labels = []
        for labs in repo_issue.original_labels:
            labels.append(labs.name)
            if len(labels) > 0 :
                issue_label_map.append({repo_issue.number : labels})
                
    print("mine closed issues")
    for repo_issue in repos.issues(state='closed'):
        issue_table_row.append([repo_issue.id,repo_issue.number,repo_issue.comments_count,repo_issue.comments_url,repo_issue.is_closed(),repo_issue.closed_at,repo_issue.html_url,repo_issue.state,repo_issue.user.login,repo_issue.updated_at,repo_issue.created_at])
        labels = []
        for labs in repo_issue.original_labels:
            labels.append(labs.name)
            if len(labels) > 0 :
                issue_label_map.append({repo_issue.number : labels})
    
    db = initializeConnections.getConnectionMySql()
    cursor = db.cursor()
        
    print ("clearing issue table") 
    clearData = "DELETE FROM Issues"
    cursor.execute(clearData)
    db.commit()
               
    print("populating issue table")
    placeholders= ', '.join(['%s']*len(issue_table_row[0]))
    insertIssueSQLQuery = "INSERT INTO Issues VALUES ({})".format(placeholders)
    
    for issue_row in issue_table_row:
        print (str(issue_row))
        cursor.execute(insertIssueSQLQuery,issue_row)
    db.commit()
    
    print ("clearing issuelabel table")
    clearData = "DELETE FROM IssueLabelMapping"
    cursor.execute(clearData)
    db.commit()
    
    print("populating issue lable table")
    placeholders= ', '.join(['%s']*2)
    insertIssueLableSQLQuery = "INSERT INTO IssueLabelMapping VALUES ({})".format(placeholders)
    
    for issue_label_info in issue_label_map:
        for (issue_id,labels_info) in issue_label_info.items():
            for label_name in labels_info:
             if label_name != '':
                 print (str([issue_id,label_name]))
                 cursor.execute(insertIssueLableSQLQuery,[issue_id,label_name])
                 
    db.commit()    
    db.close()

def populatesubscriberstable():
    import config
    from datetime import datetime
    repos = initializeConnections.getConnectionGitHub()
    
    subscribers_info = []
    for subscriber in repos.subscribers() :
        subscriptions = subscriber.subscriptions()
        for subscription in subscriptions :
            if subscription.name == config.repositoryname:
                #subscribers_info.append([subscriber.login,(subscription.created_at).strftime('%Y-%m-%d %H:%M:%S:%fZ')])
                #subscribers_info.append([subscriber.login,datetime.strptime(subscription.created_at,'%Y-%m-%dT%H:%M:%SZ')])
                print(str([subscriber.login,subscription.created_at]))
    db = initializeConnections.getConnectionMySql()
    cursor = db.cursor()
        
    print ("clearing subscribers table") 
    clearData = "DELETE FROM subscribers"
    cursor.execute(clearData)
    db.commit()
    
    print("populating subscribers table")
    placeholders= ', '.join(['%s']*2)
    insertSubscribersSQLQuery = "INSERT INTO subscribers VALUES ({})".format(placeholders)
    
    for subsciber in subscribers_info :
        cursor.execute(insertSubscribersSQLQuery,subsciber)
    
    db.commit()
    db.close()
