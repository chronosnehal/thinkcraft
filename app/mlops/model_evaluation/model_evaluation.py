#!/usr/bin/env python3
"""
Model Evaluation - MLOps Solution Implementation

Description: Comprehensive model evaluation system with metrics computation,
cross-validation, and visualization.

Time Complexity: O(n*m) for evaluation, O(k*n*m) for k-fold CV
Space Complexity: O(n) for predictions and metrics

Dependencies: scikit-learn, pandas, numpy, matplotlib, seaborn
Author: ThinkCraft
"""

from typing import Any, Dict, List, Optional, Tuple, Union
import logging
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import cross_val_score, StratifiedKFold, KFold
from sklearn.metrics import (
    # Classification
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, roc_curve, precision_recall_curve, confusion_matrix,
    classification_report,
    # Regression
    mean_squared_error, mean_absolute_error, r2_score
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

sns.set_style("whitegrid")


class ModelEvaluator:
    """
    Comprehensive model evaluation system.
    
    Supports both classification and regression tasks with extensive
    metrics, cross-validation, and visualization capabilities.
    
    Attributes:
        task_type: Task type ("classification" or "regression")
        metrics: Dictionary of computed metrics
        cv_scores: Cross-validation scores
    """
    
    def __init__(
        self,
        task_type: str = "classification",
        n_folds: int = 5,
        random_state: int = 42
    ):
        """
        Initialize model evaluator.
        
        Args:
            task_type: Task type ("classification" or "regression")
            n_folds: Number of folds for cross-validation
            random_state: Random seed
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        if task_type not in ["classification", "regression"]:
            raise ValueError(
                f"task_type must be 'classification' or 'regression', "
                f"got '{task_type}'"
            )
        
        self.task_type = task_type
        self.n_folds = n_folds
        self.random_state = random_state
        self.metrics = {}
        self.cv_scores = {}
        
        logger.info(f"Initialized evaluator for {task_type}")
    
    def evaluate(
        self,
        model: Any,
        X_test: np.ndarray,
        y_test: np.ndarray,
        save_plots: bool = False,
        plot_dir: str = "plots"
    ) -> Dict[str, float]:
        """
        Evaluate model performance.
        
        Args:
            model: Trained scikit-learn model
            X_test: Test features
            y_test: Test targets
            save_plots: Whether to save visualization plots
            plot_dir: Directory to save plots
        
        Returns:
            Dictionary of evaluation metrics
        
        Time Complexity: O(n*m)
        Space Complexity: O(n)
        """
        logger.info("Evaluating model")
        
        # Make predictions
        y_pred = model.predict(X_test)
        
        # Get prediction probabilities for classification
        y_pred_proba = None
        if self.task_type == "classification" and hasattr(model, "predict_proba"):
            try:
                y_pred_proba = model.predict_proba(X_test)
            except:
                pass
        
        # Compute metrics
        if self.task_type == "classification":
            self.metrics = self._compute_classification_metrics(
                y_test, y_pred, y_pred_proba
            )
        else:
            self.metrics = self._compute_regression_metrics(y_test, y_pred)
        
        # Generate visualizations
        if save_plots:
            self._create_visualizations(
                y_test, y_pred, y_pred_proba, plot_dir
            )
        
        logger.info(f"Evaluation complete. Metrics: {self.metrics}")
        
        return self.metrics
    
    def _compute_classification_metrics(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        y_pred_proba: Optional[np.ndarray] = None
    ) -> Dict[str, float]:
        """Compute classification metrics."""
        metrics = {}
        
        # Basic metrics
        metrics['accuracy'] = accuracy_score(y_true, y_pred)
        
        # Handle multi-class vs binary
        average = 'weighted' if len(np.unique(y_true)) > 2 else 'binary'
        
        metrics['precision'] = precision_score(
            y_true, y_pred, average=average, zero_division=0
        )
        metrics['recall'] = recall_score(
            y_true, y_pred, average=average, zero_division=0
        )
        metrics['f1_score'] = f1_score(
            y_true, y_pred, average=average, zero_division=0
        )
        
        # ROC-AUC (only for binary classification with probabilities)
        if y_pred_proba is not None and len(np.unique(y_true)) == 2:
            try:
                metrics['roc_auc'] = roc_auc_score(
                    y_true, y_pred_proba[:, 1]
                )
            except:
                metrics['roc_auc'] = 0.0
        else:
            metrics['roc_auc'] = None
        
        # Confusion matrix
        metrics['confusion_matrix'] = confusion_matrix(y_true, y_pred).tolist()
        
        return metrics
    
    def _compute_regression_metrics(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray
    ) -> Dict[str, float]:
        """Compute regression metrics."""
        metrics = {}
        
        metrics['mse'] = mean_squared_error(y_true, y_pred)
        metrics['mae'] = mean_absolute_error(y_true, y_pred)
        metrics['rmse'] = np.sqrt(metrics['mse'])
        metrics['r2_score'] = r2_score(y_true, y_pred)
        
        # MAPE (Mean Absolute Percentage Error)
        mask = y_true != 0
        if mask.any():
            metrics['mape'] = np.mean(
                np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])
            ) * 100
        else:
            metrics['mape'] = None
        
        return metrics
    
    def cross_validate(
        self,
        model: Any,
        X: np.ndarray,
        y: np.ndarray,
        scoring: Optional[str] = None
    ) -> Dict[str, float]:
        """
        Perform k-fold cross-validation.
        
        Args:
            model: Model to evaluate
            X: Features
            y: Targets
            scoring: Scoring metric (None for default)
        
        Returns:
            Dictionary of CV statistics
        """
        logger.info(f"Performing {self.n_folds}-fold cross-validation")
        
        # Determine scoring and CV strategy
        if self.task_type == "classification":
            if scoring is None:
                scoring = 'accuracy'
            cv = StratifiedKFold(
                n_splits=self.n_folds,
                shuffle=True,
                random_state=self.random_state
            )
        else:
            if scoring is None:
                scoring = 'neg_mean_squared_error'
            cv = KFold(
                n_splits=self.n_folds,
                shuffle=True,
                random_state=self.random_state
            )
        
        # Perform cross-validation
        scores = cross_val_score(model, X, y, cv=cv, scoring=scoring)
        
        # Store results
        self.cv_scores = {
            'mean': np.mean(scores),
            'std': np.std(scores),
            'scores': scores.tolist()
        }
        
        logger.info(
            f"CV {scoring}: {self.cv_scores['mean']:.4f} "
            f"(+/- {self.cv_scores['std']:.4f})"
        )
        
        return self.cv_scores
    
    def _create_visualizations(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        y_pred_proba: Optional[np.ndarray],
        plot_dir: str
    ) -> None:
        """Create and save visualization plots."""
        import os
        os.makedirs(plot_dir, exist_ok=True)
        
        if self.task_type == "classification":
            # Confusion matrix
            cm = confusion_matrix(y_true, y_pred)
            plt.figure(figsize=(8, 6))
            sns.heatmap(
                cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=np.unique(y_true),
                yticklabels=np.unique(y_true)
            )
            plt.title('Confusion Matrix')
            plt.ylabel('True Label')
            plt.xlabel('Predicted Label')
            plt.tight_layout()
            plt.savefig(f'{plot_dir}/confusion_matrix.png')
            plt.close()
            
            # ROC curve (binary classification only)
            if y_pred_proba is not None and len(np.unique(y_true)) == 2:
                fpr, tpr, _ = roc_curve(y_true, y_pred_proba[:, 1])
                plt.figure(figsize=(8, 6))
                plt.plot(fpr, tpr, label=f'ROC (AUC = {self.metrics["roc_auc"]:.3f})')
                plt.plot([0, 1], [0, 1], 'k--', label='Random')
                plt.xlabel('False Positive Rate')
                plt.ylabel('True Positive Rate')
                plt.title('ROC Curve')
                plt.legend()
                plt.tight_layout()
                plt.savefig(f'{plot_dir}/roc_curve.png')
                plt.close()
        
        else:  # regression
            # Residual plot
            residuals = y_true - y_pred
            plt.figure(figsize=(10, 5))
            
            plt.subplot(1, 2, 1)
            plt.scatter(y_pred, residuals, alpha=0.5)
            plt.axhline(y=0, color='r', linestyle='--')
            plt.xlabel('Predicted')
            plt.ylabel('Residuals')
            plt.title('Residual Plot')
            
            plt.subplot(1, 2, 2)
            plt.scatter(y_true, y_pred, alpha=0.5)
            plt.plot([y_true.min(), y_true.max()],
                    [y_true.min(), y_true.max()], 'r--', lw=2)
            plt.xlabel('True')
            plt.ylabel('Predicted')
            plt.title('Predicted vs True')
            
            plt.tight_layout()
            plt.savefig(f'{plot_dir}/regression_plots.png')
            plt.close()
        
        logger.info(f"Plots saved to {plot_dir}/")


def main():
    """Main function to demonstrate model evaluation."""
    print("=" * 70)
    print("Model Evaluation - MLOps Solution")
    print("=" * 70)
    
    # Example 1: Classification evaluation
    print("\n--- Example 1: Classification Evaluation ---")
    try:
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.datasets import make_classification
        from sklearn.model_selection import train_test_split
        
        # Generate data
        X, y = make_classification(
            n_samples=1000,
            n_features=20,
            n_classes=3,
            random_state=42
        )
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Train model
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        # Evaluate
        evaluator = ModelEvaluator(task_type="classification")
        metrics = evaluator.evaluate(model, X_test, y_test)
        
        print("\nClassification Metrics:")
        for metric, value in metrics.items():
            if metric != 'confusion_matrix':
                print(f"  {metric}: {value:.4f}" if value is not None else f"  {metric}: None")
        
        print(f"\nConfusion Matrix:")
        print(np.array(metrics['confusion_matrix']))
        
        # Cross-validation
        cv_scores = evaluator.cross_validate(model, X_train, y_train)
        print(f"\nCross-Validation Scores:")
        print(f"  Mean: {cv_scores['mean']:.4f}")
        print(f"  Std: {cv_scores['std']:.4f}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    
    # Example 2: Regression evaluation
    print("\n--- Example 2: Regression Evaluation ---")
    try:
        from sklearn.ensemble import GradientBoostingRegressor
        from sklearn.datasets import make_regression
        from sklearn.model_selection import train_test_split
        
        # Generate data
        X, y = make_regression(
            n_samples=500,
            n_features=15,
            noise=10,
            random_state=42
        )
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Train model
        model = GradientBoostingRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        # Evaluate
        evaluator = ModelEvaluator(task_type="regression")
        metrics = evaluator.evaluate(model, X_test, y_test)
        
        print("\nRegression Metrics:")
        for metric, value in metrics.items():
            if value is not None:
                print(f"  {metric}: {value:.4f}")
        
        # Cross-validation
        cv_scores = evaluator.cross_validate(model, X_train, y_train)
        print(f"\nCross-Validation Scores:")
        print(f"  Mean: {cv_scores['mean']:.4f}")
        print(f"  Std: {cv_scores['std']:.4f}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 70)
    print("Model evaluation demonstration completed!")
    print("=" * 70)


if __name__ == "__main__":
    main()

