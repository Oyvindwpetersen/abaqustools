
# -*- coding: utf-8 -*-
"""
Created on 

@author: OWP
"""

#%%

#import numpy as np

#__all__ = [
  #  'Assembly',
   # 'AssemblyEnd',
   # 'BeamAddedInertia',
   # 'BeamGeneralSection',
   # 'Boundary',
   # 'Cload',
   # 'Comment',
   # 'Dload',
   # 'Element',
   # 'Elset',
   # 'FieldOutput',
   # 'Frequency',
   # 'Gravload',
   # 'AssemblyEnd',
   # 'AssemblyEnd',
   # 'AssemblyEnd',
   # 'BeamAddedInertia'
         #  ]

import numpy as np
import putools

#%%

def Assembly(fid,assembly_name):
    
    # Inputs:
    # assembly_name: string with name

    fid.write('*ASSEMBLY, NAME=' + assembly_name.upper() + '\n')
    fid.write('**' + '\n')
    
#%%

def AssemblyEnd(fid):

    # Inputs:

    fid.write('*END ASSEMBLY' + '\n')
    fid.write('**' + '\n')
    
#%%

def BeamAddedInertia(fid,linear_mass,x1,x2,alpha,I_11,I_22,I_12):

    # Inputs:
    # linear_mass: mass kg/m
    # x1: 1-dir offset
    # x2: 2-dir offset
    # alpha: rotation offset
    # I_11: inertia kg*m^2
    # I_22: inertia kg*m^2
    # I_12: inertia kg*m^2

    fid.write('*BEAM ADDED INERTIA' + '\n')
    
    values_list=[linear_mass,x1,x2,alpha,I_11,I_22,I_12]
    str_values=putools.num.num2stre(values_list,digits=3,delimeter=', ')
    fid.write(str_values + '\n')

    #fid.write('**' + '\n')
    
#%%

def BeamSection(fid,elset,material,sectiontype,sectionproperties,direction):
    
    # Inputs:
    # elset: string with element set
    # material: string with material name
    # sectiontype: eg 'RECTANGULAR' or 'PIPE'
    # sectionproperties: array with numbers required for the above
    # direction: array with n1-direction
    
    if isinstance(elset,str):
        elset=[elset]

    sectionproperties=putools.num.ensurenp(sectionproperties)
    direction=putools.num.ensurenp(direction)

    for elset_sub in elset:
        fid.write('*BEAM SECTION, ELSET=' + elset_sub.upper() + ', MATERIAL=' + material.upper() + ', SECTION=' + sectiontype.upper() + '\n')

        putools.txt.writematrix(fid,sectionproperties,5,', ','f')
        
        putools.txt.writematrix(fid,direction,3,', ','f')
    
    fid.write('**' + '\n')
    
    
#%%

def BeamGeneralSection(fid,elset,density,sectionproperties,direction,materialproperties):
    
    # Inputs:
    # elset: string with element set
    # density: in kg/m^3
    # sectionproperties: array with numbers required: A,I11,I12,I22,It
    # direction: array with n1-direction
    # materialproperties: array [E,G]
    
    fid.write('*BEAM GENERAL SECTION, ELSET=' + elset.upper() + ', SECTION=GENERAL, DENSITY=' + putools.num.num2strf(density,3) + '\n')
    
    putools.txt.writematrix(fid,sectionproperties,5,', ','e')
    
    putools.txt.writematrix(fid,direction,3,', ','f')
    
    putools.txt.writematrix(fid,materialproperties,5,', ','e')
    
    fid.write('**' + '\n')
    
#%%

