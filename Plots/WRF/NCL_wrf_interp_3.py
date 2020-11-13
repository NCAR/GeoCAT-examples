
"""
NCL_WRF_interp_3.py
===================
This script illustrates the following concepts:
    - Interpolating a vertical cross-section from a 3D WRF-ARW field.
    - Recombining two datasets into one usable form
    - Following best practices when choosing a colormap.
      More information on colormap best practices can be found `here <https://geocat-examples.readthedocs.io/en/latest/gallery/Colors/CB_Temperature.html#sphx-glr-gallery-colors-cb-temperature-py>`_.
    
See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/wrf_interp_3.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/wrf_interp_3_lg.png
"""

###############################################################################
# Import packages

from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
import xarray as xr

from wrf import (to_np, getvar, CoordPair, vertcross, latlon_coords)
import geocat.datafiles as gdf
from geocat.viz import util as gvutil

###############################################################################
# Read in the data

# Specify the necessary variables needed from the data set in order to use 'z' and 'QVAPOR'
toinclude = ['PH', 'P', 'HGT', 'PHB', 'QVAPOR'] 
# Read in necessary datasets
ds = xr.open_mfdataset([gdf.get('netcdf_files/wrfout_d03_2012-04-22_23_00_00_Z.nc'), gdf.get('netcdf_files/wrfout_d03_2012-04-22_23_00_00_QV.nc')])

# specify a unique output file name to use to read in combined dataset later
file3 = 'wrfout_d03_2012-04-22_23.nc'
mrg = ds[toinclude].to_netcdf(file3)

# Read in the data and extract variables 
wrfin = Dataset(('wrfout_d03_2012-04-22_23.nc'))

z = getvar(wrfin, "z")
qv = getvar(wrfin, "QVAPOR")

# Pull lat/lon coords from QVAPOR data using wrf-python tools
lats, lons = latlon_coords(qv)

###############################################################################
# Create vertical cross section using wrf-python tools

# Define start and stop coordinates for cross section
start_point = CoordPair(lat=38, lon=-118)
end_point = CoordPair(lat=40, lon=-115)

qv_cross = vertcross(qv, 
                     z, 
                     wrfin=wrfin,
                     start_point=start_point, 
                     end_point=end_point,
                     latlon=True, 
                     meta=True)

# Close 'wrfin' to prevent PermissionError if code is run more than once locally
wrfin.close()
###############################################################################
# Plot the data

fig = plt.figure(figsize=(10,8))
ax = plt.axes()

qv_contours = ax.contourf(to_np(qv_cross), 
                          levels=17, 
                          cmap="magma",
                          vmin=0,
                          vmax=0.004,
                          zorder=4)


plt.colorbar(qv_contours, 
              ax=ax, 
              ticks=np.arange(0.00025, 0.004, .00025))

# Set the x-ticks to use latitude and longitude labels.
coord_pairs = to_np(qv_cross.coords["xy_loc"])
x_ticks = np.arange(coord_pairs.shape[0])
x_labels = [pair.latlon_str(fmt="{:.2f}\N{DEGREE SIGN}N, \n {:.2f}\N{DEGREE SIGN}E")
            for pair in to_np(coord_pairs)]
ax.set_xticks(x_ticks[::20])
ax.set_xticklabels(x_labels[::20], rotation=45, fontsize=8)

# Set the y-ticks to be height. (option 1)
vert_vals = to_np(qv_cross.coords["vertical"])
v_ticks = np.arange(vert_vals.shape[0])
# ax.set_yticks(v_ticks[::20])
# ax.set_yticklabels(vert_vals[::20], fontsize=8)

# Option 2
gvutil.set_axes_limits_and_ticks(ax,
                                 ylim=(0, np.nanmax(vert_vals)),
                                 yticks=np.linspace(0, 18000, 7))

# Option 3
# ax.set_yticks(np.arange(0,19000,3000))
# ax.set_yticklabels(np.arange(0,20000,3000), fontsize=8)

# Set the plot titles 
plt.title("Cross section from (38,-118) to (40,-115)", fontsize=16, y=1.07)
plt.title('Water vapor mixing ration', loc='left')
plt.title('kg kg-1', loc='right')

plt.show()

