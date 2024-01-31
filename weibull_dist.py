
# estimate of the weibull dist. parameters


import pandas as pd
import numpy as np
import os
from scipy.optimize import minimize

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

        nonoutlier_dist = distance[(distance < 3 * (np.percentile(distance, 75))) & (distance > 0)]


        def weibull_log_likelihood(params, data):
            k, lamb = params
            n = len(data)
            log_likelihood = -n*np.log((lamb**k)/k) + (k-1)*np.sum(np.log(data)) - np.sum((data/lamb)**k)
            return -log_likelihood  # Minimizing the negative log-likelihood function (max log-likelihood)


        # conversion to np.array due to the minimize function
        data = np.array(nonoutlier_dist)
        # initial parameter
        initial_guess = np.array([0.5, 0.8])

        # using minimize function to find parameter value maximizing the log-likelihood
        result = minimize(weibull_log_likelihood, initial_guess, args=data, method='BFGS')
        estimated_k, estimated_lambda = result.x

        print(estimated_k, estimated_lambda)

        # Data histogram plotting and Weibull distribution
        # the histogram is adjusted to match the density plot (param. density=True)
        #plt.hist(nonoutlier_dist, bins=30, density=True, alpha=0.7, label='Histogram dat')
        #plt.suptitle("Distance between UFO detections")
        #plt.title("Weibull distribution")
        #plt.xlabel("time in microseconds")
        #plt.show()

