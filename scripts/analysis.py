import os
import pandas as pd
import matplotlib.pyplot as plt

# Create a results directory if it doesn't exist
RESULTS_FOLDER = "results"
os.makedirs(RESULTS_FOLDER, exist_ok=True)

# Path to the data folder
DATA_FOLDER = "data/"

def clean_data(df):
    """
    Cleans the data by replacing negative values with 0 for specific columns.
    Args:
        df (DataFrame): The DataFrame to clean.
    Returns:
        DataFrame: The cleaned DataFrame.
    """
    # Columns that should not have negative values
    columns_to_clean = ['GHI', 'DNI', 'DHI', 'ModA', 'ModB', 'WS', 'WSgust']
    
    for column in columns_to_clean:
        if column in df.columns:
            df[column] = df[column].apply(lambda x: max(x, 0))  # Replace negative values with 0
            
    return df

def calculate_summary_statistics(file_path, output_folder):
    """
    Calculate and save summary statistics for a given CSV file.
    Args:
        file_path (str): Path to the CSV file.
        output_folder (str): Folder to save the summary results.
    """
    # Load the data
    df = pd.read_csv(file_path)
    
    # Clean the data by replacing negative values
    df = clean_data(df)
    
    # Compute summary statistics
    summary_stats = df.describe(include='all').T  # Transpose for better readability
    summary_stats['median'] = df.median(numeric_only=True)  # Add median column
    
    # Add missing value information
    summary_stats['missing_values'] = df.isnull().sum()
    
    # Extract base name without extension
    base_name = os.path.basename(file_path).split('.')[0]
    
    # Save the summary statistics to CSV with the same base name
    output_file = os.path.join(output_folder, f"{base_name}_summary.csv")
    summary_stats.to_csv(output_file)
    print(f"Summary statistics for {base_name} saved to {output_file}")

def plot_time_series(df, file_name):
    """
    Plot time series for GHI, DNI, DHI, and Tamb.
    Args:
        df (DataFrame): The cleaned DataFrame to plot.
        file_name (str): The base name of the file (without extension).
    """
    # Convert 'Timestamp' to datetime if it's not already
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])

    # Set 'Timestamp' as the index
    df.set_index('Timestamp', inplace=True)

    # Create the plots
    plt.figure(figsize=(14, 8))

    # Plot GHI
    plt.subplot(2, 2, 1)
    plt.plot(df.index, df['GHI'], label='GHI', color='tab:blue')
    plt.title('GHI over Time')
    plt.xlabel('Time')
    plt.ylabel('GHI (W/m²)')
    plt.grid(True)

    # Plot DNI
    plt.subplot(2, 2, 2)
    plt.plot(df.index, df['DNI'], label='DNI', color='tab:orange')
    plt.title('DNI over Time')
    plt.xlabel('Time')
    plt.ylabel('DNI (W/m²)')
    plt.grid(True)

    # Plot DHI
    plt.subplot(2, 2, 3)
    plt.plot(df.index, df['DHI'], label='DHI', color='tab:green')
    plt.title('DHI over Time')
    plt.xlabel('Time')
    plt.ylabel('DHI (W/m²)')
    plt.grid(True)

    # Plot Tamb
    plt.subplot(2, 2, 4)
    plt.plot(df.index, df['Tamb'], label='Tamb', color='tab:red')
    plt.title('Tamb over Time')
    plt.xlabel('Time')
    plt.ylabel('Tamb (°C)')
    plt.grid(True)

    # Adjust layout
    plt.tight_layout()

    # Save the plot as a PNG file with the same base name
    plt.savefig(os.path.join(RESULTS_FOLDER, f"{file_name}_time_series.png"))
    print(f"Time series plot for {file_name} saved to {RESULTS_FOLDER}")

def main():
    """
    Main function to calculate and save summary statistics and plot time series for all data files.
    """
    # Iterate over all files in the data folder
    for file_name in os.listdir(DATA_FOLDER):
        if file_name.endswith(".csv"):  # Process only CSV files
            file_path = os.path.join(DATA_FOLDER, file_name)
            df = pd.read_csv(file_path)

            # Clean the data by replacing negative values
            df = clean_data(df)
            
            # Extract base name for saving summary and plot
            base_name = os.path.basename(file_path).split('.')[0]
            
            # Call function to calculate and save summary statistics
            calculate_summary_statistics(file_path, RESULTS_FOLDER)
            
            # Call function to plot time series
            plot_time_series(df, base_name)

if __name__ == "__main__":
    main()
