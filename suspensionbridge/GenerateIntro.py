# -*- coding: utf-8 -*-
"""
Created on Sat Jan 22 09:31:11 2022

@author: oyvinpet
"""
#%%

import numpy as np
import putools
from .. import gen
import datetime

from ypstruct import *

#%%

def GenerateIntro(fid,abaqus,bearing,bridgedeck,cable,geo,hanger,modal,sadle,step,tower,time):

    comment=[]
    comment.append('Parametrized suspension bridge model')
    c=datetime.datetime.now().isoformat()
    comment.append('Model input generated ' + c[:-7])

    gen.Comment(fid,comment)
    gen.Comment(fid,['Part of abaqustools package','Oyvind Wiig Petersen, NTNU'])
    
    gen.Line(fid,'**')

    struct_all=[None]*11
    struct_all[0]=abaqus
    struct_all[1]=step
    struct_all[2]=cable
    struct_all[3]=bridgedeck
    struct_all[4]=hanger
    struct_all[5]=tower
    struct_all[6]=bearing
    struct_all[7]=sadle
    struct_all[8]=geo
    struct_all[9]=step
    struct_all[10]=modal

    struct_all_name=[None]*11
    struct_all_name[0]='abaqus'
    struct_all_name[1]='step'
    struct_all_name[2]='cable'
    struct_all_name[3]='bridgedeck'
    struct_all_name[4]='hanger'
    struct_all_name[5]='tower'
    struct_all_name[6]='bearing'
    struct_all_name[7]='sadle'
    struct_all_name[8]='geo'
    struct_all_name[9]='step'
    struct_all_name[10]='modal'

    comment=[]
    comment.append('User parameter values:')
    # comment.append('To come')

    # TODO: format intro text
    
    for k in np.arange(len(struct_all)):
            
        comment.append('')
        struct_k=struct_all[k]
        field_names=struct_k.fields()
        
        for j in np.arange(len(field_names)):

            field_value=struct_k[field_names[j]]
            
            if isinstance(field_value,str):
                comment.append(struct_all_name[k] + '.' + field_names[j] + '=' + field_value )
            
            if putools.num.isnumeric(field_value):
                field_value_str=putools.num.num2stre(field_value,5)
                comment.append(struct_all_name[k] + '.' + field_names[j] + '=' + field_value_str)
            
            if isinstance(field_value,bool):
                if field_value==False:
                    field_value_str='False'
                elif field_value==True:
                    field_value_str='True'
                comment.append(struct_all_name[k] + '.' + field_names[j] + '=' + field_value_str)
            
            if isinstance(field_value,struct):
                              
                field_names_sub=field_value.fields()
                
                for j2 in np.arange(len(field_names_sub)):
                
                    field_value_sub=field_value[field_names_sub[j2]]
                    
                    if isinstance(field_value,str):
                        comment.append(struct_all_name[k] + '.' + field_names[j] + '.' + field_names_sub[j2] + '=' + field_value_sub )
                    
                    if putools.num.isnumeric(field_value):
                        field_value_sub_str=putools.num.num2stre(field_value_sub,5)
                        comment.append(struct_all_name[k] + '.' + field_names[j] + '.' + field_names_sub[j2] + '=' + field_value_sub )
                                    
                
                             
                
    gen.Comment(fid,comment,False)
