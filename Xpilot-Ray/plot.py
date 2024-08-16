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
            y2, y1 = line.strip().split(',')
            y1_values.append((index +1, float(y1)))  # x is the index, y is y1
            y2_values.append((index +1, float(y2)))  # x is the index, y is y2
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
    ax1.plot(x_values1, y_values1, label='DCNN', linestyle='-', color="black", alpha=0.5)
    ax1.plot(x_values2, y_values2, label='Opponent', linestyle='-', color="grey", alpha=0.5)

    # Adjust vertical lines to move one index forward
    for i in range(1, len(x_values1) // 10 + 1):
        x_position = i * 10
        if x_position <= len(x_values1):
            ax1.axvline(x=x_position, color='red', linestyle='--', label='Change Of Opponent' if i == 1 else "")
    ax1.set_xlabel('Match #')
    ax1.set_ylabel('Score')
    ax1.set_title('Opponent Score vs. DCNN Score')
    ax1.legend()
    ax1.grid(True)
    ax1.set_xlim([1, max(x_values1)])
    
    # Second subplot
    ax2.fill_between(x_values1, delta_values, color="black", alpha=0.4)
    ax2.fill_between(x_values1, [-d for d in delta_values], color="black", alpha=0.4)
    for i in range(1, len(x_values1) // 10 + 1):
        x_position = i * 10
        if x_position <= len(x_values1):
            ax2.axvline(x=x_position, color='red', linestyle='--', label='Change Of Opponent' if i == 1 else "")
    ax2.set_xlabel('Match #')
    ax2.set_ylabel('Magnitude of Delta Score')
    ax2.set_title('Magnitude of Delta Score Over Matches')
    ax2.legend()
    ax2.grid(True)
    ax2.set_xlim([1, max(x_values1)])
    
    # Explicitly set x-ticks to integer values
    #max_x = max(x_values1)
    #ax1.set_xticks(range(0, max_x + 1, max_x // 10))  # Adjust this for different datasets
    #ax2.set_xticks(range(0, max_x + 1, max_x // 10))  # Adjust this for different datasets

    plt.tight_layout()
    plt.show()

# Replace 'scoreHistory.txt' with the path to your .txt file
file_path = 'scoreHistory.txt'
y1_values, y2_values = read_data(file_path)
plot_data(y1_values, y2_values)

