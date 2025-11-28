#!/usr/bin/env python3
"""
Data Analysis System - GenAI Solution Implementation

Description: Data analysis system using LLM integration to analyze datasets
and generate natural language insights, summaries, and recommendations.

This solution uses LLM capabilities to analyze various data formats (CSV, JSON,
dict, list), identify patterns, detect trends, and provide actionable business
intelligence through structured analytical reports.

Dependencies: app.utils.llm_client_manager, pandas (optional for CSV)
Time Complexity: O(n) for data loading + O(m) for LLM generation
Space Complexity: O(n) where n = dataset size
Author: chronosnehal
Date: 2025-11-27
"""

from app.utils.llm_client_manager import LLMClientManager
from typing import Optional, Dict, Any, List, Union
import json
import csv
import logging
import os
import re

# Try to import pandas for CSV handling
try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DataAnalyzer:
    """
    Data analysis system using LLM integration.
    
    This class analyzes datasets from various formats and generates natural
    language insights, patterns, trends, and recommendations using LLMClientManager.
    
    Attributes:
        manager: LLMClientManager instance
        provider: Selected LLM provider
        model: Model name to use
        max_rows_for_analysis: Maximum rows to analyze directly (default: 1000)
    """
    
    # Analysis type descriptions
    ANALYSIS_TYPES = {
        "summary": "High-level overview and key statistics",
        "patterns": "Identify patterns, correlations, and relationships",
        "trends": "Analyze trends over time or categories",
        "comparison": "Compare different segments or groups",
        "anomalies": "Detect outliers and unusual values",
        "comprehensive": "Full analysis with all components"
    }
    
    def __init__(
        self,
        provider: str = "openai",
        model: Optional[str] = None,
        max_rows_for_analysis: int = 1000
    ):
        """
        Initialize data analyzer.
        
        Args:
            provider: LLM provider name (openai, azure, gemini, claude, openrouter)
            model: Model name (defaults to provider's default)
            max_rows_for_analysis: Maximum rows to analyze directly (default: 1000)
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        self.manager = LLMClientManager()
        self.provider = provider
        self.max_rows_for_analysis = max_rows_for_analysis
        
        # Set default models per provider
        default_models = {
            "openai": "gpt-4",
            "azure": "gpt-4",
            "gemini": "gemini-pro",
            "claude": "claude-3-opus-20240229",
            "openrouter": "openai/gpt-4"
        }
        
        self.model = model or default_models.get(provider, "gpt-4")
        
        logger.info(
            f"DataAnalyzer initialized with provider: {provider}, "
            f"model: {self.model}, max_rows: {max_rows_for_analysis}"
        )
    
    def _load_data(
        self,
        data: Union[str, dict, list],
        data_format: Optional[str] = None
    ) -> tuple[Any, str, Dict[str, Any]]:
        """
        Load data from various formats.
        
        Args:
            data: Dataset (path, dict, list, or JSON string)
            data_format: Format hint (csv, json, dict, list)
        
        Returns:
            Tuple of (dataframe/dict/list, format, metadata)
        
        Raises:
            ValueError: If data cannot be loaded
        """
        # Auto-detect format if not provided
        if data_format is None:
            if isinstance(data, str):
                if data.endswith('.csv'):
                    data_format = "csv"
                elif data.endswith('.json'):
                    data_format = "json"
                elif data.startswith('{') or data.startswith('['):
                    data_format = "json"
                else:
                    # Assume CSV path
                    data_format = "csv"
            elif isinstance(data, dict):
                data_format = "dict"
            elif isinstance(data, list):
                data_format = "list"
            else:
                raise ValueError(f"Cannot auto-detect format for type: {type(data)}")
        
        # Load based on format
        if data_format == "csv":
            if isinstance(data, str) and os.path.exists(data):
                if PANDAS_AVAILABLE:
                    df = pd.read_csv(data)
                    metadata = {
                        "shape": df.shape,
                        "columns": df.columns.tolist(),
                        "dtypes": df.dtypes.to_dict()
                    }
                    return df, "csv", metadata
                else:
                    # Fallback to csv module
                    with open(data, 'r') as f:
                        reader = csv.DictReader(f)
                        rows = list(reader)
                    if not rows:
                        raise ValueError("CSV file is empty")
                    metadata = {
                        "shape": (len(rows), len(rows[0])),
                        "columns": list(rows[0].keys()),
                        "dtypes": None
                    }
                    return rows, "csv", metadata
            else:
                raise ValueError(f"CSV file not found: {data}")
        
        elif data_format == "json":
            if isinstance(data, str):
                if os.path.exists(data):
                    with open(data, 'r') as f:
                        data = json.load(f)
                else:
                    data = json.loads(data)
            
            if isinstance(data, list):
                if not data:
                    raise ValueError("JSON list is empty")
                if isinstance(data[0], dict):
                    if PANDAS_AVAILABLE:
                        df = pd.DataFrame(data)
                        metadata = {
                            "shape": df.shape,
                            "columns": df.columns.tolist(),
                            "dtypes": df.dtypes.to_dict()
                        }
                        return df, "json", metadata
                    else:
                        metadata = {
                            "shape": (len(data), len(data[0]) if data else 0),
                            "columns": list(data[0].keys()) if data else [],
                            "dtypes": None
                        }
                        return data, "json", metadata
                else:
                    metadata = {"shape": (len(data),), "columns": None, "dtypes": None}
                    return data, "json", metadata
            elif isinstance(data, dict):
                metadata = {"shape": (1, len(data)), "columns": list(data.keys()), "dtypes": None}
                return data, "json", metadata
            else:
                raise ValueError("Invalid JSON structure")
        
        elif data_format == "dict":
            if isinstance(data, dict):
                if all(isinstance(v, dict) for v in data.values()):
                    # Dict of dicts - convert to list
                    data = [{"key": k, **v} for k, v in data.items()]
                elif not isinstance(data, list):
                    # Single dict
                    data = [data]
                metadata = {
                    "shape": (len(data), len(data[0]) if data else 0),
                    "columns": list(data[0].keys()) if data else [],
                    "dtypes": None
                }
                return data, "dict", metadata
            else:
                raise ValueError("Expected dict format")
        
        elif data_format == "list":
            if isinstance(data, list):
                if not data:
                    raise ValueError("List is empty")
                metadata = {"shape": (len(data),), "columns": None, "dtypes": None}
                return data, "list", metadata
            else:
                raise ValueError("Expected list format")
        
        else:
            raise ValueError(f"Unsupported data format: {data_format}")
    
    def _prepare_data_for_analysis(self, data: Any, format_type: str) -> str:
        """
        Prepare data string representation for LLM analysis.
        
        Args:
            data: Loaded data
            format_type: Format of the data
        
        Returns:
            String representation of data
        """
        if format_type == "csv" and PANDAS_AVAILABLE and isinstance(data, pd.DataFrame):
            # Sample if too large
            if len(data) > self.max_rows_for_analysis:
                sampled = data.sample(n=self.max_rows_for_analysis, random_state=42)
                return f"[Sampled {self.max_rows_for_analysis} rows from {len(data)} total]\n" + sampled.to_string()
            return data.to_string()
        
        elif isinstance(data, list):
            # Sample if too large
            if len(data) > self.max_rows_for_analysis:
                import random
                random.seed(42)
                sampled = random.sample(data, self.max_rows_for_analysis)
                return f"[Sampled {self.max_rows_for_analysis} rows from {len(data)} total]\n" + json.dumps(sampled, indent=2)
            return json.dumps(data, indent=2)
        
        elif isinstance(data, dict):
            return json.dumps(data, indent=2)
        
        else:
            return str(data)
    
    def _build_analysis_prompt(
        self,
        data_str: str,
        analysis_type: str,
        focus_areas: Optional[List[str]],
        include_recommendations: bool,
        include_visualizations: bool,
        context: Optional[str],
        metadata: Dict[str, Any]
    ) -> str:
        """
        Build prompt for LLM data analysis.
        
        Args:
            data_str: String representation of data
            analysis_type: Type of analysis
            focus_areas: Specific areas to focus on
            include_recommendations: Whether to include recommendations
            include_visualizations: Whether to suggest visualizations
            context: Additional context
            metadata: Data metadata
        
        Returns:
            Formatted prompt string
        """
        analysis_desc = self.ANALYSIS_TYPES.get(analysis_type, analysis_type)
        
        system_prompt = f"""You are an expert data analyst. Analyze the provided dataset and generate insights.

