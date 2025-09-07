# analysis_engine.py - Complete Line-by-Line Code Explanation

## Overview
The `analysis_engine.py` file contains the core statistical analysis functionality. It performs comprehensive data analysis including descriptive statistics, correlation analysis, distribution testing, outlier detection, hypothesis testing, and visualization generation.

## Detailed Code Breakdown

### Imports and Dependencies

```python
"""
Statistical analysis engine for data files.
Performs comprehensive statistical analysis including descriptive statistics,
correlation analysis, hypothesis testing, and data quality assessment.
"""

import asyncio
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List, Union
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from config import config
```

**Lines 1-21:**
- **Lines 1-5:** Module docstring explaining comprehensive analysis capabilities
- **Line 7:** `asyncio` for asynchronous operations
- **Line 8:** `json` for JSON data handling
- **Line 9:** `logging` for structured logging
- **Line 10:** `pathlib.Path` for file path operations
- **Line 11:** Type hints for better code documentation
- **Lines 12-13:** Core data science libraries (pandas, numpy)
- **Line 14:** `scipy.stats` for statistical tests and functions
- **Lines 15-16:** Matplotlib and Seaborn for static visualizations
- **Lines 17-19:** Plotly for interactive visualizations
- **Line 21:** Import global configuration

```python
logger = logging.getLogger(__name__)
```

**Line 23:** Create module-specific logger for tracking analysis operations

---

## AnalysisEngine Class

### Class Initialization

```python
class AnalysisEngine:
    """Main statistical analysis engine."""
    
    def __init__(self):
        self.config = config
```

**Lines 25-29:**
- **Line 25:** Define main analysis engine class
- **Line 28:** Store global configuration reference

### Main Analysis Method

```python
async def analyze_file(self, file_path: str) -> Optional[Dict[str, Any]]:
    """Analyze a data file and return comprehensive results."""
    try:
        logger.info(f"Starting analysis of: {file_path}")
        
        # Load data
        data = await self._load_data(file_path)
        if data is None or data.empty:
            logger.warning(f"No data loaded from: {file_path}")
            return None
        
        # Perform analysis
        analysis_results = {
            'file_info': self._get_file_info(file_path, data),
            'data_quality': await self._assess_data_quality(data),
            'descriptive_stats': await self._descriptive_analysis(data),
            'correlation_analysis': await self._correlation_analysis(data),
            'distribution_analysis': await self._distribution_analysis(data),
            'outlier_detection': await self._detect_outliers(data),
            'hypothesis_tests': await self._hypothesis_testing(data),
            'time_series_analysis': await self._time_series_analysis(data),
            'visualizations': await self._generate_visualizations(data, file_path)
        }
        
        logger.info(f"Analysis completed for: {file_path}")
        return analysis_results
        
    except Exception as e:
        logger.error(f"Analysis failed for {file_path}: {e}")
        return None
```

**Lines 31-59:**
- **Line 31:** Main async method orchestrating all analysis
- **Line 34:** Log analysis start
- **Lines 36-40:** Load and validate data
- **Lines 42-51:** Execute all analysis components:
  - File information and metadata
  - Data quality assessment
  - Descriptive statistics
  - Correlation analysis
  - Distribution analysis
  - Outlier detection
  - Hypothesis testing
  - Time series analysis
  - Visualization generation
- **Lines 53-59:** Success logging and error handling

---

## Data Loading Methods

### Multi-Format Data Loader

```python
async def _load_data(self, file_path: str) -> Optional[pd.DataFrame]:
    """Load data from various file formats."""
    try:
        file_extension = Path(file_path).suffix.lower()
        
        if file_extension == '.csv':
            data = pd.read_csv(file_path)
        elif file_extension == '.json':
            data = pd.read_json(file_path)
        elif file_extension == '.xlsx':
            data = pd.read_excel(file_path)
        elif file_extension == '.parquet':
            data = pd.read_parquet(file_path)
        else:
            logger.error(f"Unsupported file format: {file_extension}")
            return None
        
        logger.info(f"Loaded {len(data)} rows and {len(data.columns)} columns from {file_path}")
        return data
        
    except Exception as e:
        logger.error(f"Failed to load data from {file_path}: {e}")
        return None
```

**Lines 61-81:**
- **Line 64:** Extract file extension for format detection
- **Lines 66-73:** Load data based on file format:
  - CSV: Comma-separated values
  - JSON: JavaScript Object Notation
  - Excel: Microsoft Excel format
  - Parquet: Columnar storage format
