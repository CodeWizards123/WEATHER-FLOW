# import numpy as np
# import matplotlib.pyplot as plt
# import pandas as pd

# # Load the actual and predicted values
# path_to_actuals = '/Users/adeebgaibie/Documents/GitHub/WEATHER-FLOW/Predictions_Actuals/AGCRN/Temperature/targets_unnormalised_0.npy'
# path_to_predictions = '/Users/adeebgaibie/Documents/GitHub/WEATHER-FLOW/Predictions_Actuals/AGCRN/Temperature/output_unnormaliseds_0.npy'

# actual_values = np.load(path_to_actuals)
# predicted_values = np.load(path_to_predictions)

# # Extract the first element from the 2nd and 3rd dimensions
# actual_values = actual_values[:, 0, 0, 0]  # Assuming you want the first element from the 2nd and 3rd dimensions
# predicted_values = predicted_values[:, 0, 0, 0]

# # Generate hourly time array starting from Jan 1st 00:00
# time = pd.date_range(start='2023-01-01 00:00', periods=len(actual_values), freq='H')

# # Plotting
# plt.figure(figsize=(10, 6))
# plt.plot(time, actual_values, label='Actual Values', marker='o')
# plt.plot(time, predicted_values, label='Predicted Values', marker='x')

# plt.title('Actual vs Predicted Values')
# plt.xlabel('Time')
# plt.ylabel('Value')
# plt.legend()
# plt.xticks(rotation=45)  # Rotate date labels for better readability
# plt.grid(True)
# plt.tight_layout()  # Adjust layout to not cut off labels
# plt.show()


# import numpy as np
# import matplotlib.pyplot as plt
# import pandas as pd
# import pickle

# # Load the actual values and AGCRN predictions
# path_to_actuals = '/Users/adeebgaibie/Documents/GitHub/WEATHER-FLOW/Predictions_Actuals/AGCRN/Temperature/targets_unnormalised_0.npy'
# path_to_agcrn_predictions = '/Users/adeebgaibie/Documents/GitHub/WEATHER-FLOW/Predictions_Actuals/AGCRN/Temperature/output_unnormaliseds_0.npy'

# actual_values = np.load(path_to_actuals)
# agcrn_predictions = np.load(path_to_agcrn_predictions)

# # Extract the first element from the 2nd and 3rd dimensions for AGCRN predictions
# actual_values = actual_values[:, 0, 0, 0]  # Assuming you want the first element
# agcrn_predictions = agcrn_predictions[:, 0, 0, 0]

# # Load the GWN predictions
# path_to_gwn_predictions = '/Users/adeebgaibie/Documents/GitHub/WEATHER-FLOW/Predictions_Actuals/GWN/Temperature/24 Hour Forecast/predictions.pkl'
# with open(path_to_gwn_predictions, 'rb') as file:
#     gwn_predictions = pickle.load(file)

# # Assuming GWN predictions need similar extraction, adjust as necessary
# gwn_predictions = gwn_predictions[14:, 0, 0, 0]

# # Generate hourly time array starting from Jan 1st 00:00
# time = pd.date_range(start='2023-01-01 00:00', periods=len(actual_values), freq='H')

# # Plotting
# plt.figure(figsize=(12, 7))
# plt.plot(time, actual_values, label='Actual Values', marker='o', linestyle='-')
# plt.plot(time, agcrn_predictions, label='AGCRN Predictions', marker='x', linestyle='--')
# plt.plot(time, gwn_predictions, label='GWN Predictions', marker='^', linestyle=':')

# plt.title('Actual vs Predicted Values')
# plt.xlabel('Time')
# plt.ylabel('Value')
# plt.legend()
# plt.xticks(rotation=45)  # Rotate date labels for better readability
# plt.grid(True)
# plt.tight_layout()  # Adjust layout to not cut off labels
# plt.show()


# import numpy as np
# import matplotlib.pyplot as plt
# import pandas as pd
# import pickle

