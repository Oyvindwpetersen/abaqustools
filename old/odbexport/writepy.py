# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-                       
# from sys import path
import numpy as np
# import odbAccess
import os
# from textRepr import *
# from timeit import default_timer as timer

# from .. import numtools

# def p(pstring):
#     prettyPrint(pstring)

#%%

def WriteFileExportModal(FolderODB,JobName,FolderSave,FolderPython):
    
    Lines=['']
    
    Lines.append('import os')
    Lines.append('import numpy as np')
    Lines.append('')
    
    Lines.append('FolderODB=' + '\'' + FolderODB + '\'')
    Lines.append('JobName=' + '\'' + JobName + '\'')
    Lines.append('FolderSave=' + '\'' + FolderSave + '\'')
    Lines.append('FolderPython=' + '\'' + FolderPython + '\'')
    Lines.append('Prefix=' + '\'' + JobName + '\'')
    Lines.append('')
    
    Lines.append('# Import functions for export')
    Lines.append('CurrentDir=os.getcwd()')
    Lines.append('os.chdir(FolderPython)')
    Lines.append('import odbfunc')
    Lines.append('os.chdir(CurrentDir)')
    Lines.append('')

    Lines.append('')
    Lines.append('# Open ODB')
    Lines.append( 'myOdb=odbfunc.OpenODB(FolderODB,' + '\'' + JobName + '\'' + ')' )
    Lines.append('')
    Lines.append('# Frequencies')
    Lines.append( 'freq=odbfunc.Export_HistoryOutput(myOdb,-1,' + '\'' + 'EIGFREQ' + '\'' +  ')' )
    Lines.append( 'odbfunc.SaveToTXT(FolderSave,' +  '\'freq\'' + ',freq,atype=1,Prefix=Prefix)' )
    Lines.append('')
    
    Lines.append('# Mass')
    Lines.append( 'genmass=odbfunc.Export_HistoryOutput(myOdb,-1,' + '\'' + 'GM' + '\'' +  ')' )
    Lines.append( 'odbfunc.SaveToTXT(FolderSave,' + '\'genmass\'' + ',genmass,atype=1,Prefix=Prefix)' )
    Lines.append('')

    Lines.append('# Mode shapes')
    Lines.append( '(Phi,Phi_Label)=odbfunc.Export_U_UR(myOdb,-1,FrameNumber=' '\'skipfirst\''    ')' )
    Lines.append( 'odbfunc.SaveToTXT(FolderSave,' + '\'Phi\'' + ',Phi,atype=1,Prefix)' )
    Lines.append( 'odbfunc.SaveToTXT(FolderSave,' + '\'Phi_Label\'' + ',Phi_Label,atype=2,Prefix=Prefix)' )
    Lines.append('')

    Lines.append('# Node coordinates')
    Lines.append( '(NodeCoord,NodeNumbers)=odbfunc.Export_NodeCoord(myOdb,-1,0)' )
    Lines.append( 'odbfunc.SaveToTXT(FolderSave,' + '\'NodeCoord\'' + ',NodeCoord,atype=1,Prefix)' )
    Lines.append( 'odbfunc.SaveToTXT(FolderSave,' + '\'NodeNumbers\'' + ',NodeNumbers,atype=1,Prefix=Prefix)' )
    Lines.append('')

    Lines.append('#  Modal section forces')
    Lines.append( '(Phi_SF,Phi_SF_Label)=odbfunc.Export_SectionForce(myOdb,-1,FrameNumber=' '\'skipfirst\''    ')' )
    Lines.append( 'odbfunc.SaveToTXT(FolderSave,' + '\'Phi_SF\'' + ',Phi_SF,atype=1,Prefix)' )
    Lines.append( 'odbfunc.SaveToTXT(FolderSave,' + '\'Phi_SF_Label\'' + ',Phi_SF_Label,atype=2,Prefix=Prefix)' )
    Lines.append('')
    
    Lines.append('# Close ODB')
    Lines.append( 'odbfunc.CloseODB(myOdb)' )
        
    fid=open(FolderSave + '\\' + 'ExportModal' + '.py', 'w')
    for Lines_sub in Lines:
        fid.write( Lines_sub + '\n')

    fid.close()

        