- **Lines 74-76:** Handle unsupported formats
- **Line 78:** Log successful data loading with dimensions
- **Lines 80-81:** Error handling for loading failures

### File Information Extraction

```python
def _get_file_info(self, file_path: str, data: pd.DataFrame) -> Dict[str, Any]:
    """Get basic file and dataset information."""
    file_path_obj = Path(file_path)
    return {
        'file_name': file_path_obj.name,
        'file_path': str(file_path_obj),
        'file_size_mb': file_path_obj.stat().st_size / (1024 * 1024),
        'rows': len(data),
        'columns': len(data.columns),
        'column_names': list(data.columns),
        'data_types': data.dtypes.astype(str).to_dict(),
        'memory_usage_mb': data.memory_usage(deep=True).sum() / (1024 * 1024)
    }
```

**Lines 83-93:**
- **Line 86:** Basic file metadata including name and path
- **Line 88:** File size in megabytes
- **Lines 89-90:** Dataset dimensions (rows and columns)
- **Line 91:** List of column names
- **Line 92:** Data types for each column
- **Line 93:** Memory usage of loaded data

---

## Data Quality Assessment

### Comprehensive Quality Analysis

```python
async def _assess_data_quality(self, data: pd.DataFrame) -> Dict[str, Any]:
    """Assess data quality including missing values, duplicates, etc."""
    try:
        total_cells = data.size
        missing_count = data.isnull().sum()
        
        quality_assessment = {
            'missing_values': {
                'by_column': missing_count.to_dict(),
                'total_missing': missing_count.sum(),
                'missing_percentage': (missing_count.sum() / total_cells) * 100
            },
            'duplicate_rows': {
                'count': data.duplicated().sum(),
                'percentage': (data.duplicated().sum() / len(data)) * 100
            },
            'data_completeness': {
                'complete_rows': len(data.dropna()),
                'complete_percentage': (len(data.dropna()) / len(data)) * 100
            }
        }
```

**Lines 95-114:**
- **Line 98:** Calculate total cells in dataset
- **Line 99:** Count missing values per column
- **Lines 101-106:** Missing values analysis:
  - Count by column
  - Total missing values
  - Percentage of missing data
- **Lines 107-110:** Duplicate row detection
- **Lines 111-114:** Data completeness metrics

### Column-Specific Quality Checks

```python
        # Column-specific quality checks
        column_quality = {}
        for column in data.columns:
            col_data = data[column]
            column_quality[column] = {
                'type': str(col_data.dtype),
                'missing_count': col_data.isnull().sum(),
                'missing_percentage': (col_data.isnull().sum() / len(col_data)) * 100,
                'unique_values': col_data.nunique(),
                'unique_percentage': (col_data.nunique() / len(col_data)) * 100
            }
            
            # Add numeric-specific checks
            if pd.api.types.is_numeric_dtype(col_data):
                column_quality[column].update({
                    'zero_count': (col_data == 0).sum(),
                    'negative_count': (col_data < 0).sum() if col_data.dtype != bool else 0,
                    'infinite_count': np.isinf(col_data).sum()
                })
        
        quality_assessment['column_quality'] = column_quality
        return quality_assessment
```

**Lines 116-137:**
- **Lines 118-125:** Basic column statistics:
  - Data type
  - Missing values count and percentage
  - Unique values count and percentage
- **Lines 127-132:** Numeric column specific checks:
  - Count of zero values
  - Count of negative values
  - Count of infinite values
- **Lines 134-135:** Add column quality to main assessment

---

## Descriptive Statistics Analysis

### Comprehensive Statistical Summary

```python
async def _descriptive_analysis(self, data: pd.DataFrame) -> Dict[str, Any]:
    """Perform descriptive statistical analysis."""
    try:
        numeric_columns = data.select_dtypes(include=[np.number]).columns
        categorical_columns = data.select_dtypes(include=['object', 'category']).columns
        
        analysis = {
            'numeric_summary': {},
            'categorical_summary': {},
            'overall_summary': {}
        }
        
        # Numeric analysis
        if len(numeric_columns) > 0:
            numeric_data = data[numeric_columns]
            desc_stats = numeric_data.describe()
            
            analysis['numeric_summary'] = {
                'basic_stats': desc_stats.to_dict(),
                'additional_stats': {}
            }
            
            for col in numeric_columns:
                col_data = numeric_data[col].dropna()
                if len(col_data) > 0:
                    analysis['numeric_summary']['additional_stats'][col] = {
                        'skewness': float(stats.skew(col_data)),
                        'kurtosis': float(stats.kurtosis(col_data)),
                        'variance': float(col_data.var()),
                        'coefficient_of_variation': float(col_data.std() / col_data.mean()) if col_data.mean() != 0 else None,
                        'range': float(col_data.max() - col_data.min()),
                        'iqr': float(col_data.quantile(0.75) - col_data.quantile(0.25))
                    }
```

