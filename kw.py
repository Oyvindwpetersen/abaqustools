
# -*- coding: utf-8 -*-
"""
Created on 

@author: OWP
"""

#%%

import numpy as np
import putools
import warnings

def warning_on_one_line(message, category, filename, lineno, file=None, line=None):
    return '%s:%s: %s: %s\n' % (filename, lineno, category.__name__, message)

warnings.formatwarning = warning_on_one_line

#%%

def assembly(fid,assembly_name):
    
    '''
    *ASSEMBLY
    
    Arguments
    ------------
    fid: file identifier
    assembly_name: string with name
    
    Returns
    ------------
    None
    
    '''

    fid.write('*ASSEMBLY, NAME=' + assembly_name.upper() + '\n')
    fid.write('**' + '\n')
    
#%%

def assemblyend(fid):

    '''
    *END ASSEMBLY
    
    Arguments
    ------------
    fid: file identifier
    
    Returns
    ------------
    None
    
    '''

    fid.write('*END ASSEMBLY' + '\n')
    fid.write('**' + '\n')
    
#%%

def beamaddedinertia(fid,linear_mass,x1,x2,alpha,I_11,I_22,I_12):

    '''
    *BEAM ADDED INERTIA
    
    Arguments
    ------------
    fid: file identifier
    linear_mass: mass [kg/m]
    x1: 1-dir offset [m]
    x2: 2-dir offset [m]
    alpha: rotation offset [deg]
    I_11: inertia [kg*m^2]
    I_22: inertia [kg*m^2]
    I_12: inertia [kg*m^2]
    
    Returns
    ------------
    None
    
    '''

    fid.write('*BEAM ADDED INERTIA' + '\n')
    
    values_list=[linear_mass,x1,x2,alpha,I_11,I_22,I_12]
    str_values=putools.num.num2stre(values_list,digits=3,delimeter=', ')
    fid.write(str_values + '\n')

    #fid.write('**' + '\n')
    
#%%

def beamsection(fid,elset,material,sectiontype,sectionproperties,direction):
    
    '''
    *BEAM SECTION
    
    Arguments
    ------------
    fid: file identifier
    elset: string with element set
    material: string with material name
    sectiontype: e.g. 'RECTANGULAR' or 'PIPE'
    sectionproperties: array with numbers required for the section type above
    direction: array with n1-direction, e.g. [0,1,0]
    
    Returns
    ------------
    None
    
    '''
    
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

def beamgeneralsection(fid,elset,density,sectionproperties,direction,materialproperties):
    
    '''
    *BEAM GENERAL SECTION
    
    Arguments
    ------------
    fid: file identifier
    elset: string with element set name
    density: in [kg/m^3]
    sectionproperties: [A,I11,I12,I22,It] array with cross section properties
    direction: array with n1-direction, e.g. [0,1,0]
    materialproperties: [E,G] array with elastic and shear modulus
    
    Returns
    ------------
    None
    
    '''
    
    fid.write('*BEAM GENERAL SECTION, ELSET=' + elset.upper() + ', SECTION=GENERAL, DENSITY=' + putools.num.num2strf(density,3) + '\n')
    
    putools.txt.writematrix(fid,sectionproperties,5,', ','e')
    
    putools.txt.writematrix(fid,direction,3,', ','f')
    
    putools.txt.writematrix(fid,materialproperties,5,', ','e')
    
    fid.write('**' + '\n')
    
#%%

def boundary(fid,op,nodename,BCmat,partname):

    '''
    *BOUNDARY
    
    Arguments
    ------------
    fid: file identifier
    op: 'MOD' for modified BCs or 'NEW' for new BCs (erase all old) 
    nodename: string with node set name or array with node numbers
    BCmat: array to specificy, e.g. [1,4,0] to set DOF 1,2,3,4 to zero
    partname: string with part name
    
    Returns
    ------------
    None
    
    '''
    
    checkarg(op,['MOD','NEW'])
    
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
  
    fid.write('**' + '\n')
    fid.write('**' + '\n')
    
#%%

