import os
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Rectangle
import matplotlib.colors as mcolors  # For creating custom color maps

# List of variables and metrics to iterate through
variables = ["Temperature", "WindSpeed", "Humidity", "Pressure"]

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

models = ["AGCRN", "TCN", "GWN", "CLCRN"]
base_colors = ['#FF6666', '#66FF66', '#6666FF', '#FF66FF']  # Lighter base colors for each model
bar_width = 16000

def generate_maps_with_color_gradient():
    horizon = "24h"
    base_directory = './Plots/bestmodels_colorGradient'  # Base directory for plots with color gradient

    if not os.path.exists(base_directory):
        os.makedirs(base_directory)
    metrics = ["SMAPE", "MSE", "RMSE", "MAE"]
    for selected_metric in metrics:
        metric_directory = os.path.join(base_directory, selected_metric)  # Subdirectory for each metric
        if not os.path.exists(metric_directory):
            os.makedirs(metric_directory)

        for selected_variable in variables:
            df = pd.read_csv("./DataNew/Locations/Locations.csv")
            fig, ax = plt.subplots(figsize=(8, 8))
            m = Basemap(projection='merc', llcrnrlat=-35, urcrnrlat=-25, llcrnrlon=15, urcrnrlon=33, resolution='i', ax=ax)
            m.drawcountries()
            m.drawcoastlines()
            m.drawmapboundary(fill_color='white')
            m.fillcontinents(color='lightgray', lake_color='white')

            # Create a color map for each model
            model_color_maps = {}
            for model, base_color in zip(models, base_colors):
                model_color_maps[model] = mcolors.LinearSegmentedColormap.from_list(
                    model, [base_color, 'black'])  # Gradient: base color to black

            for index, row in df.iterrows():
                station_number = int(row['Number'])
                latitude = row['Latitude']
                longitude = row['Longitude']
                x, y = m(longitude, latitude)

                # Fetch metric values for each model
                model_metrics = [(model, get_model_metric(model, selected_variable, selected_metric, horizon, station_number)) for model in models]
                min_metric, max_metric = min([metric for _, metric in model_metrics if metric is not None]), max([metric for _, metric in model_metrics if metric is not None])

                for model_idx, (model, metric) in enumerate(model_metrics):
                    if metric is not None:
                        norm = mcolors.Normalize(vmin=min_metric, vmax=max_metric)
                        color = model_color_maps[model](norm(metric))  # Get color from the model's color map
                        ax.add_patch(Rectangle((x + model_idx * bar_width - bar_width * len(models) / 2, y), bar_width, 50000, facecolor=color, label=model if index == 0 else ""))

                # Add station number text
                plt.text(x, y + 55000, f"{station_number}", fontsize=10, ha='center')

            plt.title(f"{selected_variable} - {selected_metric} with Model-specific Color Gradients ({horizon} horizon)", fontsize=16)

            filename = f'bestmodel_colorGradient_{selected_metric}_{selected_variable}_{horizon}.png'
            filepath = os.path.join(metric_directory, filename)
            fig.savefig(filepath, dpi=300)
            plt.close(fig)  # Close the figure to free memory

if __name__ == "__main__":
    generate_maps_with_color_gradient()
