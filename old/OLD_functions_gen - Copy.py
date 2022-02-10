


# -*- coding: utf-8 -*-
"""
Created on 

@author: OWP
"""

#%%

import numpy as np

__all__ = [
    'AssemblyStart',
    'AssemblyEnd',
    'BeamAddedInertia'
           ]


#%%

def Assembly(fid,assembly_name):
    
    # Inputs:
    # assemblyname: char

    fid.write('*ASSEMBLY, NAME=' + assembly_name.upper() + '\n')
    fid.write('**' + + '\n')
    
#%%

def AssemblyEnd(fid,assembly_name):

    # Inputs:
    # assemblyname: char

    fid.write('END ASSEMBLY' + '\n')
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

    fid.write('*BEAM ADDED INERTIA' + '\n'):

    values_list=[linear_mass,x1,x2,alpha,I_11,I_22,I_12]
    str_values=num2strexp(values_list,digits=3,delimeter=', ')
    fid.write(str_values + '\n'):

    fid.write('**' + '\n')
    
#%%

def BeamSection(fid,elset,material,sectiontype,sectionproperties,direction):

    if isinstance(elset,str):
        elset=[elset]

    for elset_sub in elset
        fid.write('*BEAM SECTION, ELSET=' + elset_sub.upper() + ', MATERIAL=' + material.upper() + ', SECTION=' + sectiontype.upper() + '\n')


    sectionproperties=ensurenp(sectionproperties)
    numtools.writematrix(fid,sectionproperties,5,', ','f')
    
    fid.write('**' + '\n')
    
#%%

def BeamGeneralSection(fid,elset,density,sectionproperties,direction,materialproperties):
    
    fid.write('*BEAM GENERAL SECTION, ELSET=' + elset.upper() ', SECTION=GENERAL, DENSITY=' numtools.num2strf(density,) + '\n')
    
    numtools.writematrix(fid,sectionproperties,5,', ','e')
    
    numtools.writematrix(fid,direction,5,', ','e')
    
    numtools.writematrix(fid,direction,5,', ','f')
    
    fid.write('**' + '\n')
    
#%%

def Boundary(fid,nodename,BCmat,op):

    if op.casefold!='MOD' and op.casefold!='NEW'
        raise Exception('')
        
    fid.write('*BOUNDARY, OP=' + op.upper() + '\n')

    if isinstance(nodename,str):
        fid.write(nodename + ',' + str(BCmat(1)) + ',' + str(BCmat(2)) + ',' + str(BCmat(3)) + '\n')
    elif isinstance(nodename,list):
        for node in nodename:
            fid.write(str(node) + ',' + str(BCmat(1)) + ',' + str(BCmat(2)) + ',' + str(BCmat(3)) + '\n')
    elif isinstance(nodename,int):
        fid.write(str(nodename) + ',' + str(BCmat(1)) + ',' + str(BCmat(2)) + ',' + str(BCmat(3)) + '\n')
    
    fid.write('**' + '\n')
    fid.write('**' + '\n')
    
#%%

def Cload(fid,op,nset,dof,magnitude_force,partname=''):

    partname_str=''
    if len(partname)>0
        partname_str=partname + '.'

    if op.casefold()=='DELETE':
        fid.write('*CLOAD, OP=NEW' + '\n')
    
    
    fid.write('*CLOAD, OP=' + op.upper() + '\n')
    
    magnitude_force=ensurenp(magnitude_force)
    
    if len(magnitude_force)==1:
        magnitude_force=magnitude_force*np.ones([1,len(nset)])

    if isnumeric(nset):
        for k in enumerate(nset)
            fid.write( partname_str + str(nset[k]) ', ' + str(dof) ', ' + num2strexp(magnitude_force[k],3) + '\n')
        
    if isinstance(nset,str):
        nset=[nset]

    if isinstance(nset,list):
        for nset_sub in nset
            fid.write( partname_str nset_sub ', ' + str(dof) + ', ' + num2strexp(magnitude_force[k],3) + '\n')
        
    fid.write('**' + '\n')
    fid.write('**' + '\n')
    
