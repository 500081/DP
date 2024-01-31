

# estimate of the one parameter weibull dist.
# shape parameter k = 1
# source https://www.mdpi.com/2571-905X/2/1/4

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import seaborn as sns

# files folder
#directory_path = 'C:\\Users\\user\\Documents\\Barbora\\data1.1'
#directory_path = 'C:\\Users\\user\\Documents\\Barbora\\data1.2'
directory_path = 'C:\\Users\\user\\Documents\\Barbora\\data1.3'
#df = pd.read_pickle('C:\\Users\\user\\Documents\\Barbora\\data1.2\\MSEL_00452_1_1_UFO.pkl')    #single file


# we go through every file in the folder
for filename in os.listdir(directory_path):
    if filename.endswith('.pkl'):  # .pkl files filter
        file_path = os.path.join(directory_path, filename)
        df = pd.read_pickle(file_path)

        print(f"Načten soubor: {filename}")

        channels = df.channel.unique()
        distance = pd.Series()  #empty series
        pistol_distance = pd.Series()
        blob_distance = pd.Series()
        erase_distance = pd.Series()


        # counting of distance between detections
        for channel in channels[[x[1:6] !="Macro" for x in channels]]:
            df_chan = df[(df.channel == channel) & (df.osc_type_2 == 'clear')]
            distance1 = df_chan.start_time.shift(-1) - df_chan.end_time
            distance = pd.concat([distance.dropna(), distance1.dropna()], ignore_index=True)


        nonoutlier_dist = distance[(distance < 3 * (np.percentile(distance, 75)))]

        my = np.mean(nonoutlier_dist)
        w = np.exp((1/my)*(my-1-np.sqrt(my**2+4*my+1)))  #estimate of one param. w
        print(w)
        x = np.arange(max(nonoutlier_dist)+1)
        PDF = (((np.log(w))**3)/(np.log(w)-2))*(x*(x+1)*(w**x)) # Probability density function


        # Data histogram plotting and Weibull distribution
        # the histogram is adjusted to match the density plot (param. density=True)
        plt.hist(nonoutlier_dist, bins=20, density=True, alpha=0.7, label='Histogram dat')
        sns.kdeplot(nonoutlier_dist, bw_method=0.1, color="steelblue")
        plt.plot(PDF)
        plt.suptitle("Distance between UFO detections")
        plt.title("Weibull distribution")
        plt.xlabel("time in microseconds")
        plt.show()

