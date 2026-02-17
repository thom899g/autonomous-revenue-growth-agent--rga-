import logging
from typing import Dict, Any
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RGAModule:
    """
    Base class for all RGA modules.
    Implements basic functionality and error handling.
    """
    
    def __init__(self):
        self._data = None
        self._models = {}
        
    @property
    def data(self) -> pd.DataFrame:
        return self._data
    
    @data.setter
    def data(self, value: pd.DataFrame) -> None:
        if not isinstance(value, pd.DataFrame):
            raise ValueError("Data must be a pandas DataFrame.")
        self._data = value
        
    def _train_model(self, model_name: str, features: list, target: str) -> None:
        """
        Train a machine learning model.
        
        Args:
            model_name (str): Name of the model to train.
            features (list): List of feature columns.
            target (str): Target column for prediction.
        """
        if self.data is None:
            raise ValueError("Data not available.")
            
        X = self.data[features]
        y = self.data[target]
        
        # Handle missing data
        if X.isna().any().any():
            logger.warning(f"Missing values found in features: {X.isna().sum()}")
            X = X.dropna()
            
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        
        # Train model
        if model_name not in self._models:
            raise KeyError(f"Model {model_name} does not exist.")
            
        model = self._models[model_name]
        model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        logger.info(f"Model {model_name} trained with accuracy: {accuracy}")