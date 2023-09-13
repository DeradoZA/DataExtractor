import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt


if __name__ == "__main__":
    dataCSV = os.path.join(os.getcwd(), "..", "DataExtractor", "FormattedStats", "FormattedCSGOStats.csv")

    df = pd.read_csv(dataCSV)

    value_counts = df['Team1_Player1_Deaths'].value_counts()

# # Sort the value_counts Series by index (the unique values in 'score difference')
#     value_counts_sorted = value_counts.sort_index()

#     # Plot the value counts as a bar chart
#     plt.bar(value_counts_sorted.index, value_counts_sorted) //Plotting individual columns

#     # Add labels and title
#     plt.xlabel('Score Difference')
#     plt.ylabel('Frequency')
#     plt.title('Frequency of Score Difference Values')

#     # Display the plot
#     plt.show()