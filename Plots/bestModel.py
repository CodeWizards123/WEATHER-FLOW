import os
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
from matplotlib.patches import Rectangle

def get_smape_from_file(file_path):
    if os.path.exists(file_path): 
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                if "rmse:" in line:
                    return float(line.split(":")[1].strip())
                elif  "RMSE" in line:
                    return float(line.split("RMSE")[1].strip())
                
    return None

def get_model_smape(station_name, model, split, horizon):
    if model=='TCN':
        path = f"./Results/{model}/{horizon} Hour Forecast/{station_name}/metrics/metrics_" + str(split) + ".txt"
    elif model=='AGCRN':
        path = f"./Results/{model}/{horizon} Hour Forecast/Metrics/attribute0/{station_name}/split_" + str(split) + "_metrics.txt"
    else:
        path = f"./Results/{model}/{horizon} Hour Forecast/Metrics/{station_name}/metrics_" + str(split) + ".txt"

    return get_smape_from_file(path)




models = ["AGCRN", "TCN"]

colors = ['#FF0000', 'green']

bar_width = 16000 
exaggeration_power = 1 

def main():
    split = 0
    horizon = 24

    df = pd.read_csv("./DataNew/Locations/Locations.csv")

    fig, ax = plt.subplots(figsize=(8, 8))
    
    m = Basemap(projection='merc', llcrnrlat=-35, urcrnrlat=-25,
                llcrnrlon=15, urcrnrlon=33, resolution='i', ax=ax)
    m.drawcountries()
    m.drawcoastlines()
    m.drawmapboundary(fill_color='white')
    m.fillcontinents(color='lightgray', lake_color='white')

    for index, row in df.iterrows():
        station_number = row['Number']
        station_name = row['StasName']
        latitude = row['Latitude']
        longitude = row['Longitude']
        x, y = m(longitude, latitude)

        model_smapes = [(model_to_plot, get_model_smape(station_name, model_to_plot, split, horizon)) for model_to_plot in models]

        #normalise the bar sizes
        total_smape = 0
        for model_idx, (model_to_plot, smape) in enumerate(model_smapes):

            total_smape += smape
        average_smape = total_smape / len(model_smapes)


        for model_idx, (model_to_plot, smape) in enumerate(model_smapes):
            if smape is not None:
                bar_height = ((smape/average_smape))*100000
                ax.add_patch(Rectangle((x + model_idx * bar_width - bar_width * len(models) / 2, y), bar_width, bar_height, facecolor=colors[models.index(model_to_plot)], label=model_to_plot if index == 0 else ""))

        plt.text(x + (len(models) - 1) * bar_width, y + bar_height-0.2, f"{station_number}", fontsize=10)

    plt.title(f"All models {horizon} hour horizon", fontsize=16)    

    plt.legend(loc='upper right', fontsize=12)

    directory = 'Plots'
    filename = f'bestmodel.png'

    if not os.path.exists(directory):
        os.makedirs(directory)

    filepath = os.path.join(directory, filename)
    fig.savefig(filepath, dpi=300)

if __name__ == "__main__":
    main()







