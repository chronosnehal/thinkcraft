#!/usr/bin/env python3
"""
Model Training Pipeline - MLOps Solution Implementation

Description: Complete end-to-end ML training pipeline with data loading,
preprocessing, model training, evaluation, and persistence.

This solution demonstrates ML model training, evaluation, and deployment patterns.

Time Complexity: O(n*m*k) - Training complexity depends on algorithm
Space Complexity: O(n*m) - Data storage + O(m) for model parameters

Dependencies: scikit-learn, pandas, numpy, joblib
Author: ThinkCraft
"""

from typing import Any, Dict, List, Optional, Tuple
import logging
import os
from pathlib import Path
from dataclasses import dataclass
import numpy as np
import pandas as pd
from datetime import datetime

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
    task_type: str  # "classification" or "regression"
    hyperparameters: Dict[str, Any]
    random_state: int = 42
    test_size: float = 0.2
    target_column: Optional[str] = None


class ModelTrainingPipeline:
    """
    Complete MLOps pipeline for model training.
    
    This class implements the full ML workflow:
    1. Data loading and validation
    2. Train/test splitting
    3. Data preprocessing
    4. Model training
    5. Model evaluation
    6. Model persistence
    
    Attributes:
        config: Model configuration
        model: Trained model instance
        feature_names: List of feature names
        metrics: Training and evaluation metrics
        model_version: Version string for saved model
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
        self.model_version = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Validate task type
        if config.task_type not in ["classification", "regression"]:
            raise ValueError(
                f"task_type must be 'classification' or 'regression', "
                f"got '{config.task_type}'"
            )
        
        # Validate model type
        valid_models = ["random_forest", "logistic_regression", "gradient_boosting"]
        if config.model_type not in valid_models:
            raise ValueError(
                f"model_type must be one of {valid_models}, "
                f"got '{config.model_type}'"
            )
        
        logger.info(
            f"Initialized pipeline: {config.model_type} for {config.task_type}"
        )
    
    def load_data(
        self,
        data_path: Optional[str] = None,
        dataframe: Optional[pd.DataFrame] = None
    ) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Load and validate data.
        
        Args:
            data_path: Path to data file (CSV)
            dataframe: Optional pandas DataFrame (if data_path not provided)
        
        Returns:
            Tuple of (features DataFrame, target Series)
        
        Raises:
            FileNotFoundError: If data file doesn't exist
            ValueError: If data is invalid
        
        Time Complexity: O(n) where n is number of rows
        Space Complexity: O(n*m) where m is number of features
        
        Examples:
            >>> config = ModelConfig(...)
            >>> pipeline = ModelTrainingPipeline(config)
            >>> X, y = pipeline.load_data("datasets/mlops/classification/train.csv")
        """
        logger.info(f"Loading data from {data_path or 'DataFrame'}")
        
        try:
            # Load data
            if dataframe is not None:
                df = dataframe.copy()
            elif data_path is not None:
                if not os.path.exists(data_path):
                    raise FileNotFoundError(f"Data file not found: {data_path}")
                df = pd.read_csv(data_path)
            else:
                raise ValueError("Either data_path or dataframe must be provided")
            
            # Validate data
            if df.empty:
                raise ValueError("Data is empty")
            
            if len(df) < 100:
                raise ValueError(
                    f"Insufficient data: {len(df)} samples. "
                    f"Minimum 100 samples required."
                )
            
            logger.info(f"Loaded {len(df)} rows with {len(df.columns)} columns")
            
            # Determine target column
            target_col = self.config.target_column
            if target_col is None:
                # Auto-detect target column
                if self.config.task_type == "classification":
                    target_col = "target"
                else:
                    target_col = "price"
            
            if target_col not in df.columns:
                raise ValueError(
                    f"Target column '{target_col}' not found. "
                    f"Available columns: {list(df.columns)}"
                )
            
            # Check for missing values in target
            if df[target_col].isna().any():
                raise ValueError(
                    f"Target column '{target_col}' contains missing values"
                )
            
            # Separate features and target
            X = df.drop(columns=[target_col])
            y = df[target_col]
            
            # Validate target for classification
            if self.config.task_type == "classification":
                unique_classes = y.nunique()
                if unique_classes < 2:
                    raise ValueError(
                        f"Classification requires at least 2 classes, "
                        f"found {unique_classes}"
                    )
                logger.info(f"Classification task with {unique_classes} classes")
                logger.info(f"Class distribution:\n{y.value_counts()}")
            
            self.feature_names = X.columns.tolist()
            logger.info(f"Features: {len(self.feature_names)}")
            
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
        y: pd.Series,
        fit: bool = True
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Preprocess features and target.
        
        Args:
            X: Feature DataFrame
            y: Target Series
            fit: Whether to fit preprocessing (True for training, False for inference)
        
        Returns:
            Tuple of (preprocessed features, preprocessed target)
        
        Time Complexity: O(n*m) where n is rows, m is features
        Space Complexity: O(n*m)
        """
        logger.info("Preprocessing data")
        
        X_processed = X.copy()
        
        # Handle missing values
        numeric_cols = X_processed.select_dtypes(include=[np.number]).columns
        categorical_cols = X_processed.select_dtypes(
            include=['object', 'category']
        ).columns
        
        if len(numeric_cols) > 0:
            # Impute numeric missing values with mean
            if fit:
                self.numeric_means = X_processed[numeric_cols].mean()
            X_processed[numeric_cols] = X_processed[numeric_cols].fillna(
                self.numeric_means if fit else X_processed[numeric_cols].mean()
            )
        
        if len(categorical_cols) > 0:
            # Impute categorical missing values with mode
            if fit:
                self.categorical_modes = X_processed[categorical_cols].mode().iloc[0]
            X_processed[categorical_cols] = X_processed[categorical_cols].fillna(
                self.categorical_modes if fit else X_processed[categorical_cols].mode().iloc[0]
            )
        
        # Convert categorical to numeric if needed
        if len(categorical_cols) > 0:
            X_processed = pd.get_dummies(X_processed, columns=categorical_cols, drop_first=True)
        
        logger.info(f"Preprocessed features shape: {X_processed.shape}")
        
        return X_processed.values, y.values
    
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
        logger.info(f"Training {self.config.model_type} model")
        
        # Import appropriate model based on config
        if self.config.model_type == "random_forest":
            if self.config.task_type == "classification":
                from sklearn.ensemble import RandomForestClassifier
                self.model = RandomForestClassifier(
                    **self.config.hyperparameters,
                    random_state=self.config.random_state
                )
            else:
                from sklearn.ensemble import RandomForestRegressor
                self.model = RandomForestRegressor(
                    **self.config.hyperparameters,
                    random_state=self.config.random_state
                )
        
        elif self.config.model_type == "logistic_regression":
            if self.config.task_type != "classification":
                raise ValueError(
                    "Logistic Regression only supports classification tasks"
                )
            from sklearn.linear_model import LogisticRegression
            self.model = LogisticRegression(
                **self.config.hyperparameters,
                random_state=self.config.random_state,
                max_iter=1000
            )
        
        elif self.config.model_type == "gradient_boosting":
            if self.config.task_type == "classification":
                from sklearn.ensemble import GradientBoostingClassifier
                self.model = GradientBoostingClassifier(
                    **self.config.hyperparameters,
                    random_state=self.config.random_state
                )
            else:
                from sklearn.ensemble import GradientBoostingRegressor
                self.model = GradientBoostingRegressor(
                    **self.config.hyperparameters,
                    random_state=self.config.random_state
                )
        
        # Train model
        import time
        start_time = time.time()
        self.model.fit(X_train, y_train)
        training_time = time.time() - start_time
        
        logger.info(f"Model training complete in {training_time:.2f} seconds")
    
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
        
        # Calculate metrics based on task type
        if self.config.task_type == "classification":
            from sklearn.metrics import (
                accuracy_score, precision_score, recall_score, f1_score,
                classification_report
            )
            
            self.metrics = {
                'accuracy': accuracy_score(y_test, y_pred),
                'precision': precision_score(
                    y_test, y_pred, average='weighted', zero_division=0
                ),
                'recall': recall_score(
                    y_test, y_pred, average='weighted', zero_division=0
                ),
                'f1_score': f1_score(
                    y_test, y_pred, average='weighted', zero_division=0
                )
            }
            
            logger.info("Classification Report:")
            logger.info(f"\n{classification_report(y_test, y_pred)}")
        
        else:  # regression
            from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
            
            self.metrics = {
                'mse': mean_squared_error(y_test, y_pred),
                'mae': mean_absolute_error(y_test, y_pred),
                'r2_score': r2_score(y_test, y_pred)
            }
        
        logger.info(f"Evaluation metrics: {self.metrics}")
        
        return self.metrics
    
    def save_model(self, model_dir: str = "models") -> str:
        """
        Save trained model to disk.
        
        Args:
            model_dir: Directory to save model
        
        Returns:
            Path to saved model file
        
        Time Complexity: O(m) where m is model size
        Space Complexity: O(m)
        """
        logger.info(f"Saving model to {model_dir}")
        
        if self.model is None:
            raise ValueError("No model to save")
        
        # Create directory if it doesn't exist
        Path(model_dir).mkdir(parents=True, exist_ok=True)
        
        # Generate model filename
        model_name = (
            f"{self.config.model_type}_{self.config.task_type}_"
            f"v{self.model_version}.pkl"
        )
        model_path = os.path.join(model_dir, model_name)
        
        import joblib
        joblib.dump({
            'model': self.model,
            'config': self.config,
            'feature_names': self.feature_names,
            'metrics': self.metrics,
            'version': self.model_version
        }, model_path)
        
        logger.info(f"Model saved successfully to {model_path}")
        
        return model_path
    
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
        model_data = joblib.load(model_path)
        
        self.model = model_data['model']
        self.config = model_data['config']
        self.feature_names = model_data['feature_names']
        self.metrics = model_data.get('metrics', {})
        self.model_version = model_data.get('version', 'unknown')
        
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
    Main function to demonstrate model training pipeline.
    """
    print("=" * 70)
    print("Model Training Pipeline - MLOps Solution")
    print("=" * 70)
    
    # Example 1: Classification with synthetic data
    print("\n--- Example 1: Classification Pipeline ---")
    try:
        from sklearn.datasets import make_classification
        
        # Generate synthetic classification data
        X, y = make_classification(
            n_samples=1000,
            n_features=20,
            n_informative=15,
            n_redundant=5,
            n_classes=3,
            random_state=42
        )
        
        # Convert to DataFrame
        feature_names = [f"feature_{i}" for i in range(X.shape[1])]
        df = pd.DataFrame(X, columns=feature_names)
        df['target'] = y
        
        print(f"Generated synthetic data: {len(df)} samples, {len(feature_names)} features")
        print(f"Classes: {df['target'].nunique()}")
        
        # Configure model
        config = ModelConfig(
            model_type="random_forest",
            task_type="classification",
            hyperparameters={
                'n_estimators': 100,
                'max_depth': 10,
                'min_samples_split': 5
            },
            random_state=42,
            target_column="target"
        )
        
        # Initialize pipeline
        pipeline = ModelTrainingPipeline(config)
        
        # Load data
        X_data, y_data = pipeline.load_data(dataframe=df)
        
        # Split data
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(
            X_data, y_data,
            test_size=config.test_size,
            random_state=config.random_state,
            stratify=y_data if config.task_type == "classification" else None
        )
        
        print(f"Train set: {len(X_train)} samples")
        print(f"Test set: {len(X_test)} samples")
        
        # Preprocess
        X_train_processed, y_train_processed = pipeline.preprocess_data(
            X_train, y_train, fit=True
        )
        X_test_processed, y_test_processed = pipeline.preprocess_data(
            X_test, y_test, fit=False
        )
        
        # Train model
        pipeline.train_model(X_train_processed, y_train_processed)
        
        # Evaluate model
        metrics = pipeline.evaluate_model(X_test_processed, y_test_processed)
        
        print(f"\nModel Performance:")
        for metric, value in metrics.items():
            print(f"  {metric}: {value:.4f}")
        
        # Save model
        model_path = pipeline.save_model()
        print(f"\nModel saved to: {model_path}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    
    # Example 2: Regression with synthetic data
    print("\n--- Example 2: Regression Pipeline ---")
    try:
        from sklearn.datasets import make_regression
        
        # Generate synthetic regression data
        X, y = make_regression(
            n_samples=500,
            n_features=15,
            n_informative=10,
            noise=10,
            random_state=42
        )
        
        # Convert to DataFrame
        feature_names = [f"feature_{i}" for i in range(X.shape[1])]
        df = pd.DataFrame(X, columns=feature_names)
        df['price'] = y
        
        print(f"Generated synthetic data: {len(df)} samples, {len(feature_names)} features")
        
        # Configure model
        config = ModelConfig(
            model_type="gradient_boosting",
            task_type="regression",
            hyperparameters={
                'n_estimators': 100,
                'learning_rate': 0.1,
                'max_depth': 5
            },
            random_state=42,
            target_column="price"
        )
        
        # Initialize pipeline
        pipeline = ModelTrainingPipeline(config)
        
        # Load data
        X_data, y_data = pipeline.load_data(dataframe=df)
        
        # Split data
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(
            X_data, y_data,
            test_size=config.test_size,
            random_state=config.random_state
        )
        
        # Preprocess
        X_train_processed, y_train_processed = pipeline.preprocess_data(
            X_train, y_train, fit=True
        )
        X_test_processed, y_test_processed = pipeline.preprocess_data(
            X_test, y_test, fit=False
        )
        
        # Train model
        pipeline.train_model(X_train_processed, y_train_processed)
        
        # Evaluate model
        metrics = pipeline.evaluate_model(X_test_processed, y_test_processed)
        
        print(f"\nModel Performance:")
        for metric, value in metrics.items():
            print(f"  {metric}: {value:.4f}")
        
        # Save model
        model_path = pipeline.save_model()
        print(f"\nModel saved to: {model_path}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 70)
    print("Pipeline execution completed!")
    print("=" * 70)


if __name__ == "__main__":
    main()

