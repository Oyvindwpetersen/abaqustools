# -*- coding: utf-8 -*-

#%%

import sys
import os
import numpy as np
import putools
import h5py

#%%
def static(foldername_odb,jobname,folder_save,folder_python,variables=None,stepnumber=None,framenumber=None,deletetxt=True,createh5=True,prefix=None,postfixh5=None,exportscript=None):

    # stepnumber
    stepnumber=stepnumber or -1
    
    # framenumber
    framenumber=framenumber or -1
    
    # Variables to export
    variables=variables or ['u' , 'sf' , 'nodecoord' , 'elconn' , 'elset']

    # H5 name
    postfixh5=postfixh5 or '_exportstatic'

    # Script py
    exportscript=exportscript or jobname + '_exportstatic'
    
    exportmain(foldername_odb,jobname,folder_save,folder_python,variables,stepnumber,framenumber,deletetxt=deletetxt,createh5=createh5,prefix=prefix,postfixh5=postfixh5,exportscript=exportscript)

def modal(foldername_odb,jobname,folder_save,folder_python,variables=None,stepnumber=None,framenumber=None,deletetxt=True,createh5=True,prefix=None,postfixh5=None,exportscript=None):

    # stepnumber
    stepnumber=stepnumber or -1
    
    # framenumber
    framenumber=framenumber or 'skipfirst'
    
    # Variables to export
    variables=variables or ['f' , 'gm' , 'phi' , 'phi_sf' , 'nodecoord' , 'elconn' ]

    # H5 name
    postfixh5=postfixh5 or '_exportmodal'

    # Script py
    exportscript=exportscript or jobname + '_exportmodal'
    
    exportmain(foldername_odb,jobname,folder_save,folder_python,variables,stepnumber,framenumber,deletetxt=deletetxt,createh5=createh5,prefix=prefix,postfixh5=postfixh5,exportscript=exportscript)

#%%

def exportmain(foldername_odb,jobname,folder_save,folder_python,variables,stepnumber,framenumber,deletetxt=True,createh5=True,prefix=None,postfixh5=None,exportscript=None):

    # Cut odb extension
    if jobname.endswith('.odb'):
        jobname=jobname[:-4]
    
    # prefix
    prefix=prefix or jobname+'_export_'
    
    # prefix
    postfixh5=postfixh5 or '_export'
    
    # Name of export python script
    exportscript=exportscript or jobname + '_export'
    
    file_name=foldername_odb + '\\' + jobname + '.odb'
    file_exist_logic=os.path.isfile(file_name)
    if not file_exist_logic:
        print('***** ' + file_name)
        raise Exception('***** ODB file not found')
        
    # Write py-file for export
    writepyscript(foldername_odb,jobname,folder_save,folder_python,variables,stepnumber,framenumber,exportscript=exportscript,prefix=prefix)
    
    # Run py-file in abaqus
    system_cmd='abaqus cae noGUI=' + folder_save + '/' + exportscript + '.py'
    sys_out=os.popen(system_cmd).read()
    
    # Collect data for h5
    h5_var=[]
    h5_data=[]
    h5_isnum=[]
    
    for k in np.arange(len(variables)):
        
        FileNameBase=folder_save + '/' + prefix
        
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
        hf_name=folder_save + '/' + jobname + postfixh5 + '.h5'
        export2h5(hf_name,h5_var,h5_data,h5_isnum)
        
    # Delete txt files identified by prefix
    if deletetxt==True:
        deletefiles(folder_save,prefix,['.txt'])

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
        

def deletefiles(foldername,name_match,extensions):
    
    # Find files that match
    FileNameListDir=os.listdir(foldername)
    IndexMatch=putools.num.listindexsub(FileNameListDir,name_match)
    
    for k in np.arange(len(IndexMatch)):
            
        FileNameRemove=FileNameListDir[IndexMatch[k]]
        
        # Only selected files
        match_logic=[list_sub in FileNameRemove for list_sub in extensions]
        if sum(match_logic)>0:
            os.remove(foldername + '/' + FileNameRemove)

#%% Export modal script

