#!/usr/bin/env python3
"""
Feature Engineering - MLOps Solution Implementation

Description: Comprehensive feature engineering pipeline with automatic
feature creation, transformation, and selection.

This solution demonstrates production-ready feature engineering patterns.

Time Complexity: O(n*m) for basic, O(n*m²) for interactions
Space Complexity: O(n*m) for transformed data

Dependencies: scikit-learn, pandas, numpy
Author: ThinkCraft
"""

from typing import Any, Dict, List, Optional, Tuple
import logging
import numpy as np
import pandas as pd
from sklearn.preprocessing import (
    StandardScaler, MinMaxScaler, RobustScaler,
    OneHotEncoder, LabelEncoder, TargetEncoder
)
from sklearn.feature_selection import (
    SelectKBest, f_classif, f_regression,
    mutual_info_classif, mutual_info_regression
)
from sklearn.decomposition import PCA
import warnings
warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class FeatureEngineeringPipeline:
    """
    Comprehensive feature engineering pipeline.
    
    This class implements:
    1. Feature type detection
    2. Numeric transformations (scaling, normalization, polynomial)
    3. Categorical encoding (one-hot, label, target)
    4. Temporal feature extraction
    5. Interaction feature creation
    6. Feature selection
    
    Attributes:
        numeric_features: List of numeric feature names
        categorical_features: List of categorical feature names
        temporal_features: List of temporal feature names
        transformers: Dictionary of fitted transformers
        selected_features: List of selected feature names
        feature_importance: Dictionary of feature importance scores
    """
    
    def __init__(
        self,
        scale_numeric: bool = True,
        scale_method: str = "standard",
        encode_categorical: str = "onehot",
        create_polynomial: bool = True,
        polynomial_degree: int = 2,
        create_interactions: bool = True,
        max_interactions: int = 10,
        select_features: bool = True,
        n_features: Optional[int] = None,
        task_type: str = "classification"
    ):
        """
        Initialize feature engineering pipeline.
        
        Args:
            scale_numeric: Whether to scale numeric features
            scale_method: Scaling method ("standard", "minmax", "robust")
            encode_categorical: Encoding method ("onehot", "label", "target")
            create_polynomial: Whether to create polynomial features
            polynomial_degree: Degree for polynomial features
            create_interactions: Whether to create interaction features
            max_interactions: Maximum number of interaction features
            select_features: Whether to perform feature selection
            n_features: Number of features to select (None = auto)
            task_type: Task type ("classification" or "regression")
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        self.scale_numeric = scale_numeric
        self.scale_method = scale_method
        self.encode_categorical = encode_categorical
        self.create_polynomial = create_polynomial
        self.polynomial_degree = polynomial_degree
        self.create_interactions = create_interactions
        self.max_interactions = max_interactions
        self.select_features = select_features
        self.n_features = n_features
        self.task_type = task_type
        
        self.numeric_features = []
        self.categorical_features = []
        self.temporal_features = []
        self.transformers = {}
        self.selected_features = []
        self.feature_importance = {}
        self.feature_names = []
        
        logger.info("Feature engineering pipeline initialized")
    
    def _detect_feature_types(self, df: pd.DataFrame) -> None:
        """
        Detect feature types (numeric, categorical, temporal).
        
        Args:
            df: Input DataFrame
        
        Time Complexity: O(m) where m is number of columns
        Space Complexity: O(m)
        """
        logger.info("Detecting feature types")
        
        self.numeric_features = []
        self.categorical_features = []
        self.temporal_features = []
        
        for col in df.columns:
            # Check if temporal
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                self.temporal_features.append(col)
            # Check if numeric
            elif pd.api.types.is_numeric_dtype(df[col]):
                # Check if constant
                if df[col].nunique() > 1:
                    self.numeric_features.append(col)
                else:
                    logger.warning(f"Dropping constant column: {col}")
            # Otherwise categorical
            else:
                # Check if high cardinality
                if df[col].nunique() > 50:
                    logger.warning(
                        f"High cardinality categorical: {col} "
                        f"({df[col].nunique()} unique values)"
                    )
                self.categorical_features.append(col)
        
        logger.info(
            f"Detected {len(self.numeric_features)} numeric, "
            f"{len(self.categorical_features)} categorical, "
            f"{len(self.temporal_features)} temporal features"
        )
    
    def fit(self, X: pd.DataFrame, y: Optional[pd.Series] = None) -> 'FeatureEngineeringPipeline':
        """
        Fit transformers on training data.
        
        Args:
            X: Feature DataFrame
            y: Optional target Series (needed for target encoding and feature selection)
        
        Returns:
            Self for method chaining
        
        Time Complexity: O(n*m)
        Space Complexity: O(m)
        """
        logger.info("Fitting feature engineering pipeline")
        
        # Detect feature types
        self._detect_feature_types(X)
        
        X_processed = X.copy()
        
        # Handle temporal features
        if self.temporal_features:
            X_processed = self._extract_temporal_features(X_processed, fit=True)
        
        # Handle missing values
        X_processed = self._handle_missing_values(X_processed, fit=True)
        
        # Scale numeric features
        if self.scale_numeric and self.numeric_features:
            self._fit_numeric_scaler(X_processed[self.numeric_features])
        
        # Encode categorical features
        if self.categorical_features:
            if self.encode_categorical == "target" and y is not None:
                self._fit_target_encoder(X_processed[self.categorical_features], y)
            elif self.encode_categorical == "onehot":
                self._fit_onehot_encoder(X_processed[self.categorical_features])
            else:
                self._fit_label_encoder(X_processed[self.categorical_features])
        
        # Store feature names for later
        self.feature_names = list(X_processed.columns)
        
        logger.info("Pipeline fitting complete")
        
        return self
    
    def transform(
        self,
        X: pd.DataFrame,
        y: Optional[pd.Series] = None
    ) -> pd.DataFrame:
        """
        Transform data using fitted transformers.
        
        Args:
            X: Feature DataFrame
            y: Optional target Series
        
        Returns:
            Transformed DataFrame
        
        Time Complexity: O(n*m)
        Space Complexity: O(n*m)
        """
        logger.info("Transforming data")
        
        X_processed = X.copy()
        
        # Extract temporal features
        if self.temporal_features:
            X_processed = self._extract_temporal_features(X_processed, fit=False)
        
        # Handle missing values
        X_processed = self._handle_missing_values(X_processed, fit=False)
        
        # Transform numeric features
        if self.scale_numeric and self.numeric_features:
            X_processed = self._transform_numeric_features(X_processed)
        
        # Transform categorical features
        if self.categorical_features:
            if self.encode_categorical == "target" and y is not None:
                X_processed = self._transform_target_encoder(X_processed, y)
            elif self.encode_categorical == "onehot":
                X_processed = self._transform_onehot_encoder(X_processed)
            else:
                X_processed = self._transform_label_encoder(X_processed)
        
        # Create polynomial features
        if self.create_polynomial:
            X_processed = self._create_polynomial_features(X_processed)
        
        # Create interaction features
        if self.create_interactions:
            X_processed = self._create_interaction_features(X_processed)
        
        # Feature selection
        if self.select_features and y is not None:
            X_processed, self.selected_features = self._select_features(
                X_processed, y
            )
        
        logger.info(f"Transformed data shape: {X_processed.shape}")
        
        return X_processed
    
    def fit_transform(
        self,
        X: pd.DataFrame,
        y: Optional[pd.Series] = None
    ) -> pd.DataFrame:
        """
        Fit and transform in one step.
        
        Args:
            X: Feature DataFrame
            y: Optional target Series
        
        Returns:
            Transformed DataFrame
        """
        return self.fit(X, y).transform(X, y)
    
    def _extract_temporal_features(
        self,
        df: pd.DataFrame,
        fit: bool = True
    ) -> pd.DataFrame:
        """Extract temporal features from datetime columns."""
        df_processed = df.copy()
        
        for col in self.temporal_features:
            if col not in df_processed.columns:
                continue
            
            # Extract basic temporal features
            df_processed[f'{col}_year'] = df_processed[col].dt.year
            df_processed[f'{col}_month'] = df_processed[col].dt.month
            df_processed[f'{col}_day'] = df_processed[col].dt.day
            df_processed[f'{col}_weekday'] = df_processed[col].dt.weekday
            df_processed[f'{col}_hour'] = df_processed[col].dt.hour if \
                pd.api.types.is_datetime64_any_dtype(df_processed[col]) else 0
            
            # Cyclical encoding for periodic features
            df_processed[f'{col}_month_sin'] = np.sin(
                2 * np.pi * df_processed[f'{col}_month'] / 12
            )
            df_processed[f'{col}_month_cos'] = np.cos(
                2 * np.pi * df_processed[f'{col}_month'] / 12
            )
            df_processed[f'{col}_weekday_sin'] = np.sin(
                2 * np.pi * df_processed[f'{col}_weekday'] / 7
            )
            df_processed[f'{col}_weekday_cos'] = np.cos(
                2 * np.pi * df_processed[f'{col}_weekday'] / 7
            )
            
            # Drop original temporal column
            df_processed = df_processed.drop(columns=[col])
        
        return df_processed
    
    def _handle_missing_values(
        self,
        df: pd.DataFrame,
        fit: bool = True
    ) -> pd.DataFrame:
        """Handle missing values."""
        df_processed = df.copy()
        
        for col in df_processed.columns:
            if df_processed[col].isna().any():
                if pd.api.types.is_numeric_dtype(df_processed[col]):
                    fill_value = df_processed[col].mean() if fit else \
                        self.transformers.get(f'{col}_mean', 0)
                    if fit:
                        self.transformers[f'{col}_mean'] = fill_value
                    df_processed[col] = df_processed[col].fillna(fill_value)
                else:
                    fill_value = df_processed[col].mode()[0] if fit else \
                        self.transformers.get(f'{col}_mode', 'unknown')
                    if fit:
                        self.transformers[f'{col}_mode'] = fill_value
                    df_processed[col] = df_processed[col].fillna(fill_value)
        
        return df_processed
    
    def _fit_numeric_scaler(self, X_numeric: pd.DataFrame) -> None:
        """Fit numeric scaler."""
        if self.scale_method == "standard":
            scaler = StandardScaler()
        elif self.scale_method == "minmax":
            scaler = MinMaxScaler()
        elif self.scale_method == "robust":
            scaler = RobustScaler()
        else:
            scaler = StandardScaler()
        
        scaler.fit(X_numeric)
        self.transformers['numeric_scaler'] = scaler
    
    def _transform_numeric_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Transform numeric features."""
        df_processed = df.copy()
        
        if 'numeric_scaler' in self.transformers:
            scaler = self.transformers['numeric_scaler']
            numeric_cols = [col for col in self.numeric_features if col in df_processed.columns]
            if numeric_cols:
                df_processed[numeric_cols] = scaler.transform(
                    df_processed[numeric_cols]
                )
        
        return df_processed
    
    def _fit_onehot_encoder(self, X_categorical: pd.DataFrame) -> None:
        """Fit one-hot encoder."""
        encoder = OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore')
        encoder.fit(X_categorical)
        self.transformers['onehot_encoder'] = encoder
        self.transformers['categorical_columns'] = list(X_categorical.columns)
    
    def _transform_onehot_encoder(self, df: pd.DataFrame) -> pd.DataFrame:
        """Transform using one-hot encoding."""
        df_processed = df.copy()
        
        if 'onehot_encoder' in self.transformers:
            encoder = self.transformers['onehot_encoder']
            cat_cols = self.transformers['categorical_columns']
            available_cols = [col for col in cat_cols if col in df_processed.columns]
            
            if available_cols:
                encoded = encoder.transform(df_processed[available_cols])
                encoded_df = pd.DataFrame(
                    encoded,
                    columns=encoder.get_feature_names_out(available_cols),
                    index=df_processed.index
                )
                df_processed = df_processed.drop(columns=available_cols)
                df_processed = pd.concat([df_processed, encoded_df], axis=1)
        
        return df_processed
    
    def _fit_label_encoder(self, X_categorical: pd.DataFrame) -> None:
        """Fit label encoders."""
        self.transformers['label_encoders'] = {}
        for col in X_categorical.columns:
            le = LabelEncoder()
            le.fit(X_categorical[col].astype(str))
            self.transformers['label_encoders'][col] = le
    
    def _transform_label_encoder(self, df: pd.DataFrame) -> pd.DataFrame:
        """Transform using label encoding."""
        df_processed = df.copy()
        
        if 'label_encoders' in self.transformers:
            for col, encoder in self.transformers['label_encoders'].items():
                if col in df_processed.columns:
                    try:
                        df_processed[col] = encoder.transform(
                            df_processed[col].astype(str)
                        )
                    except ValueError:
                        # Handle unseen categories
                        df_processed[col] = 0
        
        return df_processed
    
    def _fit_target_encoder(
        self,
        X_categorical: pd.DataFrame,
        y: pd.Series
    ) -> None:
        """Fit target encoder."""
        self.transformers['target_encoders'] = {}
        for col in X_categorical.columns:
            te = TargetEncoder()
            te.fit(X_categorical[col], y)
            self.transformers['target_encoders'][col] = te
    
    def _transform_target_encoder(
        self,
        df: pd.DataFrame,
        y: Optional[pd.Series] = None
    ) -> pd.DataFrame:
        """Transform using target encoding."""
        df_processed = df.copy()
        
        if 'target_encoders' in self.transformers:
            for col, encoder in self.transformers['target_encoders'].items():
                if col in df_processed.columns:
                    if y is not None:
                        df_processed[col] = encoder.transform(
                            df_processed[[col]], y
                        )
                    else:
                        # Use mean if no target available
                        df_processed[col] = encoder.transform(
                            df_processed[[col]]
                        )
        
        return df_processed
    
    def _create_polynomial_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create polynomial features."""
        df_processed = df.copy()
        
        numeric_cols = [
            col for col in df_processed.columns
            if pd.api.types.is_numeric_dtype(df_processed[col])
        ]
        
        if len(numeric_cols) > 0 and self.polynomial_degree > 1:
            # Create polynomial features for first few numeric columns
            cols_to_poly = numeric_cols[:min(5, len(numeric_cols))]
            
            for col in cols_to_poly:
                for degree in range(2, self.polynomial_degree + 1):
                    df_processed[f'{col}_pow_{degree}'] = \
                        df_processed[col] ** degree
        
        return df_processed
    
    def _create_interaction_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create interaction features."""
        df_processed = df.copy()
        
        numeric_cols = [
            col for col in df_processed.columns
            if pd.api.types.is_numeric_dtype(df_processed[col])
        ]
        
        if len(numeric_cols) >= 2:
            # Create interactions between top features
            n_interactions = min(
                self.max_interactions,
                len(numeric_cols) * (len(numeric_cols) - 1) // 2
            )
            
            interactions_created = 0
            for i, col1 in enumerate(numeric_cols[:5]):
                for col2 in numeric_cols[i+1:5]:
                    if interactions_created >= n_interactions:
                        break
                    df_processed[f'{col1}_x_{col2}'] = \
                        df_processed[col1] * df_processed[col2]
                    interactions_created += 1
        
        return df_processed
    
    def _select_features(
        self,
        X: pd.DataFrame,
        y: pd.Series
    ) -> Tuple[pd.DataFrame, List[str]]:
        """Select important features."""
        if self.task_type == "classification":
            selector = SelectKBest(
                score_func=f_classif,
                k=self.n_features or min(50, X.shape[1])
            )
        else:
            selector = SelectKBest(
                score_func=f_regression,
                k=self.n_features or min(50, X.shape[1])
            )
        
        X_selected = selector.fit_transform(X, y)
        selected_indices = selector.get_support(indices=True)
        selected_features = [X.columns[i] for i in selected_indices]
        
        # Store feature importance
        scores = selector.scores_
        self.feature_importance = {
            X.columns[i]: scores[i] for i in selected_indices
        }
        
        return pd.DataFrame(X_selected, columns=selected_features, index=X.index), selected_features