def checkarg(a_str,arg_allowed):

    '''
    Check allowable arguments
    
    Arguments
    ------------
    a_str: string with argument to check
    arg_allowed: string or list with arguments that are allowed
    
    Returns
    ------------
    None
    
    '''
    
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
def cload(fid,op,nset,dof,magnitude_force,partname=''):

    '''
    *CLOAD
    
    Arguments
    ------------
    fid: file identifier
    op: 'MOD' for modified CLOADS or 'NEW' for new CLOADS (erase all old) 
    nset: string with node set name or array with node numbers
    dof: DOF number between 1 and 6
    magnitude_force: signed force magnitude
    
    Returns
    ------------
    None
    
    '''
    
    checkarg(op,['MOD','NEW','DELETE'])

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

def comment(fid,comment_str,logic_main=False):

    '''
    Add comment to input file
    
    Arguments
    ------------
    fid: file identifier
    comment_str: string or list with comments
    logic_main: many or few stars
    
    Returns
    ------------
    None
    
    '''

    if logic_main==True:
        separatator='***********************************************************'
    else:
        separatator='**********'

    if isinstance(comment_str,str):
        comment_str=[comment_str]

    fid.write(separatator + '\n')
    for comment_sub in comment_str:
        fid.write('** ' + comment_sub + '\n')

    fid.write(separatator + '\n')


#%%

def dload(fid,op,elset,type_id,magnitude):

    '''
    *DLOAD

    Arguments
    ------------
    fid: file identifier
    op: 'MOD' for modified DLOADS or 'NEW' for new DLOADS (erase all old) 
    elset: name of element set
    type_id: load type, e.g. PZ for line load in z-direction
    magnitude: signed load magnitude
    
    Returns
    ------------
    None
    
    '''
    
    checkarg(op,['MOD','NEW','DELETE'])

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
    
def element(fid,element_nodenumber,element_type,elsetname,star=True):
    
    '''
    *ELEMENT
    
    Arguments
    ------------
    fid: file identifier
    element_nodenumber: array with rows [el_num,node_num1,node_num2]
    element_type: element type, e.g. B31
    elsetname: string with name
    
    Returns
    ------------
    None
    
    '''
    
    element_nodenumber=putools.num.ensurenp(element_nodenumber)

    id_neg=element_nodenumber<=0
    n_neg=np.sum(np.sum(id_neg))
    if n_neg>0:
        print('***** For ELSET ' + elsetname)
        raise Exception('***** Negative element or node number' )
    

    if element_type=='B31' or element_type=='B33': 
        if np.shape(element_nodenumber)[1]!=3:
            print('***** For ELSET ' + elsetname)
            raise Exception('***** B31 or B33 must have 2 nodes')
        
    if element_type=='B32':
        if np.shape(element_nodenumber)[1]!=4:
            print('***** For ELSET ' + elsetname)
            raise Exception('***** B32 must have 3 nodes')
            
    fid.write('*ELEMENT, TYPE=' + element_type.upper() + ', ELSET=' + elsetname.upper() + '\n')
    
    putools.txt.writematrix(fid,element_nodenumber,'',', ','int')
    
    if star==True:
        fid.write('**' + '\n')
        fid.write('**' + '\n')


#%%

