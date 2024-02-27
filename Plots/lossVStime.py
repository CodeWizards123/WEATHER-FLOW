# Helper functions
import pickle

def load_pickle(pickle_file):
    """
    Loads data from a pickle file

    Parameters:
        pickle_file - file to read
    Returns:
        pickle_data - returns data read from pickle file
    """

    try:
        with open(pickle_file, 'rb') as f:
            pickle_data = pickle.load(f)
    except UnicodeDecodeError as e:
        with open(pickle_file, 'rb') as f:
            pickle_data = pickle.load(f, encoding='latin1')
    except Exception as e:
        print('Unable to load data ', pickle_file, ':', e)
        raise
    return pickle_data

class NormScaler:
    """
    Creates a scaler object that performs MinMax scaling on a data set
    """

    def __init__(self, min, max):
        self.min = min
        self.max = max

    def transform(self, data):
        return (data - self.min) / (self.max - self.min)

    def inverse_transform(self, data):
        return data



# Code to plot all loss vs time
import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
import matplotlib.dates as mdates


def extract_dates_from_csv(file_path, split_start, split_end):
    # Load the CSV using pandas
    df = pd.read_csv(file_path)
    # Extract dates from split_start to split_end
    dates = df['DateT'].iloc[split_start:split_end].tolist()
    return dates


def get_tcn_loss(target_file, pred_file):
    target_df = pd.read_csv(target_file, header=None, names=["index", "value"])

    # Extract every 24th value from the "value" column of target_df
    target_values = target_df["value"].iloc[::24].values

    pred_df = pd.read_csv(pred_file, header=None, names=["index", "value"])

    # Extract every 24th value from the "value" column of pred_df
    pred_values = pred_df["value"].iloc[::24].values

    # Ensure that the arrays are of the same length before computing the difference

    return abs(target_values - pred_values)