# # Load the actual values and AGCRN predictions
# path_to_actuals = '/Users/adeebgaibie/Documents/GitHub/WEATHER-FLOW/Predictions_Actuals/AGCRN/Temperature/targets_unnormalised_0.npy'
# path_to_agcrn_predictions = '/Users/adeebgaibie/Documents/GitHub/WEATHER-FLOW/Predictions_Actuals/AGCRN/Temperature/output_unnormaliseds_0.npy'

# actual_values = np.load(path_to_actuals)
# agcrn_predictions = np.load(path_to_agcrn_predictions)

# # Extract the first element from the 2nd and 3rd dimensions for AGCRN predictions
# actual_values = actual_values[:8666, 0, 0, 0]  # Assuming you want the first element
# agcrn_predictions = agcrn_predictions[:8666, 0, 0, 0]

# # Load the GWN predictions
# path_to_gwn_predictions = '/Users/adeebgaibie/Documents/GitHub/WEATHER-FLOW/Predictions_Actuals/GWN/Temperature/24 Hour Forecast/predictions.pkl'
# with open(path_to_gwn_predictions, 'rb') as file:
#     gwn_predictions = pickle.load(file)

# # Assuming GWN predictions need similar extraction
# gwn_predictions = gwn_predictions[:8666, 0, 0, 0]

# # Load the TCN predictions
# path_to_tcn_predictions = '/Users/adeebgaibie/Documents/GitHub/WEATHER-FLOW/Predictions_Actuals/TCN/Temperature/ADDO ELEPHANT PARK_result_unnormalised_0.csv'
# tcn_predictions_df = pd.read_csv(path_to_tcn_predictions, header=None)
# tcn_predictions = tcn_predictions_df.iloc[:, 1].values  # Assuming the predictions are in the second column

# # Extract every 24th value from the TCN predictions
# tcn_predictions = tcn_predictions[::24]

# # Generate hourly time array starting from Jan 1st 00:00
# time = pd.date_range(start='2023-01-01 00:00', periods=len(actual_values), freq='H')

# # Plotting
# plt.figure(figsize=(12, 7))
# plt.plot(time, actual_values, label='Actual Values', marker='o', linestyle='-')
# plt.plot(time, agcrn_predictions, label='AGCRN Predictions', marker='x', linestyle='--')
# plt.plot(time, gwn_predictions, label='GWN Predictions', marker='^', linestyle=':')
# plt.plot(time, tcn_predictions, label='TCN Predictions', marker='s', linestyle='-.')

# plt.title('Actual vs Predicted Values')
# plt.xlabel('Time')
# plt.ylabel('Value')
# plt.legend()
# plt.xticks(rotation=45)  # Rotate date labels for better readability
# plt.grid(True)
# plt.tight_layout()  # Adjust layout to not cut off labels
# plt.show()




###############################





# import numpy as np
# import matplotlib.pyplot as plt
# import pandas as pd

# # Load the actual values and AGCRN predictions
# path_to_actuals_agcrn = '/Users/adeebgaibie/Documents/GitHub/WEATHER-FLOW/Predictions_Actuals/AGCRN/Temperature/targets_unnormalised_0.npy'
# path_to_agcrn_predictions = '/Users/adeebgaibie/Documents/GitHub/WEATHER-FLOW/Predictions_Actuals/AGCRN/Temperature/output_unnormaliseds_0.npy'

# actual_values_agcrn = np.load(path_to_actuals_agcrn)
# agcrn_predictions = np.load(path_to_agcrn_predictions)

# # Extract the first element from the 2nd and 3rd dimensions for AGCRN predictions
# actual_values_agcrn = actual_values_agcrn[:, 0, 0, 0]
# agcrn_predictions = agcrn_predictions[:, 0, 0, 0]

