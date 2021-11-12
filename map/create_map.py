from tkinter import *
from PIL import ImageTk, Image, ImageGrab
import numpy as np
import cv2
import time
import imageio


def draw_map(localizator, background, nameimages):

    '''

    Function that add images to a map
    and save the frames of the map with the new images to make a gif.

    Parameters
    ----------
    localizator: String
        String with the path of the image of the background with circles of size 15.
    background: String
        String with the path of the background image.
    nameimage: list
        A list with the path of the images to add to the map.

    '''

    # Set the tkinter for the canvas
    root = Tk() 
    root.title('Images over image tkinter canvas')
    root.resizable(width=False, height=False)
    root.geometry('+1200+750')
    root.geometry('1200x750')
    root.configure(bg='SystemButtonFace')
    # Set the background image
    myimg = Image.open(background)
    resized = myimg.resize((1330,1100), Image.ANTIALIAS)
    mymap = ImageTk.PhotoImage(resized)
    # Read the images ti add
    mapimages = []
    nimgs = len(nameimages)
    i = 0
    for i in range (nimgs):
        myimg = Image.open(nameimages[i]);
        resized = myimg.resize((50,50), Image.ANTIALIAS)
        myimageresized = ImageTk.PhotoImage(resized)
        mapimages.append(myimageresized)
        time.sleep(1)
    # Set the canvas with the background image
    canvas1 = Canvas(root, width=1000, height=1000)
    canvas1.pack()  
    background = canvas1.create_image(-170, -200, anchor=NW, image=mymap)
    # Detect where the images will be added
    image = cv2.imread(localizator)
    output = image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #detect circles in the image
    circles = cv2.HoughCircles(gray,
                               cv2.HOUGH_GRADIENT,
                               minDist=6,
                               dp=1.1,
                               param1=150,
                               param2=15,
                               minRadius=6,
                               maxRadius=8)
    # ensure at least some circles were found
    if circles is not None:
        # convert the (x, y) coordinates and radius of the circles to integers
        circles = np.round(circles[0, :]).astype("int")
    xmaps = []
    ymaps = []
    # loop over the (x, y) coordinates and radius of the circles
    for (x, y, r) in circles:
        xmaps.append(x)
        ymaps.append(y)
    ncoords = len(xmaps)
    
    nf = 0
    ni = 0
    stop = False
    imframes = []
    
    # Generation of the map
    while stop!=False:
        # Place the images in the frame
        i = 0
        canvasimages = []
        for i in range (ncoords):
            canvasimages.append(canvas1.create_image(xmaps[i], ymaps[i], anchor=NW, image=mapimages[ni]))
            ni = ni+1
        root.update_idletasks()
        root.update()
        # Save the frame in .png
        frameName = 'imap'+str(nf)+'.png'
        xc=root.winfo_rootx()+canvas1.winfo_x()
        yc=root.winfo_rooty()+canvas1.winfo_y()
        x1=xc+canvas1.winfo_width()
        y1=yc+canvas1.winfo_height()
        ImageGrab.grab((xc,yc,x1,y1)).save(frameName)
        # Prepare for the new frame
        time.sleep(1)
        i = 0
        for i in range (ncoords):
            canvas1.delete(canvasimages[i])
        nf=nf+1
        imframes.append(frameName)
        # Verify there are more images to add to a frame
        if ni==nimgs:
            stop=True
        if stop:
            # Generate the GIF
            with imageio.get_writer(title + '.gif', mode='I', duration=1) as writer:
                # Generates a GIF using the filenames stores previusly
                for filename in imframes:
                    image = imageio.imread(filename)
                    writer.append_data(image)
                for filename in set(imframes):
                    os.remove(filename)
            
    root.mainloop()
