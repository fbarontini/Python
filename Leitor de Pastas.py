"""
Created on Mon Jun  4 13:13:46 2018

@author: fbarontini
"""

import os, sys, re, shutil
from stat import *
import numpy as np

ARQUIVOS = np.array([])
link = r'X:\Pesquisa De Bens\2.CASOS'
path = 'D:\Matriculas'

def walktree(top, callback):
    '''recursively descend the directory tree rooted at top,
       calling the callback function for each regular file'''

    for f in os.listdir(top):
        pathname = os.path.join(top, f)
        mode = os.stat(pathname)[ST_MODE]
        if S_ISDIR(mode):
            # It's a directory, recurse into it
            walktree(pathname, callback)
        elif S_ISREG(mode):
            # It's a file, call the callback function
            callback(pathname)
        else:
            # Unknown file type, print a message
            print('Skipping %s' % pathname)

def visitfile(file):
    try:
        if file.endswith('pdf'):
            global ARQUIVOS
            ARQUIVOS = np.append(ARQUIVOS, file)
        #print('visiting', file)
    except FileNotFoundError:
        pass

if __name__ == '__main__':
    #walktree(sys.argv[1], visitfile)
    walktree(link, visitfile)
    
    # Converto os caracteres do array 
    ARQUIVOS = np.char.lower(ARQUIVOS)
    # Checo se existe a palavra 'Negativa' nos arquivos para excluir
    MATRICULAS = np.array([])
    for f in ARQUIVOS:
        if re.search('negativa', f):
            pass
        else:
            MATRICULAS = np.append(MATRICULAS,f)
    
    
    for mat in MATRICULAS:
        try:
            shutil.copy(mat,path)
        except:
            print("Arquivo com problemas: {}".format(mat))