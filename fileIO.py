'''
    ****fileIO.py****
Reads and writes to files. Will give error if io failed.
'''
import sys
import csv

def ReadInCSV(inputFile):
    '''Returns a csv input file read into two list of lists for MDC
        First list in return contains the file info such as class names and header.
        Second list in return contains the data.
    '''
    
    try:
        with open(inputFile) as fin:
            reader = csv.reader( fin )
            readerList = list(reader)
            info = list([readerList[0][0],readerList[0][1:],readerList[1]])
			
            for i in range(0,len(info[1])):
                info[1][i] = info[1][i][3:]
				
            data = list()
            for row in readerList[2:]:
                row[0] = int(row[0])
                row[1] = int(row[1])
                for columnNum in range(2,len(row)):
                    row[columnNum] = float(row[columnNum])
					
                data.append(row)
				
            return info,data
    except:
        print("Unable to read in file: " + inputFile)
        return list(),list()
        
def WriteDataToCV(info,accuracies,data,outputFile):
    '''Writes the info to console and a .cv output file, and data to the .cv output file'''
    
    try:
        with open(outputFile,'w') as fout:
            print(info[0])
            fout.write(info[0] + "\n")
			
            print("MDC Parameters:",end = " ")
            print("nclasses = " + str(len(info[1])) + ", nfeatures = " + str(len(info[2]) - 2) + ", nsamples = " + str(len(data)) )
			
            fout.write("MDC Parameters: ")
            fout.write("nclasses = " + str(len(info[1])) + ", nfeatures = " + str(len(info[2])) + ", nsamples = " + str(len(data)) + "\n" )

            numClasses = len(info[1])
			
            for i in range(numClasses):
                classAccuracy = round(accuracies[i][2],1)
                print("class " + str(i) + " (" + info[1][i] + ") : " + str(accuracies[i][0]) + " samples, " + str(classAccuracy) + "% accuracy")
                fout.write("class " + str(i) + " (" + info[1][i] + ") : " + str(accuracies[i][0]) + " samples, " + str(classAccuracy) + "% accuracy\n")
			
            overallAccuracy = round(accuracies[numClasses],1)
	
            print("overall: " + str(len(data)) + " samples, " + str(overallAccuracy) + "% accuracy\n")
            fout.write("overall: " + str(len(data)) + " samples, " + str(overallAccuracy) + "% accuracy\n\n")
			
            #data prints only to output file
            fout.write("Sample,Class,Predicted\n")
			
            for dataRow in data:
                fout.write(str(dataRow[0]) + "," + str(dataRow[1]) + "," + str(dataRow[2]))
                if dataRow[3] == '*':
                    fout.write(", " + dataRow[3])
                fout.write("\n")
			
    except:
        print("Failed to write data to file: " + outputFile)
		
