import os
import re
import sys

file_in = open("total_cdhit_" + sys.argv[1] + ".clstr", "r")
file_out = open("cdhit_" + sys.argv[1] + "_stat.txt", "w")

class Cluster:
    def __init__(self, num, repre, length):
        self.num = num
        self.repre = repre
        self.length = length

clst = []
num = -1
clst_list = []

while True:
    line = file_in.readline()
    
    if line == '':
        break
    
    if line[0] == ">":
        num = num + 1
        
        if clst != []:
            length = len(clst)
            clst_list.append(Cluster(num, repre, length))
            clst = []
           
    else:
        if line[-2:-1] == "*":
            result = re.search("(.*)>(.*)\.\.\. *", line)
            repre = result.group(2)
        clst.append(line)
length = len(clst)
clst_list.append(Cluster(num, repre, length))
            
for i in range(0, len(clst_list)):
    line = str(clst_list[i].num) + "\t" + clst_list[i].repre + "\t" + str(clst_list[i].length) + "\n"
    file_out.write(line)

file_in.close()
file_out.close()

    