def Boundary(fid,op,nodename,BCmat,partname):

    # Inputs:
    # op: 'MOD' or 'NEW' for new (erase all old) or modified BCs
    # nodename: string with node set name or array with node numbers
    # BCmat: e.g. [1,4,0] to set DOF1,2,3,4 to zero
    # partname: string with part name
    
    Checkarg(op,['MOD','NEW'])
    
    partname_str=''
    if len(partname)>0:
        partname_str=partname.upper() + '.'
        
    fid.write('*BOUNDARY, OP=' + op.upper() + '\n')
    
    if isinstance(nodename,str):
        nodename=[nodename]
        
    if putools.num.isnumeric(nodename):
        nodename=putools.num.ensurenp(nodename)
        for k in nodename:
            fid.write(partname_str + str(nodename[k]) + ',' + str(BCmat[0]) + ',' + str(BCmat[1]) + ',' + str(BCmat[2]) + '\n')
    elif isinstance(nodename,list):
        for node in nodename:
            fid.write(partname_str + str(node) + ',' + str(BCmat[0]) + ',' + str(BCmat[1]) + ',' + str(BCmat[2]) + '\n')
  
  # if isinstance(nodename,str):
        # fid.write(partname_str + nodename + ',' + str(BCmat[0]) + ',' + str(BCmat[1]) + ',' + str(BCmat[2]) + '\n')
    # elif isinstance(nodename,list):
        # for node in nodename:
            # fid.write(partname_str + str(node) + ',' + str(BCmat[0]) + ',' + str(BCmat[1]) + ',' + str(BCmat[2]) + '\n')
    # elif isinstance(nodename,int):
        # fid.write(partname_str + str(nodename) + ',' + str(BCmat[0]) + ',' + str(BCmat[1]) + ',' + str(BCmat[2]) + '\n')
    # elif isinstance(nodename,np.ndarray):
        # for node in np.nditer(nodename):
            # fid.write(partname_str + str(node) + ',' + str(BCmat[0]) + ',' + str(BCmat[1]) + ',' + str(BCmat[2]) + '\n')
    
    fid.write('**' + '\n')
    fid.write('**' + '\n')
    
#%%

def Checkarg(a_str,arg_allowed):

    # Inputs:
    # a_str: string with argument to check
    # arg_allowed: string or list with arguments that are allowed
    
    if isinstance(arg_allowed,str):
        arg_allowed=[arg_allowed]
    
    CorrectArg=False
    for arg in arg_allowed:
        if a_str.upper()==arg.upper():
            CorrectArg=True

    if CorrectArg==False:
        
        exc_str='Argument ' + a_str + ' not allowed, argument must be '
        for arg in arg_allowed:
            exc_str=exc_str + arg.upper() + ' or '
        
        exc_str=exc_str[:-4]
        raise Exception(exc_str)
        
#%%
def Cload(fid,op,nset,dof,magnitude_force,partname=''):

    # Inputs:
    # op: 'MOD' or 'NEW' for new (erase all old) or modified CLOADS
    # nset: string with node set name or array with node numbers
    # dof: DOF number 1-6
    # magnitude_force: signed number
    
    Checkarg(op,['MOD','NEW','DELETE'])

    partname_str=''
    if len(partname)>0:
        partname_str=partname.upper() + '.'

    if op.casefold()=='DELETE':
        fid.write('*CLOAD, OP=NEW' + '\n')
        fid.write('**' + '\n')
        return
    
    fid.write('*CLOAD, OP=' + op.upper() + '\n')
    
    magnitude_force=putools.num.ensurenp(magnitude_force)
    
    if isinstance(nset,str):
        nset=[nset]
    
    magnitude_force=np.atleast_1d(magnitude_force)
    
    if np.shape(magnitude_force)==(1,):
        magnitude_force=magnitude_force*np.ones(len(nset))
    
    if putools.num.isnumeric(nset):
        for k in np.arange(len(nset)):
            fid.write( partname_str + str(nset[k]) + ', ' + str(int(dof)) + ', ' + putools.num.num2stre(magnitude_force[k],3) + '\n')
    elif isinstance(nset,list):
        for k in np.arange(len(nset)):
            fid.write( partname_str + nset[k] + ', ' + str(int(dof)) + ', ' + putools.num.num2stre(magnitude_force[k],3) + '\n')
        
    fid.write('**' + '\n')
    #fid.write('**' + '\n')
    
#%%

def Comment(fid,comment,logic_main=False):

    # Inputs:
    # comment: string or list with comments
    # logic_main: many or few stars

    if logic_main==True:
        separatator='***********************************************************'
    else:
        separatator='**********'

    if isinstance(comment,str):
        comment=[comment]

    fid.write(separatator + '\n')
    for comment_sub in comment:
        fid.write('** ' + comment_sub + '\n')

    fid.write(separatator + '\n')


#%%

