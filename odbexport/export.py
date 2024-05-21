# -*- coding: utf-8 -*-

#%%

import sys
import os
import time
import numpy as np
import putools
import h5py
from timeit import default_timer as timer

#%%

def static(folder_odb,jobname,folder_save,folder_python,variables=None,stepnumber=None,framenumber=None,deletetxt=True,saveh5=True,prefix=None,postfixh5='_exportstatic',exportscript=None):

    '''
    Export static results from odb file

    Arguments
    ------------
    folder_odb (str): folder of odb file
    jobname (str): name of odb file
    folder_save (str): folder for export
    folder_python (str): folder where the python abaqustools repo is located (must be added in abaqus)
    variables (list): output quantities to export
    stepnumber (int): step number 
    framenumber (int or list): frame number(s)
    deletetxt (bool): delete txt output files after export
    saveh5 (bool): save output to h5 file
    prefix (str): prefix for txt files
    postfixh5 (str): postfix for h5 file
    exportscript (str): name of python script that is created
    
    Returns
    ------------
    None
    
    '''
    
    # Stepnumber
    if stepnumber is None:
        stepnumber=-1
    
    # Framenumber
    if framenumber is None:
        framenumber=-1

    # Variables to export
    if variables is None:
       variables=['u' , 'sf' , 'nodecoord' , 'elconn' , 'elset']

    # Script py file
    if exportscript is None:
       exportscript=jobname + '_exportstatic'
    
    # Run main
    exportmain(folder_odb,jobname,folder_save,folder_python,variables,stepnumber,framenumber,deletetxt=deletetxt,saveh5=saveh5,prefix=prefix,postfixh5=postfixh5,exportscript=exportscript)

def modal(folder_odb,jobname,folder_save,folder_python,variables=None,stepnumber=None,framenumber=None,deletetxt=True,saveh5=True,prefix=None,postfixh5='_exportmodal',exportscript=None,nodes=None):
    
    '''
    Export modal results from odb file

    Arguments
    ------------
    folder_odb (str): folder of odb file
    jobname (str): name of odb file
    folder_save (str): folder for export
    folder_python (str): folder where the python abaqustools repo is located (must be added in abaqus)
    variables (list): output quantities to export
    stepnumber (int): step number 
    framenumber (int or list): frame number(s)
    deletetxt (bool): delete txt output files after export
    saveh5 (bool): save output to h5 file
    prefix (str): prefix for txt files
    postfixh5 (str): postfix for h5 file
    exportscript (str): name of python script that is created
    
    Returns
    ------------
    None
    
    '''
    
    if stepnumber is None:
        stepnumber=-1
    
    # Framenumber
    if framenumber is None:
        framenumber='skipfirst'
    
    # Variables to export
    if variables is None:
       variables=['f' , 'gm' , 'phi' , 'phi_sf' , 'nodecoord' , 'elconn']

    # Script py file
    if exportscript is None:
       exportscript=jobname + '_exportmodal'
       
    # Run main
    exportmain(folder_odb,jobname,folder_save,folder_python,variables,stepnumber,framenumber,deletetxt=deletetxt,saveh5=saveh5,prefix=prefix,postfixh5=postfixh5,exportscript=exportscript,nodes=nodes)

#%%

