# 2. File Cleanup Utility
# Problem:
# Create a script that deletes all .tmp files older than 7 days in a given directory and its subdirectories.
#
# Requirements:
#
# Use file I/O and file system metadata to determine file age.
#
# Accept the target directory as a command-line argument.
#
# Print a summary of deleted files and their paths.

import os
from datetime import datetime, timedelta

def function(inputDir):
    deleted = []
    now = datetime.now()
    delta = timedelta(days=7)
    diff = now - delta

    for dirpath,dirnames,filenames in os.walk(inputDir):
        for file in filenames:
            if not file.endswith('.tmp'):
                continue


        filepath = os.path.join(dirpath,file)


        gettime = os.path.getmtime(filepath)
        file_dt = datetime.fromtimestamp(gettime)


        if file_dt < diff:
            deleted.append(filepath)
            os.remove(filepath)
            print(f"Deleted: {filepath}")



if __name__=="__main__":
    inputDir = input("Enter the path")
    function(inputDir)