**Lines 141-172:**
- **Lines 144-145:** Separate numeric and categorical columns
- **Lines 147-151:** Initialize analysis structure
- **Lines 153-157:** Generate basic pandas describe() statistics
- **Lines 164-172:** Advanced statistics for each numeric column:
  - Skewness (measure of asymmetry)
  - Kurtosis (measure of tail heaviness)
  - Variance (measure of spread)
  - Coefficient of variation (relative variability)
  - Range (max - min)
  - Interquartile range (75th - 25th percentile)

### Categorical Data Analysis

```python
        # Categorical analysis
        if len(categorical_columns) > 0:
            for col in categorical_columns:
                col_data = data[col].dropna()
                value_counts = col_data.value_counts()
                
                analysis['categorical_summary'][col] = {
                    'unique_count': len(value_counts),
                    'most_frequent': str(value_counts.index[0]) if len(value_counts) > 0 else None,
                    'most_frequent_count': int(value_counts.iloc[0]) if len(value_counts) > 0 else 0,
                    'value_counts': value_counts.head(10).to_dict(),  # Top 10 values
                    'entropy': float(stats.entropy(value_counts)) if len(value_counts) > 1 else 0.0
                }
```

**Lines 174-186:**
- **Lines 177-178:** Count frequency of each categorical value
- **Lines 180-186:** Categorical statistics:
  - Total unique values
  - Most frequent value and its count
  - Top 10 value counts
  - Shannon entropy (measure of disorder/information)

---

## Correlation Analysis

### Multi-Method Correlation Analysis

```python
async def _correlation_analysis(self, data: pd.DataFrame) -> Dict[str, Any]:
    """Analyze correlations between numeric variables."""
    try:
        numeric_data = data.select_dtypes(include=[np.number])
        
        if len(numeric_data.columns) < 2:
            return {'message': 'Insufficient numeric columns for correlation analysis'}
        
        # Calculate correlation matrices
        pearson_corr = numeric_data.corr(method='pearson')
        spearman_corr = numeric_data.corr(method='spearman')
        
        # Find strong correlations
        threshold = self.config.analysis_config['correlation_threshold']
        strong_correlations = []
        
        for i in range(len(pearson_corr.columns)):
            for j in range(i+1, len(pearson_corr.columns)):
                corr_value = pearson_corr.iloc[i, j]
                if abs(corr_value) >= threshold:
                    strong_correlations.append({
                        'variable1': pearson_corr.columns[i],
                        'variable2': pearson_corr.columns[j],
                        'pearson_correlation': float(corr_value),
                        'spearman_correlation': float(spearman_corr.iloc[i, j]),
                        'strength': 'Strong' if abs(corr_value) >= 0.7 else 'Moderate'
                    })
```

**Lines 202-227:**
- **Line 205:** Filter to numeric columns only
- **Lines 207-208:** Require at least 2 numeric columns
- **Lines 210-211:** Calculate Pearson and Spearman correlations:
  - Pearson: Linear relationships
  - Spearman: Monotonic relationships
- **Lines 213-227:** Identify strong correlations:
  - Use configurable threshold
  - Avoid duplicate pairs (i < j)
  - Classify as strong (≥0.7) or moderate

---

## Distribution Analysis

### Normality Testing and Distribution Classification

