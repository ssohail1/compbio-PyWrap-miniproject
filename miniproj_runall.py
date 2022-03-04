import os
from Bio import SeqIO
import csv

def prefetchcode(SRA):
   
    prefetchcommand = 'prefetch ' + SRA
    
    print(prefetchcommand)
    os.system(prefetchcommand)

def fastqdcode(sra):
    sracommand = 'fastq-dump -I --split-files ' + sra
    #print(sracommand)
    with open('miniproject.log','a') as output: 
        output.write(sracommand)
        output.close()
    os.system(sracommand)

def run_spades(outpath,rtype='se',*readfiles):
    spadescommand = 'spades.py'
    if rtype == 'se':
        if len(readfiles) != 1:
            print('single-end reads require 1 read file')
            return(False)
        else:
            spadescommand += ' -k 33,55,77,99,127 -t 2' + ' --only-assembler -s ' + readfiles[0] + ' -o ' + outpath + '/results'
            print(spadescommand)
            with open('miniproject.log','a') as output: 
                output.write(spadescommand + '\n')
                output.close()
            os.system(spadescommand)
    return(os.path.exists('/results'))
    
def run_genemark(rtype='fasta', *fastafile):
    genemarkcommand = 'gms2.pl'
    if rtype == 'fasta':
        genemarkcommand += ' --seq ' + fastafile[0] + ' --genome-type bacteria --faa predictseqs.fasta'
        print(genemarkcommand)
        with open('miniproject.log','a') as output: 
            output.write(genemarkcommand + '\n')
            output.close()
        os.system(genemarkcommand)
        genehmmp = 'gmhmmp2'
        genehmmp += ' --seq ' + fastafile[0] + ' --format gtf --out e_coli.gtf --mod GMS2.mod'
        print(genemarkcommand)
        with open('miniproject.log','a') as output: 
            output.write(genehmmp + '\n')
            output.close()
        os.system(genehmmp)

def run_blastp(fastafile1,fastafile2):
    blastpcommand = 'blastp'
    blastpcommand += ' -query ' + fastafile1 + ' -subject ' + fastafile2 + ' -evalue 0.001 -out predict_functionality.csv -outfmt "10 Query sequence ID, Subject sequence ID, % Identity, % Query Coverage" -max_target_seqs 1'
    os.system(blastpcommand)
    
def parse_blast(filename,headers):
    x=[]
    blast_results=open(filename,'r')
    rows=csv.DictReader(blast_results,headers,delimiter=',')
    for row in rows:
        x.append(row)
    blast_results.close()
    return x

def download_file(url,output):
    curlfunc = 'curl '
    curlfunc += url + ' --output ' + output
    os.system(curlfunc)
    gzipfunc = 'gunzip ' + output
    os.system(gzipfunc)

# ------------ Running the Functions ------------

# Download the .sra file with prefetch
sra = 'SRR8185310'
prefetchcode(sra)

# Move the .sra file from the sra/SRR_file/ directory to compbio-PyWrap-miniproject directory
currentdir = os.getcwd()   
direct = '/sra/SRR8185310/SRR8185310.sra'
movecommand = 'mv ' + direct + ' ' + currentdir
print(movecommand)
os.system(movecommand)
fastqdcode('SRR8185310.sra')

# Assemble the reads of the single-end .fastq file
outpath = os.getcwd() 
run_spades(outpath,'se','SRR8185310_1.fastq')

# Append the contigs that are greater than 1000 in assembly
f = 'results/contigs.fasta'
sequence = []
ids = []
for record in SeqIO.parse(f, "fasta"):
    sequence.append(str(record.seq))
    ids.append(str(record.id))
count = 0
if len(ids) == len(sequence):
    '''Append the id plus sequence to the contigsthousand.fasta file if the
    sequence is greater than 1000'''
    for i in range(0,len(sequence)):
        if len(sequence[i]) > 1000:
            count += 1 # counting how many sequences are greater than 1000 in the assembly
            with open('contigsthousand.fasta','a') as output: 
                output.write('>' + ids[i] + '\n' + sequence[i] + '\n')

# Write out to the log file the number of contigs that are greater than 1000 in assembly
with open('miniproject.log','a') as output:
    output.write('There are ' + str(count) + ' contigs > 1000 in the assembly.' + '\n')

# Write out to the log file the number of bp in the assembly                
count2 = 0
f = 'contigsthousand.fasta'
sequence = []
ids = []
for record in SeqIO.parse(f, "fasta"):
    sequence.append(str(record.seq))
for i in sequence:
    count2 += len(i) 
with open('miniproject.log','a') as output:
    output.write('There are ' + str(count2) + ' bp in the assembly.' + '\n')


#commands for GeneMarkS-2 & BLAST

run_genemark('fasta', 'contigsthousand.fasta')

# Blast:
# blastp -query predictseqs.fasta -subject ecoli.fasta -evalue 0.001 -out predicted_functionality.csv -outfmt 10


# parsing blastp output with the given headers (in miniproject_v2.pdf file)

filename = 'predict_functionality.csv'
headers = ['Query sequence ID', 'Subject sequence ID', '% Identity','% Query Coverage']
#Query sequence ID, Subject sequence ID, % Query Coverage, Query Start, % Identity, Length, evalue, bitscore
run_blastp('predictseqs.fasta','Ecoli.fasta')
x = parse_blast(filename,headers)
len(x)
if len(x) > 4140:
    num = len(x)-4140
    with open('miniproject.log','a') as output:
        output.write('GeneMarkS found ' + str(num) + ' additional CDS than the RefSeq.' + '\n')
if len(x) < 4140:
    num = 4140-len(x)
    with open('miniproject.log','a') as output:
        output.write('GeneMarkS found ' + str(num) + ' less CDS than the RefSeq.' + '\n')

# Download rnaseq file
def download_file(url,output):
    curlfunc = 'curl '
    curlfunc += url + ' --output ' + output
    os.system(curlfunc)
    gzipfunc = 'gunzip ' + output
    os.system(gzipfunc)


url1 = 'ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR141/006/SRR1411276/SRR1411276.fastq.gz'
output1 = 'e_coli.fastq.gz'
urlNC = 'ftp://ftp.ncbi.nlm.nih.gov/genomes/archive/old_refseq/Bacteria/Escherichia_coli_K_12_substr__MG1655_uid57779/NC_000913.fna'
output = 'e_coli.fna'

download_file(url1, output1)
download_file(urlNC, output)

def tophat_func(indexname,fastqfile):
    bowtiecmd = 'bowtie2-build'
    bowtiecmd += ' e_coli.fa e_coli'
    os.system(bowtiecmd)
    tophatcmd = 'tophat2'
    tophatcmd += ' --no-novel-juncs -o tophat2_output/ ' + indexname + ' ' + fastqfile
    os.system(tophatcmd)

indexname = 'e_coli'
fastq = 'e_coli.fastq'
tophat_func(indexname,fastq)

#gtffile = 'e_coli.gtf'

def cufflinks_func(gtffile,tophatbamfile):
    cufflinkscmd = 'cufflinks'
    cufflinkscmd += '  -o cufflinks_output -G ' + gtffile + ' ' + tophatbamfile
    os.system(cufflinkscmd)
    
    
    
    
# cufflinks -o cufflinks_output -G e_coli.gtf accepted_hits.bam

# tophat2 --no-novel-juncs -o out -p 3 e_coli e_coli.fastq 
# tophat2 --no-novel-juncs -o tophat2_output/ e_coli e_coli.fastq