#%%

def Comment(fid,comment,logic_main=False):

    # Inputs:
    # comment: char or cell with comments

    if logic_main==True:
        separatator='***********************************************************'
    else:
        separatator='**********'

    if isinstance(comment,str)
        comment=[comment]

    fid.write(separatator + '\n')
    for comment_sub in comment
        fid.write('** ' + comment_sub + '\n')

    fid.write(separatator + '\n')


#%%

    def Dload(fid,op,elset,type_id,magnitude):

    # Inputs:
    # op: operation, delete, mod or new
    # elset: name of element set
    # type_id: type_id of dload, e.g. PZ
    # magnitude: magnitude of dload

    if strcmpi(op,'DELETE'):
        fid.write('*DLOAD, OP=NEW' + '\n')
        fid.write('**' + '\n')
        fid.write('**' + '\n')
        return
    
    if isinstance(magnitude,str):
        magnitude_str=magnitude
    elif isnumeric(magnitude)
        magnitude_str=num2strexp(magnitude)
        
    fid.write('*DLOAD, OP=' + op.upper() + '\n')
    fid.write( elset + ', ' + type_id + ', ' + magnitude_str + '\n')

    fid.write('**' + '\n')
    fid.write('**' + '\n')
    
#%%
    
def Element(fid,element_nodenumber,type_id,elsetname):
    
    element_nodenumber=ensurenp(element_nodenumber)

    n_neg=sum(sum(element_nodenumber<=0))
    if n_neg> 0
        raise Exception(elsetname + ' : negative element/node number' )
    

    if type_id=='B31' or type_id=='B33' 
        if np.shape(element_nodenumber)[1]!=3:
            print('For ELSET ' + elsetname)
            raise Exception('B31 or B33 must have 2 nodes')
        
    if type_id=='B32'
        if size(element_nodenumber,1)!=4
            print('For ELSET ' + elsetname)
            raise Exception('B32 must have 2 nodes')
            
    fid.write('*ELEMENT, TYPE=' + upper(type_id) + ', ELSET=' + upper(elsetname) + '\n')
    
    list_format=['int']*size(element_nodenumber,1)
    numtools.writematrix(fid,element_nodenumber,'',', ',list_format)
        
    fid.write('**' + '\n')
    fid.write('**' + '\n')

    
#%%


def Elset(fid,elsetname,elements,option=''):
    
    fid.write('*ELSET, ELSET=' elsetname.upper() '\n')
    
    if isinstance(elements,list)
        for elements_sub in elements:
            fid.write(elements_sub.upper() + '\n')
    
    if isnumeric(elements):
        
        bins=rangebin(len(elements),16):
            
            for bins_sub in bins:
                fid.writematrix(fid,elements[bins_sub],'',',','int')
                
    fid.write('**' + '\n')

#%%

def FieldOutput(fid,type_id,variables,set_id='',options=''):
    
    comma=', '
    if len(options)<=1:
        comma=''
        options=''

    fid.write('*OUTPUT, FIELD' comma options.upper() + '\n')
    
    if type_id.upper()=='NODE'):
        if len(set_id)<=1:
            fid.write('*NODE OUTPUT \n')
        else
            fid.write('*NODE OUTPUT, NSET=' set_id + '\n')
        
    elif type_id.upper()=='ELEMENT'):
        if len(set_id)<=1:
            fid.write('*ELEMENT OUTPUT \n')
        else
            fid.write('*ELEMENT OUTPUT, ELSET=' + set_id + '\n')
        
        if isinstance(variables,str):
            variables=[variables]
    
    for variables_sub in variables:
        fid.write(variables_sub + '\n')
    
    fid.write('**' + '\n')
    # fid.write('**' + '\n')
    
#%%

def Frequency(fid,n_modes,normalization):

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