def exportmain(folder_odb,jobname,folder_save,folder_python,variables,stepnumber,framenumber,deletetxt=True,saveh5=True,prefix=None,postfixh5=None,exportscript=None,nodes=None):

    '''
    Export outputs from odb file to txt or h5 file

    Arguments
    ------------
    folder_odb (str): folder of odb file
    jobname (str): name of odb file
    folder_save (str): folder for export
    folder_python (str): folder where the python abaqustools repo is located (must be added in abaqus)
    variables (list): output quantities to export
    stepnumber (int): step number 
    framenumber (int or list): frame number(s)
    deletetxt (bool): delete txt output files after export
    saveh5 (bool): save output to h5 file
    prefix (str): prefix for txt files
    postfixh5 (str): postfix for h5 file
    exportscript (str): name of python script that is created
    
    Returns
    ------------
    None
    
    '''
    
    # Cut odb extension
    if jobname.endswith('.odb'):
        jobname=jobname[:-4]
    
    # Prefix for saving txt files
    if prefix is None:
        prefix=jobname+'_export_'
    
    # Postfix for h5 file
    if postfixh5 is None:
        postfixh5=jobname+'_export'
    
    # Check if ODB file is found
    file_name=folder_odb + '\\' + jobname + '.odb'
    file_exist_logic=os.path.isfile(file_name)
    if not file_exist_logic:
        print('***** ' + file_name)
        raise Exception('***** ODB file not found')
        
    # Check if python folder and python files are given correctly
    file_name=folder_python + '\\' + 'odbfunc.py'
    file_exist_logic=os.path.isfile(file_name)
    if not file_exist_logic:
        print('***** ' + folder_python)
        raise Exception('***** Supplied python (odbexport) folder and odbfunc module not found')    
 
    # Ensure list
    if isinstance(variables,str):
        variables=[variables]
        
    # Lower case
    variables=[x.lower() for x in variables]

    # Check input variables
    variables_allowed= ['u' , 'sf' , 'phi' , 'phi_sf' , 'f' , 'gm' , 'nodecoord' , 'elconn' , 'elset']
    for k in np.arange(len(variables)):
        if not variables[k] in variables_allowed:
            print('***** Check variable ' + variables[k])
            raise Exception('***** Variable identifier not allowed')
            
    # Write py-file for export
    writepyscript(folder_odb,jobname,folder_save,folder_python,variables,stepnumber,framenumber,exportscript=exportscript,prefix=prefix,nodes=nodes)
    
    # Run py-file in abaqus
    system_cmd='abaqus cae noGUI=' + folder_save + '/' + exportscript + '.py'
    
    t0=timer()
    sys_out=os.popen(system_cmd).read()
    t1=timer()
    
    idx_error=sys_out.find('error')

    if idx_error>0:
        print(sys_out)
        raise Exception('***** Export aborted due to errors, see above')
    else:
        print('***** ABAQUS export completed in ' + putools.num.num2strf(t1-t0,1) + ' s')

    # Save h5 file        
    if saveh5==True:

        # Base for txt files
        hf_name=folder_save + '/' + jobname + postfixh5 + '.h5'
        
        # Overwrite file
        if os.path.exists(hf_name):
            os.remove(hf_name)
            time.sleep(1)
            
        hf = h5py.File(hf_name,'w')
        dt = h5py.special_dtype(vlen=str)
            
        for k in np.arange(len(variables)):
            
            # Base for txt files
            filename_base=folder_save + '/' + prefix      
            
            # Read txt file
            data_from_txt=np.genfromtxt(filename_base+variables[k]+'.txt', delimiter=',')
            
            if variables[k]=='u':
            
                hf.create_dataset('u',data=data_from_txt)
                hf['u'].attrs.modify('Type','Displacement')
                hf['u'].attrs.modify('Unit','m, rad')
                
                fid=open(filename_base+'u_label.txt','r'); label=fid.read().splitlines(); fid.close()  
                hf.create_dataset('u_label',data=label,dtype=dt)
                hf['u_label'].attrs.modify('Type','DOF labels')
                
            elif variables[k]=='sf':
            
                hf.create_dataset('sf',data=data_from_txt)
                hf['sf'].attrs.modify('Type','Section force')
                hf['sf'].attrs.modify('Unit','m, rad')
                
                fid=open(filename_base+'sf_label.txt','r'); label=fid.read().splitlines(); fid.close()  
                hf.create_dataset('sf_label',data=label,dtype=dt)
                hf['sf_label'].attrs.modify('Type', 'Element labels')
                
            elif variables[k]=='phi':
            
                hf.create_dataset('phi',data=data_from_txt)
                hf['phi'].attrs.modify('Type','Modal displacement')
                hf['phi'].attrs.modify('Unit','m, rad')
                
                fid=open(filename_base+'phi_label.txt','r'); label=fid.read().splitlines(); fid.close()  
                hf.create_dataset('phi_label',data=label,dtype=dt)
                hf['phi_label'].attrs.modify('Type','DOF labels')
                
            elif variables[k]=='phi_sf':
            
                hf.create_dataset('phi_sf',data=data_from_txt)
                hf['phi_sf'].attrs.modify('Type','Modal section force')
                hf['phi_sf'].attrs.modify('Unit','N, Nm')
                
                fid=open(filename_base+'phi_sf_label.txt','r'); label=fid.read().splitlines(); fid.close()  
                hf.create_dataset('phi_sf_label',data=label,dtype=dt)
                hf['phi_sf_label'].attrs.modify('Type','Element labels')        
                
            elif variables[k]=='f':
            
                hf.create_dataset('f',data=data_from_txt)
                hf['f'].attrs.modify('Type','Natural frequency')
                hf['f'].attrs.modify('Unit','Hz')
                
            elif variables[k]=='gm':
            
                hf.create_dataset('gm',data=data_from_txt)
                hf['gm'].attrs.modify('Type','Generalized mass')
                hf['gm'].attrs.modify('Unit','kg')
                
            elif variables[k]=='nodecoord':
            
                hf.create_dataset('nodecoord',data=data_from_txt)
                hf['nodecoord'].attrs.modify('Type','Node coordinate')
                hf['nodecoord'].attrs.modify('Unit','Node number, m')     
                
            elif variables[k]=='elconn':
            
                hf.create_dataset('elconn',data=data_from_txt)
                hf['elconn'].attrs.modify('Type','Element connectivity')
                hf['elconn'].attrs.modify('Unit','Element number, Node number')                     
                
            elif variables[k]=='elset':
           
                hf.create_dataset('elset',data=data_from_txt)
                hf['elset'].attrs.modify('Type','Element sets')
                hf['elset'].attrs.modify('Unit','Element number')      
           
                fid=open(filename_base+'elset_label.txt','r'); label=fid.read().splitlines(); fid.close()  
                hf.create_dataset('elset_label',data=label,dtype=dt)
                hf['elset_label'].attrs.modify('Type','Element labels')    
                            

    hf.close()
    
    # Delete txt files identified by prefix
    if deletetxt==True:
        deletefiles(folder_save,prefix,['.txt'])
        
    # Delete rpy files
    deletefiles(folder_odb,'abaqus.rpy',[''])
        

