import os
from Bio import SeqIO
#os.chdir(os.path.dirname(os.path.abspath('~/Downloads/sratoolkit.3.0.0-mac64/bin/')))
#print(os.getcwd())

#''' Got this part to work!

#file = '/Users/sidra/Downloads/sratoolkit.3.0.0-mac64/bin/SRRnum'
#infile = open(file, 'r').read()
#directory = '/Users/sidra/Downloads/sratoolkit.3.0.0-mac64/bin/'
#def prefetchcode(SRA,directory):
   
#    prefetchcommand = './prefetch ' + SRA + ' -O ' + directory
    
    #prefetchcommand = './prefetch --option-file ' + SRA
    
#    print(prefetchcommand)
#    os.system(prefetchcommand)
    
    #sracommand = './fastq-dump -I --split-files *.sra'
    #os.system(sracommand)

#for i in infile:
#    prefetchcode(i,directory)
    
#    '''


''' Got this part to work!
#directory = '/Users/sidra/Downloads/sratoolkit.3.0.0-mac64/bin/'
directory = '/Users/sidra/Downloads/COMP_383-483_compbio/COMPBIO_MiniProject'
def prefetchcode(SRA,directory):
   
    prefetchcommand = './prefetch ' + SRA + ' -O ' + directory
    
    #print(prefetchcommand)
    os.system(prefetchcommand)
    
sra = 'SRR8185310'
prefetchcode(sra,directory)
   
    
direct = '/Users/sidra/Downloads/COMP_383-483_compbio/COMPBIO_MiniProject/SRR8185310/SRR8185310.sra'
movecommand = 'mv ' + direct + ' ' + directory
#print(movecommand)
os.system(movecommand)

def fastqdcode(sra):
    sracommand = './fastq-dump -I --split-files ' + sra
    #print(sracommand)
    with open('miniproject.log','a') as output: 
        output.write(sracommand)
        output.close()
    os.system(sracommand)
    
fastqdcode('SRR8185310.sra')
'''
#def sra_uncompress(*sra):
#    sracommand = './fastq-dump -I --split-files *.sra'
#    os.system(sracommand)

#def prefetch2(SRR):
#    prefetchcommand = './prefetch --option-file ' + SRR
#    os.system(prefetchcommand)
#    sracommand = './fastq-dump -I --split-files *.sra'
#    os.system(sracommand)

# change to where you want results folder to be located
outputpath = '/Users/sidra/Downloads/COMP_383-483_compbio/COMPBIO_MiniProject'
def run_spades(outputpath,rtype='se',*readfiles):
    spadescommand = 'spades.py'
    print(type(readfiles))
    if rtype == 'se':
        if len(readfiles) != 1:
            print('single-end reads require 1 read file')
            return(False)
        else:
            spadescommand += ' -k 33,55,77,99,127 -t 2' + ' --only-assembler -s ' + readfiles[0] + ' -o ' + outputpath + '/results'
            print(spadescommand)
            with open('miniproject.log','a') as output: 
                output.write(spadescommand + '\n')
                output.close()
            os.system(spadescommand)
            #print(spadescommand)
    #os.system(spadescommand)
    return(os.path.exists(outputpath+'/results'))
            
run_spades(outputpath,'se','SRR8185310_1.fastq')

f = outputpath+'/results/contigs.fasta'
sequence = []
for record in SeqIO.parse(f, "fasta"):
    sequence.append(str(record.seq))
count = 0
output = open('contigsonethousand.txt','w')
for i in sequence:
    if len(i) > 1000:
        count += 1
        output.write(i + '\n')
output.close()

f = '/Users/sidra/Downloads/COMP_383-483_compbio/COMPBIO_MiniProject/contigsonethousand.txt'
infile = open(f,'r').read().split()
num = len(infile)
with open('miniproject.log','a') as output:
    output.write('There are ' + str(num) + ' contigs > 1000 in the assembly.' + '\n')

count = 0
for i in infile:
    count += len(i)
with open('miniproject.log','a') as output:
    output.write('There are ' + str(count) + ' bp in the assembly.' + '\n')