def Dload(fid,op,elset,type_id,magnitude):

    # Inputs:
    # op: 'MOD' or 'NEW' for new (erase all old) or modified DLOADS
    # elset: name of element set
    # type_id: type, e.g. PZ for line load in z-direction
    # magnitude: signed number
    
    Checkarg(op,['MOD','NEW','DELETE'])

    if op.upper()=='DELETE':
        fid.write('*DLOAD, OP=NEW' + '\n')
        fid.write('**' + '\n')
        fid.write('**' + '\n')
        return
        
    if isinstance(magnitude,str):
        magnitude_str=magnitude
    elif putools.num.isnumeric(magnitude):
        magnitude_str=putools.num.num2stre(magnitude)
        
    fid.write('*DLOAD, OP=' + op.upper() + '\n')
    fid.write( elset + ', ' + type_id + ', ' + magnitude_str + '\n')
    
    fid.write('**' + '\n')
    #fid.write('**' + '\n')
    
#%%
    
def Element(fid,element_nodenumber,type_id,elsetname):
    
    # Inputs:
    # element_nodenumber: array with rows [Elno,Nodeno1,Nodeno2]
    # type_id: type, e.g. B31
    # elsetname: string with name
    
    element_nodenumber=putools.num.ensurenp(element_nodenumber)

    id=element_nodenumber<=0
    n_neg=np.sum(np.sum(id))
    if n_neg>0:
        print('***** For ELSET ' + elsetname)
        raise Exception('***** Negative element or node number' )
    

    if type_id=='B31' or type_id=='B33': 
        if np.shape(element_nodenumber)[1]!=3:
            print('***** For ELSET ' + elsetname)
            raise Exception('***** B31 or B33 must have 2 nodes')
        
    if type_id=='B32':
        if np.shape(element_nodenumber)[1]!=4:
            print('***** For ELSET ' + elsetname)
            raise Exception('***** B32 must have 3 nodes')
            
    fid.write('*ELEMENT, TYPE=' + type_id.upper() + ', ELSET=' + elsetname.upper() + '\n')
    
    putools.txt.writematrix(fid,element_nodenumber,'',', ','int')
    
    fid.write('**' + '\n')
    fid.write('**' + '\n')

    
#%%

def Elset(fid,elsetname,elements,option=''):
    
    # Inputs:
    # elsetname: string with name
    # elements: element numbers or list of strings to include in elset
    
    fid.write('*ELSET, ELSET=' + elsetname.upper() + '\n')
    
    if isinstance(elements,str):
        
        elements=[elements]
        
    if putools.num.isnumeric(elements):
        elements=np.atleast_1d(putools.num.ensurenp(elements))
        bins=putools.num.rangebin(len(elements),16)
        for bins_sub in bins:
            putools.txt.writematrix(fid,elements[bins_sub],'',',','int')
    else:
        for elements_sub in elements:
            fid.write(elements_sub.upper() + '\n')
                    
    fid.write('**' + '\n')
    fid.write('**' + '\n')

#%%

def FieldOutput(fid,type_id,variables,set_id='',options=''):
    
    # Inputs:
    # type_id: 'NODE' or 'ELEMENT'
    # variables: response quantity, e.g. U or SF
    # set_id: name of nodeset or elset

    comma=', '
    if len(options)<=1:
        comma=''
        options=''

    fid.write('*OUTPUT, FIELD' + comma + options.upper() + '\n')
    
    if type_id.upper()=='NODE':
        if len(set_id)<=1:
            fid.write('*NODE OUTPUT \n')
        else:
            fid.write('*NODE OUTPUT, NSET=' + set_id.upper() + '\n')
        
    elif type_id.upper()=='ELEMENT':
        if len(set_id)<=1:
            fid.write('*ELEMENT OUTPUT \n')
        else:
            fid.write('*ELEMENT OUTPUT, ELSET=' + set_id.upper() + '\n')
        
    if isinstance(variables,str):
        variables=[variables]
    
    for variables_sub in variables:
        fid.write(variables_sub + '\n')
    
    fid.write('**' + '\n')
    # fid.write('**' + '\n')
    
#%%

