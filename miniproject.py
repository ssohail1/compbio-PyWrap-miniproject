import os

# need to add the sratoolkit and SPAdes to the PATH to avoid writing in paths/directories

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
directory = '/Users/sidra/Downloads/sratoolkit.3.0.0-mac64/bin/'
def prefetchcode(SRA,directory):
   
    prefetchcommand = './prefetch ' + SRA + ' -O ' + directory
    
    #print(prefetchcommand)
    os.system(prefetchcommand)
    
sra = 'SRR8185310'
prefetchcode(sra,directory)
   
    
direct = '/Users/sidra/Downloads/sratoolkit.3.0.0-mac64/bin/SRR8185310/SRR8185310.sra'
movecommand = 'mv ' + direct + ' ' + directory
#print(movecommand)
os.system(movecommand)

def fastqdcode(sra):
    sracommand = './fastq-dump -I --split-files ' + sra
    #print(sracommand)
    with open('miniproject.log','a') as output: 
        output.write(sracommand + '\n')
        output.close()
    os.system(sracommand)
    
fastqdcode('SRR8185310.sra')
'''


outputpath = '/Users/sidra/Downloads/sratoolkit.3.0.0-mac64/bin/'
def run_spades(outputpath,rtype='se',*readfiles):
    spadescommand = 'spades.py'
    if rtype == 'se':
        if len(readfiles) != 1:
            print('single-end reads require 1 read file')
            return(False)
        else:
            spadescommand += ' -k 33,55,77,99,127 -t 2' + ' --only-assembler -s ' + readfiles[0] + ' -o ' + outputpath + '/results'
            with open('miniproject.log','a') as output: 
                output.write(spadescommand + '\n')
                output.close()
            os.system(spadescommand)
            #print(spadescommand)
    return(os.path.exists(outputpath+'/results'))
            
# run_spades(outputpath,rtype='se','SRR.fastq')
