# import os
# import csv

# def get_metrics_from_file(file_path):
#     """
#     Extracts RMSE, MSE, MAE, and SMAPE values from a given file and returns them in a dictionary.
#     """
#     metrics = {'RMSE': None, 'MSE': None, 'MAE': None, 'SMAPE': None}
#     if os.path.exists(file_path):
#         with open(file_path, 'r') as file:
#             lines = file.readlines()
#             for line in lines:
#                 for metric in metrics.keys():
#                     if metric in line.upper():
#                         try:
#                             # Attempt to extract the metric value from the line
#                             metric_value = line.split(" ")[4]
#                             metrics[metric] = float(metric_value)
#                         except (IndexError, ValueError) as e:
#                             print(f"Error parsing {metric} from line: '{line.strip()}'. Error: {e}")
#     return metrics

# def get_model_metrics(station_name, model, split, horizon):
#     """
#     Constructs the file path based on the model, station, and other parameters to retrieve the metric values.
#     """
#     if model == 'TCN':
#         path = f"./Results/{model}/{horizon} Hour Forecast/{station_name}/metrics/metrics_" + str(split) + ".txt"
#     elif model == 'AGCRN':
#         path = f"./Results/{model}/{horizon} Hour Forecast/Metrics/attribute0/{station_name}/split_" + str(split) + "_metrics.txt"
#     else:
#         path = f"./Results/{model}/{horizon} Hour Forecast/Metrics/{station_name}/metrics_" + str(split) + ".txt"

#     return get_metrics_from_file(path)

# def populate_csv_files(stations, model='TCN', split=0, horizons=[3, 6, 9, 12, 24]):
#     """
#     Creates a CSV file named metrics_{horizon}h.csv for each metric, weather attribute, and horizon,
#     containing all station numbers and their metric values.
#     """
#     weather_attributes = ["Humidity"]
#     metrics = ['RMSE', 'MSE', 'MAE', 'SMAPE']
#     base_path = "Metrics/TCN"

#     for horizon in horizons:
#         for attribute in weather_attributes:
#             for metric in metrics:
#                 # Construct the directory path for the current attribute, metric, and horizon
#                 dir_path = os.path.join(base_path, attribute, metric)
#                 # Create directory if it doesn't exist
#                 os.makedirs(dir_path, exist_ok=True)
                
#                 # Construct the CSV file name using the new naming convention
#                 csv_file_name = f"metrics_{horizon}h.csv"
#                 csv_file_path = os.path.join(dir_path, csv_file_name)

#                 with open(csv_file_path, 'w', newline='') as csvfile:
#                     csv_writer = csv.writer(csvfile)


#                     for index, station in enumerate(stations):
#                         metrics_values = get_model_metrics(station, model, split, horizon)
#                         metric_value = metrics_values[metric]
#                         # Write the station number (index) and metric value in the CSV
#                         csv_writer.writerow([index, metric_value])

#                         print(f"Added station number {index} with {metric} value: {metric_value} to {csv_file_path} for horizon {horizon}h")

# # Example usage with a list of stations
# stations = ['ADDO ELEPHANT PARK', 'ALEXANDERBAAI', 'ALIWAL-NORTH PLAATKOP', 'BARKLY-OOS (CAERLEON)',
#                 'BRANDVLEI', 'CALVINIA WO', 'CAPE TOWN WO', 'DE AAR WO', 'DOHNE - AGR', 'EAST LONDON WO',
#                 'EXCELSIOR CERES', 'FORT BEAUFORT', 'FRASERBURG', 'GEORGE WITFONTEIN', 'GEORGE WO', 
#                 'GRAAFF - REINET', 'GRAHAMSTOWN', 'KOINGNAAS', 'LADISMITH', 'LAINGSBURG', 'LANGGEWENS',
#                 'MALMESBURY', 'MOLTENO RESERVOIR','NOUPOORT','OUDTSHOORN', 'PATENSIE','POFADDER', 
#                 'PORT ALFRED - AIRPORT','PORT ELIZABETH AWOS', 'PORT ELIZABETH AWS','PORT NOLLOTH','PORTERVILLE', 
#                 'PRIESKA', 'REDELINGSHUYS-AWS','RIVERSDALE','SOMERSET EAST','SPRINGBOK WO','TWEE RIVIEREN',
#                 'UITENHAGE','UPINGTON WO', 'VANWYKSVLEI','VIOOLSDRIF - AWS','VREDENDAL','WILLOWMORE','WORCESTER-AWS'] # Add more stations as needed
# populate_csv_files(stations)



import csv
import re

# Define the horizons, metrics, and attributes
horizons = [24]
metrics = ['mae', 'smape', 'rmse', 'mse']
attributes = ['WindSpeed', 'Temperature', 'Humidity', 'Pressure']

# Base path where the files are located
base_path = '/Users/adeebgaibie/Documents/GitHub/WEATHER-FLOW/Metrics/CLCRN/'

# Function to process each file
def process_file(attribute, metric, horizon):
    # Construct the file path based on attribute, metric, and horizon
    path = f'{base_path}{attribute}/{metric}/'
    input_filename = f'{path}stationScore_{horizon}.csv'
    output_filename = f'{path}metrics_{horizon}h.csv'

    with open(input_filename, 'r') as infile, open(output_filename, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Skip the header row
        next(reader)

        for row in reader:
            # Assuming each row is a string description
            row_content = row[0]

            # Extract station number and score using regex
            match = re.search(r'station (\d+) : ([\d.]+)', row_content)
            if match:
                station_number, score = match.groups()
                writer.writerow([station_number, score])

# Loop through each attribute, metric, and horizon to process files
for attribute in attributes:
    for metric in metrics:
        for horizon in horizons:
            process_file(attribute, metric, horizon)


