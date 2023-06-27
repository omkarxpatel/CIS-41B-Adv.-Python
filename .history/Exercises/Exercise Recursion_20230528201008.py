import os

def fileList():
    return os.listdir()

def printFiles(file_list):
    for file in file_list:
        if '.' in file:
            print(file)


def recursion(list):
    if len(list) == 0:
        return None
    print(list[0])
    recursion(list[1:])

file_list = fileList()
printFiles(file_list)