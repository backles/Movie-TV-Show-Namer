import logging
import re
import glob
import os
import string
import shutil
import sys
from xml.dom import minidom


def moveMovie(readDirectory, movieDirectory, fileName):
    print("Is Movie")
    #shutil.move(readDirectory + fileName, movieDirectory + fileName)

def moveTVShow(readDirectory, tVsDirectoryDirectory, fileName):
    print("Is TVshow")
    #shutil.move(readDirectory + fileName, tVsDirectoryDirectory + fileName)
	
def getAllMP4(readDirectory, movieDirectory, tVsDirectory, files):
    for file in files:
        originalFile = file
        if file.endswith(".mp4"):
            file = file[:-4]															#removes file extension from list
            if '.' in file:																#If there are any periods in the title minus the extension
                file = file.replace(".", " ")											#remove period
            fileStringName = file.split()												#splits the string to look for movie or TV show
            length = len(fileStringName)
            makeGoodName(originalFile, file)
            #if tvRE(fileStringName[length - 1]) == 1:
            #    moveTVShow(readDirectory, tVsDirectory, originalFile)
            #else: 																			#Else if Movie
            #    moveMovie(readDirectory, movieDirectory, originalFile)

def makeGoodName(origfile, file):
    print("Original " + file)
    file = file.replace(".", " ")
    fileStringName = file.split()
    n = 0
    for item in fileStringName:
        if tvRE(item) == 1:
            break
        elif (n) == (len(fileStringName)-1):
            n = None
        else:
            n = n + 1
    if n == None:
        print("Should be movie")
        shortName = file # temporary
    else:
        lengthToShorten = (len(fileStringName)- n-1)
        if lengthToShorten == 0:
            shortName = fileStringName
            shortName = ''.join(shortName)
        else:
            shortName = fileStringName[:-lengthToShorten]
            shortName = ''.join(shortName)
    print("Short name " + shortName)


def getDirectoriesandSettings():
	xmldoc = minidom.parse('settings.xml')
	itemlist = xmldoc.getElementsByTagName('item')
	readDirectory = itemlist[0].attributes['locationToMoveFrom'].value
	movieDirectory = itemlist[1].attributes['locationToMoveMoviesTo'].value
	tVsDirectory = itemlist[2].attributes['locationToMoveTVTo'].value
	files = os.listdir(readDirectory)
	return readDirectory, movieDirectory, tVsDirectory, files

def tvRE(itemString):
    if re.match("(^[S][0-9][0-9][E][0-9][0-9])", itemString):
        return 1
    elif re.match("(^[S][0-9][E][0-9])", itemString):
        return 1
    elif re.match("(^[S][0-9][0-9][E][0-9])", itemString):
        return 1
    elif re.match("(^[S][0-9][E][0-9][0-9])", itemString):
        return 1
    elif re.match("(^[s][0-9][0-9][e][0-9][0-9])", itemString):
        return 1
    elif re.match("(^[s][0-9][e][0-9])", itemString):
        return 1
    elif re.match("(^[s][0-9][0-9][e][0-9])", itemString):
        return 1
    elif re.match("(^[s][0-9][e][0-9][0-9])", itemString):
        return 1


def main():
    cmdArgs = len(sys.argv)
    if (cmdArgs > 2):
        print("Command line arguement amount not accepted")
        print("\ML launches configuration mode")
        exit(2)
    elif(cmdArgs == 2):
        if (sys.argv[1] == "\ML"):
            print("Entered Machine learning mode.")
    else:
        rDirectory, mDirectory, tDirectory, files = getDirectoriesandSettings()
        getAllMP4(rDirectory, mDirectory, tDirectory, files)
	
main()