
# -*- coding: utf-8 -*-


#@author: OWP


#%%

import numpy as np
import os
from . import numtools
import time

#%%

def PrintError(JobName,FolderName=''):
    
    if len(FolderName)>0:
        FolderName=FolderName + '\\'
        
    if JobName[-4:].casefold()=='.odb':
            JobName=JobName[:-4]
    
    FileName=FolderName + JobName + '.msg'
    
    FileExistLogic=os.path.isfile(FileName)
    
    if FileExistLogic==True:
        fid=open(FileName, 'r')
        Lines=fid.read().splitlines()
        fid.close()
    else:
        Lines=['']
    
    
    SearchedString=' ***ERROR'
    IndexError=numtools.listindexsub(Lines,SearchedString)

    if len(IndexError)>0:
        numtools.starprint('ABAQUS ERRORS:',1)

        for k in np.arange(4):
            
            print(Lines[k+IndexError[0]])
    
#%%

def CheckDuplicateNumbers(InputFileName):

    fid=open(InputFileName, 'r')
    InputFileLines=fid.read().splitlines()
    fid.close()

    type_list=['*NODE,' , '*ELEMENT,']

    IndexStar=numtools.listindexsub(InputFileLines,'*')

    for index in np.arange(2):
        
        IndexKeyword=numtools.listindexsub(InputFileLines,type_list[index])
        
        NumbersAll=[None]*len(IndexKeyword)
    
        for k in np.arange(len(IndexKeyword)):
        
            IndexStarNext=next(x for x in IndexStar if x > IndexKeyword[k])
            
            LineRange=np.arange(IndexKeyword[k]+1,IndexStarNext)
            InputFileLinesSub = [InputFileLines[i] for i in LineRange]
            
            NumericBlock=numtools.str2num(InputFileLinesSub,'int',1)
            NumbersAll[k]=NumericBlock[:,0]
            
            #[float(s) for s in example_string.split(',')]
    
        # Find duplicates
        NumbersAllMerged=np.concatenate(NumbersAll,axis=0)
        (u,c)= np.unique(NumbersAllMerged, return_counts=True)
        NumbersDup=u[c>1]

        if len(NumbersDup)>0:
            
            print('***** Duplicate ' + type_list[index] + ' numbers:')
            print(NumbersDup)
            raise Exception('***** Duplicates not allowed, see above printed numbers')
            
            
#%%

def RunJob(abaqus_cmd,FolderName,InputName,JobName='',cpus=4,echo_cmd=True,halt_error=True,OldJobName=''):

    # Inputs:
    # abaqus_cmd: string with system command, usually 'abaqus'
    # FolderName: string with folder of input file
    # InputName: string with name of .inp file
    # JobName: string with name of .odb, if empty then equal to InputName
    # cpus: number of cores
    # halt_error: true/false, halt or not if error in Abaqus analysis
    # echo: true/false, echo console output from system
    # OldJobName: string with name of old .odb, only relevant for restart analysis, else set to empty


    if len(abaqus_cmd)<1:
        abaqus_cmd='abaqus'

    if len(JobName)<1:
        JobName=InputName;

    if JobName[-4:].casefold()=='.inp' or JobName[-4:].casefold()=='.odb':
        JobName=JobName[:-4]

    print('***** Running ABAQUS job ' + JobName)

    OriginalFolder=os.getcwd()
    os.chdir(FolderName)
    
    # Check if lock file exists
    LockFile=FolderName + '\\' + JobName + '.lck'
    if os.path.isfile(LockFile):
        print('***** Lock-file existing, deleting')
        os.remove(LockFile)
        time.sleep(0.1)

    # Create system command input
    system_cmd=''
    system_cmd=system_cmd + abaqus_cmd
    system_cmd=system_cmd +' job=' + JobName
    
    if len(OldJobName)>0:
        system_cmd=system_cmd + ' oldjob=' + OldJobName
                                         
    system_cmd=system_cmd + ' input=' + InputName
    system_cmd=system_cmd + ' interactive'
    system_cmd=system_cmd + ' cpus=' + str(cpus)
    
    # [abaqus_cmd ' job=' JobName ' input=' InputName ' interactive' ' cpus=' num2str(cpus) ]

    t0=numtools.tic()
    #(sys_out)=os.system(system_cmd)
    sys_out=os.popen(system_cmd).read()
    t1=numtools.tocs(t0)
    
    os.chdir(OriginalFolder)
    
    if echo_cmd:
        print(sys_out)

    LogicCompleted='COMPLETED' in sys_out
    if LogicCompleted:
        print('***** ABAQUS job completed in ' + numtools.num2strf(t1,1) + ' s')
        
    LogicErrorAnalysis='Abaqus/Analysis exited with error' in sys_out

    if LogicErrorAnalysis:
        time.sleep(1)
        PrintError(JobName,FolderName)
        
        if halt_error:
            raise Exception('***** Stopped due to ABAQUS errors, see message above')
            
    return LogicCompleted