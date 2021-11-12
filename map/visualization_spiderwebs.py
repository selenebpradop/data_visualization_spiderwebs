# Import the libraries
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, RegularPolygon
from matplotlib.path import Path
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D
import time

def radar_factory(num_vars, frame='circle'):
    """
    Create a radar chart with `num_vars` axes.

    This function creates a RadarAxes projection and registers it.

    Parameters
    ----------
    num_vars : int
        Number of variables for radar chart.
    frame : {'circle', 'polygon'}
        Shape of frame surrounding axes.

    """
    # Calculate evenly-spaced axis angles
    theta = np.linspace(0, 2*np.pi, num_vars, endpoint=False)

    class RadarAxes(PolarAxes):

        name = 'radar'
        # Use 1 line segment to connect specified points
        RESOLUTION = 1

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # Rotate plot such that the first axis is at the top
            self.set_theta_zero_location('N')

        def fill(self, *args, closed=True, **kwargs):
            """Override fill so that line is closed by default"""
            return super().fill(closed=closed, *args, **kwargs)

        def plot(self, *args, **kwargs):
            """Override plot so that line is closed by default"""
            lines = super().plot(*args, **kwargs)
            for line in lines:
                self._close_line(line)

        def _close_line(self, line):
            x, y = line.get_data()
            # FIXME: markers at x[0], y[0] get doubled-up
            if x[0] != x[-1]:
                x = np.append(x, x[0])
                y = np.append(y, y[0])
                line.set_data(x, y)

        def set_varlabels(self, labels):
            self.set_thetagrids(np.degrees(theta), labels)

        def _gen_axes_patch(self):
            # The Axes patch must be centered at (0.5, 0.5) and of radius 0.5 in axes coordinates.
            if frame == 'circle':
                return Circle((0.5, 0.5), 0.5)
            elif frame == 'polygon':
                return RegularPolygon((0.5, 0.5), num_vars,
                                      radius=.5, edgecolor="k")
            else:
                raise ValueError("Unknown value for 'frame': %s" % frame)

        def _gen_axes_spines(self):
            if frame == 'circle':
                return super()._gen_axes_spines()
            elif frame == 'polygon':
                # spine_type must be 'left'/'right'/'top'/'bottom'/'circle'.
                spine = Spine(axes=self,
                              spine_type='circle',
                              path=Path.unit_regular_polygon(num_vars))
                # unit_regular_polygon gives a polygon of radius 1 centered at
                # (0, 0) but we want a polygon of radius 0.5 centered at (0.5,
                # 0.5) in axes coordinates.
                spine.set_transform(Affine2D().scale(.5).translate(.5, .5)
                                    + self.transAxes)
                return {'polar': spine}
            else:
                raise ValueError("Unknown value for 'frame': %s" % frame)

    register_projection(RadarAxes)
    return theta


def create_spiderwebs(datasets, lenlines, numspiders, title, titles, spoke_labels, colors, typeframe):

    """
    Create a radar chart.

    This function receives parameters and with that a radar chart is created.

    Parameters
    ----------
    datasets: list
        A list that contains one list for each dataset.
    lenlines: int
        The length of the lines of the spiderweb.
    numspiders: int
        The number of spiderwebs to create.
    title: String
        The title of the figure.
    titles: list
        A list with the names of each spiderweb.
    spoke_labels: list
        A list with the names of each line of the spiderweb.
    colors: list    
        A list with the first letter of the color of each spiderweb [{'b', 'r', 'g', 'm', 'y'}].
    typeframe: {'circle', 'polygon'}
        A string with the name of the type of the Frame for the spiderwebs.
    """

    # Validate the parameters recibed
    allvalid = True
    if not(isinstance(datasets, list)):
        print('Please enter a valid list with each dataset. Now is: ' + str(type(datasets)))
        allvalid = False
    elif not(isinstance(lenlines, int)):
        print('Please enter a valid integer number for the length of the lines of the spiderwebs.')
        allvalid = False
    elif(lenlines<=0 or lenlines>50):
        print('Please enter a valid integer number for the length of the lines of the spider (Greater than 0 and less than 50).')
        allvalid = False
    elif not (isinstance(numspiders, int)):
        print('Please enter a valid integer number for the number of spiderwebs to create.')
        allvalid = False
    elif(numspiders<=0 or numspiders>400):
        print('Please enter a valid integer number for the number of spiderwebs to create (Greater than 0 and less than 400).')
        allvalid = False
    elif not (isinstance(title, str)):
        print('Please enter a valid string for the title of the figure.')
        allvalid = False
    elif not (isinstance(titles, list)):
        print('Please enter a valid list with the name of each spiderweb. Now is: ' + str(type(titles)))
        allvalid = False
    elif (len(titles)!=numspiders):
        print('Please enter a valid list with the name of each spiderweb. Now number of spiderwebs is different of the quantity of names.')
        allvalid = False
    elif not (isinstance(spoke_labels, list)):
        print('Please enter a valid list with the name of each line in the spiderweb. Now is: ' + str(type(spoke_labels)))
        allvalid = False
    elif (len(spoke_labels)!=len(datasets)):
        print('Please enter a valid list with the name of each line in the spiderweb. Now number of lines is different of the quantity of names.')
        allvalid = False
    elif not (isinstance(colors, list)):
        print("Please enter a valid list with the first letter of the color of each spiderweb [{'b', 'r', 'g', 'm', 'y'}]")
        allvalid = False
    elif (len(colors)!=numspiders):
        print("Please enter a valid list with the first letter of the color of each spiderweb [{'b', 'r', 'g', 'm', 'y'}]. Now number of spiderwebs is different of the quantity of colors.")
        allvalid = False
    else:
        for vcolor in colors:
            if not(vcolor=='b' or vcolor=='r' or vcolor=='g' or vcolor=='m' or vcolor=='y'):
                print("Please enter a valid list with the first letter of the color of each spiderweb [{'b', 'r', 'g', 'm', 'y'}]")
                allvalid = False
        if(typeframe!='circle' and typeframe!='polygon'):
            print("Please enter a valid string with the name of the type of the Frame for the spiderwebs. {'circle', 'polygon'}")
            allvalid = False


    if(allvalid):

        # Set the number of lines of each spiderweb
        N = len(datasets)
        theta = radar_factory(N, frame=typeframe)

        # Counter of the number of spiders
        i=0
        filenames = []
    
        # Plot each case on separate axes
        for titlespiderweb in titles:
            # Draw the shape of the spiderweb
            fig, axs = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='radar'))
            fig.subplots_adjust(wspace=0.5, hspace=0.20, top=0.85, bottom=0.05)
            newn = 0.5
            ax = axs
            # Put labels in the lines
            ax.set_title(titlespiderweb, weight='bold', size='medium', position=(0.5, 1.1), horizontalalignment='center', verticalalignment='center')
            dataspider = []
            # Normalize data
            for y in range(N):
                currentdata = datasets[y]
                number = currentdata[i]
                nmin = min(currentdata);
                nmax = max(currentdata);
                r = nmax - nmin
                x = (number-nmin)/r
                y = lenlines*x
                dataspider.append(y)
            # Draw the new lines in the spiderweb
            ax.plot(theta, dataspider, color=colors[i])
            ax.fill(theta, dataspider, facecolor=colors[i], alpha=0.25)
            # Put the name of each line in the figure
            ax.set_varlabels(spoke_labels)
            # Increment the counter
            i=i+1

            # Name of the image
            filename = title + str(i) + '.png'
            filenames.append(filename)
            # Save the figure in an image with .png format
            plt.savefig(filename, format='png', transparent=True)
            time.sleep(1)
