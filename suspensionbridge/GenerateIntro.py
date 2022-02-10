# -*- coding: utf-8 -*-
"""
Created on Sat Jan 22 09:31:11 2022

@author: oyvinpet
"""
#%%

import numpy as np
import numtools
import gen
import datetime

#%%

def GenerateIntro(fid,abaqus,bearing,bridgedeck,cable,geo,hanger,modal,sadle,step,tower,time):

    comment=[]
    comment.append('Parametrized suspension bridge model')
    c=datetime.datetime.now().isoformat()
    comment.append('Model input generated ' + c[:-7])

    gen.Comment(fid,comment)
    gen.Comment(fid,'Part of abaqtus tools package')
    gen.Comment(fid,'2022 Oyvind Wiig Petersen, NTNU')

    gen.Line(fid,'**')

    struct_all=[None]*9
    struct_all[0]=cable
    struct_all[1]=bridgedeck
    struct_all[2]=hanger
    struct_all[3]=tower
    struct_all[4]=bearing
    struct_all[5]=sadle
    struct_all[6]=geo
    struct_all[7]=step
    struct_all[8]=modal

    struct_all_name=[None]*9
    struct_all_name[0]='cable'
    struct_all_name[1]='bridgedeck'
    struct_all_name[2]='hanger'
    struct_all_name[3]='tower'
    struct_all_name[4]='bearing'
    struct_all_name[5]='sadle'
    struct_all_name[6]='geo'
    struct_all_name[7]='step'
    struct_all_name[8]='modal'

    comment=[]
    comment.append('User parameter values:')
    comment.append('To come')

    # TODO: format intro text
    
# =============================================================================
#     for k=1:length(struct_all)
#             
#         comment.append('')
# 
#         field_names=fieldnames(struct_all{k})
#         for j=1:length(field_names)
#                     
#             field_value=getfield(struct_all{k},field_names{j})
#             
#             if ischar(field_value)
#                 comment.append([struct_all_name{k} '.' field_names{j} '=' , '''' field_value '''' )
#             end
#             
#             if isnumeric(field_value)    
#                 field_value_str=PrintMatrix(field_value)
#                 comment.append([struct_all_name{k} '.' field_names{j} '=' field_value_str)
#             end
#             
#             if islogical(field_value)
#                 if field_value==False
#                     field_value_str='False'
#                 elif field_value==false
#                     field_value_str='false'
#                 end
#                 comment.append([struct_all_name{k} '.' field_names{j} '=' field_value_str)
#             end
#             
#            if isstruct(field_value)    
#                field_names_sub=fieldnames(field_value)
#                for j2=1:length(field_names_sub)
#                 field_value_sub=getfield(field_value,field_names_sub{j2})
#                 
#                 if ischar(field_value_sub)
#                 comment.append([struct_all_name{k} '.' field_names{j} '.' field_names_sub{j2} '=' , '''' field_value_sub '''' )
#                 end
#                 
#                 if isnumeric(field_value_sub)
#                 field_value_sub_str=PrintMatrix(field_value_sub)
#                 comment.append([struct_all_name{k} '.' field_names{j} '.' field_names_sub{j2} '=' field_value_sub_str)
#                 
#                 end
#                end
#            end
#             
#         end
#     end
# 
#     gen.Comment(fid,comment,False)
# 
#     end
# =============================================================================

    gen.Comment(fid,comment,False)
