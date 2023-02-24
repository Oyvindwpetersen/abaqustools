# -*- coding: utf-8 -*-

#%%

import sys
import os
import numpy as np
import putools
import h5py

#%% Run that file in abaqus

def exportmodal(FolderODB,NameODB,FolderSave,FolderPython,DeleteFiles=True,CreateH5=True):
    
    Variables=['freq' , 'genmass' , 'phi' , 'phi_sf' , 'nodecoord' , 'elconn' ]
    
    # Name of export script
    ExportScript=NameODB + '_exportmodal'
    
    # Write py-file for export
    writepyscript_modal(FolderODB,NameODB,FolderSave,FolderPython,Variables=Variables,ExportScript=ExportScript)
    
#%% Run that file in abaqus

    system_cmd='abaqus cae noGUI=' + FolderSave + '/' + ExportScript + '.py'
    sys_out=os.popen(system_cmd).read()
    
#%%

    FileNameAll=[]
    
    if 'freq' in Variables:
        FileName=FolderSave + '/' + NameODB + '_export_' + 'freq.txt'
        freq=np.genfromtxt(FileName, delimiter=',')
        FileNameAll.append(FileName)
    
    if 'genmass' in Variables:
        FileName=FolderSave + '/' + NameODB + '_export_' + 'genmass.txt'
        genmass=np.genfromtxt(FileName, delimiter=',')
        FileNameAll.append(FileName)
    
    if 'phi' in Variables:
        FileName=FolderSave + '/' + NameODB + '_export_' + 'phi.txt'
        phi=np.genfromtxt(FileName, delimiter=',')
        FileNameAll.append(FileName)

        FileName=FolderSave + '/' + NameODB + '_export_' + 'phi_label.txt'
        fid=open(FileName,'r')
        phi_label=fid.read().splitlines()
        fid.close()
        FileNameAll.append(FileName)
    
    if 'phi_sf' in Variables:
        FileName=FolderSave + '/' + NameODB + '_export_' + 'phi_sf.txt'
        phi_sf=np.genfromtxt(FileName, delimiter=',')
        FileNameAll.append(FileName)
        
        FileName=FolderSave + '/' + NameODB + '_export_' + 'phi_sf_label.txt'
        fid=open(FileName,'r')
        phi_sf_label=fid.read().splitlines()
        fid.close()
        FileNameAll.append(FileName)
    
    if 'nodecoord' in Variables:
        FileName=FolderSave + '/' + NameODB + '_export_' + 'nodecoord.txt'
        nodecoord=np.genfromtxt(FileName, delimiter=',')
        FileNameAll.append(FileName)
        
    if 'elconn' in Variables:
        FileName=FolderSave + '/' + NameODB + '_export_' + 'elconn.txt'
        elconn=np.genfromtxt(FileName, delimiter=',')
        FileNameAll.append(FileName)
        

#%%

    if CreateH5==True:
        
        hf_name=FolderSave + '/' + NameODB + '_export' + '.h5'
        
        if os.path.exists(hf_name):
            hf_name=FolderSave + '/' + NameODB + '_export_conflict' + '.h5'
        #if os.path.exists(hf_name):
        
        hf = h5py.File(hf_name,'w')

        dt = h5py.special_dtype(vlen=str) 
        
        if 'freq' in Variables:
            hf.create_dataset('freq',data=freq)
        
        if 'genmass' in Variables:
            hf.create_dataset('genmass',data=genmass)

        if 'phi' in Variables:
            hf.create_dataset('phi',data=phi)
            phi_label2=np.array(phi_label,dtype=dt)
            hf.create_dataset('phi_label',data=phi_label2)
        
        if 'phi_sf' in Variables:
            hf.create_dataset('phi_sf',data=phi_sf)
            phi_sf_label2=np.array(phi_sf_label,dtype=dt)
            hf.create_dataset('phi_sf_label',data=phi_sf_label2)
        
        if 'nodecoord' in Variables:
            hf.create_dataset('nodecoord',data=nodecoord)
        
                
        if 'elconn' in Variables:
            hf.create_dataset('elconn',data=elconn)
            
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
        
#%% 

def writepyscript_modal(FolderODB,NameODB,FolderSave,FolderPython,ExportScript='ExportModal',Variables=''):
    
    if isinstance(Variables,str):
        Variables=[Variables]
        
    if Variables=='':
        Variables=['freq' , 'genmass' , 'phi' , 'phi_sf' , 'nodecoord' , 'elconn']
    
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
    
    if 'freq' in Variables:
        Lines.append('')
        Lines.append('# Frequencies')
        Lines.append( 'freq=odbfunc.Export_HistoryOutput(myOdb,-1,' + '\'' + 'EIGFREQ' + '\'' +  ')' )
        Lines.append( 'odbfunc.SaveToTXT(FolderSave,' +  '\'freq\'' + ',freq,atype=1,Prefix=Prefix)' )
        Lines.append('')

    if 'genmass' in Variables:
        Lines.append('# Generalized mass')
        Lines.append( 'genmass=odbfunc.Export_HistoryOutput(myOdb,-1,' + '\'' + 'GM' + '\'' +  ')' )
        Lines.append( 'odbfunc.SaveToTXT(FolderSave,' + '\'genmass\'' + ',genmass,atype=1,Prefix=Prefix)' )
        Lines.append('')

    if 'phi' in Variables:
        Lines.append('# Mode shapes')
        Lines.append( '(phi,phi_label)=odbfunc.Export_U_UR(myOdb,-1,FrameNumber=' '\'skipfirst\''    ')' )
        Lines.append( 'odbfunc.SaveToTXT(FolderSave,' + '\'phi\'' + ',phi,atype=1,Prefix=Prefix)' )
        Lines.append( 'odbfunc.SaveToTXT(FolderSave,' + '\'phi_label\'' + ',phi_label,atype=2,Prefix=Prefix)' )
        Lines.append('')

    if 'phi_sf' in Variables:
        Lines.append('# Modal section forces')
        Lines.append( '(phi_sf,phi_sf_label)=odbfunc.Export_SectionForce(myOdb,-1,FrameNumber=' '\'skipfirst\''    ')' )
        Lines.append( 'odbfunc.SaveToTXT(FolderSave,' + '\'phi_sf\'' + ',phi_sf,atype=1,Prefix=Prefix)' )
        Lines.append( 'odbfunc.SaveToTXT(FolderSave,' + '\'phi_sf_label\'' + ',phi_sf_label,atype=2,Prefix=Prefix)' )
        Lines.append('')
        
    if 'nodecoord' in Variables:
        Lines.append('# Node coordinates')
        Lines.append( 'nodecoord=odbfunc.Export_NodeCoord(myOdb,-1,0)' )
        Lines.append( 'odbfunc.SaveToTXT(FolderSave,' + '\'nodecoord\'' + ',nodecoord,atype=1,Prefix=Prefix)' )
        Lines.append('')
        
    if 'elconn' in Variables:
        Lines.append('# Element connectivity')
        Lines.append( 'elconn=odbfunc.Export_ElConnectivity(myOdb)' )
        Lines.append( 'odbfunc.SaveToTXT(FolderSave,' + '\'elconn\'' + ',elconn,atype=1,Prefix=Prefix)' )
        Lines.append('')
    
    Lines.append('# Close ODB')
    Lines.append( 'odbfunc.CloseODB(myOdb)' )
        
    fid=open(FolderSave + '\\' + ExportScript + '.py', 'w')
    for Lines_sub in Lines:
        fid.write( Lines_sub + '\n')

    fid.close()

        

    