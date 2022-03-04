import os
from Bio import SeqIO
import csv

def prefetchcode(SRA):
    prefetchcommand = 'prefetch ' + SRA
    os.system(prefetchcommand)

def fastqdcode(sra):
    sracommand = 'fastq-dump -I --split-files ' + sra
    os.system(sracommand)

# readfiles input here is test data SRR8185310
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

# readfiles input here is the NC_000913 file
def run_spades2(outpath,rtype='se',*readfiles):
    spadescommand = 'spades.py'
    if rtype == 'se':
        if len(readfiles) != 1:
            print('single-end reads require 1 read file')
            return(False)
        else:
            spadescommand += ' -k 33,55,77,99,127 -t 2' + ' --only-assembler -s ' + readfiles[0] + ' -o ' + outpath + '/results2'
            print(spadescommand)
            with open('miniproject.log','a') as output: 
                output.write(spadescommand + '\n')
                output.close()
            os.system(spadescommand)
    return(os.path.exists('/results2'))

# GeneMark will output the predicted protein sequences which is the .fasta file indicated after the --faa
# it will also output the .gtf file through gmhmmp2 where output is e_coli.gtf
def run_genemark(rtype='fasta', *fastafile):
    genemarkcommand = 'gms2.pl'
    if rtype == 'fasta':
        genemarkcommand += ' --seq ' + fastafile[0] + ' --genome-type bacteria --faa predictseqs.fasta'
        print(genemarkcommand)
        with open('miniproject.log','a') as output: 
            output.write(genemarkcommand + '\n')
            output.close()
        os.system(genemarkcommand)
    # get gtf file for downstream analysis for Cufflinks    
    genehmmp = 'gmhmmp2'
    if rtype == 'fasta':
        genehmmp += ' --seq ' + fastafile[0] + ' --format gtf --out e_coli.gtf --mod GMS2.mod'
        print(genehmmp)
        with open('miniproject.log','a') as output: 
            output.write(genehmmp + '\n')
            output.close()
        os.system(genehmmp)

# running blastp where only want the best top hit as max_target_seqs is set to 1
# the headers are written right before the max_target_seqs parameter
def run_blastp(fastafile1,fastafile2):
    blastpcommand = 'blastp'
    blastpcommand += ' -query ' + fastafile1 + ' -subject ' + fastafile2 + ' -evalue 0.001 -out predict_functionality.csv -outfmt "10 Query sequence ID, Subject sequence ID, % Identity, % Query Coverage" -max_target_seqs 1'
    os.system(blastpcommand)

# parsing the blastp output and adding the headers 
def parse_blast(filename,headers):
    x=[]
    blast_results=open(filename,'r')
    rows=csv.DictReader(blast_results,headers,delimiter=',')
    for row in rows:
        x.append(row)
    blast_results.close()
    return x

# for downloading the additional RNASeq and annotated genome files
def download_files(url,output):
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
# Uncompress the .sra file to fastq
fastqdcode('SRR8185310.sra')

# Assemble the reads of the single-end .fastq file
outpath = os.getcwd() 
run_spades(outpath,'se','SRR8185310_1.fastq')

# Append the contigs that are greater than 1000 in assembly to contigsthousand.fasta
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
# Run GeneMark on the assembly of contigs greater than 1000
run_genemark('fasta', 'contigsthousand.fasta')

# Run blastp where predictseqs.fasta is GeneMark output of predicted protein sequences for the identified genes
run_blastp('predictseqs.fasta','Ecoli.fasta')

# filename is the output from blastp
filename = 'predict_functionality.csv'
# this headers list is same that is inputted to blastp function
headers = ['Query sequence ID', 'Subject sequence ID', '% Identity','% Query Coverage']
# parsing blastp output with the given headers
x = parse_blast(filename,headers)

# Write out the discrepancy to the log file
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
url1 = 'ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR141/006/SRR1411276/SRR1411276.fastq.gz'
output1 = 'ecoli.fastq.gz'
download_files(url1, output1)
# Download the complete annotated NC_000913 file
urlNC = 'ftp://ftp.ncbi.nlm.nih.gov/genomes/archive/old_refseq/Bacteria/Escherichia_coli_K_12_substr__MG1655_uid57779/NC_000913.fna'
output = 'ecoli.fa'
download_files(urlNC, output)

# Running SPAdes with complete annotated NC_000913 file as input
outpath = os.getcwd()
readfiles = 'ecoli.fa'
run_spades2(outpath, 'se', readfiles)


def tophat_func(indexname,fastqfile,fasta):
    '''first run bowtie2-build to build the index which will be used as index to 
    tophat2'''
    bowtiecmd = 'bowtie2-build '
    bowtiecmd += fasta + ' ' + indexname
    os.system(bowtiecmd)
    '''the indexname and fastqfile prefix should be same'''
    tophatcmd = 'tophat2'
    tophatcmd += ' --no-novel-juncs -o tophat2_output/ ' + indexname + ' ' + fastqfile
    os.system(tophatcmd)

indexname = 'ecoli'
# this fastq file is from url1
fastq = 'ecoli.fastq'
# this fasta file is from contigs.fasta output from SPAdes with NC_000913 file as input
fasta = 'ecoli.fa'
tophat_func(indexname,fastq,fasta)


#gtffile = 'e_coli.gtf'

def cufflinks_func(gtffile,tophatbamfile):
    cufflinkscmd = 'cufflinks'
    cufflinkscmd += '  -o cufflinks_output -G ' + gtffile + ' ' + tophatbamfile
    os.system(cufflinkscmd)

# this gtffile is output from GeneMark 
gtffile = 'e_coli.gtf'
# this file is output from running the tophat2 command
tophatbamfile = 'accepted_hits.bam'
cufflinks_func(gtffile, tophatbamfile)


