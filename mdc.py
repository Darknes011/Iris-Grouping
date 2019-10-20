'''
    ****main.py****
    
CSC 461 - Programming Languages - Fall 2017
Pattern Classification - MDC Method
Jeremy Goens
Tanner Holthus

This program will implement the use of a minimum distance classifier(MDC).
Given the name of an input file(.csv), the main program will get a list of 
data read from that csv file. Using this data, it will first find the centroids
for each classification given in the csv file. After finding the centroids, it 
will then use MDC to try and classify each of those points
'''
import sys
import fileIO
import dataProcessing

def CheckArgs(argv):
    if len(argv) != 2 or argv[1].endswith('.csv') == False:
        print("Incorrect Usage Used.\nCorrect Usage: mdc.py <.csv file>")
        return False;
    else:
        return True;
	
if __name__ == "__main__":
    if(CheckArgs(sys.argv)):
        info,data = fileIO.ReadInCSV(sys.argv[1])
        if(len(data) != 0):
            normalizedData = dataProcessing.normalizeData(data)
            countAccuracies,resultData = dataProcessing.calculateAccuracies(normalizedData,len(info[1]))
            fileNameLength = len(sys.argv[1]) - 4
            outputFile = sys.argv[1][:fileNameLength] + '.cv'
            fileIO.WriteDataToCV(info,countAccuracies,resultData,outputFile)
		
