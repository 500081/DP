
#script for calculating and ploting of distance between detections, length of det. and
#on each channel we calculate the distances between the end of the detection and the beginning of the new one.
#graphs are for separately for every channel on both electrodes

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import time

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
        min_num_of_event = 30

        # calculating of distance between detections
        for channel in channels[[x[1:6] !="Macro" for x in channels]]:
            df_chan = df[(df.channel == channel) & (df.osc_type_2 == 'clear')]
            distance = df_chan.start_time.shift(-1) - df_chan.end_time
            # plot of distance between UFO detections
            if len(distance) > min_num_of_event :
                plt.hist(distance, bins=round(np.sqrt(len(distance))))
                plt.title("Distance between UFO detections")
                plt.suptitle(channel)
                plt.xlabel("time in microseconds")
                plt.show()
                time.sleep(1)



        # distances between single type detection for pistol
        for channel in channels[[x[1:6] !="Macro" for x in channels]]:
            df_chan = df[(df.channel == channel) & (df.osc_type_2 == 'clear') & (df.shape_2 == "pistol")]
            distance = df_chan.start_time.shift(-1) - df_chan.end_time
            if len(distance) > min_num_of_event:
                plt.hist(distance, bins=round(np.sqrt(len(distance))))
                plt.title("Distance between UFO detections")
                plt.suptitle(filename)
                plt.xlabel("time in microseconds")
                plt.show()
                time.sleep(1)

        # distances between single type detection for blob
        for channel in channels[[x[1:6] !="Macro" for x in channels]]:
            df_chan = df[(df.channel == channel) & (df.osc_type_2 == 'clear') & (df.shape_2 == "blob")]
            distance = df_chan.start_time.shift(-1) - df_chan.end_time
            if len(distance) > min_num_of_event:
                plt.hist(distance, bins=round(np.sqrt(len(distance))))
                plt.title("Distance between UFO detections")
                plt.suptitle(filename)
                plt.xlabel("time in microseconds")
                plt.show()
                time.sleep(1)

