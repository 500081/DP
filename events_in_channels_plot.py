
# plot of events through channels

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
        events_through_channels = []

        # we need sequence for every single channel
        for channel in channels:
            events_through_channels.append(df.start_time[(df.channel == channel) & (df.osc_type_2 == 'clear')])

        fig, ax = plt.subplots(figsize=(10, 8))  # Increase the size of the plot

        ax.eventplot(
            events_through_channels,
            orientation="horizontal",
            lineoffsets=channels,
            linewidth=0.75,
            colors='steelblue',  # Set the color of event lines to black
        )

        # Highlighting rows and columns
        ax.set_yticks(channels)
        ax.set_xticks([])  # Turn off the X-axis
        ax.grid(axis='y', linestyle='-', linewidth=0.5, color='gray', alpha=0.5)  # Add grid lines for columns

        # Improve readability of the Y-axis labels
        ax.set_yticklabels(channels, fontsize=8)

        plt.title("Events over time for individual channels")

        plt.show()