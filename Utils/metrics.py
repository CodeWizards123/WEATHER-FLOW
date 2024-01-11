import numpy as np
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
import math

def smape(actual, predicted, epsilon=1e-5):
    """
    Calculates the SMAPE metric
    Parameters:
        actual - target values
        predicted - output values predicted by model
    Returns:
        smape - returns smape metric
    """

    # return np.mean(abs(predicted - actual) / ((abs(predicted) + abs(actual)) / 2)) * 100

    denominator = (np.abs(predicted) + np.abs(actual)) / 2
    # Avoid division by zero
    denominator = np.where(denominator == 0, epsilon, denominator)
    return np.mean(np.abs(predicted - actual) / denominator) * 100

def ZeroAdjustedSMAPE(y_true, y_pred, epsilon=1e-6):
    """
    Calculates the zero-adjusted SMAPE metric
    Parameters:
        y_true - target values
        y_pred - output values predicted by model
        epsilon - small constant to avoid division by zero
    Returns:
        smape - returns zero-adjusted SMAPE metric
    """
    
    denominator = (np.abs(y_true) + np.abs(y_pred) + epsilon) / 2
    smape = np.mean(np.abs(y_pred - y_true) / denominator) * 100
    return smape
              

def mse(target, pred):
    """
    Calculates the MSE metric
    Parameters:
        actual - target values
        predicted - output values predicted by model
    Returns:
        mse - returns MSE metric
    """

    return mean_squared_error(target, pred, squared=True)



def rmse(target, pred):
    """
    Calculates the RMSE metric
    Parameters:
        actual - target values
        predicted - output values predicted by model
    Returns:
        root - returns RMSE metric
    """

    root = math.sqrt(mse(target, pred))
    return root


def mae(target, pred):
    """
    Calculates the MAE metric
    Parameters:
        actual - target values
        predicted - output values predicted by model
    Returns:
        mae - returns MAE metric
    """
    return mean_absolute_error(target, pred)

