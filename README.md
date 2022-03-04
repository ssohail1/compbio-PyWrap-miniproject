# compbio-PyWrap-miniproject
## Sidra Sohail
### Installation
`git clone https://github.com/ssohail1/compbio-PyWrap-miniproject.git`

### Required Software and Libraries
- Python: 
    - OS: https://docs.python.org/3/library/os.html
    - csv: https://docs.python.org/3/library/csv.html
- [SRA ToolKit](https://github.com/ncbi/sra-tools/wiki/01.-Downloading-SRA-Toolkit)
- [SPAdes](https://github.com/ablab/spades)
- [GeneMark](http://exon.gatech.edu/GeneMark/license_download.cgi)
- [Bowtie2](https://ccb.jhu.edu/software/tophat/manual.shtml)
- [TopHat](http://ccb.jhu.edu/software/tophat/index.shtml)
- [Cufflinks](http://cole-trapnell-lab.github.io/cufflinks/)

### Files in Repo
- miniproject.log: log file with commands, number of contigs greater than 1000 in length, bp in assembly of contigs greater than 1000.
- miniproj_runall.py: python script to run analyses using the available tools

### Running the program for SRR8185310
This program will run for SRR8185310:  
`python miniproj_runall.py`  


If you will implement this program for a different SRR file, simply change the 'SRR8185310' in the miniproj_runall.py file to your SRR file of interest  
Move the SRR file to the compbio-PyWrap-miniproject folder:  
`mv SRRfile compbio-PyWrap-miniproject`

### Outputs
- Output from SPAdes will be in results folder within compbio-PyWrap-miniproject directory
- Output from TopHat will be in out folder within compbio-PyWrap-miniproject directory