def visualize_results(horizon, k, stations):
    #[79750, 96839, 113929]
    # x=8760
    split_start=  96839  #61320+47
    split_end=  96839+17000 #70080
    csv_file_path = "/Users/adeebgaibie/Documents/GitHub/WEATHER-FLOW/DataNew/Weather Station Data/ADDO ELEPHANT PARK.csv"  # Replace this with your actual CSV file path
    dates = extract_dates_from_csv(csv_file_path, split_start, split_end)

    # Convert the date strings to pandas datetime objects
    dates_datetime = pd.to_datetime(dates)
    

    results_file_tcn = f'Results/TCN/{horizon} Hour Forecast/ADDO ELEPHANT PARK/Predictions/result_{k}.csv'
    targets_file_tcn = f'Results/TCN/{horizon} Hour Forecast/ADDO ELEPHANT PARK/Targets/target_{k}.csv'

    loss_tcn = get_tcn_loss(targets_file_tcn, results_file_tcn)

    all_losses = [loss_tcn]
    for station in stations[1:]:
        results_file_tcn_station = f'Results/TCN/{horizon} Hour Forecast/{station}/Predictions/result_{k}.csv'
        targets_file_tcn_station = f'Results/TCN/{horizon} Hour Forecast/{station}/Targets/target_{k}.csv'
        loss_tcn_station = get_tcn_loss(targets_file_tcn_station, results_file_tcn_station)
        all_losses.append(loss_tcn_station)
    
    average_loss_tcn = np.mean(all_losses, axis=0)
    df_tcn = pd.DataFrame(average_loss_tcn, columns=["avg_loss_tcn"])
    df_tcn['moving_avg_loss_tcn'] = df_tcn['avg_loss_tcn'].rolling(window=168, center=True).mean()

    
    fileDictionary = {
        'predFile': 'Results/AGCRN/' + str(horizon) + ' Hour Forecast/Predictions/outputs_' + str(k),
        'targetFile': 'Results/AGCRN/' + str(horizon) + ' Hour Forecast/Targets/targets_' + str(k),
        # ... [rest of your dictionary items]
    }


    y_pred = np.load(fileDictionary["predFile"] + ".npy")
    y_true = np.load(fileDictionary["targetFile"] + ".npy")

    #    normalise AGCRN data
    # scaler = NormScaler(-11, 47)
    # # scaler = utils.NormScaler(y_trueO.min(), y_trueO.max())
    # y_true = scaler.transform(y_true)
    # y_pred = scaler.transform(y_pred)

    station_pred = y_pred[:17000, 23, :, 0]
    station_true = y_true[:17000, 23, :, 0]
    print("AGCRN Shape")
    print(station_pred.shape)

     # AGCRN loss computation
    loss_agcrn = abs(station_true - station_pred)
    loss_agcrn = np.mean(loss_agcrn, axis=(1))
    df_agcrn = pd.DataFrame(loss_agcrn, columns=["loss_agcrn"])
    df_agcrn['moving_avg_loss_agcrn'] = df_agcrn['loss_agcrn'].rolling(window=168, center=True).mean()
    

    # Define paths for GWN's results and targets
    results_file_gwn = 'Results/GWN/' + str(horizon) + ' Hour Forecast/Predictions/outputs_' + str(k) + '.pkl'
    targets_file_gwn = 'Results/GWN/' + str(horizon) + ' Hour Forecast/Targets/targets_' + str(k) + '.pkl'

    # Use utility function to load the pickled data
    yhat_gwn = load_pickle(results_file_gwn)
    target_gwn = load_pickle(targets_file_gwn)
    
    pred_gwn = np.array(yhat_gwn).reshape((267*64, 45, 24))[:17000, :, 23]
    print("GWN shape")
    print(pred_gwn.shape)
    real_gwn = np.array(target_gwn).reshape((267*64, 45, 24))[:17000, :, 23]
    

    # Compute the loss and sum it across the 45 dimensions
    loss_gwn = abs(real_gwn - pred_gwn).mean(axis=1)

    df_gwn = pd.DataFrame(loss_gwn, columns=["loss_gwn"])
    df_gwn['moving_avg_loss_gwn'] = df_gwn['loss_gwn'].rolling(window=168, center=True).mean()

    
    # Plotting
    plt.figure(figsize=(15, 6))
    
    # Create the main axis
    ax1 = plt.gca()

    # Plot AGCRN loss on ax1
    color = 'tab:red'
    ax1.set_xlabel("Date", fontsize=20)
    ax1.set_ylabel("Loss", fontsize=20)
    ax1.plot(dates_datetime, df_agcrn['moving_avg_loss_agcrn'], label="AGCRN loss", color=color)
    
    # Plot GWN loss on ax1
    ax1.plot(dates_datetime, df_gwn['moving_avg_loss_gwn'], label="GWN loss", color='tab:blue')
    ax1.tick_params(axis='y', labelsize=20)
    ax1.tick_params(axis='x', labelsize=20)


    # Add TCN loss to the plot
    ax1.plot(dates_datetime, df_tcn['moving_avg_loss_tcn'][:17000], label="TCN loss", color='tab:green')

    ax1.xaxis.set_major_locator(mdates.MonthLocator())

    plt.xticks(rotation=45) 


    # Create legend for both losses
    fontsize_legend = 20 
    ax1.legend(loc=2, fontsize=fontsize_legend)

    plt.tight_layout()

    directory = f"./Plots/Comparison/{str(horizon)} Hour Forecast/Plots/station_{stations[0]}_loss_plot.png"
    if not os.path.exists(directory):
        os.makedirs(directory)
    plt.show()

    plt.savefig(directory) 


def main():
    horizon = 24
    k = 0  
    stations = ['ADDO ELEPHANT PARK', 'ALEXANDERBAAI', 'ALIWAL-NORTH PLAATKOP', 'BARKLY-OOS (CAERLEON)',
                'BRANDVLEI', 'CALVINIA WO', 'CAPE TOWN WO', 'DE AAR WO', 'DOHNE - AGR', 'EAST LONDON WO',
                'EXCELSIOR CERES', 'FORT BEAUFORT', 'FRASERBURG', 'GEORGE WITFONTEIN', 'GEORGE WO', 
                'GRAAFF - REINET', 'GRAHAMSTOWN', 'KOINGNAAS', 'LADISMITH', 'LAINGSBURG', 'LANGGEWENS',
                'MALMESBURY', 'MOLTENO RESERVOIR','NOUPOORT','OUDTSHOORN', 'PATENSIE','POFADDER', 
                'PORT ALFRED - AIRPORT','PORT ELIZABETH AWOS', 'PORT ELIZABETH AWS','PORT NOLLOTH','PORTERVILLE', 
                'PRIESKA', 'REDELINGSHUYS-AWS','RIVERSDALE','SOMERSET EAST','SPRINGBOK WO','TWEE RIVIEREN',
                'UITENHAGE','UPINGTON WO', 'VANWYKSVLEI','VIOOLSDRIF - AWS','VREDENDAL','WILLOWMORE','WORCESTER-AWS']
    visualize_results(horizon, k, stations)

