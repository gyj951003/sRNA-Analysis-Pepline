import os
import re
import sys

file_in = open("total_cdhit_" + sys.argv[1] + ".clstr", "r")
file_infa = open("total_cdhit_" + sys.argv[1] + ".fa", "r")
file_remain = open("cdhit_" + sys.argv[1] + "_filtered.txt", "r")
file_out = open("cdhit_" + sys.argv[1] + "_stat.txt", "w")
file_outfa = open("total_cdhit_" + sys.argv[1] + "_filtered.fa", "w")

class Cluster:
    def __init__(self, num, repre, length):
        self.num = num
        self.repre = repre
        self.length = length

        
clst = []
num = -1
clst_list = []
remain_list = []

# Read remain list
while True:
    line = file_remain.readline()
    
    if line == '':
        break

    name = line[:-1]
    remain_list.append(name)

file_remain.close()

# Read input fasta and Write output fasta
while True:
    line = file_infa.readline()
    
    if line == '':
        break
    
    name = line[1:-1].split(" ")[0]
    sequence = file_infa.readline()
    
    if name in remain_list:
           line = ">" + name + "\n" + sequence
           file_outfa.write(line)

file_outfa.close()
file_infa.close()


# Read Cluster file and get statistics
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
     if clst_list[i].repre in remain_list:
        line = str(clst_list[i].num) + "\t" + clst_list[i].repre + "\t" + str(clst_list[i].length) + "\n"
        file_out.write(line)

file_in.close()
file_out.close()

'''
   keep = 0
    for j in range(0, len(remain_list)):
        if clst_list[i].repre == remain_list[j][:len(clst_list[i].repre) - 1]:
            keep = 1
            clst_list[i].repre = remain_list[j]
            break
        
    if keep == 1:
    '''

    