```python
async def _distribution_analysis(self, data: pd.DataFrame) -> Dict[str, Any]:
    """Analyze distributions of numeric variables."""
    try:
        numeric_columns = data.select_dtypes(include=[np.number]).columns
        
        if len(numeric_columns) == 0:
            return {'message': 'No numeric columns for distribution analysis'}
        
        distribution_analysis = {}
        
        for col in numeric_columns:
            col_data = data[col].dropna()
            
            if len(col_data) < 10:  # Skip if too few data points
                continue
            
            # Normality tests
            shapiro_stat, shapiro_p = stats.shapiro(col_data) if len(col_data) <= 5000 else (None, None)
            ks_stat, ks_p = stats.kstest(col_data, 'norm', args=(col_data.mean(), col_data.std()))
            
            distribution_analysis[col] = {
                'normality_tests': {
                    'shapiro_wilk': {
                        'statistic': float(shapiro_stat) if shapiro_stat is not None else None,
                        'p_value': float(shapiro_p) if shapiro_p is not None else None,
                        'is_normal': bool(shapiro_p > 0.05) if shapiro_p is not None else None
                    },
                    'kolmogorov_smirnov': {
                        'statistic': float(ks_stat),
                        'p_value': float(ks_p),
                        'is_normal': bool(ks_p > 0.05)
                    }
                },
                'distribution_characteristics': {
                    'skewness': float(stats.skew(col_data)),
                    'kurtosis': float(stats.kurtosis(col_data)),
                    'is_symmetric': abs(stats.skew(col_data)) < 0.5,
                    'distribution_type': self._classify_distribution(col_data)
                }
            }
```

**Lines 244-281:**
- **Lines 250-252:** Skip columns with insufficient data
- **Lines 254-255:** Normality tests:
  - Shapiro-Wilk test (limited to ≤5000 samples)
  - Kolmogorov-Smirnov test (compares to normal distribution)
- **Lines 257-271:** Store test results with statistical significance
- **Lines 272-278:** Distribution characteristics:
  - Skewness and kurtosis values
  - Symmetry assessment
  - Distribution type classification

### Distribution Classification Helper

```python
def _classify_distribution(self, data: pd.Series) -> str:
    """Classify the distribution type based on characteristics."""
    skewness = stats.skew(data)
    kurtosis = stats.kurtosis(data)
    
    if abs(skewness) < 0.5:
        if -0.5 < kurtosis < 0.5:
            return "Normal-like"
        elif kurtosis > 0.5:
            return "Leptokurtic (peaked)"
        else:
            return "Platykurtic (flat)"
    elif skewness > 0.5:
        return "Right-skewed"
    else:
        return "Left-skewed"
```

**Lines 291-306:**
- **Lines 294-295:** Calculate skewness and kurtosis
- **Lines 297-304:** Classification logic:
  - Symmetric distributions (|skewness| < 0.5): Normal-like, peaked, or flat
  - Asymmetric distributions: Right-skewed or left-skewed

---

## Outlier Detection

### Multi-Method Outlier Detection

```python
async def _detect_outliers(self, data: pd.DataFrame) -> Dict[str, Any]:
    """Detect outliers using multiple methods."""
    try:
        numeric_columns = data.select_dtypes(include=[np.number]).columns
        
        if len(numeric_columns) == 0:
            return {'message': 'No numeric columns for outlier detection'}
        
        outlier_analysis = {}
        
        for col in numeric_columns:
            col_data = data[col].dropna()
            
            if len(col_data) < 10:
                continue
            
            # IQR method
            Q1 = col_data.quantile(0.25)
            Q3 = col_data.quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            iqr_outliers = col_data[(col_data < lower_bound) | (col_data > upper_bound)]
            
            # Z-score method
            z_scores = np.abs(stats.zscore(col_data))
            z_outliers = col_data[z_scores > 3]
            
            outlier_analysis[col] = {
                'iqr_method': {
                    'count': len(iqr_outliers),
                    'percentage': (len(iqr_outliers) / len(col_data)) * 100,
                    'lower_bound': float(lower_bound),
                    'upper_bound': float(upper_bound),
                    'outlier_values': iqr_outliers.tolist()[:10]  # First 10 outliers
                },
                'zscore_method': {
                    'count': len(z_outliers),
                    'percentage': (len(z_outliers) / len(col_data)) * 100,
                    'outlier_values': z_outliers.tolist()[:10]  # First 10 outliers
                }
            }
```

**Lines 308-345:**
- **Lines 318-323:** IQR (Interquartile Range) method:
  - Calculate Q1, Q3, and IQR
  - Define bounds as Q1 - 1.5×IQR and Q3 + 1.5×IQR
  - Identify values outside bounds
- **Lines 325-326:** Z-score method:
  - Calculate standard scores
  - Identify values with |z-score| > 3
- **Lines 328-342:** Store results with counts, percentages, and sample values

---

## Hypothesis Testing

### Comprehensive Statistical Testing

