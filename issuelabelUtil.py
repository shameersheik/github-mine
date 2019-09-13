# util function with reference to labels of issues

import initializeConnections

def getNumberofIssuewrtLabel():
    from tabulate import tabulate
    import excelexport
    db = initializeConnections.getConnectionMySql()
    cursor = db.cursor()
    
    labelIssues = "select Labels , Count(*) as TotalIssues from IssueLabelMapping group by Labels order by TotalIssues desc;"
    
    cursor.execute(labelIssues)
    result = cursor.fetchall()
    db.close()
    formatteddata = []
    
    for row in result :
        formatteddata.append([row[0],row[1]])
        
    displayheaders= ["Labels","TotalIssues"]    
    print(tabulate(formatteddata,displayheaders , tablefmt="github"))
    
    exceldata = [displayheaders]
    exceldata = exceldata + formatteddata
    excelexport.saveExcel(exceldata,"LabelsTotalIssues")
    return formatteddata