def Frequency(fid,n_modes,normalization='DISPLACEMENT'):
    
    # Inputs:
    # n_modes: number of modes
    # normalization: 'DISPLACEMENT' or 'MASS'
    
    if normalization.upper()=='MASS':
        norm='MASS'
        comma=''
        options=''
    else:
        norm='DISPLACEMENT'
        comma=', '
        options='SIM=NO'

    fid.write('*FREQUENCY, NORMALIZATION=' + norm + comma + options + '\n')
    
    fid.write(str(n_modes) + '\n')
    
    fid.write('**' + '\n')
    fid.write('**' + '\n')
        
#%%

def Gravload(fid,op,elset,magnitude=9.81,partname=''):
    
    # Inputs:
    # op: 'MOD' or 'NEW' for new (erase all old) or modified DLOADS
    # magnitude: signed number

    partname_str=''
    if len(partname)>0:
        partname_str=partname.upper() + '.'
                
        
    Checkarg(op,['MOD','NEW'])

    fid.write('*DLOAD, OP=' + op.upper() + '\n')
    
    if isinstance(elset,str):
        elset=[elset]
    
    if magnitude<0:
        print('***** Gravity magnitude should generally be positive: magnitude 9.81 and direction [0 0 -1]')
    
    direction_str=' 0 , 0, -1'
    
    for elset_sub in elset:
        fid.write(partname_str + elset_sub.upper() + ', GRAV, ' + putools.num.num2strf(magnitude,5) + ',' + direction_str + '\n')
            
    fid.write('**' + '\n')
        
#%%

def HistoryOutput(fid,options=''):
    
    # Inputs:
    # options: 

    comma=', '
    if len(options)<=1:
        comma=''
        options=''
    
    fid.write('*OUTPUT, HISTORY' + comma + options.upper() + '\n')

#%%

def HistoryOutputElement(fid,variables,elset,options=''):
    
    # Inputs:
    # variables: response quantity, e.g. 'SF'
    # elset: string with element name

    fid.write('*ELEMENT OUTPUT, ELSET=' + elset + '\n')

    if isinstance(variables,str):
        variables=[variables]
            
    for variables_sub in variables:
        fid.write(variables_sub + '\n')

                
    fid.write('**' + '\n')
    
#%%
    
def HistoryOutputNode(fid,variables,nset,options=''):
    
    # Inputs:
    # variables: response quantity, e.g. 'U'
    # nset: string with node name

    fid.write('*NODE OUTPUT, NSET=' + nset + '\n')

    if isinstance(variables,str):
        variables=[variables]
            
    for variables_sub in variables:
        fid.write(variables_sub + '\n')

                
    fid.write('**' + '\n')
    
#%%

def Include(fid,filename):
    
    # Inputs:
    # filename: string with name of inp file

    fid.write('**' + '\n')
    fid.write('*INCLUDE, INPUT=' + filename + '\n')
    fid.write('**' + '\n')

#%%

def Instance(fid,instancename,partname):
    
    # Inputs:
    # instancename: string with instance
    # partname: string with part
    
    fid.write('*INSTANCE, NAME=' + instancename.upper() + ', PART=' + partname.upper() + '\n')
    fid.write('**' + '\n')


#%%

def InstanceEnd(fid):
    
    # Inputs:
    # instancename: string with instance
    # partname: string with part

    fid.write('*END INSTANCE' + '\n')
    fid.write('**' + '\n')

#%%

def Line(fid,line):
    
    # Inputs:
    # line: string or list with lines to write to file

    if isinstance(line,str):
        line=[line]

    for line_sub in line:
        fid.write(line_sub + '\n')

#%%

def MPC(fid,type_id,nodes):
    
    # Inputs:
    # type_id: e.g. 'BEAM' or 'PIN'
    # nodes: array with node numbers or list with node names

    fid.write('*MPC' + '\n')
    
    mpc_str=''
    
    if putools.num.isnumeric(nodes):
        nodes=putools.num.ensurenp(nodes)
        for nodes_sub in np.nditer(nodes):
            mpc_str=mpc_str + ',' + str(int(nodes_sub))
    elif isinstance(nodes,list):
        for nodes_sub in nodes:
            mpc_str=mpc_str + ',' + nodes_sub
        
    mpc_str=mpc_str[1:]
    fid.write(type_id +  ', ' + mpc_str + '\n')

    fid.write('**' + '\n')

#%%

