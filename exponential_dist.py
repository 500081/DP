
# estimate of parameters for gamma dist.
# funguje, ale nepouzivame mle, ale vzorce pro mle parametry, zjistit jestli je to ok

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import seaborn as sns
from scipy.stats import gamma
from scipy.stats import weibull_min
from scipy.optimize import curve_fit

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

        nonoutlier_dist = distance[distance < 3 * (np.percentile(distance, 75))]

        # estimate of exponential distribution
        lamb = 1/(np.mean(nonoutlier_dist)) # MLE parameter
        x = np.linspace(0, max(distance[distance < 3 * (np.percentile(distance, 75))]))
        pdf = lamb * np.exp(-lamb*x)



        # plot of distribution of distance between UFO detections and his kernel distribution
        plt.hist(nonoutlier_dist, bins=20, density=True, alpha=0.5)
        sns.kdeplot(nonoutlier_dist, bw_method=0.1, color="steelblue")
        plt.plot(x, pdf)
        plt.suptitle("Distance between UFO detections")
        plt.title("Exponential distribution")
        plt.xlabel("time in microseconds")
        plt.show()