if __name__ == "__main__":
    main()






import pickle

def load_pickle(pickle_file):
    """
    Loads data from a pickle file

    Parameters:
        pickle_file - file to read
    Returns:
        pickle_data - returns data read from pickle file
    """

    try:
        with open(pickle_file, 'rb') as f:
            pickle_data = pickle.load(f)
    except UnicodeDecodeError as e:
        with open(pickle_file, 'rb') as f:
            pickle_data = pickle.load(f, encoding='latin1')
    except Exception as e:
        print('Unable to load data ', pickle_file, ':', e)
        raise
    return pickle_data

class NormScaler:
    """
    Creates a scaler object that performs MinMax scaling on a data set
    """

    def __init__(self, min, max):
        self.min = min
        self.max = max

    def transform(self, data):
        return (data - self.min) / (self.max - self.min)

    def inverse_transform(self, data):
        return data




# #standard deviations

# import numpy as np
# import matplotlib.pyplot as plt
# import os
# import pandas as pd
# import matplotlib.dates as mdates


# def extract_dates_from_csv(file_path, split_start, split_end):
#     # Load the CSV using pandas
#     df = pd.read_csv(file_path)
#     # Extract dates from split_start to split_end
#     dates = df['DateT'].iloc[split_start:split_end].tolist()
#     return dates


# def get_tcn_loss(target_file, pred_file):
#     target_df = pd.read_csv(target_file, header=None, names=["index", "value"])

#     # Extract every 24th value from the "value" column of target_df
#     target_values = target_df["value"].iloc[::24].values

#     pred_df = pd.read_csv(pred_file, header=None, names=["index", "value"])

#     # Extract every 24th value from the "value" column of pred_df
#     pred_values = pred_df["value"].iloc[::24].values

#     # Ensure that the arrays are of the same length before computing the difference

#     return abs(target_values - pred_values)



# def visualize_results(horizon, k, stations):
#     #[79750, 96839, 113929]
#     split_start=  96839 
#     split_end=  96839+17000 
#     csv_file_path = "/Users/adeebgaibie/Documents/GitHub/WEATHER-FLOW/DataNew/Weather Station Data/ADDO ELEPHANT PARK.csv"  # Replace this with your actual CSV file path
#     dates = extract_dates_from_csv(csv_file_path, split_start, split_end)

#     # Convert the date strings to pandas datetime objects
#     dates_datetime = pd.to_datetime(dates)
    
#     results_file_tcn = f'Results/TCN/{horizon} Hour Forecast/ADDO ELEPHANT PARK/Predictions/result_{k}.csv'
#     targets_file_tcn = f'Results/TCN/{horizon} Hour Forecast/ADDO ELEPHANT PARK/Targets/target_{k}.csv'

#     loss_tcn = get_tcn_loss(targets_file_tcn, results_file_tcn)

#     all_losses = [loss_tcn]
#     for station in stations[1:]:
#         results_file_tcn_station = f'Results/TCN/{horizon} Hour Forecast/{station}/Predictions/result_{k}.csv'
#         targets_file_tcn_station = f'Results/TCN/{horizon} Hour Forecast/{station}/Targets/target_{k}.csv'
#         loss_tcn_station = get_tcn_loss(targets_file_tcn_station, results_file_tcn_station)
#         all_losses.append(loss_tcn_station)
    
#     average_loss_tcn = np.mean(all_losses, axis=0)
#     df_tcn = pd.DataFrame(average_loss_tcn, columns=["avg_loss_tcn"])
#     df_tcn['moving_avg_loss_tcn'] = df_tcn['avg_loss_tcn'].rolling(window=168, center=True).mean()

    