def Gravload(fid,op,elset,magnitude=9.8070):
    
    fid.write('*DLOAD, OP=' + op.upper() + '\n')
    
    if isinstance(elset,str):
        elset=[elset]
    
    if magnitude<0
        print('***** Gravity magntiude should generally be positive: magnitude 9.81 and direction [0 0 -1]')
    
    for elset_sub in elset
        fid.write(elset_sub + ', GRAV, ' + numtools.num2strf(magnitude,5) + '\n')
            
fid.write('**' + '\n')

        
#%%

def HistoryOutput(fid,type_id,variables,set_id,options=''):

    comma=', '
    if len(options)<=1
        comma=''
        options=''

    fid.write('*OUTPUT, HISTORY' + comma + options.upper() + '\n')

#%%

def HistoryOutputElement(fid,variables,elset,options=''):

    comma=', '
    if len(options)<=1
        comma=''
        options=''

    fid.write('*ELEMENT OUTPUT, ELSET=' + elset + '\n')

     if isinstance(variables,str):
        variables=[variables]
            
     for variables_sub in variables:
        fid.write(variables_sub + '\n')

                
    fid.write('**' + '\n')
    
#%%
    
def HistoryOutputNode(fid,variables,nset,options=''):

    comma=', '
    if len(options)<=1
        comma=''
        options=''

    fid.write('*NODE OUTPUT, NSET=' + nset + '\n')


     if isinstance(variables,str):
        variables=[variables]
            
     for variables_sub in variables:
        fid.write(variables_sub + '\n')

                
    fid.write('**' + '\n')
    
#%%

def Include(fid,filename):

    fid.write('**' + '\n')
    fid.write('*INCLUDE, INPUT=' + filename + '\n')
    fid.write('**' + '\n')

#%%

# fid.write('**' + '\n')
def Instance(fid,instancename,partname):

    fid.write('*INSTANCE, NAME=' + instancename.upper() + ', PART=' + partname.upper() + '\n')
    fid.write('**' + '\n')


#%%

def InstanceEnd(fid,instancename,partname):

fid.write('*END INSTANCE' + '\n')
    fid.write('**' + '\n')

#%%

def Line(fid,line):

    if isinstance(line,str)
        line=[line]

    for line_sub in line
        fid.write(line_sub + '\n')

#%%

def MPC(fid,type_id,nodes):

    fid.write('*MPC' + '\n')
    
    mpc_str=''
    
    if isnumeric(nodes)
        for nodes_sub in nodes
            mpc_str=mpc_str + ',' + str(int(nodes_sub))
    elif isinstance(nodes,list)
        for nodes_sub in nodes
            mpc_str=mpc_str + ',' + nodes_sub
        
        
        
    mpc_str=mpc_str[0:-2]
    fid.write(type_id ', ' mpc_str + '\n')

    fid.write('**' + '\n')

#%%


def Material(fid,materialname,emodulus,v,density):

    fid.write('*MATERIAL, NAME=' materialname.upper() + '\n')
    fid.write('*ELASTIC' + '\n')
    numtools.writematrix(fid,[emodulus,v],3,', ',['e' , 'f'])
    fid.write('*DENSITY' + '\n')
    numtools.writematrix(fid,[density],3,', ',['e'])
    
    fid.write('**' + '\n')
    fid.write('**' + '\n')


#%%

def ModelChange(fid,option,elset,partname=''):

    if isinstance(elset,str)
        elset=[elset]

    if len(partname)>0
        partname = '.' + partname
    
    fid.write('*MODEL CHANGE, ' + option.upper() + '\n')

    for elset_sub in elset
        fid.write(elset_sub + '\n')

    fid.write('**' + '\n')

#%%
    
def Node(fid,nodenumber_coord,nsetname):

    if any(nodenumber_coord[:,1]<=0):
        print('For NSET ' + nsetname)
        raise Exception('Negative node numbers ')
    
    numtools.writematrix(fid,element_nodenumber,5,',',['int' , 'f', 'f', 'f'])

    fid.write('**' + '\n')
    fid.write('**' + '\n')


