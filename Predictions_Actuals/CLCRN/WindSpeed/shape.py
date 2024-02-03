import pickle

# Load data from the pickle file
file_path = 'predictions.pkl'  # Replace 'your_file.pkl' with the actual file path
with open(file_path, 'rb') as file:
    data = pickle.load(file)

# Check the shape of the data

print("Data shape:", data['y_preds'].shape)
# else:
#     print("The loaded data does not have a 'shape' attribute.")
