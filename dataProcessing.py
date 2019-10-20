# dataProcessing.py
# Function Description
# CSC461 Programming Languages, Fall 2017
# Tanner Holthus, Jeremy Goens
import math

def normalizeData(data):
    ''' Given a list of data, will return a normalized version of that data
    Normalizing for each column of data is done by (value - min)/(max-min)
    '''
    #transpose data list to make it easier to work with
    dataT = list(map(list,zip(*data)))
	
    #skip first two rows, those rows are identifiers not data
    for row in dataT[2:]:
        maxNum = max(row)
        minNum = min(row)
		
        for columnNum in range(len(row)):
            row[columnNum] = (row[columnNum] - minNum) / (maxNum - minNum)
			
    #return transposed data back to original state
    returnData = list(map(list,zip(*dataT)))
    return returnData

def getClassCount(data,numClasses):
    classCount = list()
    
    for i in range(numClasses):
        classCount.append(0)

    for row in data:
        classCount[row[1]] += 1

    return classCount

    
def getFeatureTotals(oneOutData,numClasses):
    #The first few lines of code sets up a 2d array to hold
    #the centroids for each part of a flower/dataset and stores
    #them depending on what they are classified as	
    centroidList = list()
    countList = list()
    numFeatures = (len(oneOutData[0]))-2
    sizeCount = numFeatures*numClasses

    for i in range(sizeCount):
        centroidList.append(0.0)
    for j in range(numClasses):
        countList.append(0)

    dataLength = len(oneOutData)	

    #Walks through collecting the data for the entire group 
    for i in range(dataLength):
        classification = oneOutData[i][1]
        countList[classification]+=1

        #classification works
        for j in range(numFeatures):
            centroidList[(classification*numFeatures) + j] += oneOutData[i][j+2]

    return centroidList

def getCentroids(centroidList,numClasses,countList):
    numFeatures = int(len(centroidList) / numClasses)
    
    #Averages the centroids across the entire range
    for i in range(numFeatures):
        for j in range(numClasses):
            if countList[j] != 0:
                centroidList[(j*numFeatures)+i] = ((centroidList[(j*numFeatures)+i])/ (countList[j]))
            else:
                #tells us that this class had no samples in it.
                centroidList[(j*numFeatures)+i] = 100
                

    return centroidList

def classifyRow(sampleData,centroidList,numClasses):
    handledData = sampleData[2:]
    size = len(handledData)
    classification = 0
    distance = 0
    baseDistance = 100000.0

    #Walks through the two arrays and if the distance to one average is 
    #closer, it changes the classification to that order
    for i in range(numClasses):
        if centroidList[i*size] != 100:
            caseStudy = centroidList[(i*size):((i*size)+size+1)]
            distance = shortDistance(handledData, caseStudy)

            if distance < baseDistance:
                classification = i
                baseDistance = distance

    return classification

#calculates shortest distance function
def shortDistance(pList,qList):
    dist = 0.0
    length = len(pList)

    for i in range(length):
        dist += ((pList[i]-qList[i]) * (pList[i]-qList[i]))

    dist = math.sqrt(dist)
    return dist

def calculateAccuracies(sampleData,numClasses):
    #initialize list that stores the count of samples for a class,
    #correctly identified samples for that class,
    #and that class's accuracy
    #last item in the list is the overall accuracy
    countAccuracies = list()
    resultData = list()
    correctNum = 0.0

    classCount = getClassCount(sampleData,numClasses)
    
    for ix in range(numClasses):
        countAccuracies.append([classCount[ix],0,0.0])

    countAccuracies.append(0.0)

    #iterate through each row in the data list
    #find centroids for data without using that row
    #see if row is where it should be	
    dataLen = len(sampleData)

    sampleFeatureTotals = getFeatureTotals(sampleData,numClasses)
    
    for rowNum in range(dataLen):
        row = sampleData[rowNum]
        numFeatures = len(row) - 2
        #Input for number testing, throwing the wrong numbers
        #print("Starting new line: \n \n \n")
        oneOutData = sampleData[:]

        rowClassNum = row[1]
        
        del oneOutData[rowNum]

        #Finds the centroid and calculates the class based on the centroid
        #classCentroids = getCentroids(oneOutData,numClasses)
        classFeatureTotals = sampleFeatureTotals[:]
      
        for fx in range(numFeatures): 
            classFeatureTotals[row[1]*numFeatures + fx] = classFeatureTotals[row[1]*numFeatures + fx] - row[fx + 2]
        
        #remove one from class count that row belongs to
        classCount[row[1]] -= 1        

        classCentroids = getCentroids(classFeatureTotals,numClasses,classCount)

        #replace class count now that average is done for that class
        classCount[row[1]] += 1

        rowClassifyNum = classifyRow(row,classCentroids,numClasses)

        if rowClassifyNum != row[1]:
            resultData.append([row[0],row[1],rowClassifyNum,'*'])
        else:
            correctNum += 1
            countAccuracies[rowClassNum][1] += 1
            resultData.append([row[0],row[1],rowClassifyNum,''])

    for ix in range(numClasses):
        classTotalCount = float(countAccuracies[ix][0])
        classCorrectCount = float(countAccuracies[ix][1])

	#Calculates accuracy. If 0, we report 0 without float error
        if classTotalCount == 0:
            countAccuracies[ix][2] = 0
        else:
            countAccuracies[ix][2] = 100 * classCorrectCount / classTotalCount

    if dataLen != 0:
        countAccuracies[numClasses] = 100 * correctNum / dataLen
    else:
        countAccuracies[numClasses] = 100	
	
    return countAccuracies,resultData
