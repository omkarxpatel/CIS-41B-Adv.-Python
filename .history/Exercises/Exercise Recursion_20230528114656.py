import os

def fileList(): # example function
    return ['myfile.txt', 'myfile2.txt', 'my_folder/my_file.txt']

def printFiles(file_list):
    for file in file_list:
        if '.' in file:
            print(file.split("/")[-1])
            

file_list = fileList()
printFiles(file_list)