import csv
import matplotlib.pyplot as plt
import cv2

with open('../gif-test/prueba.csv') as csv_file:
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


    img_array = []
    for filename in filenames:
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width,height)
        img_array.append(img)

    out = cv2.VideoWriter('project.avi',cv2.VideoWriter_fourcc(*'DIVX'), 15, size)

    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()
