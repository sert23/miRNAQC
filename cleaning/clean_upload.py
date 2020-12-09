import sys
import os

import time
import shutil
numdays = 86400 * 22
now = time.time()

folder_to_clean = sys.argv[1]
white_file = os.path.join(folder_to_clean,"white_list")
white_list = []

with open(white_file,"r") as rfile:
    lines= rfile.readlines()
    for line in lines:
        white_list.append(line.rstrip())

folders = [x for x in os.listdir(folder_to_clean) if os.path.isdir(os.path.join(folder_to_clean,x))]
to_rem = [os.path.join(folder_to_clean,x) for x in folders if x not in white_list]


with open(os.path.join(folder_to_clean,"test.txt") , "w") as testfile:
    for dir in to_rem:
        timestamp = os.path.getmtime(dir)
        #testfile.write(dir + " " + str(timestamp) +" " + str(now - numdays) + "\n")
        if now - numdays > timestamp:
            #testfile.write(dir + " " + str(timestamp) + "\n")
            try:
                testfile.write(dir+"\n")
                shutil.rmtree(dir) #uncomment to use
            except:
                testfile.write("")