```python
async def _hypothesis_testing(self, data: pd.DataFrame) -> Dict[str, Any]:
    """Perform various hypothesis tests."""
    try:
        numeric_columns = data.select_dtypes(include=[np.number]).columns
        
        if len(numeric_columns) < 2:
            return {'message': 'Insufficient numeric columns for hypothesis testing'}
        
        tests_results = {
            'one_sample_tests': {},
            'two_sample_tests': {},
            'anova_tests': {}
        }
        
        # One-sample t-tests (testing if mean significantly differs from 0)
        for col in numeric_columns:
            col_data = data[col].dropna()
            if len(col_data) > 30:  # Sufficient sample size
                t_stat, p_value = stats.ttest_1samp(col_data, 0)
                tests_results['one_sample_tests'][col] = {
                    'test': 'One-sample t-test (mean != 0)',
                    't_statistic': float(t_stat),
                    'p_value': float(p_value),
                    'significant': bool(p_value < 0.05),
                    'mean': float(col_data.mean())
                }
```

**Lines 355-380:**
- **Lines 362-365:** Initialize test results structure
- **Lines 367-380:** One-sample t-tests:
  - Test if population mean significantly differs from 0
  - Require sample size > 30 for validity
  - Store t-statistic, p-value, and significance

### Two-Sample Testing

```python
        # Two-sample tests between pairs of numeric columns
        for i, col1 in enumerate(numeric_columns):
            for col2 in numeric_columns[i+1:]:
                data1 = data[col1].dropna()
                data2 = data[col2].dropna()
                
                if len(data1) > 10 and len(data2) > 10:
                    # Independent t-test
                    t_stat, p_value = stats.ttest_ind(data1, data2)
                    
                    # Mann-Whitney U test (non-parametric)
                    u_stat, u_p_value = stats.mannwhitneyu(data1, data2, alternative='two-sided')
                    
                    tests_results['two_sample_tests'][f"{col1}_vs_{col2}"] = {
                        'independent_t_test': {
                            't_statistic': float(t_stat),
                            'p_value': float(p_value),
                            'significant': bool(p_value < 0.05)
                        },
                        'mann_whitney_u': {
                            'u_statistic': float(u_stat),
                            'p_value': float(u_p_value),
                            'significant': bool(u_p_value < 0.05)
                        }
                    }
```

**Lines 382-404:**
- **Lines 383-385:** Test all pairs of numeric columns
- **Lines 387-388:** Require minimum sample sizes
- **Lines 389-390:** Independent t-test (parametric)
- **Lines 392-393:** Mann-Whitney U test (non-parametric alternative)
- **Lines 395-404:** Store both test results with significance

---

## Time Series Analysis

### Time Series Detection and Analysis

```python
async def _time_series_analysis(self, data: pd.DataFrame) -> Dict[str, Any]:
    """Analyze time series data if date columns are present."""
    try:
        # Look for date/time columns
        date_columns = []
        for col in data.columns:
            if data[col].dtype == 'datetime64[ns]' or 'date' in col.lower() or 'time' in col.lower():
                try:
                    pd.to_datetime(data[col])
                    date_columns.append(col)
                except:
                    continue
        
        if not date_columns:
            return {'message': 'No time series data detected'}
```

**Lines 414-427:**
- **Lines 417-423:** Detect date/time columns:
  - Check for datetime data type
  - Check for 'date' or 'time' in column names
  - Validate convertibility to datetime
- **Lines 425-426:** Return early if no time data found

### Time Series Frequency Analysis

```python
def _analyze_time_frequency(self, date_series: pd.Series) -> Dict[str, Any]:
    """Analyze frequency patterns in time series data."""
    try:
        # Calculate time differences
        sorted_dates = date_series.dropna().sort_values()
        if len(sorted_dates) < 2:
            return {}
        
        time_diffs = sorted_dates.diff().dropna()
        
        # Most common time difference
        most_common_diff = time_diffs.mode()
        
        return {
            'total_records': len(sorted_dates),
            'unique_dates': len(sorted_dates.unique()),
            'most_common_interval': str(most_common_diff.iloc[0]) if len(most_common_diff) > 0 else None,
            'avg_interval': str(time_diffs.mean()),
            'data_coverage': {
                'daily_coverage': len(sorted_dates.dt.date.unique()),
                'monthly_coverage': len(sorted_dates.dt.to_period('M').unique()),
                'yearly_coverage': len(sorted_dates.dt.to_period('Y').unique())
            }
        }
```

**Lines 471-490:**
- **Lines 474-477:** Calculate time differences between consecutive dates
- **Line 480:** Find most common time interval
- **Lines 482-490:** Time series characteristics:
  - Total records and unique dates
  - Most common and average intervals
  - Coverage at daily, monthly, yearly levels