#%% 

def deletefiles(foldername,name_match,extensions):
    
    '''
    Delete files in folder that match search criteria

    Arguments
    ------------
    foldername (str): folder to search
    name_match (str): file name to delete (partial match allowed)
    extensions (list): specified extensions to include
    
    Returns
    ------------
    None
    
    '''

    # Find files that match file name 
    
    filenames_dir=os.listdir(foldername)
    idx_match=putools.num.listindexsub(filenames_dir,name_match)
    
    for k in np.arange(len(idx_match)):
            
        filename_remove=filenames_dir[idx_match[k]]
        
        match_ext=[filename_remove.endswith(ext) for ext in extensions]
        
        # Only files with specified extensions
        if any(match_ext):
        
            try:
                os.remove(foldername + '/' + filename_remove)
            except:
                print('***** Was not able to delete file ' + foldername + '/' + filename_remove)
                    
            

#%% Export modal script

def writepyscript(folder_odb,jobname,folder_save,folder_python,variables,stepnumber,framenumber,exportscript='Export',prefix='_export',nodes=None):
    
    '''
    Write py script that for export within Abaqus environment

    Arguments
    ------------
    folder_odb (str): folder of odb file
    jobname (str): name of odb file
    folder_save (str): folder where output files are saved
    folder_python (str): folder where the python abaqustools repo is located (must be added in abaqus)
    folder_python (str): folder where the python abaqustools repo is located (must be added in abaqus)
    variables (list): output quantities to export
    stepnumber (int): step number 
    framenumber (int or list): frame number(s)
    exportscript (str): name of python script that is created
    prefix (str): prefix for txt files

    Returns
    ------------
    None
    
    '''
        
    # Ensure list
    if isinstance(variables,str):
        variables=[variables]
    
    # Format folder
    folder_odb=folder_odb.replace('\\','/')
    folder_save=folder_save.replace('\\','/')
    
    lines=['']
    
    lines.append('import os')
    lines.append('import sys')
    lines.append('import numpy as np')
    lines.append('')
    
    lines.append('folder_odb=' + '\'' + folder_odb + '\'')
    lines.append('jobname=' + '\'' + jobname + '\'')
    lines.append('folder_save=' + '\'' + folder_save + '\'')
    lines.append('folder_python=' + '\'' + folder_python + '\'')
    
    lines.append('prefix=' + '\'' + prefix + '\'')
    lines.append('')
    
    lines.append('# Import functions for export (odbexport package)')
    lines.append('sys.path.append(folder_python)')
    lines.append('import odbfunc')
    lines.append('')
    
    lines.append('# Open ODB')
    lines.append('odb_id=odbfunc.open_odb(folder_odb,jobname)')
    lines.append('')
    
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
        

    lines.append('# Step and frames to export')
    lines.append('stepnumber=' + stepnumber_str)
    lines.append('framenumber=' + framenumber_str)
    lines.append('')
    
    lines.append('# Node numbers to export')
    
    if nodes is None:
        lines.append('nodes=' + 'None')
    else:
    
        nodes = [int(num) for num in nodes]
        lines.append('nodes=' + '[')

        for i in range(0, len(nodes), 20):
            str_nodes_sub=', '.join(map(str, nodes[i:i+20]))
            lines.append(str_nodes_sub + ',')
        
        lines.append(']')
        
    lines.append('')

    if 'f' in variables:
        lines.append('# Frequencies')
        lines.append('f=odbfunc.exporthistoryoutput(odb_id,stepnumber,' + '\'' + 'EIGFREQ' + '\'' +  ')')
        lines.append('odbfunc.save2txt(folder_save,' +  '\'f\'' + ',f,atype=1,prefix=prefix)')
        lines.append('')

    if 'gm' in variables:
        lines.append('# Generalized mass')
        lines.append('gm=odbfunc.exporthistoryoutput(odb_id,stepnumber,' + '\'' + 'GM' + '\'' +  ')')
        lines.append('odbfunc.save2txt(folder_save,' + '\'gm\'' + ',gm,atype=1,prefix=prefix)')
        lines.append('')

    if 'phi' in variables:
        lines.append('# Mode shapes')
        lines.append('(phi,phi_label)=odbfunc.exportdisplacement(odb_id,stepnumber,framenumber=framenumber,nodes=nodes' + ')')
        lines.append('odbfunc.save2txt(folder_save,' + '\'phi\'' + ',phi,atype=1,prefix=prefix)')
        lines.append('odbfunc.save2txt(folder_save,' + '\'phi_label\'' + ',phi_label,atype=2,prefix=prefix)')
        lines.append('')

    if 'phi_sf' in variables:
        lines.append('# Modal section forces')
        lines.append('(phi_sf,phi_sf_label)=odbfunc.exportsectionforce(odb_id,stepnumber,framenumber=framenumber' + ')')
        lines.append('odbfunc.save2txt(folder_save,' + '\'phi_sf\'' + ',phi_sf,atype=1,prefix=prefix)')
        lines.append('odbfunc.save2txt(folder_save,' + '\'phi_sf_label\'' + ',phi_sf_label,atype=2,prefix=prefix)')
        lines.append('')

    if 'u' in variables:
        lines.append('# Displacements')
        lines.append('(u,u_label)=odbfunc.exportdisplacement(odb_id,stepnumber,framenumber=framenumber,nodes=nodes' + ')')
        lines.append('odbfunc.save2txt(folder_save,' + '\'u\'' + ',u,atype=1,prefix=prefix)')
        lines.append('odbfunc.save2txt(folder_save,' + '\'u_label\'' + ',u_label,atype=2,prefix=prefix)')
        lines.append('')

    if 'sf' in variables:
        lines.append('# Section forces')
        lines.append('(sf,sf_label)=odbfunc.exportsectionforce(odb_id,stepnumber,framenumber=framenumber' + ')')
        lines.append('odbfunc.save2txt(folder_save,' + '\'sf\'' + ',sf,atype=1,prefix=prefix)')
        lines.append('odbfunc.save2txt(folder_save,' + '\'sf_label\'' + ',sf_label,atype=2,prefix=prefix)')
        lines.append('')
        
    if 'nodecoord' in variables:
        lines.append('# Node coordinates')
        lines.append('nodecoord=odbfunc.exportnodecoord(odb_id,stepnumber' + ',0)')
        lines.append('odbfunc.save2txt(folder_save,' + '\'nodecoord\'' + ',nodecoord,atype=1,prefix=prefix)')
        lines.append('')
        
    if 'elconn' in variables:
        lines.append('# Element connectivity')
        lines.append('elconn=odbfunc.exportelconn(odb_id)')
        lines.append('odbfunc.save2txt(folder_save,' + '\'elconn\'' + ',elconn,atype=1,prefix=prefix)')
        lines.append('')
        
    if 'elset' in variables:
        lines.append('# Element sets')
        lines.append('(elset,elset_label)=odbfunc.exportelsets(odb_id)')
        lines.append('odbfunc.save2txt(folder_save,' + '\'elset\'' + ',elset,atype=1,prefix=prefix)')
        lines.append('odbfunc.save2txt(folder_save,' + '\'elset_label\'' + ',elset_label,atype=2,prefix=prefix)')
        lines.append('')
    
    lines.append('# Close ODB')
    lines.append('odbfunc.close_odb(odb_id)')
        
    # Write py script
    fid=open(folder_save + '\\' + exportscript + '.py', 'w')
    for lines_sub in lines:
        fid.write( lines_sub + '\n')

    fid.close()

