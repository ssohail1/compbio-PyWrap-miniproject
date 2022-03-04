# compbio-PyWrap-miniproject
## Sidra Sohail
### Installation
Clone repository into personal directory using this command,  
`git clone https://github.com/ssohail1/compbio-PyWrap-miniproject.git`  

To move into compbio-PyWrap-miniproject directory use cd,  
`cd compbio-PyWrap-miniproject`

## Required Software and Libraries
- Python: 
    - OS: https://docs.python.org/3/library/os.html
    - csv: https://docs.python.org/3/library/csv.html
- [SRA ToolKit](https://github.com/ncbi/sra-tools/wiki/01.-Downloading-SRA-Toolkit)
- [SPAdes](https://github.com/ablab/spades)
- [GeneMark](http://exon.gatech.edu/GeneMark/license_download.cgi)
- [Bowtie2](https://ccb.jhu.edu/software/tophat/manual.shtml)
- [TopHat](http://ccb.jhu.edu/software/tophat/index.shtml)
- [Cufflinks](http://cole-trapnell-lab.github.io/cufflinks/)

## Running the program for SRR8185310
This program will run for SRR8185310:  
`python miniproj_runall.py`

## Files in Repo
- miniproject.log: log file with commands, number of contigs greater than 1000 in length, bp in assembly of contigs greater than 1000 in length.
- miniproj_runall.py: python script to run analyses using the tools described. It includes functions that download SRA files, pulls fasta files, run SPades, assembles the reads, counts the number of contigs and number of base pairs in the assembly, runs GeneMark to output the predicted protein sequences for the identified genes, runs BLAST with the GeneMark protein output against the protein database, calculate difference between the RefSeq for E. coli K-12 (NC_000913) and BLAST output.


If you will implement this program for a different SRR file, simply change the 'SRR8185310' in the miniproj_runall.py file to your SRR file of interest  
Move the SRR file to the compbio-PyWrap-miniproject folder:  
`mv SRRfile compbio-PyWrap-miniproject`

##= Outputs
- SPAdes output will be in results folder within compbio-PyWrap-miniproject directory
- TopHat output will be in out folder within compbio-PyWrap-miniproject directory