---

## Visualization Generation

### Comprehensive Visualization Suite

```python
async def _generate_visualizations(self, data: pd.DataFrame, file_path: str) -> Dict[str, Any]:
    """Generate visualizations and save them."""
    try:
        visualizations = {
            'generated_files': [],
            'descriptions': {}
        }
        
        output_dir = Path(self.config.output_directory) / 'visualizations'
        output_dir.mkdir(parents=True, exist_ok=True)
        
        file_name = Path(file_path).stem
        
        numeric_columns = data.select_dtypes(include=[np.number]).columns
        
        # 1. Correlation heatmap
        if len(numeric_columns) > 1:
            plt.figure(figsize=(12, 10))
            corr_matrix = data[numeric_columns].corr()
            sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, 
                       square=True, fmt='.2f')
            plt.title(f'Correlation Matrix - {file_name}')
            heatmap_path = output_dir / f'{file_name}_correlation_heatmap.png'
            plt.savefig(heatmap_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            visualizations['generated_files'].append(str(heatmap_path))
            visualizations['descriptions']['correlation_heatmap'] = 'Correlation matrix showing relationships between numeric variables'
```

**Lines 492-519:**
- **Lines 495-497:** Initialize visualization tracking
- **Lines 499-503:** Setup output directory and file naming
- **Lines 507-519:** Correlation heatmap:
  - Create seaborn heatmap with annotations
  - Use diverging colormap centered at 0
  - Save as high-resolution PNG
  - Track generated file and description

### Distribution and Box Plot Generation

```python
        # 2. Distribution plots
        if len(numeric_columns) > 0:
            fig, axes = plt.subplots(2, 2, figsize=(15, 12))
            axes = axes.ravel()
            
            for i, col in enumerate(numeric_columns[:4]):  # First 4 columns
                if i < len(axes):
                    data[col].hist(bins=30, ax=axes[i], alpha=0.7)
                    axes[i].set_title(f'Distribution of {col}')
                    axes[i].set_xlabel(col)
                    axes[i].set_ylabel('Frequency')
            
            # Hide empty subplots
            for i in range(len(numeric_columns), len(axes)):
                axes[i].axis('off')
            
            plt.tight_layout()
            dist_path = output_dir / f'{file_name}_distributions.png'
            plt.savefig(dist_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            visualizations['generated_files'].append(str(dist_path))
            visualizations['descriptions']['distributions'] = 'Distribution plots for numeric variables'
        
        # 3. Box plots for outlier detection
        if len(numeric_columns) > 0:
            fig, ax = plt.subplots(figsize=(12, 8))
            data[numeric_columns].boxplot(ax=ax)
            plt.title(f'Box Plots - {file_name}')
            plt.xticks(rotation=45)
            boxplot_path = output_dir / f'{file_name}_boxplots.png'
            plt.savefig(boxplot_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            visualizations['generated_files'].append(str(boxplot_path))
            visualizations['descriptions']['boxplots'] = 'Box plots for outlier detection in numeric variables'
        
        return visualizations
```

**Lines 521-553:**
- **Lines 521-540:** Distribution histograms:
  - Create 2×2 subplot grid
  - Generate histograms for first 4 numeric columns
  - Hide unused subplots
- **Lines 542-553:** Box plots:
  - Create box plots for all numeric columns
  - Useful for outlier visualization
  - Rotate x-axis labels for readability

---

## Key Design Patterns and Principles

### 1. **Async Processing Pattern**
- All analysis methods are asynchronous
- Prevents blocking during long-running analyses
- Enables concurrent processing of multiple aspects

### 2. **Comprehensive Analysis Strategy**
- Multiple statistical approaches for robust insights
- Both parametric and non-parametric tests
- Validation of assumptions (normality, sample size)

### 3. **Error Resilience**
- Graceful handling of insufficient data
- Skip problematic columns rather than failing entirely
- Detailed error logging for debugging

### 4. **Configurable Thresholds**
- Statistical significance levels
- Correlation thresholds
- Sample size requirements
- All configurable via environment variables

### 5. **Multi-Format Support**
- Handles various data file formats
- Consistent analysis regardless of input format
- Extensible for additional formats

### 6. **Visualization Integration**
- Automatic generation of relevant plots
- High-quality output suitable for reports
- Descriptive file naming and tracking

This analysis engine provides a comprehensive statistical toolkit that can handle various data types and formats while producing both numerical results and visual insights suitable for both technical and non-technical audiences.