Analysis Type: {analysis_type}
Description: {analysis_desc}

Dataset Information:
- Shape: {metadata.get('shape', 'Unknown')}
- Columns: {metadata.get('columns', 'N/A')}
"""
        
        if context:
            system_prompt += f"\nContext: {context}\n"
        
        if focus_areas:
            system_prompt += f"\nFocus Areas: {', '.join(focus_areas)}\n"
        
        system_prompt += "\nAnalysis Requirements:\n"
        system_prompt += "- Provide clear, actionable insights\n"
        system_prompt += "- Identify key patterns and trends\n"
        system_prompt += "- Use natural language explanations\n"
        system_prompt += "- Be specific with numbers and metrics\n"
        
        if analysis_type == "patterns":
            system_prompt += "- Focus on correlations and relationships\n"
        elif analysis_type == "trends":
            system_prompt += "- Identify temporal or categorical trends\n"
        elif analysis_type == "anomalies":
            system_prompt += "- Highlight outliers and unusual values\n"
        elif analysis_type == "comprehensive":
            system_prompt += "- Provide complete analysis covering all aspects\n"
        
        if include_recommendations:
            system_prompt += "\nInclude actionable recommendations based on findings.\n"
        
        if include_visualizations:
            system_prompt += "\nSuggest appropriate visualizations (charts, graphs) for the data.\n"
        
        system_prompt += "\nOutput Format:\n"
        system_prompt += "SUMMARY:\n[High-level summary]\n\n"
        system_prompt += "INSIGHTS:\n- [Insight 1]\n- [Insight 2]\n...\n\n"
        system_prompt += "PATTERNS:\n- [Pattern 1]\n- [Pattern 2]\n...\n\n"
        system_prompt += "TRENDS:\n- [Trend 1]\n- [Trend 2]\n...\n\n"
        
        if analysis_type in ["anomalies", "comprehensive"]:
            system_prompt += "ANOMALIES:\n- [Anomaly 1]\n- [Anomaly 2]\n...\n\n"
        
        if include_recommendations:
            system_prompt += "RECOMMENDATIONS:\n- [Recommendation 1]\n- [Recommendation 2]\n...\n\n"
        
        if include_visualizations:
            system_prompt += "VISUALIZATIONS:\n- [Visualization 1]\n- [Visualization 2]\n...\n"
        
        user_prompt = f"Analyze this dataset:\n\n{data_str}"
        
        return f"{system_prompt}\n\n{user_prompt}"
    
    def _extract_structured_insights(self, response: str, analysis_type: str) -> Dict[str, Any]:
        """
        Extract structured insights from LLM response.
        
        Args:
            response: Raw LLM response
            analysis_type: Type of analysis performed
        
        Returns:
            Dictionary with extracted insights
        """
        insights = {
            "summary": "",
            "insights": [],
            "patterns": [],
            "trends": [],
            "anomalies": [],
            "recommendations": [],
            "visualization_suggestions": []
        }
        
        # Extract summary
        summary_match = re.search(r'SUMMARY:\s*(.*?)(?=\n(?:INSIGHTS:|$))', response, re.DOTALL)
        if summary_match:
            insights["summary"] = summary_match.group(1).strip()
        
        # Extract insights
        insights_match = re.search(r'INSIGHTS:\s*(.*?)(?=\n(?:PATTERNS:|TRENDS:|ANOMALIES:|RECOMMENDATIONS:|VISUALIZATIONS:|$))', response, re.DOTALL)
        if insights_match:
            insights["insights"] = [
                line.strip()[2:] if line.strip().startswith('-') else line.strip()
                for line in insights_match.group(1).strip().split('\n')
                if line.strip()
            ]
        
        # Extract patterns
        patterns_match = re.search(r'PATTERNS:\s*(.*?)(?=\n(?:TRENDS:|ANOMALIES:|RECOMMENDATIONS:|VISUALIZATIONS:|$))', response, re.DOTALL)
        if patterns_match:
            insights["patterns"] = [
                line.strip()[2:] if line.strip().startswith('-') else line.strip()
                for line in patterns_match.group(1).strip().split('\n')
                if line.strip()
            ]
        
        # Extract trends
        trends_match = re.search(r'TRENDS:\s*(.*?)(?=\n(?:ANOMALIES:|RECOMMENDATIONS:|VISUALIZATIONS:|$))', response, re.DOTALL)
        if trends_match:
            insights["trends"] = [
                line.strip()[2:] if line.strip().startswith('-') else line.strip()
                for line in trends_match.group(1).strip().split('\n')
                if line.strip()
            ]
        
        # Extract anomalies (if applicable)
        if analysis_type in ["anomalies", "comprehensive"]:
            anomalies_match = re.search(r'ANOMALIES:\s*(.*?)(?=\n(?:RECOMMENDATIONS:|VISUALIZATIONS:|$))', response, re.DOTALL)
            if anomalies_match:
                insights["anomalies"] = [
                    line.strip()[2:] if line.strip().startswith('-') else line.strip()
                    for line in anomalies_match.group(1).strip().split('\n')
                    if line.strip()
                ]
        
        # Extract recommendations
        recommendations_match = re.search(r'RECOMMENDATIONS:\s*(.*?)(?=\n(?:VISUALIZATIONS:|$))', response, re.DOTALL)
        if recommendations_match:
            insights["recommendations"] = [
                line.strip()[2:] if line.strip().startswith('-') else line.strip()
                for line in recommendations_match.group(1).strip().split('\n')
                if line.strip()
            ]
        
        # Extract visualization suggestions
        visualizations_match = re.search(r'VISUALIZATIONS:\s*(.*?)$', response, re.DOTALL)
        if visualizations_match:
            insights["visualization_suggestions"] = [
                line.strip()[2:] if line.strip().startswith('-') else line.strip()
                for line in visualizations_match.group(1).strip().split('\n')
                if line.strip()
            ]
        
        # Fallback: if structured extraction failed, use response as summary
        if not insights["summary"] and not insights["insights"]:
            insights["summary"] = response.strip()
        
        return insights
    
    def analyze(
        self,
        data: Union[str, dict, list],
        analysis_type: str,
        data_format: Optional[str] = None,
        focus_areas: Optional[List[str]] = None,
        include_recommendations: bool = True,
        include_visualizations: bool = False,
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Analyze dataset and generate insights.
        
        Args:
            data: Dataset (path, dict, list, or JSON string)
            analysis_type: Type of analysis (summary, patterns, trends, comparison, anomalies, comprehensive)
            data_format: Format hint (csv, json, dict, list) - auto-detected if None
            focus_areas: Specific columns/fields to analyze
            include_recommendations: Whether to include recommendations
            include_visualizations: Whether to suggest visualizations
            context: Additional context about the data
        
        Returns:
            Dictionary with analysis results and metadata
        
        Raises:
            ValueError: If input is invalid
        
        Time Complexity: O(n) for data loading + O(m) for LLM generation
        Space Complexity: O(n) where n = dataset size
        
        Examples:
            >>> analyzer = DataAnalyzer()
            >>> result = analyzer.analyze(
            ...     {"sales": [100, 200, 300], "month": ["Jan", "Feb", "Mar"]},
            ...     "summary"
            ... )
            >>> print(result["summary"])
        """
        # Validate input
        if analysis_type not in self.ANALYSIS_TYPES:
            raise ValueError(
                f"Invalid analysis_type: {analysis_type}. "
                f"Supported: {list(self.ANALYSIS_TYPES.keys())}"
            )
        
        if context and len(context) > 200:
            raise ValueError("Context must be at most 200 characters")
        
        logger.info(f"Analyzing data with type: {analysis_type}")
        
        try:
            # Load data
            loaded_data, format_type, metadata = self._load_data(data, data_format)
            
            # Prepare data for analysis
            data_str = self._prepare_data_for_analysis(loaded_data, format_type)
            
            # Build analysis prompt
            prompt = self._build_analysis_prompt(
                data_str=data_str,
                analysis_type=analysis_type,
                focus_areas=focus_areas,
                include_recommendations=include_recommendations,
                include_visualizations=include_visualizations,
                context=context,
                metadata=metadata
            )
            
            # Generate analysis using LLM
            response = self.manager.generate(
                provider=self.provider,
                prompt=prompt,
                model=self.model,
                temperature=0.7
            )
            
            # Extract structured insights
            insights = self._extract_structured_insights(response, analysis_type)
            
            # Prepare metadata
            result_metadata = {
                "data_shape": metadata.get("shape"),
                "columns": metadata.get("columns"),
                "analysis_type": analysis_type,
                "data_types": metadata.get("dtypes")
            }
            
            logger.info(f"Analysis completed successfully")
            
            return {
                "success": True,
                "summary": insights["summary"],
                "insights": insights["insights"],
                "patterns": insights["patterns"],
                "trends": insights["trends"],
                "anomalies": insights["anomalies"] if analysis_type in ["anomalies", "comprehensive"] else [],
                "recommendations": insights["recommendations"] if include_recommendations else [],
                "visualization_suggestions": insights["visualization_suggestions"] if include_visualizations else [],
                "metadata": result_metadata,
                "error": None
            }
            
        except ValueError as e:
            logger.error(f"Validation error: {e}")
            raise
        
        except Exception as e:
            logger.error(f"Analysis failed: {e}")
            return {
                "success": False,
                "summary": "",
                "insights": [],
                "patterns": [],
                "trends": [],
                "anomalies": [],
                "recommendations": [],
                "visualization_suggestions": [],
                "metadata": {},
                "error": f"Analysis failed: {str(e)}"
            }


