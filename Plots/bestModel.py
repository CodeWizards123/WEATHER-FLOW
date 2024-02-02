# import os
# import pandas as pd
# import matplotlib.pyplot as plt
# from mpl_toolkits.basemap import Basemap
# import numpy as np
# from matplotlib.patches import Rectangle

# def get_smape_from_file(file_path):
#     if os.path.exists(file_path): 
#         with open(file_path, 'r') as file:
#             lines = file.readlines()
#             for line in lines:
#                 if "rmse:" in line:
#                     return float(line.split(":")[1].strip())
#                 elif  "RMSE" in line:
#                     return float(line.split("RMSE")[1].strip())
                
#     return None

# def get_model_smape(station_name, model, split, horizon):
#     if model=='TCN':
#         path = f"./Results/{model}/{horizon} Hour Forecast/{station_name}/metrics/metrics_" + str(split) + ".txt"
#     elif model=='AGCRN':
#         path = f"./Results/{model}/{horizon} Hour Forecast/Metrics/attribute0/{station_name}/split_" + str(split) + "_metrics.txt"
#     else:
#         path = f"./Results/{model}/{horizon} Hour Forecast/Metrics/{station_name}/metrics_" + str(split) + ".txt"

#     return get_smape_from_file(path)




# models = ["AGCRN", "TCN"]

# colors = ['#FF0000', 'green']

# bar_width = 16000 
# exaggeration_power = 1 

# def main():
#     split = 0
#     horizon = 24

#     df = pd.read_csv("./DataNew/Locations/Locations.csv")

#     fig, ax = plt.subplots(figsize=(8, 8))
    
#     m = Basemap(projection='merc', llcrnrlat=-35, urcrnrlat=-25,
#                 llcrnrlon=15, urcrnrlon=33, resolution='i', ax=ax)
#     m.drawcountries()
#     m.drawcoastlines()
#     m.drawmapboundary(fill_color='white')
#     m.fillcontinents(color='lightgray', lake_color='white')

#     for index, row in df.iterrows():
#         station_number = row['Number']
#         station_name = row['StasName']
#         latitude = row['Latitude']
#         longitude = row['Longitude']
#         x, y = m(longitude, latitude)

#         model_smapes = [(model_to_plot, get_model_smape(station_name, model_to_plot, split, horizon)) for model_to_plot in models]

#         #normalise the bar sizes
#         total_smape = 0
#         for model_idx, (model_to_plot, smape) in enumerate(model_smapes):

#             total_smape += smape
#         average_smape = total_smape / len(model_smapes)


#         for model_idx, (model_to_plot, smape) in enumerate(model_smapes):
#             if smape is not None:
#                 bar_height = ((smape/average_smape))*100000
#                 ax.add_patch(Rectangle((x + model_idx * bar_width - bar_width * len(models) / 2, y), bar_width, bar_height, facecolor=colors[models.index(model_to_plot)], label=model_to_plot if index == 0 else ""))

#         plt.text(x + (len(models) - 1) * bar_width, y + bar_height-0.2, f"{station_number}", fontsize=10)

#     plt.title(f"All models {horizon} hour horizon", fontsize=16)    

#     plt.legend(loc='upper right', fontsize=12)

#     directory = 'Plots'
#     filename = f'bestmodel.png'

#     if not os.path.exists(directory):
#         os.makedirs(directory)

#     filepath = os.path.join(directory, filename)
#     fig.savefig(filepath, dpi=300)

# if __name__ == "__main__":
#     main()


########################
# import os
# import pandas as pd
# import matplotlib.pyplot as plt
# from mpl_toolkits.basemap import Basemap
# from matplotlib.patches import Rectangle

# # Specify the variable and metric here
# selected_variable = "Humidity"  # Example: "Humidity", "WindSpeed", "Temperature", "Pressure"
# selected_metric = "RMSE"  # Example: "RMSE", "MSE", "MAE"

# def get_metric_for_station(file_path, station_number, metric):
#     if os.path.exists(file_path): 
#         df = pd.read_csv(file_path, header=None, names=['Station', metric])
#         metric_value = df[df['Station'] == station_number][metric].values
#         if metric_value.size > 0:
#             print(metric_value[0])
#             return metric_value[0]
#     return None

