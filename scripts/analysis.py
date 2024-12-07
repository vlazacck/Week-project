import os
import pandas as pd
import matplotlib.pyplot as plt
from windrose import WindroseAxes
import matplotlib.cm as cm  # Required for colormaps
import numpy as np

# Create a results directory if it doesn't exist
RESULTS_FOLDER = "results"
os.makedirs(RESULTS_FOLDER, exist_ok=True)

# Path to the data folder
DATA_FOLDER = "data/"

def clean_data(df):
    """
    Clean the data by replacing negative values with 0 for specific columns.
    Tracks cleaning in a new 'Cleaning' column.
    Args:
        df (DataFrame): The DataFrame to clean.
    Returns:
        DataFrame: The cleaned DataFrame with a 'Cleaning' column.
    """
    df['Cleaning'] = 0
    columns_to_clean = ['GHI', 'DNI', 'DHI', 'ModA', 'ModB', 'WS', 'WSgust', 'RH']
    
    for column in columns_to_clean:
        if column in df.columns:
            df['Cleaning'] = df['Cleaning'] | (df[column] < 0)
            df[column] = df[column].apply(lambda x: max(x, 0))  # Replace negative values with 0
            
    return df

def plot_temperature_analysis(df, file_name):
    """
    Analyze the relationship between relative humidity (RH), temperature, and solar radiation.
    Args:
        df (DataFrame): The cleaned DataFrame with temperature and humidity data.
        file_name (str): The base name of the file (without extension).
    """
    if 'RH' not in df.columns or 'ModA' not in df.columns or 'ModB' not in df.columns:
        print(f"Skipping temperature analysis for {file_name}: Missing required columns ('RH', 'ModA', 'ModB').")
        return

    plt.figure(figsize=(10, 6))
    plt.scatter(df['RH'], df['ModA'], label='Temperature ModA', alpha=0.5, color='blue')
    plt.scatter(df['RH'], df['ModB'], label='Temperature ModB', alpha=0.5, color='orange')
    plt.title(f"Relative Humidity vs. Temperature for {file_name}")
    plt.xlabel("Relative Humidity (%)")
    plt.ylabel("Temperature (°C)")
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(RESULTS_FOLDER, f"{file_name}_RH_vs_Temperature.png"))
    plt.close()
    print(f"RH vs. Temperature scatter plot for {file_name} saved to {RESULTS_FOLDER}")

    if 'GHI' in df.columns:
        plt.figure(figsize=(10, 6))
        plt.scatter(df['RH'], df['GHI'], label='Global Horizontal Irradiance (GHI)', alpha=0.5, color='green')
        plt.title(f"Relative Humidity vs. Solar Radiation for {file_name}")
        plt.xlabel("Relative Humidity (%)")
        plt.ylabel("Solar Radiation (W/m²)")
        plt.grid(True)
        plt.legend()
        plt.savefig(os.path.join(RESULTS_FOLDER, f"{file_name}_RH_vs_SolarRadiation.png"))
        plt.close()
        print(f"RH vs. Solar Radiation scatter plot for {file_name} saved to {RESULTS_FOLDER}")

def plot_wind_analysis(df, file_name):
    """
    Create wind roses and radial bar plots to visualize wind speed and direction.
    Args:
        df (DataFrame): The cleaned DataFrame with wind data.
        file_name (str): The base name of the file (without extension).
    """
    if 'WS' not in df.columns or 'WD' not in df.columns:
        print(f"Skipping wind analysis for {file_name}: 'WS' or 'WD' column missing.")
        return

    df = df.dropna(subset=['WS', 'WD'])

    # Wind rose plot
    plt.figure(figsize=(8, 8))
    ax = WindroseAxes.from_ax()
    ax.bar(
        df['WD'], 
        df['WS'], 
        nsector=16, 
        opening=0.8, 
        edgecolor='white', 
        cmap=cm.cool  # Use callable colormap
    )
    ax.set_title(f"Wind Rose for {file_name}")
    plt.savefig(os.path.join(RESULTS_FOLDER, f"{file_name}_wind_rose.png"))
    plt.close()
    print(f"Wind rose plot for {file_name} saved to {RESULTS_FOLDER}")

    # Radial bar plot for wind direction variability
    bin_edges = np.linspace(0, 360, 13)
    direction_labels = [f"{int(bin_edges[i])}-{int(bin_edges[i+1])}" for i in range(len(bin_edges)-1)]
    wind_direction_bins = pd.cut(df['WD'], bins=bin_edges, labels=direction_labels, include_lowest=True)

    frequency = wind_direction_bins.value_counts(sort=False)

    plt.figure(figsize=(8, 8))
    theta = np.linspace(0.0, 2 * np.pi, len(frequency), endpoint=False)
    radii = frequency.values
    width = 2 * np.pi / len(frequency)

    ax = plt.subplot(111, polar=True)
    bars = ax.bar(theta, radii, width=width, bottom=0.0, color='skyblue', edgecolor='black')

    ax.set_title(f"Wind Direction Variability for {file_name}")
    plt.savefig(os.path.join(RESULTS_FOLDER, f"{file_name}_wind_direction_variability.png"))
    plt.close()
    print(f"Wind direction variability plot for {file_name} saved to {RESULTS_FOLDER}")

def main():
    """
    Main function to calculate and save summary statistics, cleaning impact, and wind analysis.
    """
    for file_name in os.listdir(DATA_FOLDER):
        if file_name.endswith(".csv"):  # Process only CSV files
            file_path = os.path.join(DATA_FOLDER, file_name)
            df = pd.read_csv(file_path)

            # Clean the data
            df = clean_data(df)
            
            # Extract base name
            base_name = os.path.basename(file_path).split('.')[0]
            
            # Perform analyses
            plot_wind_analysis(df, base_name)
            plot_temperature_analysis(df, base_name)

if __name__ == "__main__":
    main()