def writepyscript(foldername_odb,jobname,folder_save,folder_python,variables,stepnumber,framenumber,exportscript='ExportModal',prefix='_export'):
    
    if isinstance(variables,str):
        variables=[variables]
    
    Lines=['']
    
    Lines.append('import os')
    Lines.append('import sys')
    Lines.append('import numpy as np')
    Lines.append('')
    
    Lines.append('foldername_odb=' + '\'' + foldername_odb + '\'')
    Lines.append('jobname=' + '\'' + jobname + '\'')
    Lines.append('folder_save=' + '\'' + folder_save + '\'')
    Lines.append('folder_python=' + '\'' + folder_python + '\'')
    
    Lines.append('prefix=' + '\'' + prefix + '\'')
    Lines.append('')
    
    Lines.append('# Import functions for export (odbexport package)')
    Lines.append('sys.path.append(folder_python)')
    
    #Lines.append('CurrentDir=os.getcwd()')
    #Lines.append('os.chdir(folder_python)')
    Lines.append('import odbfunc')
    #Lines.append('os.chdir(CurrentDir)')
    Lines.append('')
    
    #Lines=writepyscript_begin(foldername_odb,jobname,folder_save,folder_python,prefix)
    
    Lines.append('# Open ODB')
    Lines.append( 'odb_id=odbfunc.open_odb(foldername_odb,jobname)')
    Lines.append('')
    
    if isinstance(stepnumber,str):
        stepnumber_str=stepnumber
    else:
        stepnumber_str=str(stepnumber)
    
    if isinstance(framenumber,str):
        framenumber_str=framenumber
        if framenumber_str=='skipfirst':
            framenumber_str='\'skipfirst\''
    else:
        framenumber_str=str(framenumber)
        
    Lines.append('# Step and frames to export')
    Lines.append( 'stepnumber=' + stepnumber_str)
    Lines.append( 'framenumber=' + framenumber_str)
    Lines.append('')

    if 'f' in variables:
        Lines.append('# Frequencies')
        Lines.append( 'f=odbfunc.exporthistoryoutput(odb_id,stepnumber,' + '\'' + 'EIGFREQ' + '\'' +  ')' )
        Lines.append( 'odbfunc.save2txt(folder_save,' +  '\'f\'' + ',f,atype=1,prefix=prefix)' )
        Lines.append('')

    if 'gm' in variables:
        Lines.append('# Generalized mass')
        Lines.append( 'gm=odbfunc.exporthistoryoutput(odb_id,stepnumber,' + '\'' + 'GM' + '\'' +  ')' )
        Lines.append( 'odbfunc.save2txt(folder_save,' + '\'gm\'' + ',gm,atype=1,prefix=prefix)' )
        Lines.append('')

    if 'phi' in variables:
        Lines.append('# Mode shapes')
        Lines.append( '(phi,phi_label)=odbfunc.exportdisplacement(odb_id,stepnumber,framenumber=framenumber' + ')' )
        Lines.append( 'odbfunc.save2txt(folder_save,' + '\'phi\'' + ',phi,atype=1,prefix=prefix)' )
        Lines.append( 'odbfunc.save2txt(folder_save,' + '\'phi_label\'' + ',phi_label,atype=2,prefix=prefix)' )
        Lines.append('')

    if 'phi_sf' in variables:
        Lines.append('# Modal section forces')
        Lines.append( '(phi_sf,phi_sf_label)=odbfunc.exportsectionforce(odb_id,stepnumber,framenumber=framenumber' + ')' )
        Lines.append( 'odbfunc.save2txt(folder_save,' + '\'phi_sf\'' + ',phi_sf,atype=1,prefix=prefix)' )
        Lines.append( 'odbfunc.save2txt(folder_save,' + '\'phi_sf_label\'' + ',phi_sf_label,atype=2,prefix=prefix)' )
        Lines.append('')

    if 'u' in variables:
        Lines.append('# Displacements')
        Lines.append( '(u,u_label)=odbfunc.exportdisplacement(odb_id,stepnumber,framenumber=framenumber' + ')' )
        Lines.append( 'odbfunc.save2txt(folder_save,' + '\'u\'' + ',u,atype=1,prefix=prefix)' )
        Lines.append( 'odbfunc.save2txt(folder_save,' + '\'u_label\'' + ',u_label,atype=2,prefix=prefix)' )
        Lines.append('')

    if 'sf' in variables:
        Lines.append('# Section forces')
        Lines.append( '(sf,sf_label)=odbfunc.exportsectionforce(odb_id,stepnumber,framenumber=framenumber' + ')' )
        Lines.append( 'odbfunc.save2txt(folder_save,' + '\'sf\'' + ',sf,atype=1,prefix=prefix)' )
        Lines.append( 'odbfunc.save2txt(folder_save,' + '\'sf_label\'' + ',sf_label,atype=2,prefix=prefix)' )
        Lines.append('')
        
    if 'nodecoord' in variables:
        Lines.append('# Node coordinates')
        Lines.append( 'nodecoord=odbfunc.exportnodecoord(odb_id,stepnumber' + ',0)' )
        Lines.append( 'odbfunc.save2txt(folder_save,' + '\'nodecoord\'' + ',nodecoord,atype=1,prefix=prefix)' )
        Lines.append('')
        
    if 'elconn' in variables:
        Lines.append('# Element connectivity')
        Lines.append( 'elconn=odbfunc.exportelconn(odb_id)' )
        Lines.append( 'odbfunc.save2txt(folder_save,' + '\'elconn\'' + ',elconn,atype=1,prefix=prefix)' )
        Lines.append('')
        
    if 'elset' in variables:
        Lines.append('# Element sets')
        Lines.append( '(elset,elset_label)=odbfunc.exportelsets(odb_id)' )
        Lines.append( 'odbfunc.save2txt(folder_save,' + '\'elset\'' + ',elset,atype=1,prefix=prefix)' )
        Lines.append( 'odbfunc.save2txt(folder_save,' + '\'elset_label\'' + ',elset_label,atype=2,prefix=prefix)' )
        Lines.append('')
    
    Lines.append('# Close ODB')
    Lines.append( 'odbfunc.close_odb(odb_id)' )
        
    fid=open(folder_save + '\\' + exportscript + '.py', 'w')
    for Lines_sub in Lines:
        fid.write( Lines_sub + '\n')

    fid.close()

