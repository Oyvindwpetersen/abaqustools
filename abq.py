
# -*- coding: utf-8 -*-


#@author: OWP


#%%

import numpy as np
import os
import putools
import time

#%%

def printerror(jobname,foldername=''):

    '''
    Search through msg or dat file for errors, print error if found
    
    Arguments
    ------------
    jobname (string): name of odb file
    foldername (string): folder of odb file
    
    Returns
    ------------
    None
    
    '''
    
    if len(foldername)>0:
        foldername=foldername + '\\'
        
    # Remove odb extension if provided
    if jobname.endswith('.odb'):
            jobname=jobname[:-4]
    
    
    filename=foldername + jobname + '.msg'
    file_exist=os.path.isfile(filename)
    
    # If msg file dont exist, try dat
    if file_exist==False:
        filename=foldername + jobname + '.dat'
        file_exist=os.path.isfile(filename)
    
    # If file dont exist, set empty
    if file_exist==True:
        fid=open(filename, 'r')
        lines=fid.read().splitlines()
        fid.close()
    else:
        lines=['']
    
    # Search for error, print if found
    search_string=' ***ERROR'
    idx_error=putools.num.listindexsub(lines,search_string)

    if len(idx_error)>0:
        putools.txt.starprint('FOUND ABAQUS ERRORS:',1)

        for k in np.arange(4):
            
            print(lines[k+idx_error[0]])
    
#%%

def checkduplicate(inputname):
    
    '''
    Check input file, alert if duplicate node or element numbers
    
    Arguments
    ------------
    inputname (string): name of input file
    
    Returns
    ------------
    None
    
    '''
    
    file_exist=os.path.isfile(inputname)
    
    # Error if input file dont exist
    if file_exist==False:
        print('***** File ' + inputname)
        raise Exception('***** File not found')
    
    fid=open(inputname, 'r')
    input_file_lines=fid.read().splitlines()
    fid.close()

    node_or_element=['*NODE,' , '*ELEMENT,']

    # Index of lines with star, used for finding end of node/element block
    idx_star=putools.num.listindexsub(input_file_lines,'*')

    for index in np.arange(2):
        
        # Find all lines with *NODE or *ELEMENT
        idx_keyword=putools.num.listindexsub(input_file_lines,node_or_element[index])
        
        numbers_list=[None]*len(idx_keyword)
    
        # Find node or element numbers 
        for k in np.arange(len(idx_keyword)):
        
            idx_star_next=next(x for x in idx_star if x > idx_keyword[k])
            
            line_range=np.arange(idx_keyword[k]+1,idx_star_next)
            input_file_lines_sub = [input_file_lines[i] for i in line_range]
            
            numeric_block=putools.num.str2num(input_file_lines_sub,'int',1)
            numbers_list[k]=numeric_block[:,0]
            
            #[float(s) for s in example_string.split(',')]
    
        # Find duplicates
        numbers_all=np.concatenate(numbers_list,axis=0)
        (u,c)= np.unique(numbers_all, return_counts=True)
        numbers_dup=u[c>1]

        if len(numbers_dup)>0:
            
            print('***** Duplicate ' + node_or_element[index] + ' numbers:')
            print(numbers_dup)
            raise Exception('***** Duplicates not allowed, see above printed numbers')
            
            
#%%

def runjob(foldername,inputname,jobname='',abaqus_cmd='abaqus',cpus=4,echo_cmd=True,halt_error=True,oldjobname=''):
    
    '''
    Check input file, alert if duplicate node or element numbers
    
    Arguments
    ------------
    foldername (string): folder of input file
    inputname (string): name of input file
    jobname (string): name of odb file, if empty then equal to inputname
    abaqus_cmd (string): string supplied to system command, usually 'abaqus'
    cpus (number): number of cores
    echo_cmd (bool): echo console output from system
    halt_error (bool): halt or not if error in Abaqus analysis
    oldjobname (string): name of old odb file, only relevant for restart analysis, else set to empty
        
    Returns
    ------------
    completed (bool): if the job is completed or not
    
    
    '''        
    
    if len(abaqus_cmd)<1:
        abaqus_cmd='abaqus'
    
    if len(jobname)<1:
        jobname=inputname;
    
    if jobname[-4:].casefold()=='.inp' or jobname[-4:].casefold()=='.odb':
        jobname=jobname[:-4]
    
    print('***** Running ABAQUS job ' + jobname)
    
    # Save current folder
    folder_current=os.getcwd()
    
    # Change to folder where inputfile is
    os.chdir(foldername)
    
    # If lock file exists, delete
    file_name_lock=foldername + '\\' + jobname + '.lck'
    file_exist=os.path.isfile(file_name_lock)
    if file_exist:
        print('***** Lock-file existing, deleting')
        os.remove(file_name_lock)
        time.sleep(0.1)

    # Create system command input
    system_cmd=''
    system_cmd=system_cmd + abaqus_cmd
    system_cmd=system_cmd +' job=' + jobname
    
    # Add oldjob if provided
    if len(oldjobname)>0:
        system_cmd=system_cmd + ' oldjob=' + oldjobname
                                         
    system_cmd=system_cmd + ' input=' + inputname
    system_cmd=system_cmd + ' interactive'
    system_cmd=system_cmd + ' cpus=' + str(cpus)
    
    # [abaqus_cmd ' job=' jobname ' input=' inputname ' interactive' ' cpus=' num2str(cpus) ]

    t0=putools.timing.tic()
    #(sys_out)=os.system(system_cmd)
    sys_out=os.popen(system_cmd).read()
    t1=putools.timing.tocs(t0)
    
    # Change back to original folder
    os.chdir(folder_current)
    
    if echo_cmd:
        print(sys_out)
    
    # Check if job is successful
    completed='COMPLETED' in sys_out
    if completed:
        print('***** ABAQUS job completed in ' + putools.num.num2strf(t1,1) + ' s')
    
    error_bool='Abaqus/Analysis exited with error' in sys_out

    if error_bool:
        time.sleep(1)
        printerror(jobname,foldername)
        
        if halt_error:
            raise Exception('***** Stopped due to ABAQUS errors, see message above')
            
    return completed