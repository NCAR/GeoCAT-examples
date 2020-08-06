"""NCL_pdf_1.py===============This script illustrates the following concepts:   - Generating univariate probability distributions   - Generating PDFs of each sample distribution   - Paneling two plots horizontally on a pageSee following URLs to see the reproduced NCL plot & script:    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/pdf_1.ncl    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/pdf_1_lg.png"""################################################################################ Import packages:import numpy as npimport matplotlib.pyplot as pltfrom scipy import statsfrom geocat.viz import util as gvutil################################################################################ Generate univariate probability distributions:# Normal distribution################################################################################ Plot:# Set up figure using a subplot grid to create top centered plot# Having a 4x2 subplot grid and having each plot span 2 columns allows for the top# plot to span middle two columnsfig = plt.figure(figsize=(6,6))ax1 = plt.subplot2grid((2,4), (0,1), colspan=2)ax2 = plt.subplot2grid((2,4), (1,0), colspan=2)ax3 = plt.subplot2grid((2,4), (1,2), colspan=2)# Use the geocat.viz function to set the main title of the plotgvutil.set_titles_and_labels(ax1,                             maintitle='Univariate PDFs of Three Variables',                             maintitlefontsize=18,                             ylabel='PDF (%)',                             labelfontsize=12)plt.show()