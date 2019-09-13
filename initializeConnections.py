#connection related utility file for github and mysql connection
#author - sheik shameer s

import config

def getConnectionMySql() :
    import pymysql
    db = pymysql.connect(config.mysqlhost,config.mysqlusername,config.mysqlpassword,config.databasename)
    return db

def getConnectionGitHub() :
    import github3
    print(config.githubusername)
    github = github3.login(username=config.githubusername, password=config.githubpassword)
    repos = github.repository(config.repositoryowner,config.repositoryname)
    return repos
    
