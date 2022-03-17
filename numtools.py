
# -*- coding: utf-8 -*-
"""
Created on 

@author: OWP
"""

#%%

import numpy as np
import time

#%%

def argmin(A,a_search):

    # Find closest match of a in A

    # Inputs: 
    # A: parent vector
    # a_search: elements to find
    
    # Outputs:
    # IndexMin: indices

    if np.shape(a_search)==():
        ind_min=np.amin(np.abs(A-a_search))
        IndexMin=ind_min
        
    if isinstance(a_search,list) or isinstance(a_search,np.ndarray):
    
        IndexMin=np.zeros(np.shape(a_search),dtype=int) #*np.nan
        for k in np.arange(len(a_search)):
            ind_min=np.argmin(np.abs(A-a_search[k]))
            IndexMin[k]=ind_min.astype('int')
        
    return IndexMin

#%%

def starprint(A_list,n=0):

    # Print message 

    # Inputs: 
    # A_list: list or string with message
    # n: number of 25-star lines

    star_25='*************************'
    star_5='***** '
    
    if isinstance(A_list,str):
        A_list=[A_list]
    
    for k in np.arange(n):
        print(star_25)
        
    for A_list_sub in A_list:
        print(star_5 + A_list_sub)
        
    for k in np.arange(n):
        print(star_25)
        
        
#%%

def tic():

    # Timing function
    
    # Outputs:
    # t0: initial time
    
    t0=time.time()
    return t0

def toc(t0,digits=5):

    # Timing function
    
    # Inputs:
    # t0: initial time

    t1=time.time()
    dt=t1-t0   
    
    if dt>1:
        digits=2
    elif dt>0.1:
        digits=3
    elif dt>0.01:
        digits=4

    format_f='{:.' + str(digits) + 'f}'
    print('Elapsed time: ' + format_f.format(dt) + ' seconds.')

    

def tocs(t0):

    # Timing function
    
    # Inputs:
    # t0: initial time
    
    # Outputs:
    # dt: elapsed time

    t1=time.time()
    dt=t1-t0   

    return dt
    
#%%

def readfile(InputFileName):

    # Read file to list
    
    # Inputs:
    # InputFileName: filename
    
    # Outputs:
    # InputFileLines: list with each line as string

    fid=open(InputFileName,'r')
    InputFileLines=fid.read().splitlines()
    fid.close()
    
    return InputFileLines
    

#%%

def listindexsub(A_list,search_str,casesens=False):
    
    # Gives index of string among list of strings (partial match allowed)

    # Inputs:
    # A_list: parent list
    # search_str: search list
    # casesens: case sensitivity
    
    # Outputs:
    # index: indices of match
    
    if casesens==False:
        index = [i for i, s in enumerate(A_list) if search_str.casefold() in s.casefold()]
    elif casesens==True:
        index = [i for i, s in enumerate(A_list) if search_str in s]

    return index


#%%

#https://stackoverflow.com/questions/60618271/python-find-index-of-unique-substring-contained-in-list-of-strings-without-go

def listindexsingle(L_all,L_search_sub):
        
    try:
        ind_sub=L_all.index(L_search_sub)        
    except:        
        ind_sub=None
        
    return ind_sub


def listindex(L_all,L_search):
    
    # Gives index of string list among bigger string list (exact match, no partial)
    # Error if no match or more than one match
    # Case sensitive

    # Inputs:
    # L_all: parent list
    # L_search: search list
    
    # Outputs:
    # index: indices of match
    
    if isinstance(L_search,str):
        L_search=[L_search]
        
    index=[None]*len(L_search)
    for k,L_search_sub in enumerate(L_search):
        
        ind_sub=listindexsingle(L_all,L_search_sub)
        
        if ind_sub==None:
            raise Exception('No match for ' + L_search_sub)
        else:
            
            # Check if any match in remainder of list
            ind_sub_check=listindexsingle(L_all[(ind_sub+1):],L_search_sub)
            
            if ind_sub_check==None: # Ok, no more matches for this word
                index[k]=ind_sub
            else:
                print(ind_sub)
                print(ind_sub_check)
                raise Exception('Two or more matches for ' + L_search_sub)
                
        
    return index