#     # Define paths for GWN's results and targets
#     results_file_gwn = 'Results/GWN/' + str(horizon) + ' Hour Forecast/Predictions/outputs_' + str(k) + '.pkl'
#     targets_file_gwn = 'Results/GWN/' + str(horizon) + ' Hour Forecast/Targets/targets_' + str(k) + '.pkl'

#     # Use utility function to load the pickled data
#     yhat_gwn = load_pickle(results_file_gwn)
#     target_gwn = load_pickle(targets_file_gwn)
    
#     pred_gwn = np.array(yhat_gwn).reshape((267*64, 45, 24))[:17000, :, 23]
#     print("GWN shape")
#     print(pred_gwn.shape)
#     real_gwn = np.array(target_gwn).reshape((267*64, 45, 24))[:17000, :, 23]
    
#     # Compute the loss and sum it across the 45 dimensions
#     loss_gwn = abs(real_gwn).mean(axis=1)

#     # Now, the shape of loss_gwn will be (8760,)
#     df_gwn = pd.DataFrame(loss_gwn, columns=["loss_gwn"])
#     df_gwn['moving_avg_loss_gwn'] = df_gwn['loss_gwn'].rolling(window=300, center=True).std()


#     # Plotting
#     plt.figure(figsize=(15, 6))
    
#     # Create the main axis
#     ax1 = plt.gca()

#     # # Plot AGCRN loss on ax1
#     color = 'tab:red'
#     ax1.set_xlabel("Date", fontsize=20)
#     ax1.set_ylabel("Std", fontsize=20)
#     # ax1.plot(dates_datetime, df_agcrn['moving_avg_loss_agcrn'], label="AGCRN loss", color=color)
    
#     # Plot GWN loss on ax1
#     ax1.plot(dates_datetime, df_gwn['moving_avg_loss_gwn'], label="std of actauls", color='tab:blue')
#     ax1.tick_params(axis='y', labelsize=20)
#     ax1.tick_params(axis='x', labelsize=20)


#     # Create legend for both losses
#     fontsize_legend = 20  # Size for legend labels
#     ax1.legend(loc=2, fontsize=fontsize_legend)

#     plt.tight_layout()

#     directory = f"./Plots/Comparison/{str(horizon)} Hour Forecast/Plots/station_{stations[0]}_loss_plot.png"
#     if not os.path.exists(directory):
#         os.makedirs(directory)
#     plt.show()

#     plt.savefig(directory) 


# def main():
#     horizon = 24
#     k = 0  
#     stations = ['ADDO ELEPHANT PARK', 'ALEXANDERBAAI', 'ALIWAL-NORTH PLAATKOP', 'BARKLY-OOS (CAERLEON)',
#                 'BRANDVLEI', 'CALVINIA WO', 'CAPE TOWN WO', 'DE AAR WO', 'DOHNE - AGR', 'EAST LONDON WO',
#                 'EXCELSIOR CERES', 'FORT BEAUFORT', 'FRASERBURG', 'GEORGE WITFONTEIN', 'GEORGE WO', 
#                 'GRAAFF - REINET', 'GRAHAMSTOWN', 'KOINGNAAS', 'LADISMITH', 'LAINGSBURG', 'LANGGEWENS',
#                 'MALMESBURY', 'MOLTENO RESERVOIR','NOUPOORT','OUDTSHOORN', 'PATENSIE','POFADDER', 
#                 'PORT ALFRED - AIRPORT','PORT ELIZABETH AWOS', 'PORT ELIZABETH AWS','PORT NOLLOTH','PORTERVILLE', 
#                 'PRIESKA', 'REDELINGSHUYS-AWS','RIVERSDALE','SOMERSET EAST','SPRINGBOK WO','TWEE RIVIEREN',
#                 'UITENHAGE','UPINGTON WO', 'VANWYKSVLEI','VIOOLSDRIF - AWS','VREDENDAL','WILLOWMORE','WORCESTER-AWS']
#     visualize_results(horizon, k, stations)

# if __name__ == "__main__":
#     main()












