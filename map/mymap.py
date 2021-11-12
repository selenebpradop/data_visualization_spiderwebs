import pandas as pd
import plotly
import plotly.graph_objects as go
import visualization_spiderwebs as vs
from create_map import draw_map
import time

def plot_map(day: str) -> None:

    '''

    Save two images of the day (day) selected:
    1. Image of the map.
    2. Image of the map with circles of size 15 in the stations.
    
    '''

    
    # Read the station coordinates
    coords = pd.read_csv('coords.csv')

    frames, frames1 = [], []

    xcoords, ycoords, zcoords = coords.lon, coords.lat, coords.station
    
    # Set the frames of the 1st image
    frames.append({
        'name': day,
        'data': [
            dict(
                type='scattermapbox',
                lon=xcoords,
                lat=ycoords,
                mode='text',
                marker=dict(
                    symbol='circle',
                    size=15,
                    allowoverlap=True,
                    color='rgb(255, 0, 0)',
                    cmin=0,
                    cmax=0,
                    autocolorscale=True,
                    ),
            )
        ]
    })
    
    # Set the frames of the 2nd image
    frames1.append({
        'name': day,
        'data': [
            dict(
                type='scattermapbox',
                lon=xcoords,
                lat=ycoords,
                mode='markers',
                marker=dict(
                    symbol='circle',
                    size=15,
                    allowoverlap=True,
                    color='rgb(255, 0, 0)',
                    cmin=0,
                    cmax=60,
                    autocolorscale=True,
                    ),
                text = zcoords
            )
        ]
    })  
    
    with open('mytoken.txt', 'r') as file:
        token = file.read()

    layout = go.Layout(
        autosize=True,
        mapbox=dict(
            accesstoken=token,
            center=dict(lat=25.56, lon=-100.338),
            zoom=8.4, 
        )
    )

    data = frames[0]['data']
    data1 = frames1[0]['data']

    # Create the figures    
    figure = go.Figure(data=data, layout=layout, frames=frames)
    figure1 = go.Figure(data=data1, layout=layout, frames=frames1)

    # Save the images from the figures
    figure.write_image("map.png")
    figure1.write_image("map_x.png")


def call_spiderwebs(day: str) -> None:
    '''
    Call function that create the spiderwebs
    '''

    # Colums to extract from the CSV
    columns1 = ['timestamp', 'station', 'PM2_5', 'velocity', 'direction']
    dataframe1 = pd.read_csv('filled.csv', usecols=columns1).dropna()
    columns2 = ['timestamp', 'station', 'PM10', 'velocity', 'direction']
    dataframe2 = pd.read_csv('filled.csv', usecols=columns2).dropna()
    columns3 = ['timestamp', 'station', 'NOX', 'velocity', 'direction']
    dataframe3 = pd.read_csv('filled.csv', usecols=columns3).dropna()
    columns4 = ['timestamp', 'station', 'NO2', 'velocity', 'direction']
    dataframe4 = pd.read_csv('filled.csv', usecols=columns4).dropna()
    
    # Read the station coordinates
    coords = pd.read_csv('coords.csv')

    # Filter the records of the day selected
    dataset1 = coords.merge(dataframe1.loc[dataframe1['timestamp'].str.startswith(day)], on='station')
    dataset2 = coords.merge(dataframe2.loc[dataframe2['timestamp'].str.startswith(day)], on='station')
    dataset3 = coords.merge(dataframe3.loc[dataframe3['timestamp'].str.startswith(day)], on='station')
    dataset4 = coords.merge(dataframe4.loc[dataframe4['timestamp'].str.startswith(day)], on='station')

    # Convert strings variables to datetime variables
    strfdt = '%d-%b-%y %H'
    dataset1['timestamp'] = pd.to_datetime(dataset1['timestamp'], format=strfdt)
    dataset2['timestamp'] = pd.to_datetime(dataset2['timestamp'], format=strfdt)
    dataset3['timestamp'] = pd.to_datetime(dataset3['timestamp'], format=strfdt)
    dataset4['timestamp'] = pd.to_datetime(dataset4['timestamp'], format=strfdt)
    

    # Filter all the hours registered in the day selected
    hours1 = dataset1.timestamp.unique()
    hours1.sort()
    hours2 = dataset2.timestamp.unique()
    hours2.sort()
    hours3 = dataset3.timestamp.unique()
    hours3.sort()
    hours4 = dataset4.timestamp.unique()
    hours4.sort()
    hours = []
    # Verify hours in common
    for i in hours1:
        if (i not in hours) and (i in hours2) and (i in hours3) and (i in hours4):
            hours.append(i)
    h=0
    nameimages=[]
    for hour in hours:
        titles = []
        mydataset = []
        # Select the records of the hour
        data1 = dataset1.loc[dataset1['timestamp'] == hour]
        data2 = dataset2.loc[dataset2['timestamp'] == hour]
        data3 = dataset3.loc[dataset3['timestamp'] == hour]
        data4 = dataset4.loc[dataset4['timestamp'] == hour]

        # Organize by station
        xcoords, ycoords = coords.lon, coords.lat        

        mydataset1 = []
        mydataset2 = []
        mydataset3 = []
        mydataset4 = []
        for st in coords.station:
            station = str(st)
            titles.append(station)
            mydata1 = data1.loc[data1['station'] == station]
            mydata2 = data2.loc[data2['station'] == station]
            mydata3 = data3.loc[data3['station'] == station]
            mydata4 = data4.loc[data4['station'] == station]

            verify1 = len(mydata1)
            verify2 = len(mydata2)
            verify3 = len(mydata3)
            verify4 = len(mydata4)
            if(verify1==0):
                mydataset1.append(0)
            if(verify2==0):
                mydataset2.append(0)
            if(verify3==0):
                mydataset3.append(0)
            if(verify4==0):
                mydataset4.append(0)
        
            for x in mydata1.PM2_5:
                mydataset1.append(x)
            for x in mydata2.PM10:
                mydataset2.append(x)
            for x in mydata3.NOX:
                mydataset3.append(x)
            for x in mydata4.NO2:
                mydataset4.append(x)
        mydataset.append(mydataset1)
        mydataset.append(mydataset2)
        mydataset.append(mydataset3)
        mydataset.append(mydataset4)
        h=h+1
        total = len(titles)
        title = 'hour'+str(h)+'_'
        nstations = len(coords)
        for s in range(nstations):
            nn=s+1
            nameimages.append(title+str(nn)+'.png')
        spoke_labels = ['PM2,5','PM10','NOX','NO2']
        colors = ['b', 'r', 'g', 'm', 'y']
        nc = len(colors)
        mycolors = []
        c = 0
        for i in range(total):
            mycolors.append(colors[c])
            c = c+1
            if c >= nc:
                c = 0
        vs.create_spiderwebs(mydataset, 4, total, title, titles, spoke_labels, mycolors, 'polygon')
    time.sleep(5)
    draw_map('map_x.png', 'map.png', nameimages)