def main():
    """Main function to demonstrate feature engineering pipeline."""
    print("=" * 70)
    print("Feature Engineering Pipeline - MLOps Solution")
    print("=" * 70)
    
    # Example 1: Mixed data types
    print("\n--- Example 1: Mixed Data Types ---")
    try:
        # Create sample data
        np.random.seed(42)
        n_samples = 200
        
        df = pd.DataFrame({
            'age': np.random.randint(18, 65, n_samples),
            'income': np.random.normal(50000, 15000, n_samples),
            'category': np.random.choice(['A', 'B', 'C'], n_samples),
            'city': np.random.choice(['NYC', 'LA', 'Chicago', 'Houston'], n_samples),
            'purchase_date': pd.date_range('2024-01-01', periods=n_samples, freq='D')
        })
        
        # Add some missing values
        df.loc[df.sample(10).index, 'income'] = np.nan
        
        print(f"Original data shape: {df.shape}")
        print(f"Original columns: {list(df.columns)}")
        
        # Initialize pipeline
        pipeline = FeatureEngineeringPipeline(
            scale_numeric=True,
            scale_method="standard",
            encode_categorical="onehot",
            create_polynomial=True,
            create_interactions=True,
            select_features=False,
            task_type="classification"
        )
        
        # Create target for demonstration
        y = pd.Series(np.random.choice([0, 1], n_samples))
        
        # Fit and transform
        X_transformed = pipeline.fit_transform(df, y)
        
        print(f"\nTransformed data shape: {X_transformed.shape}")
        print(f"New columns (first 10): {list(X_transformed.columns[:10])}")
        print(f"\nSample of transformed data:")
        print(X_transformed.head())
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    
    # Example 2: With feature selection
    print("\n--- Example 2: With Feature Selection ---")
    try:
        from sklearn.datasets import make_classification
        
        X, y = make_classification(
            n_samples=500,
            n_features=20,
            n_informative=10,
            random_state=42
        )
        
        feature_names = [f'feature_{i}' for i in range(X.shape[1])]
        df = pd.DataFrame(X, columns=feature_names)
        df['category'] = np.random.choice(['X', 'Y', 'Z'], len(df))
        
        print(f"Original data shape: {df.shape}")
        
        pipeline = FeatureEngineeringPipeline(
            scale_numeric=True,
            encode_categorical="onehot",
            create_polynomial=False,
            create_interactions=False,
            select_features=True,
            n_features=15,
            task_type="classification"
        )
        
        y_series = pd.Series(y)
        X_transformed = pipeline.fit_transform(df, y_series)
        
        print(f"Transformed data shape: {X_transformed.shape}")
        print(f"Selected features: {len(pipeline.selected_features)}")
        print(f"\nTop 5 feature importance scores:")
        sorted_importance = sorted(
            pipeline.feature_importance.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]
        for feature, score in sorted_importance:
            print(f"  {feature}: {score:.4f}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 70)
    print("Feature engineering pipeline demonstration completed!")
    print("=" * 70)


if __name__ == "__main__":
    main()

