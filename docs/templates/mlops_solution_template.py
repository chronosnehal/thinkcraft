#!/usr/bin/env python3
"""
[Problem Title] - MLOps Solution Implementation

Description: [Brief description of the ML/MLOps solution]

This solution demonstrates ML model training, evaluation, and deployment patterns.

Time Complexity: O(?) - Training complexity
Space Complexity: O(?) - Model and data size

Dependencies: scikit-learn, pandas, numpy
Author: chronosnehal
Date: [YYYY-MM-DD]
"""

from typing import Any, Dict, List, Optional, Tuple
import logging
import numpy as np
import pandas as pd
from dataclasses import dataclass

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class ModelConfig:
    """Configuration for model training."""
    model_type: str
    hyperparameters: Dict[str, Any]
    random_state: int = 42


class MLOpsPipeline:
    """
    Complete MLOps pipeline for [Problem Name].
    
    This class implements the full ML workflow:
    1. Data preprocessing
    2. Feature engineering
    3. Model training
    4. Model evaluation
    5. Model deployment preparation
    
    Attributes:
        config: Model configuration
        model: Trained model instance
        feature_names: List of feature names
        metrics: Training and evaluation metrics
    """
    
    def __init__(self, config: ModelConfig):
        """
        Initialize MLOps pipeline.
        
        Args:
            config: Model configuration
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        self.config = config
        self.model = None
        self.feature_names = []
        self.metrics = {}
        
        logger.info(f"Initialized MLOps pipeline with {config.model_type}")
    
    def load_data(self, data_path: str) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Load and validate data.
        
        Args:
            data_path: Path to data file (e.g., "datasets/mlops/classification/train.csv")
        
        Returns:
            Tuple of (features DataFrame, target Series)
        
        Raises:
            FileNotFoundError: If data file doesn't exist
            ValueError: If data is invalid
        
        Time Complexity: O(n) where n is number of rows
        Space Complexity: O(n*m) where m is number of features
        
        Examples:
            >>> pipeline = MLOpsPipeline(config)
            >>> X, y = pipeline.load_data("datasets/sample/iris.csv")
        """
        logger.info(f"Loading data from {data_path}")
        
        try:
            # Load data from datasets directory
            df = pd.read_csv(data_path)
            
            # Validate data
            if df.empty:
                raise ValueError("Data is empty")
            
            logger.info(f"Loaded {len(df)} rows with {len(df.columns)} columns")
            
            # Separate features and target
            # Adjust column names based on your data
            target_col = 'target'  # Change as needed
            
            if target_col not in df.columns:
                raise ValueError(f"Target column '{target_col}' not found")
            
            X = df.drop(columns=[target_col])
            y = df[target_col]
            
            self.feature_names = X.columns.tolist()
            
            return X, y
            
        except FileNotFoundError:
            logger.error(f"Data file not found: {data_path}")
            raise
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise
    
    def preprocess_data(
        self,
        X: pd.DataFrame,
        y: pd.Series
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Preprocess features and target.
        
        Args:
            X: Feature DataFrame
            y: Target Series
        
        Returns:
            Tuple of (preprocessed features, preprocessed target)
        
        Time Complexity: O(n*m) where n is rows, m is features
        Space Complexity: O(n*m)
        """
        logger.info("Preprocessing data")
        
        # Handle missing values
        X_processed = X.fillna(X.mean())
        
        # Handle categorical variables if needed
        # X_processed = pd.get_dummies(X_processed, drop_first=True)
        
        # Scale features if needed
        # from sklearn.preprocessing import StandardScaler
        # scaler = StandardScaler()
        # X_processed = scaler.fit_transform(X_processed)
        
        logger.info("Preprocessing complete")
        
        return X_processed.values, y.values
    
    def engineer_features(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Create engineered features.
        
        Args:
            X: Feature DataFrame
        
        Returns:
            DataFrame with engineered features
        
        Time Complexity: O(n*m)
        Space Complexity: O(n*m)
        """
        logger.info("Engineering features")
        
        X_engineered = X.copy()
        
        # Add feature engineering logic here
        # Example: polynomial features, interactions, etc.
        
        logger.info(f"Created {len(X_engineered.columns)} features")
        
        return X_engineered
    
    def train_model(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray
    ) -> None:
        """
        Train the model.
        
        Args:
            X_train: Training features
            y_train: Training target
        
        Time Complexity: O(n*m*k) where k depends on algorithm
        Space Complexity: O(m) for model parameters
        """
        logger.info("Training model")
        
        # Import appropriate model based on config
        if self.config.model_type == "random_forest":
            from sklearn.ensemble import RandomForestClassifier
            self.model = RandomForestClassifier(
                **self.config.hyperparameters,
                random_state=self.config.random_state
            )
        elif self.config.model_type == "logistic_regression":
            from sklearn.linear_model import LogisticRegression
            self.model = LogisticRegression(
                **self.config.hyperparameters,
                random_state=self.config.random_state
            )
        else:
            raise ValueError(f"Unknown model type: {self.config.model_type}")
        
        # Train model
        self.model.fit(X_train, y_train)
        
        logger.info("Model training complete")
    
    def evaluate_model(
        self,
        X_test: np.ndarray,
        y_test: np.ndarray
    ) -> Dict[str, float]:
        """
        Evaluate model performance.
        
        Args:
            X_test: Test features
            y_test: Test target
        
        Returns:
            Dictionary of evaluation metrics
        
        Time Complexity: O(n*m)
        Space Complexity: O(n)
        """
        logger.info("Evaluating model")
        
        if self.model is None:
            raise ValueError("Model not trained yet")
        
        # Make predictions
        y_pred = self.model.predict(X_test)
        
        # Calculate metrics
        from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
        
        self.metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred, average='weighted'),
            'recall': recall_score(y_test, y_pred, average='weighted'),
            'f1_score': f1_score(y_test, y_pred, average='weighted')
        }
        
        logger.info(f"Evaluation metrics: {self.metrics}")
        
        return self.metrics
    
    def save_model(self, model_path: str) -> None:
        """
        Save trained model to disk.
        
        Args:
            model_path: Path to save model
        
        Time Complexity: O(m) where m is model size
        Space Complexity: O(m)
        """
        logger.info(f"Saving model to {model_path}")
        
        if self.model is None:
            raise ValueError("No model to save")
        
        import joblib
        joblib.dump(self.model, model_path)
        
        logger.info("Model saved successfully")
    
    def load_model(self, model_path: str) -> None:
        """
        Load trained model from disk.
        
        Args:
            model_path: Path to model file
        
        Time Complexity: O(m)
        Space Complexity: O(m)
        """
        logger.info(f"Loading model from {model_path}")
        
        import joblib
        self.model = joblib.load(model_path)
        
        logger.info("Model loaded successfully")
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Make predictions on new data.
        
        Args:
            X: Feature array
        
        Returns:
            Predictions array
        
        Time Complexity: O(n*m)
        Space Complexity: O(n)
        """
        if self.model is None:
            raise ValueError("Model not trained or loaded")
        
        return self.model.predict(X)


def main():
    """
    Main function to demonstrate MLOps pipeline.
    """
    print("=" * 60)
    print("MLOps Pipeline: [Problem Title]")
    print("=" * 60)
    
    # Example 1: Train a model
    print("\n--- Example 1: Train Model ---")
    try:
        # Configure model
        config = ModelConfig(
            model_type="random_forest",
            hyperparameters={
                'n_estimators': 100,
                'max_depth': 10
            }
        )
        
        # Initialize pipeline
        pipeline = MLOpsPipeline(config)
        
        # Option 1: Load data from datasets directory
        # X, y = pipeline.load_data("datasets/mlops/classification/train.csv")
        # X, y = pipeline.load_data("datasets/sample/iris.csv")
        
        # Option 2: For demo, create synthetic data
        from sklearn.datasets import make_classification
        X, y = make_classification(
            n_samples=1000,
            n_features=20,
            n_informative=15,
            n_redundant=5,
            random_state=42
        )
        print(f"Using synthetic data: {X.shape[0]} samples, {X.shape[1]} features")
        
        # Split data
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Train model
        pipeline.train_model(X_train, y_train)
        
        # Evaluate model
        metrics = pipeline.evaluate_model(X_test, y_test)
        
        print(f"\nModel Performance:")
        for metric, value in metrics.items():
            print(f"  {metric}: {value:.4f}")
        
        # Save model
        # pipeline.save_model("models/model.pkl")
        
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 2: Load and predict
    print("\n--- Example 2: Load Model and Predict ---")
    try:
        # For demo, use the already trained model
        # In practice, you would load from disk:
        # pipeline.load_model("models/model.pkl")
        
        # Make predictions on new data
        X_new = X_test[:5]  # Use first 5 test samples
        predictions = pipeline.predict(X_new)
        
        print(f"\nPredictions for {len(X_new)} samples:")
        print(predictions)
        
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "=" * 60)
    print("Pipeline execution completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()

