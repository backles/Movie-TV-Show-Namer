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

def tvShow(readDirectory, tVsDirectoryDirectory, fileName):
	print("Is TVshow")
	#shutil.move(readDirectory + fileName, movieDirectory + fileName)
	
def getAllMP4(readDirectory, movieDirectory, tVsDirectory, files):
	for file in files:
		originalFile = file
		if file.endswith(".mp4"):
			file = file[:-4]															#removes file extension from list
			if '.' in file:																#If there are any periods in the title minus the extension
				file = file.replace(".", " ")											#remove periods
			fileStringName = file.split()												#splits the string to look for movie or TV show	
			length = len(fileStringName)
			if re.match("(^[A-Z][0-9][0-9][A-Z][0-9][0-9])", fileStringName[length-1]):
				tvShow(readDirectory, tVsDirectory, originalFile)
			elif re.match("(^[A-Z][0-9][A-Z][0-9])", fileStringName[length-1]):
				tvShow(readDirectory, tVsDirectory, originalFile)
			elif re.match("(^[A-Z][0-9][0-9][A-Z][0-9])", fileStringName[length-1]):
				tvShow(readDirectory, tVsDirectory, originalFile)
			elif re.match("(^[A-Z][0-9][A-Z][0-9][0-9])", fileStringName[length-1]):
				tvShow(readDirectory, tVsDirectory, originalFile)
			elif re.match("(^[a-z][0-9][0-9][a-z][0-9][0-9])", fileStringName[length-1]):
				tvShow(readDirectory, tVsDirectory, originalFile)
			elif re.match("(^[a-z][0-9][a-z][0-9])", fileStringName[length-1]):
				tvShow(readDirectory, tVsDirectory, originalFile)
			elif re.match("(^[a-z][0-9][0-9][a-z][0-9])", fileStringName[length-1]):				
				tvShow(readDirectory, tVsDirectory, originalFile)
			elif re.match("(^[a-z][0-9][a-z][0-9][0-9])", fileStringName[length-1]):
				tvShow(readDirectory, tVsDirectory, originalFile)
			else: 																			#Else if Movie
				moveMovie(readDirectory, moveMovie, originalFile)

def getDirectoriesandSettings():
	xmldoc = minidom.parse('settings.xml')
	itemlist = xmldoc.getElementsByTagName('item')
	readDirectory = itemlist[0].attributes['locationToMoveFrom'].value
	movieDirectory = itemlist[1].attributes['locationToMoveMoviesTo'].value
	tVsDirectory = itemlist[2].attributes['locationToMoveTVTo'].value
	files = os.listdir(readDirectory)
	return readDirectory, movieDirectory, tVsDirectory, files
	
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