import os
import csv

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

import os
import re

def get_metrics_from_file(file_path):
    """
    Extracts RMSE, MSE, MAE, and SMAPE values from a given file and returns them in a dictionary.
    """
    metrics = {' RMSE': None, ' MSE': None, ' MAE': None, ' SMAPE': None}
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                for metric in metrics.keys():
                    if metric in line.upper():
                        try:
                            # Updated regular expression to match floating point numbers and scientific notation
                            metric_value_search = re.search(r'\b\d+\.\d+([eE][-+]?\d+)?\b', line)
                            if metric_value_search:
                                metric_value = metric_value_search.group(0)
                                metrics[metric] = float(metric_value)
                        except ValueError as e:
                            print(f"Error parsing {metric} from line: '{line.strip()}'. Error: {e}")
    return metrics

def get_model_metrics(station_name, model, split, horizon):
    """
    Constructs the file path based on the model, station, and other parameters to retrieve the metric values.
    """
    if model == 'TCN':
        path = f"./Results/{model}/{horizon} Hour Forecast/{station_name}/metrics/metrics_" + str(split) + ".txt"
    elif model == 'AGCRN':
        path = f"./Results/{model}/{horizon} Hour Forecast/Metrics/attribute0/{station_name}/split_" + str(split) + "_metrics.txt"
    else:
        path = f"./Results/{model}/{horizon} Hour Forecast/Metrics/{station_name}/metrics_" + str(split) + ".txt"

    return get_metrics_from_file(path)

def populate_csv_files(stations, model='TCN', split=0, horizons=[3, 6, 9, 12, 24]):
    """
    Creates a CSV file named metrics_{horizon}h.csv for each metric, weather attribute, and horizon,
    containing all station numbers and their metric values.
    """
    weather_attributes = ["Pressure"]
    metrics = [' RMSE', ' MSE', ' MAE', ' SMAPE']
    base_path = "Metrics/TCN"

    for horizon in horizons:
        for attribute in weather_attributes:
            for metric in metrics:
                # Construct the directory path for the current attribute, metric, and horizon
                dir_path = os.path.join(base_path, attribute, metric)
                # Create directory if it doesn't exist
                os.makedirs(dir_path, exist_ok=True)
                
                # Construct the CSV file name using the new naming convention
                csv_file_name = f"metrics_{horizon}h.csv"
                csv_file_path = os.path.join(dir_path, csv_file_name)

                with open(csv_file_path, 'w', newline='') as csvfile:
                    csv_writer = csv.writer(csvfile)

                    for index, station in enumerate(stations):
                        metrics_values = get_model_metrics(station, model, split, horizon)
                        metric_value = metrics_values[metric]

                        # Format the metric value to ensure it's written in standard decimal format
                        # You can adjust the '.6f' to control the number of decimal places
                        formatted_metric_value = f"{metric_value:.13f}"

                        # Write the station number (index) and formatted metric value in the CSV
                        csv_writer.writerow([index, formatted_metric_value])

                        print(f"Added station number {index} with {metric} value: {formatted_metric_value} to {csv_file_path} for horizon {horizon}h")


# Example usage with a list of stations
stations = ['ADDO ELEPHANT PARK', 'ALEXANDERBAAI', 'ALIWAL-NORTH PLAATKOP', 'BARKLY-OOS (CAERLEON)',
                'BRANDVLEI', 'CALVINIA WO', 'CAPE TOWN WO', 'DE AAR WO', 'DOHNE - AGR', 'EAST LONDON WO',
                'EXCELSIOR CERES', 'FORT BEAUFORT', 'FRASERBURG', 'GEORGE WITFONTEIN', 'GEORGE WO', 
                'GRAAFF - REINET', 'GRAHAMSTOWN', 'KOINGNAAS', 'LADISMITH', 'LAINGSBURG', 'LANGGEWENS',
                'MALMESBURY', 'MOLTENO RESERVOIR','NOUPOORT','OUDTSHOORN', 'PATENSIE','POFADDER', 
                'PORT ALFRED - AIRPORT','PORT ELIZABETH AWOS', 'PORT ELIZABETH AWS','PORT NOLLOTH','PORTERVILLE', 
                'PRIESKA', 'REDELINGSHUYS-AWS','RIVERSDALE','SOMERSET EAST','SPRINGBOK WO','TWEE RIVIEREN',
                'UITENHAGE','UPINGTON WO', 'VANWYKSVLEI','VIOOLSDRIF - AWS','VREDENDAL','WILLOWMORE','WORCESTER-AWS'] # Add more stations as needed