# # Load the TCN actuals and predictions
# path_to_tcn_actuals = '/Users/adeebgaibie/Documents/GitHub/WEATHER-FLOW/Predictions_Actuals/TCN/Temperature/target_unnormalised_0.csv'
# path_to_tcn_predictions = '/Users/adeebgaibie/Documents/GitHub/WEATHER-FLOW/Predictions_Actuals/TCN/Temperature/result_unnormalised_0.csv'

# tcn_actuals_df = pd.read_csv(path_to_tcn_actuals, header=None)
# print('actual')
# print(tcn_actuals_df.shape)
# tcn_predictions_df = pd.read_csv(path_to_tcn_predictions, header=None)
# print('preds')
# print(tcn_predictions_df.shape)
# tcn_actuals = tcn_actuals_df.iloc[:, 1].values  # Assuming the actuals are in the second column
# tcn_predictions = tcn_predictions_df.iloc[:, 1].values

# # Extract every 24th value to match the prediction frequency
# tcn_actuals = tcn_actuals[::]
# tcn_predictions = tcn_predictions[::]

# # Generate hourly time array starting from Jan 1st 00:00 for AGCRN
# time_agcrn = pd.date_range(start='2023-01-01 00:00', periods=len(actual_values_agcrn), freq='H')

# # Plot for AGCRN
# plt.figure(figsize=(12, 7))
# plt.plot(time_agcrn, actual_values_agcrn, label='Actual Values', marker='o', linestyle='-')
# plt.plot(time_agcrn, agcrn_predictions, label='AGCRN Predictions', marker='x', linestyle='--')

# plt.title('AGCRN Actual vs Predicted Values')
# plt.xlabel('Time')
# plt.ylabel('Value')
# plt.legend()
# plt.xticks(rotation=45)
# plt.grid(True)
# plt.tight_layout()
# plt.show()

# # Generate hourly time array starting from Jan 1st 00:00 for TCN (assuming the same length as tcn_actuals)
# time_tcn = pd.date_range(start='2023-01-01 00:00', periods=len(tcn_actuals), freq='H')

# # Plot for TCN
# plt.figure(figsize=(12, 7))
# plt.plot(time_tcn[:8666], tcn_actuals[:8666], label='Actual Values', marker='o', linestyle='-')
# plt.plot(time_tcn[:8666], tcn_predictions[:8666], label='TCN Predictions', marker='x', linestyle='--')
 
# plt.title('TCN Actual vs Predicted Values')
# plt.xlabel('Time')
# plt.ylabel('Value')
# plt.legend()
# plt.xticks(rotation=45)
# plt.grid(True)
# plt.tight_layout()
# plt.show()



###################################



# import numpy as np
# import matplotlib.pyplot as plt
# import pandas as pd
# import pickle  # For loading the CLCRN predictions

# # Load the actual values and AGCRN predictions
# path_to_actuals_agcrn = '/Users/adeebgaibie/Documents/GitHub/WEATHER-FLOW/Predictions_Actuals/AGCRN/Temperature/targets_unnormalised_0.npy'
# path_to_agcrn_predictions = '/Users/adeebgaibie/Documents/GitHub/WEATHER-FLOW/Predictions_Actuals/AGCRN/Temperature/output_unnormaliseds_0.npy'

# actual_values_agcrn = np.load(path_to_actuals_agcrn)
# agcrn_predictions = np.load(path_to_agcrn_predictions)

# # Extract the first element from the 2nd and 3rd dimensions for AGCRN predictions
# actual_values_agcrn = actual_values_agcrn[:, 0, 0, 0]
# agcrn_predictions = agcrn_predictions[:, 0, 0, 0]

# # Load the CLCRN predictions
# path_to_clcrn_predictions = '/Users/adeebgaibie/Documents/GitHub/WEATHER-FLOW/Predictions_Actuals/CLCRN/Temperature/predictions.pkl'
# with open(path_to_clcrn_predictions, 'rb') as f:
#     clcrn_predictions = pickle.load(f)

