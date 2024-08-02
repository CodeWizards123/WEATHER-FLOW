# import os
# import pandas as pd

# # List of variables and metrics to iterate through
# variables = ["Temperature"]

# def get_metric_for_station(file_path, station_number, metric):
#     if os.path.exists(file_path): 
#         df = pd.read_csv(file_path, header=None, names=['Station', metric])
#         metric_value = df[df['Station'] == station_number][metric].values
#         if metric_value.size > 0:
#             return metric_value[0]
#     return None

# def get_model_metric(model, variable, metric, horizon, station_number):
#     path = f"./Metrics/{model}/{variable}/{metric}/metrics_{horizon}.csv"
#     return get_metric_for_station(path, station_number, metric)

# models = ["TCN", "AGCRN", "CLCRN", "GWN"]
# horizons = ["3h", "9h", "12h", "24h"]

# def generate_csv_for_horizon(horizon, selected_metric):
#     base_directory = './Plots/Delta'  # Base directory for the CSV files
#     unranked_directory = os.path.join(base_directory, 'unranked')
#     ranked_directory = os.path.join(base_directory, 'ranked')
    
#     if not os.path.exists(unranked_directory):
#         os.makedirs(unranked_directory)
#     if not os.path.exists(ranked_directory):
#         os.makedirs(ranked_directory)

#     unranked_csv_path = os.path.join(unranked_directory, f'{selected_metric}_comparison_{horizon}.csv')
#     ranked_csv_path = os.path.join(ranked_directory, f'{selected_metric}_comparison_{horizon}.csv')
    
#     # Read station locations
#     df_locations = pd.read_csv("./DataNew/Locations/Locations.csv")
#     station_numbers = df_locations['Number'].astype(int).tolist()

#     rows = []
#     for station_number in station_numbers:
#         row = [station_number]
#         metrics = {}
#         for model in models:
#             metric = get_model_metric(model, "Temperature", selected_metric, horizon, station_number)
#             metrics[model] = metric
#             row.append(metric)
        
#         # Calculate differences
#         if metrics["TCN"] is not None and metrics["AGCRN"] is not None:
#             row.append(metrics["TCN"] - metrics["AGCRN"])
#         else:
#             row.append(None)
#             print('reach1')
        
#         if metrics["TCN"] is not None and metrics["CLCRN"] is not None:
#             row.append(metrics["TCN"] - metrics["CLCRN"])
#         else:
#             row.append(None)
#             print('reach2')
        
#         if metrics["TCN"] is not None and metrics["GWN"] is not None:
#             row.append(metrics["TCN"] - metrics["GWN"])
#         else:
#             row.append(None)
#             print('reach3')

#         rows.append(row)

#     # Create DataFrame
#     columns = ["Station", "TCN", "AGCRN", "CLCRN", "GWN", "TCN-AGCRN", "TCN-CLCRN", "TCN-GWN"]
#     df_results = pd.DataFrame(rows, columns=columns)
    
#     # Save unranked CSV
#     df_results.to_csv(unranked_csv_path, index=False)
#     print(f"Unranked CSV file saved to {unranked_csv_path}")
    
#     # Rank by TCN-AGCRN and save ranked CSV
#     df_ranked = df_results.sort_values(by="TCN-AGCRN").reset_index(drop=True)
#     df_ranked.to_csv(ranked_csv_path, index=False)
#     print(f"Ranked CSV file saved to {ranked_csv_path}")

# if __name__ == "__main__":
#     metrics = ["SMAPE", "MSE"]
#     for metric in metrics:
#         for horizon in horizons:
#             generate_csv_for_horizon(horizon, metric)

import os
import pandas as pd
import matplotlib.pyplot as plt

# List of variables and metrics to iterate through
variables = ["Temperature"]

def get_metric_for_station(file_path, station_number, metric):
    if os.path.exists(file_path): 
        df = pd.read_csv(file_path, header=None, names=['Station', metric])
        metric_value = df[df['Station'] == station_number][metric].values
        if metric_value.size > 0:
            return metric_value[0]
    return None

def get_model_metric(model, variable, metric, horizon, station_number):
    path = f"./Metrics/{model}/{variable}/{metric}/metrics_{horizon}.csv"
    return get_metric_for_station(path, station_number, metric)

