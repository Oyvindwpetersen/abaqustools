# -*- coding: utf-8 -*-

#%%

import sys
import os
import numpy as np
import putools
import h5py

#%%
def static(FolderODB,NameODB,FolderSave,FolderPython,variables=None,StepNumber=None,FrameNumber=None,deletetxt=True,createh5=True,prefix=None,postfixh5=None,ExportScript=None):

    # StepNumber
    StepNumber=StepNumber or -1
    
    # FrameNumber
    FrameNumber=FrameNumber or -1
    
    # Variables to export
    variables=variables or ['u' , 'sf' , 'nodecoord' , 'elconn' , 'elset']

    # H5 name
    postfixh5=postfixh5 or '_exportstatic'

    # Script py
    ExportScript=ExportScript or NameODB + '_exportstatic'
    
    exportmain(FolderODB,NameODB,FolderSave,FolderPython,variables,StepNumber,FrameNumber,deletetxt=deletetxt,createh5=createh5,prefix=prefix,postfixh5=postfixh5,ExportScript=ExportScript)

def modal(FolderODB,NameODB,FolderSave,FolderPython,variables=None,StepNumber=None,FrameNumber=None,deletetxt=True,createh5=True,prefix=None,postfixh5=None,ExportScript=None):

    # StepNumber
    StepNumber=StepNumber or -1
    
    # FrameNumber
    FrameNumber=FrameNumber or 'skipfirst'
    
    # Variables to export
    variables=variables or ['f' , 'gm' , 'phi' , 'phi_sf' , 'nodecoord' , 'elconn' ]

    # H5 name
    postfixh5=postfixh5 or '_exportmodal'

    # Script py
    ExportScript=ExportScript or NameODB + '_exportmodal'
    
    exportmain(FolderODB,NameODB,FolderSave,FolderPython,variables,StepNumber,FrameNumber,deletetxt=deletetxt,createh5=createh5,prefix=prefix,postfixh5=postfixh5,ExportScript=ExportScript)

#%%

def exportmain(FolderODB,NameODB,FolderSave,FolderPython,variables,StepNumber,FrameNumber,deletetxt=True,createh5=True,prefix=None,postfixh5=None,ExportScript=None):

    # Cut odb extension
    if NameODB.endswith('.odb'):
        NameODB=NameODB[:-4]
    
    # prefix
    prefix=prefix or NameODB+'_export_'
    
    # prefix
    postfixh5=postfixh5 or '_export'
    
    # Name of export python script
    ExportScript=ExportScript or NameODB + '_export'
    
    # Write py-file for export
    writepyscript(FolderODB,NameODB,FolderSave,FolderPython,variables,StepNumber,FrameNumber,ExportScript=ExportScript,prefix=prefix)
    
    # Run py-file in abaqus
    system_cmd='abaqus cae noGUI=' + FolderSave + '/' + ExportScript + '.py'
    sys_out=os.popen(system_cmd).read()
    
    # Collect data for h5
    h5_var=[]
    h5_data=[]
    h5_isnum=[]
    
    for k in np.arange(len(variables)):
        
        FileNameBase=FolderSave + '/' + prefix
        
        # Read txt file
        data_temp=np.genfromtxt(FileNameBase+variables[k]+'.txt', delimiter=',')
        h5_var.append(variables[k])
        h5_data.append(data_temp)
        h5_isnum.append(True)
        
        # Special cases
        if variables[k]=='phi':
            fid=open(FileNameBase+'phi_label.txt','r')
            phi_label=fid.read().splitlines()
            fid.close()
            h5_var.append('phi_label')
            h5_data.append(phi_label)
            h5_isnum.append(False)
        elif variables[k]=='phi_sf':
            fid=open(FileNameBase+'phi_sf_label.txt','r')
            phi_sf_label=fid.read().splitlines()
            fid.close()
            h5_var.append('phi_sf_label')
            h5_data.append(phi_sf_label)
            h5_isnum.append(False)
        elif variables[k]=='u':
            fid=open(FileNameBase+'u_label.txt','r')
            u_label=fid.read().splitlines()
            fid.close()
            h5_var.append('u_label')
            h5_data.append(u_label)
            h5_isnum.append(False)
        elif variables[k]=='sf':
            fid=open(FileNameBase+'sf_label.txt','r')
            sf_label=fid.read().splitlines()
            fid.close()
            h5_var.append('sf_label')
            h5_data.append(sf_label)
            h5_isnum.append(False)
        elif variables[k]=='elset':
            fid=open(FileNameBase+'elset_label.txt','r')
            elset_label=fid.read().splitlines()
            fid.close()
            h5_var.append('elset_label')
            h5_data.append(elset_label)
            h5_isnum.append(False)
            
            
    if createh5==True:
        
        #if os.path.exists(hf_name):
        hf_name=FolderSave + '/' + NameODB + postfixh5 + '.h5'
        export2h5(hf_name,h5_var,h5_data,h5_isnum)
        
    # Delete txt files identified by prefix
    if deletetxt==True:
        deletetxtfiles(FolderSave,prefix)

