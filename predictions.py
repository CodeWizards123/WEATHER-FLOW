import os
import shutil

# List of stations
stations = [
    'ADDO ELEPHANT PARK', 'ALEXANDERBAAI', 'ALIWAL-NORTH PLAATKOP', 'BARKLY-OOS (CAERLEON)',
    'BRANDVLEI', 'CALVINIA WO', 'CAPE TOWN WO', 'DE AAR WO', 'DOHNE - AGR', 'EAST LONDON WO',
    'EXCELSIOR CERES', 'FORT BEAUFORT', 'FRASERBURG', 'GEORGE WITFONTEIN', 'GEORGE WO', 
    'GRAAFF - REINET', 'GRAHAMSTOWN', 'KOINGNAAS', 'LADISMITH', 'LAINGSBURG', 'LANGGEWENS',
    'MALMESBURY', 'MOLTENO RESERVOIR', 'NOUPOORT', 'OUDTSHOORN', 'PATENSIE', 'POFADDER', 
    'PORT ALFRED - AIRPORT', 'PORT ELIZABETH AWOS', 'PORT ELIZABETH AWS', 'PORT NOLLOTH', 'PORTERVILLE', 
    'PRIESKA', 'REDELINGSHUYS-AWS', 'RIVERSDALE', 'SOMERSET EAST', 'SPRINGBOK WO', 'TWEE RIVIEREN',
    'UITENHAGE', 'UPINGTON WO', 'VANWYKSVLEI', 'VIOOLSDRIF - AWS', 'VREDENDAL', 'WILLOWMORE', 'WORCESTER-AWS'
]

# List of variables
variables = ['Humidity', 'Temperature', 'Pressure', 'WindSpeed']

base_source_path = '/Users/adeebgaibie/Documents/GitHub/WEATHER-FLOW/TCN_v1'
base_destination_path = '/Users/adeebgaibie/Documents/GitHub/WEATHER-FLOW/Predictions_Actuals/TCN'

# Loop through each variable
for variable in variables:
    # Loop through each station
    for station in stations:
        # Construct the source file path
        source_file_path = f'{base_source_path}/{variable}/24 Hour Forecast/{station}/Predictions/result_unnormalised_0.csv'
        
        # Construct the destination directory path
        destination_dir_path = f'{base_destination_path}/{variable}'
        
        # Ensure the destination directory exists
        os.makedirs(destination_dir_path, exist_ok=True)
        
        # Construct the destination file path
        destination_file_path = os.path.join(destination_dir_path, f'{station}_result_unnormalised_0.csv')
        
        # Copy the file from the source to the destination
        if os.path.exists(source_file_path):
            shutil.copy(source_file_path, destination_file_path)
            print(f'File copied for {station} in {variable}')
        else:
            print(f'File not found: {source_file_path}')

print('All files have been copied successfully.')
