# -*- coding: utf-8 -*-

#%%

import sys
import os
import numpy as np
import putools
import h5py

#%% Run that file in abaqus

def exportstatic(FolderODB,NameODB,FolderSave,FolderPython,DeleteFiles=True,CreateH5=True):
    
    Variables=[ 'u' , 'sf' ]
    
    # Name of export script
    ExportScript=NameODB + '_exportstatic'
    
    # Write py-file for export
    writepyscript_static(FolderODB,NameODB,FolderSave,FolderPython,Variables=Variables,ExportScript=ExportScript)
    
#%% Run that file in abaqus

    system_cmd='abaqus cae noGUI=' + FolderSave + '/' + ExportScript + '.py'
    sys_out=os.popen(system_cmd).read()
    
#%%

    FileNameAll=[]
    
    if 'u' in Variables:
        FileName=FolderSave + '/' + NameODB + '_export_' + 'u.txt'
        u=np.genfromtxt(FileName, delimiter=',')
        FileNameAll.append(FileName)

        FileName=FolderSave + '/' + NameODB + '_export_' + 'u_label.txt'
        fid=open(FileName,'r')
        u_label=fid.read().splitlines()
        fid.close()
        FileNameAll.append(FileName)
    
    if 'sf' in Variables:
        FileName=FolderSave + '/' + NameODB + '_export_' + 'sf.txt'
        sf=np.genfromtxt(FileName, delimiter=',')
        FileNameAll.append(FileName)
        
        FileName=FolderSave + '/' + NameODB + '_export_' + 'sf_label.txt'
        fid=open(FileName,'r')
        sf_label=fid.read().splitlines()
        fid.close()
        FileNameAll.append(FileName)
    
    
#%%

    if CreateH5==True:
        
        hf_name=FolderSave + '/' + NameODB + '_export' + '.h5'
        
        if os.path.exists(hf_name):
            hf_name=FolderSave + '/' + NameODB + '_export_conflict3' + '.h5'
        
        hf = h5py.File(hf_name,'w')

        dt = h5py.special_dtype(vlen=str) 
        
        if 'u' in Variables:
            hf.create_dataset('u',data=u)
            u_label2=np.array(u_label,dtype=dt)
            hf.create_dataset('u_label',data=u_label2)
            
        if 'sf' in Variables:
            hf.create_dataset('sf',data=sf)
            sf_label2=np.array(sf_label,dtype=dt)
            hf.create_dataset('sf_label',data=sf_label2)

        hf.close()
        

#%%

    if DeleteFiles==True:
        FileNameListDir=os.listdir(FolderSave)
        IndexMatch=putools.num.listindexsub(FileNameListDir,NameODB + '_export_')
    
        for k in np.arange(len(IndexMatch)):
            
            FileNameRemove=FileNameListDir[IndexMatch[k]]
            if not '.txt' in FileNameRemove:
                continue
            
            os.remove(FolderSave + '/' + FileNameRemove)
        
    return hf_name
#%% 

def writepyscript_static(FolderODB,NameODB,FolderSave,FolderPython,ExportScript='ExportModal',Variables=''):
    
    if isinstance(Variables,str):
        Variables=[Variables]
        
    if Variables=='':
        Variables=['u' , 'sf']
    

    Lines=['']
    
    Lines.append('import os')
    Lines.append('import numpy as np')
    Lines.append('')
    
    Lines.append('FolderODB=' + '\'' + FolderODB + '\'')
    Lines.append('JobName=' + '\'' + NameODB + '\'')
    Lines.append('FolderSave=' + '\'' + FolderSave + '\'')
    Lines.append('FolderPython=' + '\'' + FolderPython + '\'')
    
    Prefix=NameODB + '_export_'
    
    Lines.append('Prefix=' + '\'' + Prefix + '\'')
    Lines.append('')
    
    Lines.append('# Import functions for export')
    Lines.append('CurrentDir=os.getcwd()')
    Lines.append('os.chdir(FolderPython)')
    Lines.append('import odbfunc')
    Lines.append('os.chdir(CurrentDir)')
    Lines.append('')
    
    Lines.append('# Open ODB')
    Lines.append( 'myOdb=odbfunc.OpenODB(FolderODB,' + '\'' + NameODB + '\'' + ')' )
    
    if 'u' in Variables:
        Lines.append('# Displacements')
        Lines.append( '(u,u_label)=odbfunc.Export_U_UR(myOdb,-1,FrameNumber=-1)' )
        Lines.append( 'odbfunc.SaveToTXT(FolderSave,' + '\'u\'' + ',u,atype=1,Prefix=Prefix)' )
        Lines.append( 'odbfunc.SaveToTXT(FolderSave,' + '\'u_label\'' + ',u_label,atype=2,Prefix=Prefix)' )
        Lines.append('')

    if 'sf' in Variables:
        Lines.append('#  Section forces')
        Lines.append( '(sf,sf_label)=odbfunc.Export_SectionForce(myOdb,-1,FrameNumber=-1)' )
        Lines.append( 'odbfunc.SaveToTXT(FolderSave,' + '\'sf\'' + ',sf,atype=1,Prefix=Prefix)' )
        Lines.append( 'odbfunc.SaveToTXT(FolderSave,' + '\'sf_label\'' + ',sf_label,atype=2,Prefix=Prefix)' )
        Lines.append('')
        
    
    Lines.append('# Close ODB')
    Lines.append( 'odbfunc.CloseODB(myOdb)' )
        
    fid=open(FolderSave + '\\' + ExportScript + '.py', 'w')
    for Lines_sub in Lines:
        fid.write( Lines_sub + '\n')

    fid.close()


        

    