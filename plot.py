import matplotlib.pyplot as plt
import numpy as np

# Function to read data from file
def read_data(file_path):
    with open(file_path, 'r') as file:
        data = file.readlines()
    y1_values = []
    y2_values = []
    for index, line in enumerate(data):
        try:
            y1, y2 = line.strip().split(',')
            y1_values.append((index, float(y1)))  # x is the index, y is y1
            y2_values.append((index, float(y2)))  # x is the index, y is y2
        except ValueError:
            continue  # Skip lines that do not conform to expected format
    return y1_values, y2_values

# Function to plot data
def plot_data(y1_values, y2_values):
    # Extract x and y values for both lines
    x_values1, y_values1 = zip(*y1_values)
    x_values2, y_values2 = zip(*y2_values)
    delta_values = [abs(y1 - y2) for y1, y2 in zip(y_values1, y_values2)]  # Calculate absolute delta values
    
    # Create a plot with subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))

    # Plot base lines
    ax1.plot(x_values1, y_values1, label='DCNN', linestyle='-', color="black", alpha=1)
    ax1.plot(x_values2, y_values2, label='Opponent', linestyle='-', color="grey", alpha=1)
    
    # Plot trend lines for each segment, skipping the first point
    segment_indices = [0] + [i * 5 for i in range(1, len(x_values1) // 5 + 2)]
    for start, end in zip(segment_indices[:-1], segment_indices[1:]):
        # Skip the first point in each segment
        start += 1
        if start < end and len(x_values1[start:end]) > 1 and True:  # Ensure there are enough points after skipping
            # Fit trendlines for Opponent
            z = np.polyfit(x_values1[start:end], y_values1[start:end], 1)
            p = np.poly1d(z)
            ax1.plot(x_values1[start:end], p(x_values1[start:end]), linestyle='--', color="black", alpha=1)

            # Fit trendlines for DCNN
            z = np.polyfit(x_values2[start:end], y_values2[start:end], 1)
            p = np.poly1d(z)
            ax1.plot(x_values2[start:end], p(x_values2[start:end]), linestyle='--', color="grey", alpha=1)

    # Adjust vertical lines to move one index forward
    for i in range(1, len(x_values1) // 5 ):
        ax1.axvline(x=x_values1[min(i * 5, len(x_values1) - 1)], color='red', linestyle='--', label='Change Of Opponent' if i == 1 else "")
    ax1.set_xlabel('Match #')
    ax1.set_ylabel('Score')
    ax1.set_title('Opponent Score vs. DCNN Score')
    ax1.legend()
    ax1.grid(True)
    
    # Second subplot
    ax2.fill_between(x_values1, delta_values, color="black", alpha=0.4)
    ax2.fill_between(x_values1, [-d for d in delta_values], color="black", alpha=0.4)
    for i in range(1, len(x_values1) // 5 ):
        ax2.axvline(x=x_values1[min(i * 5, len(x_values1) - 1)], color='red', linestyle='--', label='Change Of Opponent' if i == 1 else "")
    ax2.set_xlabel('Match #')
    ax2.set_ylabel('Magnitude of Delta Score')
    ax2.set_title('Magnitude of Delta Score Over Matches')
    ax2.legend()
    ax2.grid(True)
    
    # Explicitly set x-ticks to integer values
    max_x = max(x_values1)
    ax1.set_xticks(range(0, max_x + 1, max_x // 10))  # Adjust this for different datasets
    ax2.set_xticks(range(0, max_x + 1, max_x // 10))  # Adjust this for different datasets

    plt.tight_layout()
    plt.show()

# Replace 'scoreHistory.txt' with the path to your .txt file
file_path = 'scoreHistory.txt'
y1_values, y2_values = read_data(file_path)
plot_data(y1_values, y2_values)

