import os

def fileList():
    return os.listdir()

def printFiles(file_list):
            
    if len(file_list) == 0:
        return None
    print(file_list[0])      
    printFiles(list[1:])  

file_list = fileList()
printFiles(file_list)