# def get_model_metric(model, variable, metric, horizon, station_number):
#     # Adjust the path according to your directory structure
#     path = f"./Metrics/{model}/{variable}/{metric}/metrics_{horizon}.csv"
#     return get_metric_for_station(path, station_number, metric)

# models = ["AGCRN", "TCN", "GWN", "CLCRN"]
# colors = ['#FF0000', 'green', 'blue', 'cyan']  # Make sure to have enough colors for each model

# bar_width = 16000 

# def main():
#     horizon = "24h"

#     df = pd.read_csv("./DataNew/Locations/Locations.csv")

#     fig, ax = plt.subplots(figsize=(8, 8))
    
#     m = Basemap(projection='merc', llcrnrlat=-35, urcrnrlat=-25,
#                 llcrnrlon=15, urcrnrlon=33, resolution='i', ax=ax)
#     m.drawcountries()
#     m.drawcoastlines()
#     m.drawmapboundary(fill_color='white')
#     m.fillcontinents(color='lightgray', lake_color='white')

#     for index, row in df.iterrows():
#         station_number = int(row['Number'])
#         latitude = row['Latitude']
#         longitude = row['Longitude']
#         x, y = m(longitude, latitude)

#         model_metrics = [(model, get_model_metric(model, selected_variable, selected_metric, horizon, station_number)) for model in models]

#         # Normalize the bar sizes
#         metrics = [metric for _, metric in model_metrics if metric is not None]
#         if metrics:  # Check if there are any valid metric values to avoid division by zero
#             average_metric = sum(metrics) / len(metrics)

#             for model_idx, (model, metric) in enumerate(model_metrics):
#                 if metric is not None:
#                     print(str(model_idx) + ":  " + str(metric))
#                     bar_height = (metric / average_metric) * 100000
#                     ax.add_patch(Rectangle((x + model_idx * bar_width - bar_width * len(models) / 2, y), bar_width, bar_height, facecolor=colors[models.index(model)], label=model if index == 0 else ""))

#             plt.text(x + (len(models) - 1) * bar_width, y + bar_height - 0.2, f"{station_number}", fontsize=10)

#     plt.title(f"{selected_variable} - {selected_metric} for all models ({horizon} horizon)", fontsize=16)
#     plt.legend(loc='upper right', fontsize=12)

#     directory = 'Plots'
#     filename = f'bestmodel1_{selected_variable}_{selected_metric}_{horizon}.png'

#     if not os.path.exists(directory):
#         os.makedirs(directory)

#     filepath = os.path.join(directory, filename)
#     fig.savefig(filepath, dpi=300)

# if __name__ == "__main__":
#     main()

import os
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Rectangle

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
colors = ['#FF0000', 'green', 'blue', 'cyan']  # Colors for each model
bar_width = 16000 

def generate_maps():
    horizon = "24h"
    base_directory = './Plots/bestmodels'  # Base directory for all plots

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

            for index, row in df.iterrows():
                station_number = int(row['Number'])
                latitude = row['Latitude']
                longitude = row['Longitude']
                x, y = m(longitude, latitude)
                model_metrics = [(model, get_model_metric(model, selected_variable, selected_metric, horizon, station_number)) for model in models]
                metrics = [metric for _, metric in model_metrics if metric is not None]
                if metrics:
                    average_metric = sum(metrics) / len(metrics)
                    for model_idx, (model, metric) in enumerate(model_metrics):
                        if metric is not None:
                            bar_height = (metric / average_metric) * 100000
                            ax.add_patch(Rectangle((x + model_idx * bar_width - bar_width * len(models) / 2, y), bar_width, bar_height, facecolor=colors[models.index(model)], label=model if index == 0 else ""))

            plt.title(f"{selected_variable} - {selected_metric} for all models ({horizon} horizon)", fontsize=16)
            plt.legend(loc='upper right', fontsize=12)

            filename = f'bestmodel_{selected_metric}_{selected_variable}_{horizon}.png'
            filepath = os.path.join(metric_directory, filename)
            fig.savefig(filepath, dpi=300)
            plt.close(fig)  # Close the figure to free memory

if __name__ == "__main__":
    generate_maps()