models = ["TCN", "AGCRN", "CLCRN", "GWN"]
horizons = ["3h", "9h", "12h", "24h"]

def generate_csv_for_horizon(horizon, selected_metric):
    base_directory = './Plots/Delta'  # Base directory for the CSV files
    unranked_directory = os.path.join(base_directory, 'unranked')
    ranked_directory = os.path.join(base_directory, 'ranked')
    
    if not os.path.exists(unranked_directory):
        os.makedirs(unranked_directory)
    if not os.path.exists(ranked_directory):
        os.makedirs(ranked_directory)

    unranked_csv_path = os.path.join(unranked_directory, f'{selected_metric}_comparison_{horizon}.csv')
    ranked_csv_path = os.path.join(ranked_directory, f'{selected_metric}_comparison_{horizon}.csv')
    
    # Read station locations
    df_locations = pd.read_csv("./DataNew/Locations/Locations.csv")
    station_numbers = df_locations['Number'].astype(int).tolist()

    rows = []
    for station_number in station_numbers:
        row = [station_number]
        metrics = {}
        for model in models:
            metric = get_model_metric(model, "Temperature", selected_metric, horizon, station_number)
            metrics[model] = metric
            row.append(metric)
        
        # Calculate differences
        if metrics["TCN"] is not None and metrics["AGCRN"] is not None:
            row.append(metrics["TCN"] - metrics["AGCRN"])
        else:
            row.append(None)
        
        if metrics["TCN"] is not None and metrics["CLCRN"] is not None:
            row.append(metrics["TCN"] - metrics["CLCRN"])
        else:
            row.append(None)
        
        if metrics["TCN"] is not None and metrics["GWN"] is not None:
            row.append(metrics["TCN"] - metrics["GWN"])
        else:
            row.append(None)

        rows.append(row)

    # Create DataFrame
    columns = ["Station", "TCN", "AGCRN", "CLCRN", "GWN", "TCN-AGCRN", "TCN-CLCRN", "TCN-GWN"]
    df_results = pd.DataFrame(rows, columns=columns)
    
    # Save unranked CSV
    df_results.to_csv(unranked_csv_path, index=False)
    print(f"Unranked CSV file saved to {unranked_csv_path}")
    
    # Rank by TCN-AGCRN and save ranked CSV
    df_ranked = df_results.sort_values(by="TCN-AGCRN").reset_index(drop=True)
    df_ranked.to_csv(ranked_csv_path, index=False)
    print(f"Ranked CSV file saved to {ranked_csv_path}")

    # Generate plot for the unranked CSV
    generate_plot(unranked_csv_path, horizon, selected_metric)

def generate_plot(csv_path, horizon, selected_metric):
    df = pd.read_csv(csv_path)
    
    # Calculate average delta for each station
    df['Average Delta'] = df[['TCN-AGCRN', 'TCN-CLCRN', 'TCN-GWN']].mean(axis=1)

    # Plotting
    plt.figure(figsize=(14, 8))
    plt.plot(df['Station'], df['TCN-AGCRN'], label='TCN-AGCRN',color='red')
    plt.plot(df['Station'], df['TCN-CLCRN'], label='TCN-CLCRN',color='blue')
    plt.plot(df['Station'], df['TCN-GWN'], label='TCN-GWN',color='green')
    plt.plot(df['Station'], df['Average Delta'], label='Average Delta', linestyle='--', color='black')

    plt.xlabel('Station')
    plt.ylabel('Delta')
    plt.title(f'{selected_metric} Delta Comparison for {horizon}')
    plt.legend()
    plt.grid(True)

    # Save plot
    plot_directory = './Plots/Delta/Plots'
    if not os.path.exists(plot_directory):
        os.makedirs(plot_directory)
    plot_path = os.path.join(plot_directory, f'{selected_metric}_comparison_{horizon}.png')
    plt.savefig(plot_path)
    plt.close()

    print(f"Plot saved to {plot_path}")

if __name__ == "__main__":
    metrics = ["SMAPE", "MSE"]
    for metric in metrics:
        for horizon in horizons:
            generate_csv_for_horizon(horizon, metric)
