# Jupyter interactive notebook (Python v3.x)
#
# - Download CO2 data from MG's GitHub repository
# - Perform exloratory data analysis, with commentary

import pycurl
try:
    import certifi
    https = 1
except ImportError:
    https = 0
import glob
import numpy
import matplotlib.pyplot

# Function to download a specified URL to a file (data files, web pages, etc.)
#
def get_file(url,fname):
    print('Downloading %s' % fname)
    print('from %s' % url)
    c = pycurl.Curl()
    f = open(fname,'wb')
    if https:
        c.setopt(pycurl.CAINFO, certifi.where())
        print('- Using http-secure transfer protocol')
    else:
        c.setopt(pycurl.SSL_VERIFYPEER, 0)
        c.setopt(pycurl.SSL_VERIFYHOST, 0)
        print('- Using unsecure http transfer protocol')
    c.setopt(c.URL, url)
    c.setopt(c.WRITEDATA, f)
    c.perform()
    responsecode = c.getinfo(c.RESPONSE_CODE)
    if responsecode == 200:
        print('- Status: OK')
        print('- Elapsed time: %f sec' % c.getinfo(c.TOTAL_TIME))
    else:
        print('- Status: ERROR, response code %d' % responsecode)
    c.close()
    print(' ')
    return

# Download data from MG's GitHub repository (calls the "get_file" function)
#
base_url = 'https://raw.githubusercontent.com/megarcia/SWC_Python/master/'
file_names = ['MaunaLoa_CO2_monthly_filled_1959-1975.csv',
              'MaunaLoa_CO2_monthly_filled_1976-2000.csv',
              'MaunaLoa_CO2_monthly_filled_2001-2015.csv']
for fname in file_names:
    url = base_url + fname
    get_file(url,fname)

# Read the csv data files into an array
#
filelist = sorted(glob.glob('MaunaLoa_*.csv'))
data1 = numpy.loadtxt(fname=filelist[0],delimiter=',')
all_data = numpy.copy(data1)
for filename in filelist[1:]:
    new_data = numpy.loadtxt(fname=filename,delimiter=',')
    all_data = numpy.append(all_data, new_data, axis=0)

# Slice the measurement values from the data array
#
CO2_vals = all_data[:,2]

# Get some parameters to label the plots correctly
#
nmonths = numpy.shape(CO2_vals)[0]
nyears = int(nmonths / 12)

# From looking at the full data array, we know that the time series starts in 1959 and 
#     ends at the end of 2015. For plotting, it would be nice to put those dates on the 
#     x-axis. The function to make those x-axis locations is stored in a variable for 
#     passing to the plot.
#
# The length of this array must match the length of our time series variable array.
#
x = numpy.linspace(1959,2016,nmonths)

# Generate our 1st plot from the dataset
#
matplotlib.pyplot.figure()
matplotlib.pyplot.plot(x, CO2_vals)
matplotlib.pyplot.xlabel('Year')
matplotlib.pyplot.ylabel('CO2 [ppm]')
matplotlib.pyplot.title('Mauna Loa CO2 Observations, 1959-2015')
#
# Un-comment this show() line to show the plot on your screen instead of going right to
#     saving it. This will probably pause the script until you close that pop-up window.
#
# matplotlib.pyplot.show()

# Save the plot to a png file
#
plotfname = 'analysis_Keeling_Curve.png'
print('saving figure as %s' % plotfname)
matplotlib.pyplot.savefig(plotfname, dpi=300)

# It's the Keeling Curve! 
#     See http://scrippsco2.ucsd.edu/
#     and http://en.wikipedia.org/wiki/Keeling_Curve
#
# There are two things about this plot that we'll explore further:
#     1. the seasonal variation
#     2. the annual trend
#
# Instead of finding a new dataset in the right shape, we can use what we already have 
#     and "reshape" it. We want an array that has each year in a row and each month in a 
#     column. You'll see why in a few more lines. The "reshape" command takes our 1-D list
#     of values and converts it into a 2-D array (as used here). The value of rows * columns
#     in the 2-D array must be the same as the number of items in the 1-D array, or else
#     Python will give us an error regarding the array dimensions.
#
data_arr = CO2_vals.reshape(nyears,12)