def main():
    """Demonstrate data analyzer with examples."""
    analyzer = DataAnalyzer(provider="openai")
    
    print("=" * 80)
    print("Data Analysis System - Examples")
    print("=" * 80)
    
    # Example 1: Sales Data Summary
    print("\n" + "-" * 80)
    print("Example 1: Sales Data Summary")
    print("-" * 80)
    
    try:
        sales_data = {
            "month": ["Jan", "Feb", "Mar", "Apr", "May"],
            "sales": [10000, 12000, 15000, 14000, 18000],
            "region": ["North", "South", "North", "South", "North"]
        }
        
        result1 = analyzer.analyze(
            data=sales_data,
            analysis_type="summary",
            include_recommendations=True,
            context="Monthly sales data for Q1-Q2"
        )
        
        if result1["success"]:
            print(f"\n✓ Summary:\n{result1['summary']}\n")
            print(f"✓ Insights: {len(result1['insights'])} found")
            for i, insight in enumerate(result1['insights'][:3], 1):
                print(f"  {i}. {insight}")
            print(f"\n✓ Recommendations: {len(result1['recommendations'])} found")
            for i, rec in enumerate(result1['recommendations'][:3], 1):
                print(f"  {i}. {rec}")
            print(f"\nMetadata: {result1['metadata']}\n")
        else:
            print(f"✗ Error: {result1['error']}\n")
    
    except Exception as e:
        print(f"✗ Exception: {e}\n")
    
    # Example 2: Pattern Analysis
    print("\n" + "-" * 80)
    print("Example 2: Pattern Analysis")
    print("-" * 80)
    
    try:
        employee_data = [
            {"age": 25, "salary": 50000, "department": "Engineering"},
            {"age": 30, "salary": 70000, "department": "Engineering"},
            {"age": 28, "salary": 45000, "department": "Marketing"},
            {"age": 35, "salary": 80000, "department": "Engineering"}
        ]
        
        result2 = analyzer.analyze(
            data=employee_data,
            analysis_type="patterns",
            focus_areas=["salary", "department"],
            include_recommendations=True
        )
        
        if result2["success"]:
            print(f"\n✓ Summary:\n{result2['summary'][:200]}...\n")
            print(f"✓ Patterns: {len(result2['patterns'])} found")
            for i, pattern in enumerate(result2['patterns'][:3], 1):
                print(f"  {i}. {pattern}")
            print(f"\nMetadata: {result2['metadata']}\n")
        else:
            print(f"✗ Error: {result2['error']}\n")
    
    except Exception as e:
        print(f"✗ Exception: {e}\n")
    
    # Example 3: Trends Analysis
    print("\n" + "-" * 80)
    print("Example 3: Trends Analysis")
    print("-" * 80)
    
    try:
        trend_data = {
            "quarter": ["Q1", "Q2", "Q3", "Q4"],
            "revenue": [100000, 120000, 150000, 180000],
            "expenses": [80000, 85000, 90000, 95000],
            "profit": [20000, 35000, 60000, 85000]
        }
        
        result3 = analyzer.analyze(
            data=trend_data,
            analysis_type="trends",
            include_recommendations=True
        )
        
        if result3["success"]:
            print(f"\n✓ Summary:\n{result3['summary'][:200]}...\n")
            print(f"✓ Trends: {len(result3['trends'])} found")
            for i, trend in enumerate(result3['trends'][:3], 1):
                print(f"  {i}. {trend}")
            print(f"\nMetadata: {result3['metadata']}\n")
        else:
            print(f"✗ Error: {result3['error']}\n")
    
    except Exception as e:
        print(f"✗ Exception: {e}\n")
    
    # Example 4: Error case - invalid analysis_type
    print("\n" + "-" * 80)
    print("Example 4: Error Case - Invalid Analysis Type")
    print("-" * 80)
    
    try:
        result4 = analyzer.analyze(
            data={"value": [1, 2, 3]},
            analysis_type="invalid_type"  # Invalid
        )
        print(f"Result: {result4}\n")
    except ValueError as e:
        print(f"✓ Caught expected error: {e}\n")
    
    # Example 5: Error case - empty data
    print("\n" + "-" * 80)
    print("Example 5: Error Case - Empty Data")
    print("-" * 80)
    
    try:
        result5 = analyzer.analyze(
            data=[],
            analysis_type="summary"
        )
        print(f"Result: {result5}\n")
    except ValueError as e:
        print(f"✓ Caught expected error: {e}\n")
    
    print("=" * 80)
    print("Examples completed!")
    print("=" * 80)


if __name__ == "__main__":
    main()