def elementjointc(fid,node1,node2,coord1,coord2,node_num_base,el_num_base,element_type,setname,direction,kj1,kj2,offset1=0,offset2=0,n_el=10,max_length=None):
                
    '''
    Beam member with user-defined stiffness at member joints
    
    N1 J1     MemberEl1    MemberEl2    MemberEl3    MemberEl4    MemberEl5     J2 N2
    O~~~~~~O------------o-------------o------------o------------o------------O~~~~~~O

    Arguments
    ------------
    fid: file identifier
    node1: (super)node number at joint 1
    node2: (super)node number at joint 2
    coord1: coordinates of node 1
    coord2: coordinates of node 2
    node_num_base: base node number for member
    el_num_base: base element number for member
    element_type: element type, e.g. B31
    setname: name for member
    direction: array with n1-direction, e.g. [0,1,0]
    kj1: [kx,ky,kz,krx,kry,krz] array with 6 spring stiffnesses in [N/m] and [Nm/rad] for joint 1
    kj2: [kx,ky,kz,krx,kry,krz] array with 6 spring stiffnesses in [N/m] and [Nm/rad] for joint 2
    offset1: eccentricity offset of member end 1 in [m]
    offset2: eccentricity offset of member end 2 in [m]
    n_el: number of elements in member
    max_length: max element length (overrides n_el)

    Returns
    ------------
    None
    
    '''
    
    setname=setname.upper()
    
    comment(fid,'Member ' + setname)
    
    # Vector for n1-direction (lateral)
    direction=putools.num.ensurenp(direction)
    direction=direction/np.sqrt(sum(direction**2))
    
    # Joint stiffness
    kj1=putools.num.ensurenp(kj1)
    kj2=putools.num.ensurenp(kj2)
    
    # Misc checks
    
    # Only allow 2-node elements
    checkarg(element_type,['B31','B33'])
        
    if any(kj1<0):
        raise Exception('***** kj1 is negative for set ' + setname)
    
    if any(kj2<0):
        raise Exception('***** kj2 is negative for set ' + setname)
    
    if offset1<0:
        raise Exception('***** offset1 is negative for set ' + setname)
    
    if offset2<0:
        raise Exception('***** offset2 is negative for set ' + setname)
        
    if all(kj1==0):
        warnings.warn('***** kj1 is all zero for set ' + setname, stacklevel=2)
    
    if all(kj2==0):
        warnings.warn('***** kj2 is all zero for set ' + setname, stacklevel=2)


    # Vector along member
    t_vec=putools.num.ensurenp(coord2)-putools.num.ensurenp(coord1)
    
    L0=np.sqrt(sum(t_vec**2))
    
    if L0==0:
        raise Exception('***** L0 is zero for set ' + setname)
        
    # Determine number of elements
    if (n_el is None):
        n_el=np.ceil(L0/max_length) 
    elif max_length is not None:
    
        # If n_el is specified then use it as a miniumum, else use only length
        if n_el is not None:
            n_el=np.max([n_el,np.ceil(L0/max_length)])
        elif n_el is None:
            n_el=np.ceil(L0/max_length)
            
    n_el=int(n_el)        
        
    # Shorten member by offset
    if offset1>0:
        coord1=coord1+t_vec/L0*offset1
        
    if offset2>0:
        coord2=coord2-t_vec/L0*offset2
    
    # Member nodes and elements
    x=np.linspace(coord1[0],coord2[0],n_el+1)    
    y=np.linspace(coord1[1],coord2[1],n_el+1)    
    z=np.linspace(coord1[2],coord2[2],n_el+1)
    
    node_num=np.arange(1,len(x)+1)+node_num_base
    el_num=np.arange(1,len(x))+el_num_base
    
    # Write node sand elements
    node(fid,np.column_stack((node_num,x,y,z)),setname)
    
    el_matrix=np.column_stack((el_num,node_num[0:-1],node_num[1:]))
    
    # If kj stiffnesses are all inf, the member in continuous and therefore
    # instead directly linked to the supernode, the offset is thus ignored
    
    # In the future, this should be replaced by an input argument instead
    
    inf_threshold=1e30
    
    if all(kj1>inf_threshold):
        J1_cont=True
        el_matrix[0,1]=node1
    else:
        J1_cont=False
    
    if all(kj2>inf_threshold):
        J2_cont=True
        el_matrix[-1,-1]=node2
    else:
        J2_cont=False
        
    
    # Write elements of member
    element(fid,el_matrix,element_type,setname)

    # Create local orientation system along member
    a=node2
    b=node_num[0]-1
    c=node1
    
    line(fid,'** Extra node (b) for definition of orientation system')
    node(fid,np.array([b,x[0]+direction[0],y[0]+direction[1],z[0]+direction[2]]),setname + '_BNODE')
    
    orientation(fid,setname + '_LOCSYS','NODES',a,b,c)
    
    DOFS=['1','2','3','4','5','6']
    
    # Joints
    
    for j in np.arange(0,2):
        
        if j==0:
            joint_str='J1'
            kj=kj1
            el_node_matrix=[el_num[-1]+1,node1,node_num[0]]
            
            if J1_cont==True:
                fid.write('**'  + '\n')
                fid.write('** Joint 1 for ' + setname + ' is continuous, no stiffness defined' +'\n') #
                continue
            
        elif j==1:
            joint_str='J2'
            kj=kj2
            el_node_matrix=[el_num[-1]+2,node_num[-1],node2]
            
            if J2_cont==True:
                fid.write('**'  + '\n')
                fid.write('** Joint 2 for ' + setname + ' is continuous, no stiffness defined' +'\n') #
                continue
            
        line(fid,'** Joint ' + joint_str)
        
        elset_name=setname + '_' + joint_str
        
        element(fid,el_node_matrix,'JOINTC',elset_name,star=False)
        
        ori_str=', ORIENTATION=' + setname + '_LOCSYS'
        
        fid.write('*JOINT, ELSET=' + elset_name + ori_str +'\n') #
        
        dof_zero=[]
        for k in np.arange(0,6):
            
            if kj[k]==0:
                dof_zero.append(DOFS[k])
                continue
                        
            # From Abaqus doc:
            # If the *SPRING option is being used to define part of the behavior 
            # of ITS or JOINTC elements, it must be used in conjunction with the
            # *ITS or *JOINT options and the ELSET and ORIENTATION parameters
            # should not be used.
            str_el=''
                        
            fid.write('*SPRING' + str_el + '\n')
            fid.write(DOFS[k] + ',' + DOFS[k] + '\n')
            putools.txt.writematrix(fid,kj[k],3,',','e')
    
        if len(dof_zero)>0:
            for dof in dof_zero:
                fid.write('** Zero joint stiffness in DOF ' + dof + '\n')
    
    
    fid.write('**' + '\n')
    fid.write('**' + '\n')    

