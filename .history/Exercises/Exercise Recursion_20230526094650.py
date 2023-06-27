def fileList():
    return ['myfile.txt', 'myfile2.txt']

def printFiles(file_list):
    for file in file_list:
        if '.' in file:
            print(file)

file_list = fileList()
printFiles(file_list)
