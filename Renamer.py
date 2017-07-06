import logging
import re
import glob
import os
import string
import shutil

tVShowDirectory = 'D:\TransferTV'
movieDirectory = 'D:\Transfer'
readDirectory = 'C:\\Users\\Admin\\Desktop'
TVString = 'S**E**'
files = os.listdir(readDirectory)

#print(files)




def moveMovie(fileName):
	print("Is Movie")
	shutil.move(readDirectory + fileName, movieDirectory + fileName)

def tvShow():
	print("Is TVshow")

def main():
	for file in files:
		if file.endswith(".mp4"):
			file = file[:-4]				#removes file extension from list
			fileStringName = file.split()	#splits the string to look for movie or TV show	
			print (fileStringName)			#print the list		
			if re.match("(^[A-Z]\d[A-Z]\d", fileStringName[-1]):
				print("It worked")
			else: #Movie
				moveMovie(file)

main()