#%%

def elset(fid,elsetname,elements,option=''):
    
    '''
    *ELSET
    
    Arguments
    ------------
    fid: file identifier
    elsetname: string with name
    elements: element numbers or list of strings to include in elset
    
    Returns
    ------------
    None
    
    '''
    
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

def fieldoutput(fid,id_type,variables,set_id='',options=''):
    
    '''
    *FIELD OUTPUT
    
    Arguments
    ------------
    fid: file identifier
    id_type: 'NODE' or 'ELEMENT'
    variables: response quantity, e.g. U or SF
    set_id: name of nodeset or elset
    
    Returns
    ------------
    None
    
    '''

    comma=', '
    if len(options)<=1:
        comma=''
        options=''

    fid.write('*OUTPUT, FIELD' + comma + options.upper() + '\n')
    
    if id_type.upper()=='NODE':
        if not set_id:
            fid.write('*NODE OUTPUT \n')
        else:
            fid.write('*NODE OUTPUT, NSET=' + set_id.upper() + '\n')
        
    elif id_type.upper()=='ELEMENT':
        if not set_id:
            fid.write('*ELEMENT OUTPUT \n')
        else:
            fid.write('*ELEMENT OUTPUT, ELSET=' + set_id.upper() + '\n')
        
    if isinstance(variables,str):
        variables=[variables]
    
    for variables_sub in variables:
        fid.write(variables_sub + '\n')
    
    fid.write('**' + '\n')
        
#%%

def frequency(fid,n_modes,normalization='DISPLACEMENT'):
    
    '''
    *FREQUENCY
    
    Arguments
    ------------
    fid: file identifier
    n_modes: number of modes
    normalization: 'DISPLACEMENT' or 'MASS'
    
    Returns
    ------------
    None
    
    '''
    
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