#%%

def Nonstructuralmass(fid,elset,unit,mass):
    
    fid.write('*NONSTRUCTURAL MASS, ELSET=' + elset.upper() + ', UNITS=' + unit.upper() + '\n')
    
    numtools.writematrix(fid,mass,5,',','e')
    
    fid.write('**' + '\n')

#%%

def Nset(fid,nsetname,nodes,option=''):
    
    comma=', '
    if len(options)<=1:
        comma=''
        options=''
    
    fid.write('*NSET, NSET=' + nsetname + comma + option.upper() + '\n')
    
    
    if isinstance(nodes,list)
        for nodes_sub in nodes:
            fid.write(nodes_sub.upper() + '\n')
    
    if isnumeric(nodes):
        
        bins=rangebin(len(nodes),16):
            
            for bins_sub in bins:
                fid.writematrix(fid,nodes[bins_sub],'',',','int')
                
                

    fid.write('**' + '\n')
    fid.write('**' + '\n')
    

#%%

def Parameter(fid,parameternames,values):
    
    if isinstance(parameternames,str)
        parameternames=[parameternames]

    if len(values)==1
        values=values*np.ones(len(parameternames))
    
    fid.write('*PARAMETER' + '\n')
    
    for k in np.arange(len(parameternames))
        fid.write( parameternames[k] + '=' + numtools.num2stre(values[k],5,',') + '\n')
    
    fid.write('**' + '\n')

#%%

def Part(fid,partname):
    
    fid.write('*PART, NAME=' + partname.upper() + '\n')
    fid.write('**' + '\n')

#%%

def PartEnd(fid):

    fid.write('*END PART' + '\n')
    fid.write('**' + '\n')

#%%

def Release(fid,elset,end_id,release_id):

    if isinstance(elset,str):
        elset=[elset]
        
    if isinstance(end_id,str):
        end_id=[end_id]

    if isinstance(release_id,str):
        release_id=[release_id]

    fid.write('*RELEASE' + '\n')

    for i in np.arange(len(end_id)):
        for j in np.arange(len(release_id)):
            for k in np.arange(len(elset)):
        
                if isnumeric(elset):
                    elset_string=str(int(elset[k])):
                elif isinstance(elset,list):
                    elset_string=elset[k];
        
                fid.write(elset_string + ', ' + end_id[i] + ', ' + release_id[j]  + '\n')
    
    
    fid.write('**' + '\n')

#%%

def Restart(fid,type_id,frequency,step)
    
   #if nargin<3 | isempty(frequency) | strcmpi(frequency,' ')
    #frequencyString=''
   # else
   # frequencyString=[', FREQUENCY=' num2str(frequency)]
    
   # if nargin<3 | isempty(step) | strcmpi(step,' ')
   # stepString=''
   # else
   # stepString=[', STEP=' num2str(step)]
    
  #  fid.write('*RESTART,' type_id stepString frequencyString + '\n')
   # fid.write('**' + '\n')


#%%

def ShellSection(fid,elset,material,options,shellproperties):

    fid.write('*SHELL SECTION, ELSET=' + elset.upper() + ',' + ' MATERIAL=' + material.upper() + ', ' + options.upper() + '\n')

    numtools.writematrix(fid,shellproperties,3,',','f')

    fid.write('**\n'])

#%%

def ShearCenter(fid,x1,x2):

    fid.write('*SHEAR CENTER' + '\n')
    numtools.writematrix(fid,[x1,x2],3,',','f')

#%%

