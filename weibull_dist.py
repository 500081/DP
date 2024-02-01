# code to estimate the parameters of the Weibull distribution with the function exponweib.fit

import numpy as np
from scipy.stats import exponweib
import matplotlib.pyplot as plt
import pandas as pd
import os

# files folder
#directory_path = 'C:\\Users\\user\\Documents\\Barbora\\data1.1'
#directory_path = 'C:\\Users\\user\\Documents\\Barbora\\data1.2'
directory_path = 'C:\\Users\\user\\Documents\\Barbora\\data1.3'
#df = pd.read_pickle('C:\\Users\\user\\Documents\\Barbora\\data1.2\\MSEL_00452_1_1_UFO.pkl')    #single file


# we go through every file in the folder
for filename in os.listdir(directory_path):
    if filename.endswith('.pkl'):  # .pkl files filter
        file_path = os.path.join(directory_path, filename)
        df = pd.read_pickle(file_path) # loading data


        channels = df.channel.unique()  # list of channels on which there is some detection
        distance = pd.Series()  #empty series
        pistol_distance = pd.Series()
        blob_distance = pd.Series()
        erase_distance = pd.Series()


        # counting of distance between detections
        # through individual channels, but for the entire electrode together
        for channel in channels[[x[1:6] !="Macro" for x in channels]]:
            df_chan = df[(df.channel == channel) & (df.osc_type_2 == 'clear')]
            distance1 = df_chan.start_time.shift(-1) - df_chan.end_time
            distance = pd.concat([distance.dropna(), distance1.dropna()], ignore_index=True)

        # outlier removal by rule > 3*quantile(0.75) and also the value less than or equal to zero
        nonoutlier_dist = distance[(distance < 3 * (np.percentile(distance, 75))) & (distance > 0)]

        # Fit the Weibull distribution to the data
        params = exponweib.fit(nonoutlier_dist, floc=0, fa=1)

        # Extract the estimated parameters
        est_shape, est_scale = params[1], params[3]

        # Display the estimated parameters
        print(f'Estimated Shape Parameter: {est_shape}')
        print(f'Estimated Scale Parameter: {est_scale}')

        # Optional: Plot the histogram of the data with the fitted distribution
        plt.hist(nonoutlier_dist, bins=30, density=True, alpha=0.5, color='g')
        xmin, xmax = plt.xlim()
        x = np.linspace(xmin, xmax, 100)
        p = exponweib.pdf(x, *params)
        plt.plot(x, p, 'k', linewidth=2)
        title = "Fit results: shape = %.2f, scale = %.2f" % (est_shape, est_scale)
        plt.title(title)
        plt.show()