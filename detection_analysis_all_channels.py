
#script for calculating and ploting of distance between detections, length of det. and
#on each channel we calculate the distances between the end of the detection and the beginning of the new one.
#graphs are for all detections on both electrodes

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

        channels = df.channel.unique()  #
        distance = pd.Series()  #empty series
        pistol_distance = pd.Series()
        blob_distance = pd.Series()
        erase_distance = pd.Series()


        # calculating of distance between detections
        for channel in channels[[x[1:6] !="Macro" for x in channels]]:
            df_chan = df[(df.channel == channel) & (df.osc_type_2 == 'clear')]
            distance1 = df_chan.start_time.shift(-1) - df_chan.end_time
            distance = pd.concat([distance.dropna(), distance1.dropna()], ignore_index=True)


        # distances between single type detection for pistol
        for channel in channels[[x[1:6] !="Macro" for x in channels]]:
            df_chan = df[(df.channel == channel) & (df.osc_type_2 == 'clear') & (df.shape_2 == "pistol")]
            distance1 = df_chan.start_time.shift(-1) - df_chan.end_time
            pistol_distance = pd.concat([pistol_distance.dropna(), distance1.dropna()], ignore_index=True)

        # distances between single type detection for blob
        for channel in channels[[x[1:6] !="Macro" for x in channels]]:
            df_chan = df[(df.channel == channel) & (df.osc_type_2 == 'clear') & (df.shape_2 == "blob")]
            distance1 = df_chan.start_time.shift(-1) - df_chan.end_time
            blob_distance = pd.concat([blob_distance.dropna(), distance1.dropna()], ignore_index=True)


        # plot of distance between UFO detections
        plt.hist(distance, bins=50)
        plt.title("Distance between UFO detections")
        plt.suptitle(filename)
        plt.xlabel("time in microseconds")
        plt.show()

        # plot of distance between UFO detections without outliers
        plt.hist(distance[distance<3*(np.percentile(distance, 75))], bins=30)
        plt.suptitle("Distance between UFO detections")
        plt.title(("without outliers", filename))
        plt.xlabel("time in microseconds")
        plt.show()




        if len(pistol_distance) != 0:
            plt.hist(pistol_distance[pistol_distance<3*(np.percentile(pistol_distance, 75))], bins=30)
            # rule for outliers   outliers > 3*(np.percentile(pistol_distance, 75))
            plt.suptitle("Distance between pistol detections")
            plt.title(("without outliers", filename))
            plt.xlabel("time in microseconds")

            plt.show()

        if len(blob_distance) != 0:
            plt.hist(blob_distance[blob_distance<3*np.percentile(blob_distance, 75)], bins=30)
            plt.suptitle("Distance between blob detections")
            plt.title(("without outliers", filename))
            plt.xlabel("time in microseconds")
            plt.show()


        # types of UFO
        plt.hist([df.start_time[df.shape_2=="pistol"], df.start_time[df.shape_2=="blob"]])
        plt.suptitle("types of UFO detections")
        plt.title(filename)
        plt.legend(["pistol", "blob"])
        plt.xlabel("time in microseconds")
        plt.show()

        # length of blob detections
        if len(df.start_time[df.shape_2 == "pistol"]) != 0:
            length = df.end_time[df.shape_2 == "pistol"] - df.start_time[df.shape_2 == "pistol"]
            plt.hist(length, bins=10)
            plt.xlim([3500,10500])
            plt.suptitle("length of pistol detections")
            plt.title(filename)
            plt.xlabel("time in microseconds")
            plt.show()

        # length of blob detections
        if len(df.start_time[df.shape_2 == "blob"]) != 0:
            length = df.end_time[df.shape_2 == "blob"]-df.start_time[df.shape_2 == "blob"]
            plt.hist(length, bins=10)
            plt.xlim([3500,10500])
            plt.suptitle("length of blob detections")
            plt.title(filename)
            plt.xlabel("time in microseconds")
            plt.show()


