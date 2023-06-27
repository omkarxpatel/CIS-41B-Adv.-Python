import os

def fileList():
    return os.listdir()

def printFiles(file_list):
    for file in file_list:
        if '.' in file:
            print(file)

file_list = fileList()
printFiles(file_list)