def gravload(fid,op,elset,magnitude=9.81,direction='z',partname=''):
    
    '''
    Gravity load through *DLOAD
    
    Arguments
    ------------
    fid: file identifier
    op: 'MOD' or 'NEW'
    elset: element set
    magnitude: gravitational constant
    direction: 'x','y', or 'z'
    partname: unsigned load magnitude
    
    Returns
    ------------
    None
    
    '''

    partname_str=''
    if len(partname)>0:
        partname_str=partname.upper() + '.'
                
    checkarg(op,['MOD','NEW'])

    fid.write('*DLOAD, OP=' + op.upper() + '\n')
    
    if isinstance(elset,str):
        elset=[elset]
    
    if magnitude<0:
        print('***** Gravity magnitude should generally be positive: magnitude 9.81 and direction [0 0 -1]')
    
    if direction=='x':
        direction_str=' -1 , 0, 0'
    elif direction=='y':
        direction_str=' 0 , -1, 0'
    elif direction=='z':
        direction_str=' 0 , 0, -1'
        
    for elset_sub in elset:
        fid.write(partname_str + elset_sub.upper() + ', GRAV, ' + putools.num.num2strf(magnitude,5) + ',' + direction_str + '\n')
            
    fid.write('**' + '\n')
        
#%%

def historyoutput(fid,options=''):
    
    '''
    *OUTPUT, HISTORY
    
    Arguments
    ------------
    fid: file identifier
    options: 
    
    Returns
    ------------
    None
    
    '''

    comma=', '
    if len(options)<=1:
        comma=''
        options=''
    
    fid.write('*OUTPUT, HISTORY' + comma + options.upper() + '\n')

#%%

def historyoutputelement(fid,variables,elset,options=''):
    
    '''
    *ELEMENT OUTPUT
    
    Arguments
    ------------
    fid: file identifier
    variables: response quantity, e.g. SF
    elset: string with element name
    
    Returns
    ------------
    None
    
    '''

    fid.write('*ELEMENT OUTPUT, ELSET=' + elset + '\n')

    if isinstance(variables,str):
        variables=[variables]
            
    for variables_sub in variables:
        fid.write(variables_sub + '\n')

                
    fid.write('**' + '\n')
    
#%%
    
def historyoutputnode(fid,variables,nset,options=''):
    
    '''
    *NODE OUTPUT
    
    Arguments
    ------------
    fid: file identifier
    variables: response quantity, e.g. 'U'
    nset: string with node name
    
    Returns
    ------------
    None
    
    '''

    fid.write('*NODE OUTPUT, NSET=' + nset + '\n')

    if isinstance(variables,str):
        variables=[variables]
            
    for variables_sub in variables:
        fid.write(variables_sub + '\n')

                
    fid.write('**' + '\n')
    
#%%

def include(fid,filename):
    
    '''
    *INCLUDE
    
    Arguments
    ------------
    fid: file identifier
    filename: string with name of inp file
    
    Returns
    ------------
    None
    
    '''

    fid.write('**' + '\n')
    fid.write('*INCLUDE, INPUT=' + filename + '\n')
    fid.write('**' + '\n')

#%%

def instance(fid,instancename,partname):
    
    '''
    *INSTANCE
    
    Arguments
    ------------
    fid: file identifier
    instancename: string with instance
    partname: string with part
    
    Returns
    ------------
    None
    
    '''
    
    fid.write('*INSTANCE, NAME=' + instancename.upper() + ', PART=' + partname.upper() + '\n')
    fid.write('**' + '\n')


#%%

def instanceend(fid):
    
    '''
    *END INSTANCE
    
    Arguments
    ------------
    fid: file identifier
    
    Returns
    ------------
    None
    
    '''
    
    fid.write('*END INSTANCE' + '\n')
    fid.write('**' + '\n')

#%%

def line(fid,line):
    
    '''
    Write line(s) of code in input file
    
    Arguments
    ------------
    fid: file identifier
    line: string or list with lines to write to file
    
    Returns
    ------------
    None
    
    '''

    if isinstance(line,str):
        line=[line]

    for line_sub in line:
        fid.write(line_sub + '\n')

#%%

def mpc(fid,id_type,nodes):
    
    '''
    *MPC
    
    Arguments
    ------------
    fid: file identifier
    id_type: e.g. 'BEAM' or 'PIN'
    nodes: array with node numbers or list with node names
    
    Returns
    ------------
    None
    
    '''

    fid.write('*MPC' + '\n')
    
    mpc_str=''
    
    if putools.num.isnumeric(nodes):
        nodes=putools.num.ensurenp(nodes)
        for nodes_sub in np.nditer(nodes):
            mpc_str=mpc_str + ',' + str(int(nodes_sub))
    elif isinstance(nodes,list):
        for nodes_sub in nodes:
            mpc_str=mpc_str + ',' + nodes_sub.upper()
        
    mpc_str=mpc_str[1:]
    fid.write(id_type +  ', ' + mpc_str + '\n')

    fid.write('**' + '\n')

