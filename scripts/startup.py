# -*- coding: utf-8 -*-
"""
Created on Thu Dec 15 14:18:01 2016

@author: Shaurita D. Hutchins

"""

# Startup certain files or programs once I login to my computer.

# Modules used
import os
import time as t
import sys
import logging as log

# List the program paths if necessary. May be necessary if the default working
# directory of your command prompt does not include the programs.
spotify = r'C:\Users\shutchins2\AppData\Roaming\Spotify\Spotify.exe'
firefox = r'C:\"Program Files (x86)"\"Mozilla Firefox"\firefox.exe'
spyder = r'C:\Users\shutchins2\Desktop\Spyder.lnk'  # Shortcut link
winscp = r'C:\Users\shutchins2\Desktop\"Software & Executables"\WinSCP\WinSCP.exe'
putty = r'C:\Users\shutchins2\Desktop\"Software & Executables"\PUTTY\putty.exe'
slack = r'C:\Users\shutchins2\AppData\Local\slack\slack.exe'
outlook = 'OUTLOOK.EXE'
excel = 'EXCEL.EXE'
word = 'WINWORD.EXE'

# Make a list of the programs
programslist = [spotify, firefox, spyder, winscp, putty, slack, outlook,
                excel, word]

print(programslist)
###############################################################################
###############################################################################
###############################################################################

## Create an aspect of this program that takes input in the form of a path.
## From there it also takes a name of the program or file.
## Lastly it appends that program/file to the list before the for loop.
#
#listofprograms = input('What is the path of the program? ')
#path = listofprograms
#
#if path == programslist:
#    x = input('What is the common name of the program? ')
#    print('The common name is ' + x)
#else:
#    print('You did not enter a path.')
#    sys.exit('Bye.')

###############################################################################
###############################################################################
###############################################################################

# Create a for loop to simplify the code and make this faster.
for program in programslist:
        # The os.system() function uses Windows command prompt (cmd).
        os.system('start ' + program)
        t.sleep(1) # Take a short sleep as to not overwhelm the ram.

sys.exit("The end.") # let it be known that the script is ending