def Spring(fid,elset,element_nodenumber,dofno,springstiffness):

    #*ELEMENT, TYPE=SPRING2, ELSET=SADLESPRING_X
    #301001, 100075, 10051
    #301002, 200075, 10169
    #301003, 110075, 20051
    #301004, 210075, 20169
    #*SPRING,ELSET=SADLESPRING_X
    # 1,1
    # 1.00000e+12

    # For now, springstiffness is a scalar

    if isinstance(springstiffness,str):
        springstiffness=[springstiffness]
        
    fid.write('*ELEMENT, TYPE=SPRING2, ELSET=' + elset.upper() + '\n')

    numtools.writematrix(fid,element_nodenumber,'',',','int')

    fid.write('*SPRING,ELSET=' + elset.upper() + '\n')
    
    numtools.writematrix(fid,[dofno_sub,dofno_sub],'',',','int')

    if isnumeric(springstiffness):
        numtools.writematrix(fid,springstiffness,5,',','e')
    elif isinstance(springstiffness,list):
        fid.write( springstiffness + '\n')

    fid.write('**' + '\n')
    fid.write('**' + '\n')
    
#%%

def SpringA(fid,elset,element_nodenumber,springstiffness):

    # For now, springstiffness is a scalar

    if isinstance(springstiffness,str):
        springstiffness=[springstiffness]
        
    fid.write('*ELEMENT, TYPE=SPRINGA, ELSET=' + elset.upper() + '\n')

    numtools.writematrix(fid,element_nodenumber,'',',','int')

    fid.write('*SPRING,ELSET=' + elset.upper() + '\n')

    if isnumeric(springstiffness)
        numtools.writematrix(fid,springstiffness,5,',','e')
    elif isinstance(springstiffness,list):
        fid.write( springstiffness + '\n')

    fid.write('**' + '\n')
    fid.write('**' + '\n')

#%%
    
def Static(fid,time)

# Time=[Initial Total Min Max]

fid.write('*STATIC \n'])

if isnumeric(time)
    numtools.writematrix(fid,'1',',','e')
elif isinstance(time,str):
    fid.write(time):

fid.write('**' + '\n')
fid.write('**' + '\n')

def Step(fid,options='',comment='')
    
    comma=', '
    if len(options)<=1:
        comma=''
        options=''
    
    genComment(fid,comment)
    fid.write('*STEP ' + comma + options.upper() + '\n')
    
    fid.write('**' + '\n')

def StepEnd(fid):
    
    fid.write('*END STEP' + '\n'):
    fid.write('**' + '\n'):

def Tie(fid,tiename,adjust,postol,slavename,mastername):
    
    fid.write('*TIE, NAME=' tiename.upper() ', ADJUST=' adjust.upper() ', ' 'POSITION TOLERANCE=' numtools.num2stre(postol,3) '\n']):
    fid.write(slavename + ', ' + mastername '\n']):

    fid.write('**' + '\n')



def Temp(fid,op,nset,magnitude)

    fid.write('*TEMPERATURE, OP=' + op.upper() + '\n')
    
    if isinstance(nset,str):
        nset=[nset]
        
    if len(magnitude_force)==1:
        magnitude_force=magnitude_force*np.ones([1,len(nset)])
    
    if isnumeric(nset)
        nset=ensurenp(nset)
        for k in np.arange(nset)
            numtools.writematrix(fid,[nset[k],magnitude_force[k],5,',',['int' 'f'])

    if isinstance(nset,list):
        for k in np.arange(nset)
            fid.write(nset + '' numtools.num2strf(magnitude_force[k],5,',') + 'n')
    
    fid.write('**' + '\n')
    fid.write('**' + '\n')
    
def TransverseShearStiffness(fid,k23,k13):

fid.write('*TRANSVERSE SHEAR STIFFNESS' + '\n')
fid.write(num2str(k23,'%0.3e') ', ' num2str(k13,'%0.3e') + '\n')




# https://www.sharcnet.ca/Software/Abaqus/6.14.2/v6.14/books/usb/default.htm?startat=pt06ch29s03alm08.html#usb-elm-ebeamelem-transshear-override


# k23: shear stiffness in 2-dir
# k13: shear stiffness in 1-dir


