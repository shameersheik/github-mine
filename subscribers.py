#Utility function with reference to subscribers table

import initializeConnections

def getSubscribersData() :
    from tabulate import tabulate
    import excelexport
    db = initializeConnections.getConnectionMySql()
    cursor = db.cursor()
    
    subFreq = "SELECT YEAR(SUBSCRIBEDDATE), MONTH(SUBSCRIBEDDATE) MONTH, COUNT(*) TOTALSUBSCRIBERS FROM subscribers  GROUP BY YEAR(SUBSCRIBEDDATE), MONTH(SUBSCRIBEDDATE) ORDER BY TOTALSUBSCRIBERS DESC"
    
    cursor.execute(subFreq)
    result = cursor.fetchall()
    db.close()
    
    formatteddata = []
    
    for row in result :
        formatteddata.append([row[0],row[1],row[2]])
        
    displayheaders= ["YEAR","MONTH","NOOFSUBSCRIBERS" ]    
    print(tabulate(formatteddata,displayheaders , tablefmt="github"))
    
    exceldata = [displayheaders]
    exceldata = exceldata + formatteddata
    excelexport.saveExcel(exceldata,"frequencyofSubscribers")
    return formatteddata
    
