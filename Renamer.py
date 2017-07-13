import logging
import re
import os
import string
import shutil
import sys
from xml.dom import minidom


def moveMovie(origName, readDirectory, movieDirectory, fileName):
    print("Is Movie")
    #shutil.move(readDirectory + fileName, movieDirectory + fileName)

def moveTVShow(origName, readDirectory, tVsDirectory, fileName , tvName, season):
    fileName = fileName + ".mp4"
    showDirectory = tVsDirectory + "/" + tvName
    seasonDirectory = showDirectory + "/" + "Season " + season
    while True:
        if os.path.isdir(tVsDirectory):
            if os.path.isdir(showDirectory):
                if os.path.isdir(seasonDirectory):
                    print("Moving File: " + fileName)
                    shutil.move(readDirectory + '/' + origName, seasonDirectory + '/' + fileName)
                    break
                else:
                    os.makedirs(seasonDirectory)
            else:
                os.makedirs(showDirectory)
        else:
            os.makedirs(tVsDirectory)

def getAllMP4(readDirectory, movieDirectory, tVsDirectory, files):
    for file in files:
        originalFile = file
        if file.endswith(".mp4"):
            file = file[:-4]															#removes file extension from list
            if '.' in file:																#If there are any periods in the title minus the extension
                file = file.replace(".", " ")											#remove period
            fileStringName = file.split()												#splits the string to look for movie or TV show
            length = len(fileStringName)
            newName, tvName, season = makeGoodName(file)
            tmp = newName.split()
            length = len(tmp)
            if tvRE(tmp[length - 1]) == 1:
                moveTVShow(originalFile, readDirectory, tVsDirectory, newName, tvName, season)
            else: 																			#Else if Movie
                moveMovie(originalFile, readDirectory, movieDirectory, newName)

def makeGoodName(file):
    #print("     Name Before: " + file)
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
    else:
        lengthToShorten = (len(fileStringName)- n-1)
        if lengthToShorten == 0:
            shortName = fileStringName
        else:
            shortName = fileStringName[:-lengthToShorten]
    tvName = ""
    for item in shortName[:-1]:
        tvName = tvName + item
        if item != shortName[-1]:
            tvName = tvName + " "
        #print("TV Show Name: " + tvName)
    newFileName = ""
    for element in shortName:
        newFileName = newFileName + element
        if element != shortName[-1]:
            newFileName = newFileName + " "
            #print(newFileName)
    season = shortName.pop()
    season = re.search('S(.*)E', season)
    #print("Season: " + season.group(1))
    #print("     Name After: " + newFileName)
    return newFileName, tvName.rstrip(), season.group(1)

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