in_file = open("cdhit0.5_ABR_blast_cov40_results.out", "r")
out_file = open("denovo_ref_list.txt", "w")

class Pair:
    def __init__(self, query, hit_list):
        self.query = query #string
        self.hit_list = hit_list #list

pair_list = []
query = ""
hit_list = []

while True:
    line = in_file.readline()
    if line == '':
        break

    if len(line) >= 7 and line[:7] == "Query= ":
        if query != "":
            pair_list.append(Pair(query, hit_list))
            query = ""
            hit_list = []
        query = line[7:-1]

    if len(line) >= 3 and line[:2] == "> ":
        hit = line[2:-1]
        hit_list.append(hit)
        
pair_list.append(Pair(query, hit_list))

for i in range(0, len(pair_list)):
    hit_line = ""
    
    for j in range(0, len(pair_list[i].hit_list)):
        if hit_line == "":
            if pair_list[i].hit_list[j] == []:
                hit_line = "\s"
            else:
                hit_line = pair_list[i].hit_list[j]
        else:
            hit_line = hit_line + ";" + pair_list[i].hit_list[j]
        
    line = pair_list[i].query + "\t" + hit_line + "\n"
    out_file.write(line)
    
in_file.close()
out_file.close()

    
        
