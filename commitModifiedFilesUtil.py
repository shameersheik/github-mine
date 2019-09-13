#Utility functions related to mining modifiedfiles with respect to commit
#author - sheik shameer

import initializeConnections
import config

def getNumberofFilesTouched(label) :
    from tabulate import tabulate
    db = initializeConnections.getConnectionMySql()
    cursor = db.cursor()
    
    file_issuefixSQL = "select FILENAME,Count( distinct ILM.Issue) as TOTAL,GROUP_CONCAT(distinct ILM.Issue SEPARATOR ',') as Issues  from IssueLabelMapping as ILM inner join CommitIssueMapping on ILM.Issue = CommitIssueMapping.ISSUE inner join CommitModifiedFilesMapping on CommitIssueMapping.COMMIT = CommitModifiedFilesMapping.COMMIT where Labels = '" + label +"'  group by FILENAME order by TOTAL DESC;"
    cursor.execute(file_issuefixSQL)
    
    result = cursor.fetchall()
    db.close()
    
    formatted_data = []
    for row in result:
        formatted_data.append([row[0],row[1],row[2]])
    
    print(tabulate(formatted_data, ["FILEPATH","TOTAL",label.upper()], tablefmt="github"))
    
    return formatted_data;

def getNumberofFilesTouchedForBugs() :
    return getNumberofFilesTouched(config.fieldlabelbug)
    
def getNumberofFilesTouchedForFeature() :
    return getNumberofFilesTouched(config.fieldlabelfeature)  

def getDistinctLabels():
    db = initializeConnections.getConnectionMySql()
    cursor = db.cursor()
    
    distinct_labelSQL = "select distinct(Labels) from IssueLabelMapping"
    cursor.execute(distinct_labelSQL)
    
    result = cursor.fetchall()
    db.close()
    
    labels = []
    for row in result:
        labels.append(row[0])
        
    return labels

def getNumberOfFilesTouchedByAllLabels() :
    import excelexport
    
    labels = getDistinctLabels()
       
    for label in labels :
        print ("\n\n\n Files touched for ----" + (label))
        formattedata = [["FILENAME","TOTAL",label.upper()]]
        formattedata = formattedata + getNumberofFilesTouched(label)
        
        excelexport.saveExcel(formattedata,"filestouchedby"+label)
        