def Material(fid,materialname,emodulus,v,density):
    
    # Inputs:
    # materialname: string with name
    # emodulus: modulus in Pa
    # v: Poisson ratio
    # density: in kg/m^3

    fid.write('*MATERIAL, NAME=' + materialname.upper() + '\n')
    fid.write('*ELASTIC' + '\n')
    putools.txt.writematrix(fid,[emodulus,v],3,', ',['e' , 'f'])
    fid.write('*DENSITY' + '\n')
    putools.txt.writematrix(fid,[density],3,', ',['e'])
    
    fid.write('**' + '\n')
    fid.write('**' + '\n')


#%%

def ModelChange(fid,option,elset,partname=''):
    
    # Inputs:
    # option: 'ADD' or 'REMOVE'
    # elset: string or list with element sets

    Checkarg(option,['ADD','REMOVE'])

    if isinstance(elset,str):
        elset=[elset]

    partname_str=''
    if len(partname)>0:
        partname_str=partname.upper() + '.'
    
    fid.write('*MODEL CHANGE, ' + option.upper() + '\n')

    for elset_sub in elset:
        fid.write(partname_str + elset_sub.upper() + '\n')

    fid.write('**' + '\n')

#%%
    
def Node(fid,nodenumber_coord,nsetname):
    
    # Inputs:
    # nodenumber_coord: array with rows [Nodeno,CoordX,CoordY,CoordZ]
    # nsetname: string with name
    
    if any(nodenumber_coord[:,0]<=0):
        putools.num.starprint('For NSET ' + nsetname,1)
        raise Exception('***** Negative node numbers')
        
        
    if np.isnan(nodenumber_coord).any():
        putools.num.starprint('For NSET ' + nsetname,1)
        raise Exception('***** Containing NAN')
    
    fid.write('*NODE' + ',NSET=' + nsetname.upper() + '\n')
    putools.txt.writematrix(fid,nodenumber_coord,5,',',['int' , 'f', 'f', 'f'])

    fid.write('**' + '\n')
    fid.write('**' + '\n')


#%%

def Nonstructuralmass(fid,elset,unit,mass):
    
    # Inputs:
    # elset: string with name
    # unit: MASS PER LENGTH or TOTAL MASS
    # mass: 

    fid.write('*NONSTRUCTURAL MASS, ELSET=' + elset.upper() + ', UNITS=' + unit.upper() + '\n')
    
    putools.txt.writematrix(fid,mass,5,',','e')
    
    fid.write('**' + '\n')

#%%

def Nset(fid,nsetname,nodes,option=''):
    
    # Inputs:
    # nsetname: string with name
    # nodes: array with numbers or list with node set names

    comma=', '
    if len(option)<=1:
        comma=''
        option=''
        
    if isinstance(nsetname,list):
        nsetname=nsetname[0]
        
    fid.write('*NSET, NSET=' + nsetname.upper() + comma + option.upper() + '\n')
    
    if putools.num.isnumeric(nodes):
        nodes=np.atleast_1d(putools.num.ensurenp(nodes))
        bins=putools.num.rangebin(len(nodes),16)
            
        for bins_sub in bins:
            putools.txt.writematrix(fid,nodes[bins_sub],'',',','int')
                
    elif isinstance(nodes,list):
        for nodes_sub in nodes:
            fid.write(nodes_sub.upper() + '\n')
    
    fid.write('**' + '\n')
    fid.write('**' + '\n')
    

#%%

def Parameter(fid,parameternames,values):
    
    # Inputs:
    # parameternames: string or list with names
    # values: array with numbers

    if isinstance(parameternames,str):
        parameternames=[parameternames]

    if len(values)==1:
        values=values*np.ones(len(parameternames))
    
    fid.write('*PARAMETER' + '\n')
    
    for k in np.arange(len(parameternames)):
        fid.write( parameternames[k] + '=' + putools.num.num2stre(values[k],5,',') + '\n')
    
    fid.write('**' + '\n')

#%%

def Part(fid,partname):
    
    # Inputs:
    # partname: string with name

    fid.write('*PART, NAME=' + partname.upper() + '\n')
    fid.write('**' + '\n')

#%%

def PartEnd(fid):
    
    # Inputs:

    fid.write('*END PART' + '\n')
    fid.write('**' + '\n')

