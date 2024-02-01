 # code for kernel estimation of density for positive values only, using gaussian kernel


import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import statsmodels.api as sm
import pandas as pd
import os

directory_path = 'C:\\Users\\user\\Documents\\Barbora\\data1.1'
#directory_path = 'C:\\Users\\user\\Documents\\Barbora\\data1.2'
#directory_path = 'C:\\Users\\user\\Documents\\Barbora\\data1.3'
#df = pd.read_pickle('C:\\Users\\user\\Documents\\Barbora\\data1.2\\MSEL_00452_1_1_UFO.pkl')    #single file


# we go through every file in the folder
for filename in os.listdir(directory_path):
    if filename.endswith('.pkl'):  # .pkl files filter
        file_path = os.path.join(directory_path, filename)
        df = pd.read_pickle(file_path)

        print(f"Načten soubor: {filename}")

        channels = df.channel.unique()  #
        distance = pd.Series()  #empty series
        pistol_distance = pd.Series()
        blob_distance = pd.Series()
        erase_distance = pd.Series()


        # counting of distance between detections
        for channel in channels[[x[1:6] !="Macro" for x in channels]]:
            df_chan = df[(df.channel == channel) & (df.osc_type_2 == 'clear')]
            distance1 = df_chan.start_time.shift(-1) - df_chan.end_time
            distance = pd.concat([distance.dropna(), distance1.dropna()], ignore_index=True)

        nonoutlier_dist = distance[(distance < 3 * (np.percentile(distance, 75))) & (distance > 0)]


        # Function to compute truncated Gaussian kernel values
        def truncated_gaussian_kernel(x):
            return np.where(x < 0, 0, norm.pdf(x))

        # Create a grid of x values for plotting
        x_values = np.linspace(0, max(nonoutlier_dist))

        # Bandwidth for kernel density estimation
        bandwidth = 0.5

        # Use KDEUnivariate without fit, and set kernel and bandwidth separately
        kde = sm.nonparametric.KDEUnivariate(nonoutlier_dist)
        kde.kernel = truncated_gaussian_kernel
        kde.bw = bandwidth
        kde.fit()

        # Plot the data and kernel density estimate
        plt.hist(nonoutlier_dist, bins=30, density=True, alpha=0.5, label='Histogram of Data')
        plt.plot(x_values, kde.evaluate(x_values), label='Kernel Density Estimate (Truncated Gaussian Kernel)')
        plt.title('Kernel Density Estimation with Truncated Gaussian Kernel (statsmodels)')
        plt.xlabel('Values')
        plt.ylabel('Density')
        plt.legend()
        plt.show()
