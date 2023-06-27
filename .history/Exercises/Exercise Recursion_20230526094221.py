def fileList():
    return ['file1.txt', 'file2.txt', 'folder1/file3.txt', 'folder2/file4.txt', 'folder2/folder3/file5.txt']

def printFiles(file_list):
    for file in file_list:
        if '.' in file:
            # File found, print its name
            print(file)
        else:
            # It's a folder, call the function recursively
            sub_folder_files = fileList()
            sub_folder_files = [file + '/' + sub_file for sub_file in sub_folder_files]
            printFiles(sub_folder_files)

# Call the function to print all files
file_list = fileList()
printFiles(file_list)