#%%

def Release(fid,elset,end_id,release_id):
    
    # Inputs:
    # elset: string or list with element set name
    # end_id: string or list with end ids, e.g. 'S1' 'S2'
    # release_id: string or list with end ids, choose from M1, M2, T, M1-M2, M1-T, M2-T, ALLM
    
    # M1	
    # refers to the rotation about the n1-axis,

    # M2	
    # refers to the rotation about the n2-axis,

    # M1-M2	
    # refers to a combination of rotational degrees of freedom about the n1-axis and the n2-axis,

    # T	
    # refers to the rotation about the t-axis,

    # M1-T	
    # refers to a combination of rotational degrees of freedom about the n1-axis and the t-axis,

    # M2-T	
    # refers to a combination of rotational degrees of freedom about the n2-axis and the t-axis, and

    # ALLM	
    # represents a combination of all the rotational degrees of freedom (i.e., M1, M2, and T).



    if isinstance(elset,str):
        elset=[elset]
        
    if isinstance(end_id,str):
        end_id=[end_id]

    if isinstance(release_id,str):
        release_id=[release_id]

    fid.write('*RELEASE' + '\n')
    
    for i in np.arange(len(end_id)):
        for j in np.arange(len(release_id)):
        
            if putools.num.isnumeric(elset):
                elset=putools.num.ensurenp(elset)
                for elset_sub in np.nditer(elset):
                    fid.write( str(int(elset_sub)) + ', ' + end_id[i] + ', ' + release_id[j]  + '\n')
            else:
                for elset_sub in elset:
                    fid.write(elset_sub + ', ' + end_id[i] + ', ' + release_id[j]  + '\n')
                    
    fid.write('**' + '\n')

#%%

def Restart(fid,type_id,step=-1,frequency=100):
    
    # Inputs:
    # type_id: 'READ' or 'WRITE'
    # step: number, usually the last
    # frequency: frequency

    Checkarg(type_id,['READ' , 'WRITE'])
    
    if type_id.upper()=='READ':
        freq_str=''
    else:
        freq_str=', FREQUENCY=' + str(frequency)
    
    if type_id.upper()=='WRITE':
        step_str=''
    else:
        step_str=', STEP=' + str(step)
    
    
    fid.write('*RESTART' + type_id + step_str + freq_str + '\n')
    fid.write('**' + '\n')

#%%

def ShellSection(fid,elset,material,options,shellproperties):
    
    # Inputs:
    # elset: string with element set name
    # material: string with material set name
    # options: e.g.  OFFSET=SNEG
    # shellproperties: array with [thickness,number of integration points]

    fid.write('*SHELL SECTION, ELSET=' + elset.upper() + ',' + ' MATERIAL=' + material.upper() + ', ' + options.upper() + '\n')

    putools.txt.writematrix(fid,shellproperties,3,',',['f','int'])

    fid.write('**' + '\n')

#%%

def ShearCenter(fid,x1,x2):
    
    # Inputs:
    # x1: offset in 1-dir
    # x2: offset in 2-dir
 
    fid.write('*SHEAR CENTER' + '\n')
    putools.txt.writematrix(fid,[x1,x2],3,',','e')
    fid.write('**' + '\n')
    
#%%

def Spring(fid,elset,element_nodenumber,dofno,springstiffness):

    # Inputs:
    # elset: string with element set name
    # element_nodenumber: [Elno,Nodeno1,Nodeno2]
    # dofno: DOF 1-6
    # springstiffness: in N/m

    #*ELEMENT, TYPE=SPRING2, ELSET=SADLESPRING_X
    #301001, 100075, 10051
    #301002, 200075, 10169
    #301003, 110075, 20051
    #301004, 210075, 20169
    #*SPRING,ELSET=SADLESPRING_X
    # 1,1
    # 1.00000e+12

    # For now, springstiffness is a scalar
    # For now, dofno is a scalar
        
    fid.write('*ELEMENT, TYPE=SPRING2, ELSET=' + elset.upper() + '\n')

    putools.txt.writematrix(fid,element_nodenumber,'',',','int')

    fid.write('*SPRING, ELSET=' + elset.upper() + '\n')
    
    putools.txt.writematrix(fid,[dofno,dofno],'',',','int')

    if putools.num.isnumeric(springstiffness):
        putools.txt.writematrix(fid,springstiffness,5,',','e')
    #elif isinstance(springstiffness,list):
        #fid.write( springstiffness + '\n')

    fid.write('**' + '\n')
    fid.write('**' + '\n')
    
