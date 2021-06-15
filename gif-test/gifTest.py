import csv
import matplotlib.pyplot as plt
import imageio
import os

with open('prueba.csv') as csv_file:
    csv_file = csv.reader(csv_file, delimiter=',')

    #skips the header
    next(csv_file)
    
    dataVal = []
    for row in csv_file:
        dataVal.append(int(row[1]))

    filenames = []
    j = 0

    for i in dataVal:
        plt.plot(dataVal[:j])
        plt.ylim(min(dataVal)-(min(dataVal)*0.2), max(dataVal)+(max(dataVal)*0.2))

        filename = f'{j}.png'
        filenames.append(filename)

        plt.savefig(filename)
        plt.close()

        j += 1

    #print(filenames)
    
    with imageio.get_writer('mygif.gif', mode='I') as writer:
        for filename in filenames:
            print(filename)
            image = imageio.imread(filename)
            writer.append_data(image)

    #for filename in set(filenames):
        #os.remove(filename)
