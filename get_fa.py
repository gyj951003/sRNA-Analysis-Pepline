import os
import re
import sys



file_infa = open(sys.argv[1], "r")
file_remain = open(sys.argv[2] + ".txt", "r")
file_outfa = open(sys.argv[2] + ".fa", "w")


remain_list = []

# Read remain list
while True:
    line = file_remain.readline()
    
    if line == '':
        break

    name = line[:-1]
    remain_list.append(name)

file_remain.close()

in_fa_list = []
out_fa_dic = {}
# Read input fasta and Write output fasta
while True:
    line = file_infa.readline()
    
    if line == '':
        break

    info = line
    name = line[1:-1]
    subname = name.split(" ")[0]
    
    in_fa_list.append(subname)

    sequence = file_infa.readline()
    info = info + sequence
    
    if subname in remain_list:
        out_fa_dic.update({subname:info})

file_infa.close()

for i in range(0, len(remain_list)):
    if remain_list[i] not in in_fa_list:
        print("Error!" + remain_list[i] + "is not found!\n")
        file_outfa.close()
        sys.exit(0)

for i in range(0, len(remain_list)):
    line = out_fa_dic[remain_list[i]]
    file_outfa.write(line)

file_outfa.close()
file_infa.close()