#%%

def material(fid,materialname,E,v,density):
    
    '''
    *MATERIAL
    
    Arguments
    ------------
    fid: file identifier
    materialname: string with name
    E: elastic modulus in [Pa]
    v: Poisson ratio
    density: in [kg/m^3]
    
    Returns
    ------------
    None
    
    '''

    fid.write('*MATERIAL, NAME=' + materialname.upper() + '\n')
    fid.write('*ELASTIC' + '\n')
    putools.txt.writematrix(fid,[E,v],3,', ',['e' , 'f'])
    fid.write('*DENSITY' + '\n')
    putools.txt.writematrix(fid,[density],3,', ',['e'])
    
    fid.write('**' + '\n')
    fid.write('**' + '\n')


#%%

def modelchange(fid,option,elset,partname=''):
    
    '''
    *MODEL CHANGE
    
    Arguments
    ------------
    fid: file identifier
    option: 'ADD' or 'REMOVE'
    elset: string or list with element sets
    
    Returns
    ------------
    None
    
    '''

    checkarg(option,['ADD','REMOVE'])

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
    
def node(fid,nodenumber_coord,nsetname):
    
    '''
    *NODE
    
    Arguments
    ------------
    fid: file identifier
    nodenumber_coord: array with rows [node_num,coord_x,coord_y,coord_z]
    nsetname: string with name
    
    Returns
    ------------
    None
    
    '''
    
    nodenumber_coord=np.atleast_2d(nodenumber_coord)
    
    if any(nodenumber_coord[:,0]<=0):
        putools.txt.starprint('For NSET ' + nsetname,1)
        raise Exception('***** Negative node numbers')
        
        
    if np.isnan(nodenumber_coord).any():
        putools.txt.starprint('For NSET ' + nsetname,1)
        raise Exception('***** Coordinates containing NAN')
    
    fid.write('*NODE' + ',NSET=' + nsetname.upper() + '\n')
    putools.txt.writematrix(fid,nodenumber_coord,5,',',['int' , 'f', 'f', 'f'])

    fid.write('**' + '\n')
    fid.write('**' + '\n')


#%%

def nonstructuralmass(fid,elset,unit,mass):
    
    '''
    *NONSTRUCTURAL MASS
    
    Arguments
    ------------
    fid: file identifier
    elset: string with name
    unit: MASS PER LENGTH or TOTAL MASS
    mass: magnitude 
    
    Returns
    ------------
    None
    
    '''

    fid.write('*NONSTRUCTURAL MASS, ELSET=' + elset.upper() + ', UNITS=' + unit.upper() + '\n')
    
    putools.txt.writematrix(fid,mass,5,',','e')
    
    fid.write('**' + '\n')

#%%

def nset(fid,nsetname,nodes,option=''):
    
    '''
    
    
    Arguments
    ------------
    fid: file identifier
    nsetname: string with name
    nodes: array with numbers or list with node set names
    
    Returns
    ------------
    None
    
    '''

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

def orientation(fid,name,defi,a,b,c):

    '''
    *ORIENTATION
    
    Arguments
    ------------
    fid: file identifier
    def: NODES
    
    Returns
    ------------
    None
    
    '''
    
    fid.write('*ORIENTATION, NAME=' + name.upper() + ', DEFINITION=' + defi.upper() + '\n')

    putools.txt.writematrix(fid,[a,b,c],'',',',['int'])
    fid.write('**' + '\n')
    fid.write('**' + '\n')

#%%

