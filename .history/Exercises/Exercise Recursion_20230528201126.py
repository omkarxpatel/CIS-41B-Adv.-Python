import os

def fileList():
    return os.listdir()

def printFiles(file_list):
            
    if len(file_list) == 0:
        return None
    if "."
    print(file_list[0])      
    printFiles(file_list[1:])  

file_list = fileList()
printFiles(file_list)