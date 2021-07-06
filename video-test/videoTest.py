import csv
import matplotlib.pyplot as plt
import cv2
import os

with open('../gif-test/prueba.csv') as csv_file:
    csv_file = csv.reader(csv_file, delimiter=',')

    #skips the header
    next(csv_file)

    '''
    windowLength, t0, tn are parameters given by the user.
    add boolean to switch between GIF and Video generation.
    TODO: create a function that generates either a GIF or video.
    '''
    windowLength = 5
    t0 = 2
    tn = 30
    dataY = []
    dataX = []

    #Stores the data from the csv as X and Y values
    for row in csv_file:
        dataY.append(int(row[1]))
        dataX.append(int(row[0]))

    filenames = []
    j = 1

    xMin = min(dataX)
    xMax = max(dataX)
    counter = 0
    xInit = t0
    xLimit = xInit + windowLength
    dataNumber = t0 + 1

    for i in range(t0, tn+1):

        if counter >= windowLength:
            xInit += 1
            xLimit += 1

        plt.plot(dataY[:dataNumber])
        plt.ylim(min(dataY)-(min(dataY)*0.2), max(dataY)+(max(dataY)*0.2))
        plt.xlim(xInit, xLimit)

        #stores filename with the corresponding numbers
        filename = f'{j}.png'
        filenames.append(filename)

        #saves the plot into an png file.
        plt.savefig(filename)
        plt.close()

        dataNumber += 1
        counter += 1
        j += 1


    img_array = []
    for filename in filenames:
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width,height)
        img_array.append(img)

    out = cv2.VideoWriter('project.avi',cv2.VideoWriter_fourcc(*'DIVX'), 5, size)

    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()

    # Removes the PNG images tfrom the system
    for filename in set(filenames):
        os.remove(filename)