def parameter(fid,parameternames,values):
    
    '''
    *PARAMETER
    
    Arguments
    ------------
    fid: file identifier
    parameternames: string or list with names
    values: array with numbers
    
    Returns
    ------------
    None
    
    '''

    if isinstance(parameternames,str):
        parameternames=[parameternames]

    if len(values)==1:
        values=values*np.ones(len(parameternames))
    
    fid.write('*PARAMETER' + '\n')
    
    for k in np.arange(len(parameternames)):
        fid.write( parameternames[k] + '=' + putools.num.num2stre(values[k],5,',') + '\n')
    
    fid.write('**' + '\n')

#%%

def part(fid,partname):
    
    '''
    *PART
    
    Arguments
    ------------
    fid: file identifier
    partname: string with name
    
    Returns
    ------------
    None
    
    '''

    fid.write('*PART, NAME=' + partname.upper() + '\n')
    fid.write('**' + '\n')

#%%

def partend(fid):
    
    '''
    *END PART
    
    Arguments
    ------------
    fid: file identifier
    
    Returns
    ------------
    None
    
    '''
    
    fid.write('*END PART' + '\n')
    fid.write('**' + '\n')

#%%

def release(fid,elset,end_id,release_id):
    
    '''
    *RELEASE
    
    Arguments
    ------------
    fid: file identifier
    elset: string or list with element set name
    end_id: string or list with end ids, e.g. 'S1' 'S2'
    release_id: string or list with end ids
    
    Returns
    ------------
    None
    
    '''
    
    # M1: refers to the rotation about the n1-axis,
    # M2 refers to the rotation about the n2-axis,
    # M1-M2: refers to a combination of rotational degrees of freedom about the n1-axis and the n2-axis,
    # T: refers to the rotation about the t-axis,
    # M1-T: refers to a combination of rotational degrees of freedom about the n1-axis and the t-axis,
    # M2-T: refers to a combination of rotational degrees of freedom about the n2-axis and the t-axis, and
    # ALLM: represents a combination of all the rotational degrees of freedom (i.e., M1, M2, and T).
    
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

def restart(fid,id_type,step=-1,frequency=100):
    
    '''
    *RESTART
    
    Arguments
    ------------
    fid: file identifier
    id_type: 'READ' or 'WRITE'
    step: number, usually the last
    frequency: frequency
    
    Returns
    ------------
    None
    
    '''

    checkarg(id_type,['READ' , 'WRITE'])
    
    if id_type.upper()=='READ':
        freq_str=''
    else:
        freq_str=', FREQUENCY=' + str(frequency)
    
    if id_type.upper()=='WRITE':
        step_str=''
    else:
        step_str=', STEP=' + str(step)
    
    
    fid.write('*RESTART' + id_type + step_str + freq_str + '\n')
    fid.write('**' + '\n')

#%%

def shellsection(fid,elset,material,options,shellproperties):
    
    '''
    *SHELL SECTION
    
    Arguments
    ------------
    fid: file identifier
    elset: string with element set name
    material: string with material set name
    options: e.g.  OFFSET=SNEG
    shellproperties: array with [thickness,number of integration points]
    
    Returns
    ------------
    None
    
    '''
    
    fid.write('*SHELL SECTION, ELSET=' + elset.upper() + ',' + ' MATERIAL=' + material.upper() + ', ' + options.upper() + '\n')

    putools.txt.writematrix(fid,shellproperties,3,',',['f','int'])

    fid.write('**' + '\n')

#%%

def shearcenter(fid,x1,x2):
    
    '''
    *SHEAR CENTER
    
    Arguments
    ------------
    fid: file identifier
    x1: offset in 1-dir in [m]
    x2: offset in 2-dir in [m]
    
    Returns
    ------------
    None
    
    '''
 
    fid.write('*SHEAR CENTER' + '\n')
    putools.txt.writematrix(fid,[x1,x2],3,',','e')
    fid.write('**' + '\n')
    
#%%

