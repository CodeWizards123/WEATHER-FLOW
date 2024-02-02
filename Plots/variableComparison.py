import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Variables and models to iterate through
variables = ["Temperature", "WindSpeed", "Humidity", "Pressure"]
models = ["AGCRN", "TCN", "GWN", "CLCRN"]
colors = ['#FF0000', 'green', 'blue', 'cyan']  # Colors for each model
bar_width = 0.2  # Width of each bar in the bar chart

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

def calculate_average_metric(variable, metric="RMSE", horizon="24h"):
    station_numbers = range(1, 45)  # Assuming 44 stations as per the CSV format provided
    model_averages = {}
    
    for model in models:
        metrics = []
        for station_number in station_numbers:
            metric_value = get_model_metric(model, variable, metric, horizon, station_number)
            if metric_value is not None:
                metrics.append(metric_value)
        
        if metrics:  # Ensure there are valid metric values before calculating the average
            model_averages[model] = sum(metrics) / len(metrics)
        else:
            model_averages[model] = 0  # Set to 0 if no valid metric values are found

    return model_averages

def plot_metric(metric, horizon="24h"):
    n_groups = len(variables)
    fig, ax = plt.subplots(figsize=(10, 6))
    index = np.arange(n_groups)
    
    for model_idx, model in enumerate(models):
        averages = [calculate_average_metric(variable, metric, horizon)[model] for variable in variables]
        plt.bar(index + model_idx * bar_width, averages, bar_width, label=model, color=colors[model_idx])

    plt.xlabel('Variable', fontsize=14)
    plt.ylabel(f'Average {metric}', fontsize=14)
    plt.title(f'Average {metric} by Model and Variable ({horizon} Horizon)', fontsize=16)
    plt.xticks(index + bar_width / 2 * (len(models) - 1), variables)
    plt.legend()
    plt.tight_layout()
    
    # Create directories and save the plot
    save_dir = f"./Plots/variableComparison/{metric}"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    plt.savefig(f"{save_dir}/variableComparison_{metric}_{horizon}h.png")
    plt.close(fig)  # Close the figure after saving to free up memory

if __name__ == "__main__":
    metrics = ["RMSE", "MAE", "SMAPE", "MSE"]
    for metric in metrics:
        plot_metric(metric)
