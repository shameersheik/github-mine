#Utility file for writing data to a excel file

from xlwt import Workbook 


def saveExcel(datalist,filename) :
    wb = Workbook() 

    sheet1 = wb.add_sheet('Sheet 1') 
    rowindex = 0
    columnindex =0
    for row in datalist :
        for col in row :    
            sheet1.write(rowindex, columnindex, col) 
            columnindex = columnindex + 1
        rowindex = rowindex + 1
        columnindex = 0
    wb.save(filename+".xls")
    