#%%

def SpringA(fid,elset,element_nodenumber,springstiffness):

    # Inputs:
    # elset: string with element set name
    # element_nodenumber: [Elno,Nodeno1,Nodeno2]
    # springstiffness: in N/m

    # For now, springstiffness is a scalar
        
    fid.write('*ELEMENT, TYPE=SPRINGA, ELSET=' + elset.upper() + '\n')

    putools.txt.writematrix(fid,element_nodenumber,'',',','int')

    fid.write('*SPRING,ELSET=' + elset.upper() + '\n')

    if putools.num.isnumeric(springstiffness):
        putools.txt.writematrix(fid,springstiffness,5,',','e')
    #elif isinstance(springstiffness,list):
        #fid.write( springstiffness + '\n')

    fid.write('**' + '\n')
    fid.write('**' + '\n')

#%%
    
def Static(fid,time):

    # Inputs:
    # time: string or array with [Initial Total Min Max]

    fid.write('*STATIC \n')

    if putools.num.isnumeric(time):
        putools.txt.writematrix(fid,time,'1',',','e')
    elif isinstance(time,str):
        fid.write(time +' \n')

    #fid.write('**' + '\n')
    fid.write('**' + '\n')

#%%

def Step(fid,options='',comment=''):

    # Inputs:

    comma=', '
    if len(options)<1:
        comma=''
        options=''
    
    Comment(fid,comment)
    fid.write('*STEP ' + comma + options.upper() + '\n')
    
#%%

def StepEnd(fid):

    # Inputs:

    fid.write('*END STEP' + '\n')
    fid.write('**' + '\n')
    fid.write('**' + '\n')
    
#%%

def Temp(fid,op,nset,magnitude_temp,partname=''):

    # Inputs:
    # op: 'MOD' or 'NEW' for new (erase all old) or modified TEMP
    # nset: string with node name
    # magnitude_temp: in K

    Checkarg(op,['MOD','NEW'])

    fid.write('*TEMPERATURE, OP=' + op.upper() + '\n')
    
    partname_str=''
    if len(partname)>0:
        partname_str=partname.upper() + '.'

    if isinstance(nset,str):
        nset=[nset]
        
    magnitude_temp=putools.num.ensurenp(magnitude_temp)
    
    magnitude_temp=np.atleast_1d(magnitude_temp)
    
    if len(magnitude_temp)==1:
        magnitude_temp=magnitude_temp*np.ones([1,len(nset)])
        
    if isinstance(nset,list):
        for k,nset_sub in enumerate(nset):
           fid.write( partname_str + nset_sub + ', ' + putools.num.num2stre(magnitude_temp[k],3) + '\n')
           
    fid.write('**' + '\n')
    fid.write('**' + '\n')
    
    
 #%%

def Tie(fid,tiename,adjust,postol,slavename,mastername):

    # Inputs:
    # tiename: string with name
    # adjust: 'YES' or 'NO' adjustment of slave node
    # postol: in m, nodes outside will not be tied
    # slavename: name of surface
    # mastername: name of surface
    
    Checkarg(adjust,['YES','NO'])
    
    fid.write('*TIE, NAME=' + tiename.upper() + ', ADJUST=' + adjust.upper() + ', ' 'POSITION TOLERANCE=' + putools.num.num2stre(postol,3) + '\n')
    fid.write(slavename.upper() + ', ' + mastername.upper() + '\n')
    
    fid.write('**' + '\n')

#%%
   
def TransverseShearStiffness(fid,k23,k13):

    # Inputs:
    # k23: shear stiffness in 2-dir
    # k13: shear stiffness in 1-dir
    
    fid.write('*TRANSVERSE SHEAR STIFFNESS' + '\n')
    putools.txt.writematrix(fid,[k23,k13],3,',','e')

    # https://www.sharcnet.ca/Software/Abaqus/6.14.2/v6.14/books/usb/default.htm?startat=pt06ch29s03alm08.html#usb-elm-ebeamelem-transshear-override



