#Utility file for mining the frequency of an entity
#author - sheik shameer s

import initializeConnections

def getCommitFrequency():
    from tabulate import tabulate
    import excelexport
    db = initializeConnections.getConnectionMySql()
    cursor = db.cursor()
    
    commitFreq = "SELECT YEAR(COMMITEDDATE), MONTH(COMMITEDDATE) MONTH, COUNT(*) TOTALCOMMIT FROM Commits GROUP BY YEAR(COMMITEDDATE), MONTH(COMMITEDDATE) ORDER BY TOTALCOMMIT DESC"
    
    cursor.execute(commitFreq)
    result = cursor.fetchall()
    
    formatteddata = []
    
    for row in result :
        formatteddata.append([row[0],row[1],row[2]])
        
    displayheaders= ["YEAR","MONTH","NOOFCOMMITS"]    
    print(tabulate(formatteddata,displayheaders , tablefmt="github"))
    
    exceldata = [displayheaders]
    exceldata = exceldata + formatteddata
    excelexport.saveExcel(exceldata,"frequencyofcommits")
    return formatteddata

def getIssueFrequency():
    from tabulate import tabulate
    import excelexport
    db = initializeConnections.getConnectionMySql()
    cursor = db.cursor()
    
    issueFreq = "SELECT YEAR(CREATEDATE), MONTH(CREATEDATE) MONTH, COUNT(*) TOTALISSUES FROM Issues GROUP BY YEAR(CREATEDATE), MONTH(CREATEDATE) ORDER BY TOTALISSUES DESC"
    
    cursor.execute(issueFreq)
    result = cursor.fetchall()
    
    formatteddata = []
    
    for row in result :
        formatteddata.append([row[0],row[1],row[2]])
        
    displayheaders= ["YEAR","MONTH","NOOFISSUES"]    
    print(tabulate(formatteddata,displayheaders , tablefmt="github"))
    
    exceldata = [displayheaders]
    exceldata = exceldata + formatteddata
    excelexport.saveExcel(exceldata,"frequencyofIssues")
    return formatteddata

def getIssueFrequencyForLabelsCreation(label):
    from tabulate import tabulate
    import excelexport
    db = initializeConnections.getConnectionMySql()
    cursor = db.cursor()
    
    labelFreq = "SELECT YEAR(CREATEDATE), MONTH(CREATEDATE) MONTH, COUNT(*) TOTALISSUES FROM Issues inner join IssueLabelMapping ON Issues.NUMBER = IssueLabelMapping.Issue where IssueLabelMapping.Labels = '"+label+"' GROUP BY YEAR(CREATEDATE), MONTH(CREATEDATE) ORDER BY TOTALISSUES DESC"
    
    cursor.execute(labelFreq)
    result = cursor.fetchall()
    
    formatteddata = []
    
    for row in result :
        formatteddata.append([row[0],row[1],row[2]])
        
    displayheaders= ["YEAR","MONTH","NOOF" + label]    
    print(tabulate(formatteddata,displayheaders , tablefmt="github"))
    
    exceldata = [displayheaders]
    exceldata = exceldata + formatteddata
    excelexport.saveExcel(exceldata,"frequencyofCreation"+label)
    return formatteddata

def getIssueCreationFrequencyForAllLabels() :
    from commitModifiedFilesUtil import getDistinctLabels
    
    labels = getDistinctLabels()
    
    for label in labels :
        getIssueFrequencyForLabelsCreation(label)
        
        
def getIssueFrequencyForLabelsClosed(label):
    from tabulate import tabulate
    import excelexport
    db = initializeConnections.getConnectionMySql()
    cursor = db.cursor()
    
    labelFreq = "SELECT YEAR(CLOSEDAT), MONTH(CLOSEDAT) MONTH, COUNT(*) TOTALISSUES FROM Issues inner join IssueLabelMapping ON Issues.NUMBER = IssueLabelMapping.Issue where IssueLabelMapping.Labels = '"+label+"' GROUP BY YEAR(CLOSEDAT), MONTH(CLOSEDAT) ORDER BY TOTALISSUES DESC"
    
    cursor.execute(labelFreq)
    result = cursor.fetchall()
    db.close()
    formatteddata = []
    
    for row in result :
        formatteddata.append([row[0],row[1],row[2]])
        
    displayheaders= ["YEAR","MONTH","NOOF" + label]    
    print(tabulate(formatteddata,displayheaders , tablefmt="github"))
    
    exceldata = [displayheaders]
    exceldata = exceldata + formatteddata
    excelexport.saveExcel(exceldata,"frequencyofClosed"+label)
    return formatteddata

def getIssueClosureFrequencyForAllLabels() :
    from commitModifiedFilesUtil import getDistinctLabels
    
    labels = getDistinctLabels()
    
    for label in labels :
        getIssueFrequencyForLabelsClosed(label)
