import os

def fileList():
    return os.listdir()

def printFiles(file_list):
            
    if len(file_list) == 0:
        return None
    print(file_list[0])      
    printFiles(list[1:])  


def recursion(list):
    if len(list) == 0:
        return None
    print(list[0])
    recursion(list[1:])

file_list = fileList()
printFiles(file_list)