#%%

def num2stre(a,digits=6,delimeter=', '):
    
    # Number(s) to string in scientific format 

    # Inputs:
    # a: vector or list 
    # digits: digits
    # delimeter: delimeter
    
    # Outputs:
    # str_out: string with numbers
    
    #format_exp='{:.6e}'
    format_exp='{:.' + str(digits) + 'e}'
    
    str_out='Empty_string'
    
    if isinstance(a,int):
        str_out=format_exp.format(a)
        
    elif isinstance(a,float):
        str_out=format_exp.format(a)
      
    elif isinstance(a,np.int32):
        str_out=format_exp.format(a)
          
    elif isinstance(a,list):
        
        str_out=''
        for a_element in a:
            str_out=str_out+format_exp.format(a_element) + delimeter
            
        str_out=str_out[0:(-1-len(delimeter))]
        
    elif isinstance(a,np.ndarray):
    
        str_out=''
        for a_element in np.nditer(a):
            str_out=str_out+np.format_float_scientific(a_element, unique=False, precision=digits) + delimeter
        
        str_out=str_out[0:(-len(delimeter))]
        
    return str_out

#%%

def num2strf(a,digits=6,delimeter=', '):
    
    # Number(s) to string in float format 

    # Inputs:
    # a: vector or list 
    # digits: digits
    # delimeter: delimeter
    
    # Outputs:
    # str_out: string with numbers
    
    format_f='{:.6f}'
    format_f='{:.' + str(digits) + 'f}'

    str_out='Empty_string'

    if isinstance(a,int):
        str_out=format_f.format(a)
        
    elif isinstance(a,float):
        str_out=format_f.format(a)
        
    elif isinstance(a,np.int32):
        str_out=format_f.format(a)
         
    elif isinstance(a,list):
        
        str_out=''
        for a_element in a:
            str_out=str_out+format_f.format(a_element) + delimeter
            
        str_out=str_out[:(-1-len(delimeter))]
    elif isinstance(a,np.ndarray):
    
        str_out=''
        for a_element in np.nditer(a):
            str_out=str_out + format_f.format(a_element) + delimeter
        
        str_out=str_out[:(-len(delimeter))]
        
    return str_out

#%%

def writematrix(fid,matrix,digits=3,delimeter=', ',list_format='e'):
    
    # Write matrix to file  

    # Inputs:
    # matrix: vector or matrix with numbers 
    # digits: digits
    # delimeter: delimeter
    # list_format: e,f, or int (for all numbers same format) or [int,e,e] for different
    
    matrix=np.atleast_2d(matrix)
    (n_row,n_col)=np.shape(matrix)

    if isinstance(list_format,str):
        list_format=[list_format]
        
    if len(list_format)==1:
        list_format=n_col*list_format;
    
    for k in np.arange(n_row):
        
        str_row=''
        a_el_str='None '
        for j in np.arange(n_col):
            if list_format[j]=='int':
                a_el_str=str(int(matrix[k,j]))
            elif list_format[j]=='e':
                a_el_str=num2stre(matrix[k,j],digits)
            elif list_format[j]=='f':
                a_el_str=num2strf(matrix[k,j],digits)
            else:
                raise Exception('Invalid format: ' + list_format[j])
                
            str_row=str_row + a_el_str + delimeter
            
        str_row=str_row[:(-len(delimeter))] + '\n'    

        fid.write(str_row)

#%%

def rangebin(n,d):
    
    # Divide range into bins of given size
    # n=12,d=5 gives bin1=[1,2,3,4,5] bin2=[6,7,8,9,10] bin3=[11,12]

    # Inputs:
    # n: number
    # d: bin size
    
    # Outputs:
    # bins: list with bins indicies

    if n<=d:
        bins=[np.arange(n)]
    else:
        nbins=int(np.ceil(n/d))
        
        bins=[None]*nbins
        for k in range(nbins):
            bins[k]=k*d+np.arange(d)
            
        if bins[-1][-1]>n:
            bins[-1]=np.arange(bins[-2][-1]+1,n)
            
    return bins

