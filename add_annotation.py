##### This script is to add upstream and downstream annotated rnas into the descriptional f of sRNAs.
##### Columns: Name in .fa f + Antisense rna info + Upstream rna info + Downstream rna info,
##### info includes: (type + strand + beg + end + other)
import os

## Define Classes and Operators
class Gene:
    def __init__(self, rnatype, chrom, strand, beg, end, other):
        self.rnatype = rnatype #string: "trna"/"rnas"/"CDS"
        self.chrom = chrom #string
        self.strand = strand #character: "+"/"-"
        self.beg = beg #integer
        self.end = end #integer
        self.other = other #last column of gff annotations

    def __le__(self, other):
        return self.end < other.beg

    def __gt__(self, other):
        return self.beg > other.end

class Srna(Gene): #Inherited from Gene Class
    def __init__(self, rnatype, chrom, strand, beg, end, other, name):
        Gene.__init__(self, rnatype, chrom, strand, beg, end, other)
        self.name = name

## Define functions
def read_Gene(line):
    sep = line.split("\t")
    chrom = sep[0]
    rnatype = sep[2]
    beg = int(sep[3])
    end = int(sep[4])
    strand = sep[6]
    other = sep[8][:-1]
    return Gene(rnatype, chrom, strand, beg, end, other)

def read_sRNA(line):
    sep = line.split("\t")
    chrom = sep[0]
    rnatype = sep[2]
    beg = int(sep[3])
    end = int(sep[4])
    strand = sep[6]
    other = sep[8][:-1]
    name = chrom + ":" + str(beg - 1) + "-" + str(end) + "(" + "" + strand + ")"
    return Srna(rnatype, chrom, strand, beg, end, other, name)

def locate_sRNA(sRNA, ref_list, pos):
    for i in range(pos, len(ref_list)):
        pos = i
        if ref_list[i] > sRNA:
            break
        
    if pos == 0:
        return Gene("NA", "NA", "NA", "NA", "NA", "NA"), Gene("NA", "NA", "NA", "NA", "NA", "NA"), ref_list[pos], pos
    if pos == 1 and not (sRNA > ref_list[pos - 1]):
        return ref_list[pos - 1], Gene("NA", "NA", "NA", "NA", "NA", "NA"), ref_list[pos], pos - 1
    if pos == len(ref_list) - 1 and not (ref_list[pos] > sRNA) and (ref_list[pos] < sRNA):
        return Gene("NA", "NA", "NA", "NA", "NA", "NA"), ref_list[pos] > sRNA, Gene("NA", "NA", "NA", "NA", "NA", "NA"), pos - 1
    if pos == len(ref_list) - 1 and not (ref_list[pos] > sRNA) and not(ref_list[pos] < sRNA):
        return ref_list[pos], ref_list[pos - 1], Gene("NA", "NA", "NA", "NA", "NA", "NA"), pos - 1
    if sRNA > ref_list[pos - 1]:
        return Gene("NA", "NA", "NA", "NA", "NA", "NA"), ref_list[pos - 1], ref_list[pos], pos - 1
    else:
        return ref_list[pos - 1], ref_list[pos - 2], ref_list[pos], pos - 1

def write_info(sRNA, ATgene, UPgene, DWgene):
    line = sRNA.name + "\t" + ATgene.rnatype + "\t" + ATgene.strand + "\t" + str(ATgene.beg) + "\t" + str(ATgene.end) + "\t" + ATgene.other + "\t"
    line = line + UPgene.rnatype + "\t" + UPgene.strand + "\t" +str(UPgene.beg) + "\t" + str(UPgene.end) + "\t" + UPgene.other + "\t"
    line = line + DWgene.rnatype + "\t" + DWgene.strand + "\t" + str(DWgene.beg) + "\t" + str(DWgene.end) + "\t" + DWgene.other + "\n"
    return line

## Read Files
f_ref = open("BJAB071041_annot_rna.gff", "r")
f_s = open("ABR_sRNA_ref_based.gff", "r")
f_info = open("ABR_sRNA_ref_based_info.txt", "w")

## Read f_ref and store it into the ref_list
ref1 = [] #"CP003846.1"
ref2 = [] #"CP003887.1"
ref3 = [] #"CP003907.1"
while True:
    line = f_ref.readline()
    if line == '':
        break
    gene = read_Gene(line)
    if gene.chrom == "CP003846.1":
        ref1.append(gene)
    elif gene.chrom == "CP003887.1":
        ref2.append(gene)
    elif gene.chrom == "CP003907.1":
        ref3.append(gene)
    else:
        print("Error! Chromosome of gene is not defined!")
f_ref.close()


## Read sRNA, locate it and write info
pos1 = 0
pos2 = 0
pos3 = 0
while True:
    line = f_s.readline()
    if line == '':
        break
    sRNA = read_sRNA(line)
    if sRNA.chrom == "CP003846.1":
        ATgene, UPgene, DWgene, pos1 = locate_sRNA(sRNA, ref1, pos1)
    elif sRNA.chrom == "CP003887.1":
        ATgene, UPgene, DWgene, pos2 = locate_sRNA(sRNA, ref2, pos2)
    elif sRNA.chrom == "CP003907.1":
        ATgene, UPgene, DWgene, pos3 = locate_sRNA(sRNA, ref3, pos3)
    else:
        print("Error! Chromosome of sRNA is not defined!")
    line = write_info(sRNA, ATgene, UPgene, DWgene)
    f_info.write(line)

f_s.close()
f_info.close()

        
