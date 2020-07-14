"""
NCL_xy_5.py
===============
This script illustrates the following concepts:
   - Draw multiple curves on an XY plot
   - Drawing a Y reference line in an XY plot
   - Filling the areas of an XY curve above and below a reference line
   - Using named colors to indicate a fill color
   - Creating array of dates to use as x-axis tick labels
   - Creating a main title
   - Setting the mininum/maximum value of the Y axis in an XY plot

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/xy_5.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/xy_5_1_lg.png
"""

###############################################################################
# Import packages:
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt

import geocat.datafiles as gdf
from geocat.viz import util as gvutil

###############################################################################
# Read in data:

# Open a netCDF data file using xarray default engine and load the data into xarrays
ds = xr.open_dataset(gdf.get("netcdf_files/soi.nc"))
dsoik = ds.DSOI_KET
dsoid = ds.DSOI_DEC
date = ds.date

# Creating a new array for x axis labels
datedim = np.shape(date)[0]
new_date = np.empty_like(date)
# Dates in the file are represented by year and month
# Create array that represents data by year and months as a fraction of a year
for n in np.arange(0, datedim, 1):
    yyyy = date[n]/100
    mon = date[n]-yyyy*100
    new_date[n] = yyyy + (mon-1)/12

###############################################################################
# Plot:

# Generate figure (set its size (width, height) in inches) and axes
plt.figure(figsize=(8, 4))
ax = plt.gca()

# Plot reference line
plt.plot([0, datedim], [0, 0], color='grey', linewidth=0.75)

# Plot data
# _labels=False prevents axis labels from being drawn
dsoik.plot.line(ax=ax, color='black', linewidth=0.5, _labels=False)
dsoid.plot.line(ax=ax, color='black', _labels=False)

# Fill above and below the 0 line
ax.fill_between(dsoik.time, dsoik, where=dsoik>0, color='red')
ax.fill_between(dsoik.time, dsoik, where=dsoik<0, color='blue')


# Use geocat.viz.util convenience function to add minor and major tick lines
gvutil.add_major_minor_ticks(ax, x_minor_per_major=4, y_minor_per_major=5, 
                             labelsize=14)

# Use geocat.viz.util convenience function to set axes parameters
gvutil.set_axes_limits_and_ticks(ax, ylim=(-3, 3), 
                                     yticks=np.linspace(-3, 3, 7),
                                     yticklabels=np.linspace(-3, 3, 7),
                                     xlim=(0, datedim),
                                     xticks=np.arange(0, datedim, 12*20),
                                     xticklabels=np.arange(1880, 1995, 20))

# Use geocat.viz.util convenience function to set titles and labels
gvutil.set_titles_and_labels(ax, maintitle="Darwin Southern Oscillation Index")

plt.show()