def spring(fid,elset,element_nodenumber,dofno,springstiffness):

    '''
    *ELEMENT, TYPE=SPRING2
    *SPRING
    
    Arguments
    ------------
    fid: file identifier
    elset: string with element set name
    element_nodenumber: [el,node1,node2]
    dofno: DOF 1-6
    springstiffness: in N/m
    
    Returns
    ------------
    None
    
    '''

    #*ELEMENT, TYPE=SPRING2, ELSET=SADLESPRING_X
    #301001, 100075, 10051
    #301002, 200075, 10169
    #301003, 110075, 20051
    #301004, 210075, 20169
    #*SPRING,ELSET=SADLESPRING_X
    # 1,1
    # 1.00000e+12
    
        
    fid.write('*ELEMENT, TYPE=SPRING2, ELSET=' + elset.upper() + '\n')

    putools.txt.writematrix(fid,element_nodenumber,'',',','int')

    fid.write('*SPRING, ELSET=' + elset.upper() + '\n')
    
    putools.txt.writematrix(fid,[dofno,dofno],'',',','int')

    if putools.num.isnumeric(springstiffness):
        putools.txt.writematrix(fid,springstiffness,5,',','e')
    

    fid.write('**' + '\n')
    fid.write('**' + '\n')
    
#%%

def springa(fid,elset,element_nodenumber,springstiffness):

    '''
    *ELEMENT, TYPE=SPRINGA
    *SPRING    
    
    Arguments
    ------------
    fid: file identifier
    elset: string with element set name
    element_nodenumber: [Elno,Nodeno1,Nodeno2]
    springstiffness: in N/m
    
    Returns
    ------------
    None
    
    '''
        
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
    
def static(fid,time):

    '''
    *STATIC    
    
    Arguments
    ------------
    fid: file identifier
    time: string or array with [Initial Total Min Max]
    
    Returns
    ------------
    None
    
    '''

    fid.write('*STATIC \n')

    if putools.num.isnumeric(time):
        putools.txt.writematrix(fid,time,'1',',','e')
    elif isinstance(time,str):
        fid.write(time +' \n')
    
    fid.write('**' + '\n')

#%%

def step(fid,options='',comment_str=''):

    '''
    *STEP    
    
    Arguments
    ------------
    
    Returns
    ------------
    None
    
    '''

    comma=', '
    if len(options)<1:
        comma=''
        options=''
    
    comment(fid,comment_str)
    fid.write('*STEP ' + comma + options.upper() + '\n')
    
#%%

def stepend(fid):

    '''
    *END STEP
    
    Arguments
    ------------
    fid: file identifier
    
    Returns
    ------------
    None
    
    '''
    
    fid.write('*END STEP' + '\n')
    fid.write('**' + '\n')
    fid.write('**' + '\n')
    
#%%

def temperature(fid,op,nset,magnitude_temp,partname=''):

    '''
    *TEMPERATURE
    
    Arguments
    ------------
    fid: file identifier
    op: 'MOD' or 'NEW' for new (erase all old) or modified TEMP
    nset: string with node name
    magnitude_temp: in K
    
    Returns
    ------------
    None
    
    '''

    checkarg(op,['MOD','NEW'])

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

def tie(fid,tiename,adjust,postol,slavename,mastername):

    '''
    *TIE
    
    Arguments
    ------------
    fid: file identifier
    tiename: string with name
    adjust: 'YES' or 'NO' adjustment of slave node
    postol: in m, nodes outside will not be tied
    slavename: name of surface
    mastername: name of surface
    
    Returns
    ------------
    None
    
    '''
    
    checkarg(adjust,['YES','NO'])
    
    fid.write('*TIE, NAME=' + tiename.upper() + ', ADJUST=' + adjust.upper() + ', ' 'POSITION TOLERANCE=' + putools.num.num2stre(postol,3) + '\n')
    fid.write(slavename.upper() + ', ' + mastername.upper() + '\n')
    
    fid.write('**' + '\n')

#%%
   
def transverseshearstiffness(fid,k23,k13):

    '''
    *TRANSVERSE SHEAR STIFFNESS
    
    Arguments
    ------------
    fid: file identifier
    k23: shear stiffness in 2-dir
    k13: shear stiffness in 1-dir
    
    Returns
    ------------
    None
    
    '''
    
    fid.write('*TRANSVERSE SHEAR STIFFNESS' + '\n')
    putools.txt.writematrix(fid,[k23,k13],3,',','e')

    