# # Assuming the CLCRN predictions are structured similarly, extract the relevant values
# # Update this line if the CLCRN predictions structure is different
# print("boog")


# clcrn_predictions = clcrn_predictions['y_preds'][:8690]

# clcrn_predictions = clcrn_predictions[:, 0, 0, 0]  # Update this line as necessary

# # Generate hourly time array starting from Jan 1st 00:00 for AGCRN and CLCRN
# time_agcrn_clcrn = pd.date_range(start='2023-01-01 00:00', periods=len(actual_values_agcrn), freq='H')
# print(time_agcrn_clcrn.shape)
# # Plot for AGCRN and CLCRN
# plt.figure(figsize=(12, 7))
# plt.plot(time_agcrn_clcrn, actual_values_agcrn, label='Actual Values', marker='o', linestyle='-')
# plt.plot(time_agcrn_clcrn, agcrn_predictions, label='AGCRN Predictions', marker='x', linestyle='--')
# plt.plot(time_agcrn_clcrn, clcrn_predictions, label='CLCRN Predictions', marker='s', linestyle='-.')  # Added CLCRN

# plt.title('AGCRN and CLCRN Actual vs Predicted Values')
# plt.xlabel('Time')
# plt.ylabel('Value')
# plt.legend()
# plt.xticks(rotation=45)
# plt.grid(True)
# plt.tight_layout()
# plt.show()


##################################




import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle  # For loading the CLCRN predictions

# Load the actual values and AGCRN predictions
path_to_actuals_agcrn = '/Users/adeebgaibie/Documents/GitHub/WEATHER-FLOW/Predictions_Actuals/AGCRN/Temperature/targets_unnormalised_0.npy'
path_to_agcrn_predictions = '/Users/adeebgaibie/Documents/GitHub/WEATHER-FLOW/Predictions_Actuals/AGCRN/Temperature/output_unnormaliseds_0.npy'

actual_values_agcrn = np.load(path_to_actuals_agcrn)
agcrn_predictions = np.load(path_to_agcrn_predictions)

# Extract the first element from the 2nd and 3rd dimensions for AGCRN predictions
actual_values_agcrn = actual_values_agcrn[:, 0, 13, 0]
agcrn_predictions = agcrn_predictions[:, 0, 13, 0]

# Load the CLCRN predictions
path_to_clcrn_predictions = '/Users/adeebgaibie/Documents/GitHub/WEATHER-FLOW/Predictions_Actuals/CLCRN/Temperature/predictions.pkl'
with open(path_to_clcrn_predictions, 'rb') as f:
    clcrn_predictions = pickle.load(f)

# Assuming the CLCRN predictions are structured similarly, extract the relevant values
clcrn_predictions = clcrn_predictions['y_preds'][:len(actual_values_agcrn)]
clcrn_predictions = clcrn_predictions[:, 0, 13, 0]  # Adjust this line if necessary

# Generate hourly time array starting from Jan 1st 00:00 for AGCRN and CLCRN
time_agcrn_clcrn = pd.date_range(start='2023-01-01 00:00', periods=len(actual_values_agcrn), freq='H')

plt.figure(figsize=(12, 7))

# Actual Values with solid line and thicker width, no transparency needed


# CLCRN Predictions with dotted line and markers
plt.plot(time_agcrn_clcrn, clcrn_predictions, label='CLCRN Predictions', linestyle='-', marker='x', markersize=2, color='blue', linewidth=2)

# AGCRN Predictions with dashed line and markers
plt.plot(time_agcrn_clcrn, agcrn_predictions, label='AGCRN Predictions', linestyle='-', marker='x', markersize=2, color='red')

plt.plot(time_agcrn_clcrn, actual_values_agcrn, label='Actual Values', linestyle='-', color='grey')

plt.title('AGCRN and CLCRN Actual vs Predicted Temperature Values')
plt.xlabel('Time')
plt.ylabel('Temperature')
plt.legend()
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()
