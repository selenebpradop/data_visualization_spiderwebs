import csv
import matplotlib.pyplot as plt
import imageio
import os

with open('prueba.csv') as csv_file:
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

    with imageio.get_writer('mygif.gif', mode='I') as writer:
        # Generates a GIF using the filenames stores previusly
        for filename in filenames:
            image = imageio.imread(filename)
            writer.append_data(image)

    # Removes the PNG images tfrom the system
    for filename in set(filenames):
        os.remove(filename)