populate_csv_files(stations)



############################################################################
# import csv
# import re

# # Define the horizons, metrics, and attributes
# horizons = [24]
# metrics = ['mae', 'smape', 'rmse', 'mse'] #
# attributes = ['WindSpeed', 'Temperature', 'Humidity', 'Pressure'] #

# # Base path where the files are located
# base_path = '/Users/adeebgaibie/Documents/GitHub/WEATHER-FLOW/Metrics/CLCRN/'

# # Function to process each file
# def process_file(attribute, metric, horizon):
#     # Construct the file path based on attribute, metric, and horizon
#     path = f'{base_path}{attribute}/{metric}/'
#     input_filename = f'{path}stationScore_{horizon}.csv'
#     output_filename = f'{path}metrics_{horizon}h.csv'

#     with open(input_filename, 'r') as infile, open(output_filename, 'w', newline='') as outfile:
#         reader = csv.reader(infile)
#         writer = csv.writer(outfile)

#         # Skip the header row
#         next(reader)

#         for row in reader:
#             # Assuming each row is a string description

#             # Assuming 'row' is a variable you're iterating over, and 'writer' is a csv.writer object
#             row_content = row[0]
#             print(row_content)

#             # Extract station number and score using regex
#             match = re.search(r'station (\d+) : ([\d.]+(?:e-?\d+)?)', row_content)  # Updated regex to match scientific notation
#             if match:
#                 station_number, score = match.groups()
                
#                 # Convert score from scientific notation to float and then format
#                 score_float = float(score)  # Convert score to float to handle scientific notation
#                 formatted_score = "{:.11f}".format(score_float).rstrip('0').rstrip('.')  # Format float with 11 decimal places, then remove trailing zeros and the decimal point if it's an integer

#                 if formatted_score.startswith('0.') or formatted_score == '0':  # Check if formatted score is less than 1
#                     # Ensure the formatted score is displayed with leading zeros after the decimal point
#                     formatted_score = '0' + formatted_score[formatted_score.index('.'):]

#                 print(formatted_score)
#                 writer.writerow([str(int(station_number)-1), formatted_score])


# # Loop through each attribute, metric, and horizon to process files
# for attribute in attributes:
#     for metric in metrics:
#         for horizon in horizons:
#             process_file(attribute, metric, horizon)

# import os
# import pandas as pd

# # Define your current base path
# base_path = '/Users/adeebgaibie/Documents/GitHub/WEATHER-FLOW/Metrics/GWNResults'
# # Define the target base path for the new structure
# target_base_path = '/Users/adeebgaibie/Documents/GitHub/WEATHER-FLOW/Metrics/GWN'

# # Variables, metrics, and horizons as per your requirement
# variables = ['Humidity', 'WindSpeed', 'Temperature', 'Pressure']
# metrics = ['MAE.csv', 'SMAPE.csv', 'RMSE.csv', 'MSE.csv']
# horizons = ['3', '6', '9', '12', '24']

# # Function to create new directory structure and move files
# def rearrange_files():
#     for variable in variables:
#         for metric in metrics:
#             for horizon in horizons:
#                 # Old filename pattern
#                 old_filename_pattern = f"{horizon} Hour Forecast/{variable}/{metric}"
#                 old_file_path = os.path.join(base_path, old_filename_pattern)

#                 # New filename and path
#                 new_directory = os.path.join(target_base_path, variable, metric.split('.')[0])
#                 new_filename = f"metrics_{horizon}h.csv"
#                 new_file_path = os.path.join(new_directory, new_filename)

#                 # Create the directory if it doesn't exist
#                 os.makedirs(new_directory, exist_ok=True)

#                 # Check if the old file exists
#                 if os.path.exists(old_file_path):
#                     # Read the CSV file without skipping any rows
#                     df = pd.read_csv(old_file_path)

#                     # Check if DataFrame is not empty and has more than one row (to exclude average row safely)
#                     if not df.empty and len(df) > 1:
#                         df = df[:-1]  # Remove the last row (average)

#                         # Save the modified DataFrame to the new file path without including the header
#                         df.to_csv(new_file_path, index=False, header=False)
#                         print(f"Processed and moved file to: {new_file_path}")
#                 else:
#                     print(f"File not found: {old_file_path}, skipping...")

# # Execute the function
# rearrange_files()