# To look at the seasonal variation, we want a value for each month that is the average 
#     over all years. That means we're averaging over axis 0.
#
seasonal = numpy.mean(data_arr, axis=0)

# Create a variable to help labeling the months on the x-axis
#
x = numpy.linspace(1,12,12)

# Make a plot of these monthly averages
#
matplotlib.pyplot.figure()
matplotlib.pyplot.plot(x, seasonal)
matplotlib.pyplot.xlabel('Month')
matplotlib.pyplot.ylabel('mean CO2 for 1959-2015 [ppm]')
matplotlib.pyplot.title('Mauna Loa CO2 Observations')

# Un-comment this show() line to show the plot on your screen instead of going right to
#     saving it. This will probably pause the script until you close that pop-up window.
#
# matplotlib.pyplot.show()

# Save the plot to a png file
#
plotfname = 'analysis_Keeling_Curve_monthly_mean.png'
print('saving figure as %s' % plotfname)
matplotlib.pyplot.savefig(plotfname, dpi=300)

# Note that these plotted values include the mean over all of the years. We can subtract 
#     that out to get an idea of the variation within any single year.
#
mean = numpy.mean(seasonal)
seasonal_adj = seasonal - mean

# Make a plot of these adjusted monthly averages
#
matplotlib.pyplot.figure()
matplotlib.pyplot.plot(x, seasonal_adj)
matplotlib.pyplot.xlabel('Month')
matplotlib.pyplot.ylabel('CO2 [ppm] relative to 1959-2015 mean')
matplotlib.pyplot.title('Mauna Loa CO2 Observations')

# Un-comment this show() line to show the plot on your screen instead of going right to
#     saving it. This will probably pause the script until you close that pop-up window.
#
# matplotlib.pyplot.show()

# Save the plot to a png file
#
plotfname = 'analysis_Keeling_Curve_monthly_adjusted.png'
print('saving figure as %s' % plotfname)
matplotlib.pyplot.savefig(plotfname, dpi=300)

# Notice the CO2 concentration decreases between late Spring and early Autumn (in the 
#     Northern Hemisphere). There is more land area in the NH, and all that plant growth 
#     is drawing CO2 from the atmosphere. At other times, plant respiration, cement 
#     production, and fossil fuels cause a net increase in CO2 concentration.
#
# The Earth breathes!
#
# Watch: 
# http://1.bp.blogspot.com/-LemiCA8B_H4/UfLN63QLXdI/AAAAAAAACyM/Xc3HtckubEg/s640/Animated.gif
# http://www.jpl.nasa.gov/video/details.php?id=1163
#
# To look at the annual variation, we want the mean values over all months for each year. 
#     That means that we can use the same data array, but average over axis 1 this time.
#
annual = numpy.mean(data_arr, axis=1)

# Create a variable to label the years on the x-axis
#
x = numpy.linspace(1959,2015,nyears)

# Make a plot of these annual averages
#
matplotlib.pyplot.figure()
matplotlib.pyplot.plot(x, annual)
matplotlib.pyplot.xlabel('Year')
matplotlib.pyplot.ylabel('annual mean CO2 [ppm]')
matplotlib.pyplot.title('Mauna Loa CO2 Observations, 1959-2015')

# Un-comment this show() line to show the plot on your screen instead of going right to
#     saving it. This will probably pause the script until you close that pop-up window.
#
# matplotlib.pyplot.show()

# Save the plot to a png file
#
plotfname = 'analysis_Keeling_Curve_annual_mean.png'
print('saving figure as %s' % plotfname)
matplotlib.pyplot.savefig(plotfname, dpi=300)

# Notice there are a couple of times when the trend gets shallow:
# early 1970s: Inflation, oil crisis (possibly)
# early 1990s: Mount Pinatubo eruption in 1991 (cooler summers, less energy use)
#
# Notice also the most recent milestone: graph crosses 400 ppm in 2015!
#
# You've just done some exploratory data analysis!
#
# You deserve a final treat! 
#
import antigravity