#%% 

def export2h5(hf_name,h5_var,h5_data,h5_isnum):
    
    hf = h5py.File(hf_name,'w')
    dt = h5py.special_dtype(vlen=str)
    
    for k in np.arange(len(h5_var)):
        
        # If data is not numeric (text), convert
        if h5_isnum[k]==True:
            hf.create_dataset(h5_var[k],data=h5_data[k])
        else:
            data_temp=np.array(h5_data[k],dtype=dt)
            hf.create_dataset(h5_var[k],data=data_temp)
        

def deletetxtfiles(FolderSave,name_match):

    # Find files that match
    FileNameListDir=os.listdir(FolderSave)
    IndexMatch=putools.num.listindexsub(FileNameListDir,name_match)
    
    for k in np.arange(len(IndexMatch)):
            
        FileNameRemove=FileNameListDir[IndexMatch[k]]
            
        # Only txt files
        if not '.txt' in FileNameRemove:
            continue
            
        os.remove(FolderSave + '/' + FileNameRemove)

#%% Export modal script

def writepyscript(FolderODB,NameODB,FolderSave,FolderPython,variables,StepNumber,FrameNumber,ExportScript='ExportModal',prefix='_export'):
    
    if isinstance(variables,str):
        variables=[variables]
    
    Lines=['']
    
    Lines.append('import os')
    Lines.append('import sys')
    Lines.append('import numpy as np')
    Lines.append('')
    
    Lines.append('FolderODB=' + '\'' + FolderODB + '\'')
    Lines.append('JobName=' + '\'' + NameODB + '\'')
    Lines.append('FolderSave=' + '\'' + FolderSave + '\'')
    Lines.append('FolderPython=' + '\'' + FolderPython + '\'')
    
    Lines.append('prefix=' + '\'' + prefix + '\'')
    Lines.append('')
    
    Lines.append('# Import functions for export')
    Lines.append('sys.path.append(FolderPython)')
    
    #Lines.append('CurrentDir=os.getcwd()')
    #Lines.append('os.chdir(FolderPython)')
    Lines.append('import odbfunc')
    #Lines.append('os.chdir(CurrentDir)')
    Lines.append('')
    
    #Lines=writepyscript_begin(FolderODB,NameODB,FolderSave,FolderPython,prefix)
    
    Lines.append('# Open ODB')
    Lines.append( 'myOdb=odbfunc.open_odb(FolderODB,' + '\'' + NameODB + '\'' + ')' )
    Lines.append('')
    
    if isinstance(StepNumber,str):
        StepNumber_str=StepNumber
    else:
        StepNumber_str=str(StepNumber)
    
    if isinstance(FrameNumber,str):
        FrameNumber_str=FrameNumber
        if FrameNumber_str=='skipfirst':
            FrameNumber_str='\'skipfirst\''
    else:
        FrameNumber_str=str(FrameNumber)
        
    Lines.append('# Step and frames to export')
    Lines.append( 'StepNumber=' + StepNumber_str)
    Lines.append( 'FrameNumber=' + FrameNumber_str)
    Lines.append('')

    if 'f' in variables:
        Lines.append('# Frequencies')
        Lines.append( 'f=odbfunc.exporthistoryoutput(myOdb,StepNumber,' + '\'' + 'EIGFREQ' + '\'' +  ')' )
        Lines.append( 'odbfunc.save2txt(FolderSave,' +  '\'f\'' + ',f,atype=1,prefix=prefix)' )
        Lines.append('')

    if 'gm' in variables:
        Lines.append('# Generalized mass')
        Lines.append( 'gm=odbfunc.exporthistoryoutput(myOdb,StepNumber,' + '\'' + 'GM' + '\'' +  ')' )
        Lines.append( 'odbfunc.save2txt(FolderSave,' + '\'gm\'' + ',gm,atype=1,prefix=prefix)' )
        Lines.append('')

    if 'phi' in variables:
        Lines.append('# Mode shapes')
        Lines.append( '(phi,phi_label)=odbfunc.exportdisplacement(myOdb,StepNumber,FrameNumber=FrameNumber' + ')' )
        Lines.append( 'odbfunc.save2txt(FolderSave,' + '\'phi\'' + ',phi,atype=1,prefix=prefix)' )
        Lines.append( 'odbfunc.save2txt(FolderSave,' + '\'phi_label\'' + ',phi_label,atype=2,prefix=prefix)' )
        Lines.append('')

    if 'phi_sf' in variables:
        Lines.append('# Modal section forces')
        Lines.append( '(phi_sf,phi_sf_label)=odbfunc.exportsectionforce(myOdb,StepNumber,FrameNumber=FrameNumber' + ')' )
        Lines.append( 'odbfunc.save2txt(FolderSave,' + '\'phi_sf\'' + ',phi_sf,atype=1,prefix=prefix)' )
        Lines.append( 'odbfunc.save2txt(FolderSave,' + '\'phi_sf_label\'' + ',phi_sf_label,atype=2,prefix=prefix)' )
        Lines.append('')

    if 'u' in variables:
        Lines.append('# Displacements')
        Lines.append( '(u,u_label)=odbfunc.exportdisplacement(myOdb,StepNumber,FrameNumber=FrameNumber' + ')' )
        Lines.append( 'odbfunc.save2txt(FolderSave,' + '\'u\'' + ',u,atype=1,prefix=prefix)' )
        Lines.append( 'odbfunc.save2txt(FolderSave,' + '\'u_label\'' + ',u_label,atype=2,prefix=prefix)' )
        Lines.append('')

    if 'sf' in variables:
        Lines.append('# Section forces')
        Lines.append( '(sf,sf_label)=odbfunc.exportsectionforce(myOdb,StepNumber,FrameNumber=FrameNumber' + ')' )
        Lines.append( 'odbfunc.save2txt(FolderSave,' + '\'sf\'' + ',sf,atype=1,prefix=prefix)' )
        Lines.append( 'odbfunc.save2txt(FolderSave,' + '\'sf_label\'' + ',sf_label,atype=2,prefix=prefix)' )
        Lines.append('')
        
    if 'nodecoord' in variables:
        Lines.append('# Node coordinates')
        Lines.append( 'nodecoord=odbfunc.exportnodecoord(myOdb,StepNumber' + ',0)' )
        Lines.append( 'odbfunc.save2txt(FolderSave,' + '\'nodecoord\'' + ',nodecoord,atype=1,prefix=prefix)' )
        Lines.append('')
        
    if 'elconn' in variables:
        Lines.append('# Element connectivity')
        Lines.append( 'elconn=odbfunc.exportelconn(myOdb)' )
        Lines.append( 'odbfunc.save2txt(FolderSave,' + '\'elconn\'' + ',elconn,atype=1,prefix=prefix)' )
        Lines.append('')
        
    if 'elset' in variables:
        Lines.append('# Element sets')
        Lines.append( '(elset,elset_label)=odbfunc.exportelsets(myOdb)' )
        Lines.append( 'odbfunc.save2txt(FolderSave,' + '\'elset\'' + ',elset,atype=1,prefix=prefix)' )
        Lines.append( 'odbfunc.save2txt(FolderSave,' + '\'elset_label\'' + ',elset_label,atype=2,prefix=prefix)' )
        Lines.append('')
    
    Lines.append('# Close ODB')
    Lines.append( 'odbfunc.close_odb(myOdb)' )
        
    fid=open(FolderSave + '\\' + ExportScript + '.py', 'w')
    for Lines_sub in Lines:
        fid.write( Lines_sub + '\n')

    fid.close()