#%%

def isnumeric(a):
    
    # Check if a is numeric, i.e. numpy or numbers in list range into bins of given size

    # Inputs:
    # a: number

    # Outputs:
    # isnum: logical
    
    
    isnum=False    
    if isinstance(a,int):
        isnum=True
    elif isinstance(a,float):
        isnum=True
    elif isinstance(a,list):
        
        if len(a)>0:
            if isinstance(a[0],int):
                isnum=True
            elif isinstance(a[0],float):
                isnum=True
                
        
    elif isinstance(a,np.ndarray):
        isnum=True
        
    if isinstance(a,bool):
        isnum=False   
        
    return isnum
            
#%%

def ensurenp(a,Force1d=False):
    
    # Convert a number to numpy array

    # Inputs:
    # a: number
    # Force1d: keep vector format (not 2d)

    # Outputs:
    # b: numpy array

    if isinstance(a,np.ndarray):
        if np.shape(a)==():
            if Force1d==True:
                b=np.array([a])
            else:
                b=np.copy(a)
            
        else:
            b=np.copy(a)
        
    elif isinstance(a,int) or isinstance(a,float):
        if Force1d==True:
            b=np.array([a])
        else:
            b=np.array(a)
    
    elif isinstance(a,list):
        b=np.array(a)

    else:
        raise Exception('Not supported type of a')
    
    return b

#%%

def str2num(a_list,numformat='float',n_col=''):
    
    # Convert list of strings to matrix

    # Inputs:
    # a_list: list with strings
    # numformat: 'float' or 'int'
    # n_col: number of columns to read

    # Outputs:
    # M: numpy array

    if isinstance(a_list,str):
        a_list=[a_list]   
        
    # Testdata
    #a_list=[None]*2
    #a_list[0]='12.44, 212, 0.0001, 1e-3, -2, -2.21'
    #a_list[1]='-3.11e-3, 6e6, -212, , -2.0 , 55.99'

    # Find right size if none specified
    if n_col=='':
        n_col=len(a_list[0].split(','))
    
    n_row=len(a_list)
    
    M=np.zeros((n_row,n_col))*np.nan
    
    for k in np.arange(n_row):
        
        a_row=a_list[k].split(',')
        
        for j in np.arange(n_col):
        
            if a_row[j]=='' or a_row[j]==' ' or a_row[j]=='  ':
                #M[k,j]=0.0
                #continue
                a_row[j]='0.0'
            
            if numformat=='float':
                M[k,j]=float(a_row[j])
            elif numformat=='int':
                M[k,j]=int(a_row[j])
        
    
    return M

#%%

def genlabel(number,dof,midfix='_'):
    
    if isinstance(dof,str):
        if dof=='all':
            dof=['U1','U2','U3','UR1','UR2','UR3']
        else:
            dof=[dof]
        
    if isinstance(number,int):
        number=[number]
        
    if isinstance(number,np.int32):
        number=[number]
        
    if isinstance(number,float):
        number=[number]    

    A_label=[ str(int(number_sub)) + midfix + dof_sub for number_sub in number for dof_sub in dof]
        
    return A_label

#%%

def norm_fast(a):
    return sum(a*a)**0.5
    
#%%

#@nb.njit(fastmath=True)
def norm_fast_old(a):
    s = 0.
    for i in range(a.shape[0]):
        s += a[i]**2
    return np.sqrt(s)
    
#%%

def cross_fast(a,b):
    c=np.array([
        a[1]*b[2] - a[2]*b[1] ,
        a[2]*b[0] - a[0]*b[2] ,
        a[0]*b[1] - a[1]*b[0] ,
        ])
    
    return c

#%%

def block_diag_rep(A,r):

    m,n = A.shape
    out = np.zeros((r,m,r,n), dtype=A.dtype)
    diag = np.einsum('ijik->ijk',out)
    diag[:] = A
    
    return out.reshape(-1,n*r)


