#Utility functions with reference to user activity

import initializeConnections

def getNoOfCommitsByUsers():
    from tabulate import tabulate
    import excelexport
    db = initializeConnections.getConnectionMySql()
    cursor = db.cursor()
    
    commitsSQL = "select EMAIL, count(*) as total  from Commits group by EMAIL order by total desc"
    
    cursor.execute(commitsSQL)
    result = cursor.fetchall()
    
    formatteddata = []
    
    for row in result :
        formatteddata.append([row[0],row[1]])
        
    displayheaders= ["EMAIL","TOTALCOMMITS"]    
    print(tabulate(formatteddata,displayheaders , tablefmt="github"))
    
    exceldata = [displayheaders]
    exceldata = exceldata + formatteddata
    excelexport.saveExcel(exceldata,"UserCommits")
    return formatteddata

def getNoOfIssueByLabel(label) :
    from tabulate import tabulate
    import excelexport
    db = initializeConnections.getConnectionMySql()
    cursor = db.cursor()
    
    labelFreq = "SELECT USERLOGIN, COUNT(*) as TOTAL  FROM Issues inner join IssueLabelMapping ON Issues.NUMBER = IssueLabelMapping.Issue where IssueLabelMapping.Labels = '"+label+"' group by USERLOGIN order by TOTAL desc"
    
    cursor.execute(labelFreq)
    result = cursor.fetchall()
    
    formatteddata = []
    
    for row in result :
        formatteddata.append([row[0],row[1]])
        
    displayheaders= ["USERNAME","TOTAL"+label]    
    print(tabulate(formatteddata,displayheaders , tablefmt="github"))
    
    exceldata = [displayheaders]
    exceldata = exceldata + formatteddata
    excelexport.saveExcel(exceldata,"usercreatedissues"+label)
    return formatteddata

def getNoOfIssueForAllLabels(label):
    from commitModifiedFilesUtil import getDistinctLabels
    
    labels = getDistinctLabels()
    
    for label in labels :
        getNoOfIssueByLabel(label)
