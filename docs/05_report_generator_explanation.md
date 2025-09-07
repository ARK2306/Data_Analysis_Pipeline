# report_generator.py - Complete Line-by-Line Code Explanation

## Overview
The `report_generator.py` file handles integration with the Amplify API for AI-powered insights and generates comprehensive reports in multiple formats (HTML, JSON, and text summaries).

## Detailed Code Breakdown

### Imports and Dependencies

```python
"""
Report generator with Amplify API integration for AI-powered insights.
Generates comprehensive reports combining statistical analysis with AI insights.
"""

import asyncio
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List
import requests
from jinja2 import Template

from config import config
```

**Lines 1-15:**
- **Lines 1-4:** Module docstring explaining dual functionality
- **Line 6:** `asyncio` for asynchronous API calls
- **Line 7:** `json` for JSON data handling
- **Line 8:** `logging` for structured logging
- **Line 9:** `datetime` for timestamps in reports
- **Line 10:** `pathlib.Path` for file operations
- **Line 11:** Type hints for better code documentation
- **Line 12:** `requests` for HTTP API communication
- **Line 13:** `jinja2.Template` for HTML template rendering
- **Line 15:** Import global configuration

```python
logger = logging.getLogger(__name__)
```

**Line 17:** Create module-specific logger for tracking report generation

---

## AmplifyAPIClient Class

### API Client Initialization

```python
class AmplifyAPIClient:
    """Client for interacting with Amplify API."""
    
    def __init__(self):
        self.api_key = config.amplify_api_key
        self.base_url = config.amplify_base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        })
```

**Lines 19-29:**
- **Line 19:** Define API client class
- **Line 22:** Get API key from configuration
- **Line 23:** Get base URL from configuration
- **Line 24:** Create persistent HTTP session for efficiency
- **Lines 25-28:** Configure session headers:
  - Bearer token authorization
  - JSON content type

### AI Insights Generation

```python
async def generate_insights(self, analysis_data: Dict[str, Any], file_info: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Generate AI-powered insights from analysis data."""
    try:
        logger.info("Generating AI insights via Amplify API")
        
        # Prepare the prompt for the AI
        prompt = self._create_analysis_prompt(analysis_data, file_info)
        
        payload = {
            "messages": [
                {
                    "role": "system",
                    "content": "You are a data analyst AI assistant. Analyze the provided statistical data and provide actionable insights, key findings, and recommendations. Focus on business implications and data quality issues."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": 2000,
            "temperature": 0.7,
            "model": "claude-3-sonnet-20240229"
        }
        
        response = self.session.post(
            f"{self.base_url}/messages",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            logger.info("AI insights generated successfully")
            return {
                'insights': result.get('content', [{}])[0].get('text', ''),
                'model': result.get('model', 'unknown'),
                'usage': result.get('usage', {})
            }
        else:
            logger.error(f"Amplify API error: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        logger.error(f"Failed to generate AI insights: {e}")
        return None
```

**Lines 31-67:**
- **Line 31:** Main async method for AI insight generation
- **Line 36:** Create structured prompt from analysis data
- **Lines 38-49:** Construct API payload:
  - System message defines AI role and capabilities
  - User message contains analysis data
  - Configure response parameters (tokens, temperature, model)
- **Lines 51-55:** Make API request with timeout
- **Lines 57-65:** Process successful response:
  - Extract insights text from response
  - Store model and usage information
- **Lines 66-70:** Error handling and logging

### Prompt Creation for AI Analysis

```python
def _create_analysis_prompt(self, analysis_data: Dict[str, Any], file_info: Dict[str, Any]) -> str:
    """Create a comprehensive prompt for AI analysis."""
    prompt_parts = []
    
    # File information
    prompt_parts.append(f"Dataset Information:")
    prompt_parts.append(f"- File: {file_info.get('file_name', 'Unknown')}")
    prompt_parts.append(f"- Rows: {file_info.get('rows', 0):,}")
    prompt_parts.append(f"- Columns: {file_info.get('columns', 0)}")
    prompt_parts.append("")
```

**Lines 69-78:**
- **Line 71:** Initialize list to build structured prompt
- **Lines 74-78:** Add basic file information:
  - File name and dataset dimensions
  - Formatted row count with thousands separators

### Data Quality Summary in Prompt

```python
    # Data quality summary
    if 'data_quality' in analysis_data:
        quality = analysis_data['data_quality']
        missing_pct = quality.get('missing_values', {}).get('missing_percentage', 0)
        duplicate_pct = quality.get('duplicate_rows', {}).get('percentage', 0)
        
        prompt_parts.append(f"Data Quality:")
        prompt_parts.append(f"- Missing values: {missing_pct:.1f}%")
        prompt_parts.append(f"- Duplicate rows: {duplicate_pct:.1f}%")
        prompt_parts.append("")
```

**Lines 80-88:**
- **Line 81:** Check if data quality analysis exists
- **Lines 82-83:** Extract missing values and duplicate percentages
- **Lines 85-88:** Add formatted quality metrics to prompt

### Statistical Summary in Prompt

```python
    # Statistical summary
    if 'descriptive_stats' in analysis_data:
        stats = analysis_data['descriptive_stats']
        numeric_count = stats.get('overall_summary', {}).get('numeric_columns_count', 0)
        categorical_count = stats.get('overall_summary', {}).get('categorical_columns_count', 0)
        
        prompt_parts.append(f"Statistical Summary:")
        prompt_parts.append(f"- Numeric columns: {numeric_count}")
        prompt_parts.append(f"- Categorical columns: {categorical_count}")
        
        # Add key statistics for first few numeric columns
        numeric_summary = stats.get('numeric_summary', {})
        basic_stats = numeric_summary.get('basic_stats', {})
        additional_stats = numeric_summary.get('additional_stats', {})
        
        for col, col_stats in list(basic_stats.items())[:3]:  # First 3 columns
            prompt_parts.append(f"  {col}:")
            prompt_parts.append(f"    - Mean: {col_stats.get('mean', 0):.2f}")
            prompt_parts.append(f"    - Std: {col_stats.get('std', 0):.2f}")
            
            if col in additional_stats:
                skew = additional_stats[col].get('skewness', 0)
                prompt_parts.append(f"    - Skewness: {skew:.2f}")
        
        prompt_parts.append("")
```

**Lines 90-112:**
- **Lines 93-94:** Extract column counts by type
- **Lines 96-98:** Add column type summary
- **Lines 100-102:** Get detailed statistics for numeric columns
- **Lines 104-111:** Add key statistics for first 3 numeric columns:
  - Mean, standard deviation, and skewness
  - Formatted to 2 decimal places

### Correlation and Outlier Information in Prompt

```python
    # Correlation findings
    if 'correlation_analysis' in analysis_data:
        corr = analysis_data['correlation_analysis']
        strong_corr = corr.get('strong_correlations', [])
        
        if strong_corr:
            prompt_parts.append(f"Strong Correlations Found ({len(strong_corr)}):")
            for correlation in strong_corr[:5]:  # Top 5
                prompt_parts.append(f"- {correlation['variable1']} vs {correlation['variable2']}: {correlation['pearson_correlation']:.3f}")
            prompt_parts.append("")
    
    # Outlier information
    if 'outlier_detection' in analysis_data:
        outliers = analysis_data['outlier_detection']
        prompt_parts.append("Outlier Detection:")
        for col, col_outliers in list(outliers.items())[:3]:  # First 3 columns
            if isinstance(col_outliers, dict):
                iqr_count = col_outliers.get('iqr_method', {}).get('count', 0)
                iqr_pct = col_outliers.get('iqr_method', {}).get('percentage', 0)
                prompt_parts.append(f"- {col}: {iqr_count} outliers ({iqr_pct:.1f}%)")
        prompt_parts.append("")
```

**Lines 114-131:**
- **Lines 116-121:** Add strong correlations (limit to top 5)
- **Lines 123-130:** Add outlier detection results:
  - Show outlier counts and percentages
  - Limit to first 3 columns for brevity

### AI Request Instructions

```python
    prompt_parts.append("Please provide:")
    prompt_parts.append("1. Key findings and insights")
    prompt_parts.append("2. Data quality assessment and recommendations")
    prompt_parts.append("3. Business implications of the statistical findings")
    prompt_parts.append("4. Recommendations for further analysis or data collection")
    prompt_parts.append("5. Any potential issues or concerns identified")
    
    return "\n".join(prompt_parts)
```

**Lines 146-153:**
- **Lines 146-152:** Specific instructions for AI analysis:
  - Key findings and insights
  - Data quality assessment
  - Business implications
  - Further analysis recommendations
  - Issue identification
- **Line 153:** Join all prompt parts into single string

---

## ReportGenerator Class

### Report Generator Initialization

```python
class ReportGenerator:
    """Main report generator class."""
    
    def __init__(self):
        self.config = config
        self.amplify_client = AmplifyAPIClient()
        self.output_dir = Path(self.config.output_directory) / 'reports'
        self.output_dir.mkdir(parents=True, exist_ok=True)
```

**Lines 155-162:**
- **Line 158:** Store configuration reference
- **Line 159:** Create Amplify API client instance
- **Lines 160-161:** Setup output directory for reports

### Main Report Generation Method

```python
async def generate_report(self, file_path: str, analysis_results: Dict[str, Any]) -> Optional[str]:
    """Generate a comprehensive analysis report."""
    try:
        logger.info(f"Generating report for analysis of: {file_path}")
        
        file_name = Path(file_path).stem
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Generate AI insights
        ai_insights = await self.amplify_client.generate_insights(
            analysis_results, 
            analysis_results.get('file_info', {})
        )
        
        # Create comprehensive report
        report_data = {
            'metadata': {
                'file_path': file_path,
                'file_name': file_name,
                'analysis_timestamp': datetime.now().isoformat(),
                'report_version': '1.0'
            },
            'analysis_results': analysis_results,
            'ai_insights': ai_insights,
            'executive_summary': self._create_executive_summary(analysis_results, ai_insights)
        }
        
        # Generate HTML report
        html_report_path = await self._generate_html_report(report_data, file_name, timestamp)
        
        # Generate JSON report
        json_report_path = await self._generate_json_report(report_data, file_name, timestamp)
        
        # Generate summary report
        summary_report_path = await self._generate_summary_report(report_data, file_name, timestamp)
        
        logger.info(f"Reports generated successfully:")
        logger.info(f"- HTML: {html_report_path}")
        logger.info(f"- JSON: {json_report_path}")
        logger.info(f"- Summary: {summary_report_path}")
        
        return html_report_path
        
    except Exception as e:
        logger.error(f"Report generation failed: {e}")
        return None
```

**Lines 164-202:**
- **Line 167:** Extract file name and create timestamp
- **Lines 171-174:** Generate AI insights using analysis data
- **Lines 176-185:** Create comprehensive report data structure:
  - Metadata with file info and timestamps
  - Complete analysis results
  - AI insights
  - Executive summary
- **Lines 187-193:** Generate multiple report formats
- **Lines 195-199:** Log successful generation
- **Line 201:** Return HTML report path (primary format)

### Executive Summary Creation

```python
def _create_executive_summary(self, analysis_results: Dict[str, Any], ai_insights: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """Create an executive summary of the analysis."""
    summary = {
        'dataset_overview': {},
        'key_findings': [],
        'data_quality_score': 0,
        'recommendations': []
    }
    
    # Dataset overview
    file_info = analysis_results.get('file_info', {})
    summary['dataset_overview'] = {
        'total_rows': file_info.get('rows', 0),
        'total_columns': file_info.get('columns', 0),
        'file_size_mb': file_info.get('file_size_mb', 0),
        'data_types': len(set(file_info.get('data_types', {}).values()))
    }
    
    # Data quality score calculation
    quality_data = analysis_results.get('data_quality', {})
    missing_pct = quality_data.get('missing_values', {}).get('missing_percentage', 0)
    duplicate_pct = quality_data.get('duplicate_rows', {}).get('percentage', 0)
    complete_pct = quality_data.get('data_completeness', {}).get('complete_percentage', 100)
    
    # Simple quality score (0-100)
    quality_score = max(0, 100 - missing_pct - duplicate_pct * 0.5)
    summary['data_quality_score'] = round(quality_score, 1)
```

**Lines 204-229:**
- **Lines 206-210:** Initialize summary structure
- **Lines 212-218:** Extract dataset overview metrics
- **Lines 220-224:** Extract data quality metrics
- **Lines 226-227:** Calculate simple quality score:
  - Start at 100%
  - Subtract missing value percentage
  - Subtract half of duplicate percentage
  - Ensure non-negative result

### Key Findings Extraction

```python
    # Key findings from statistical analysis
    findings = []
    
    # Missing values finding
    if missing_pct > 5:
        findings.append(f"High missing values: {missing_pct:.1f}% of data is missing")
    elif missing_pct > 1:
        findings.append(f"Some missing values: {missing_pct:.1f}% of data is missing")
    
    # Duplicate findings
    if duplicate_pct > 1:
        findings.append(f"Duplicate records detected: {duplicate_pct:.1f}% of rows")
    
    # Correlation findings
    corr_data = analysis_results.get('correlation_analysis', {})
    strong_corrs = corr_data.get('strong_correlations', [])
    if strong_corrs:
        findings.append(f"Found {len(strong_corrs)} strong correlations between variables")
    
    # Outlier findings
    outlier_data = analysis_results.get('outlier_detection', {})
    if outlier_data:
        outlier_columns = [col for col, data in outlier_data.items() 
                         if isinstance(data, dict) and data.get('iqr_method', {}).get('count', 0) > 0]
        if outlier_columns:
            findings.append(f"Outliers detected in {len(outlier_columns)} columns")
    
    summary['key_findings'] = findings
```

**Lines 231-253:**
- **Lines 234-237:** Add missing value findings based on severity
- **Lines 239-241:** Add duplicate record findings
- **Lines 243-246:** Add correlation findings
- **Lines 248-252:** Add outlier detection findings
- **Line 253:** Store all findings in summary

---

## HTML Report Generation

### Comprehensive HTML Template

```python
async def _generate_html_report(self, report_data: Dict[str, Any], file_name: str, timestamp: str) -> str:
    """Generate an HTML report."""
    html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Data Analysis Report - {{ file_name }}</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .header { text-align: center; margin-bottom: 30px; padding-bottom: 20px; border-bottom: 2px solid #333; }
        .section { margin: 20px 0; }
        .section h2 { color: #333; border-bottom: 1px solid #ddd; padding-bottom: 10px; }
        .section h3 { color: #555; margin-top: 20px; }
        .metric-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 15px 0; }
        .metric-card { background: #f8f9fa; padding: 15px; border-radius: 5px; border-left: 4px solid #007bff; }
        .metric-value { font-size: 24px; font-weight: bold; color: #333; }
        .metric-label { color: #666; font-size: 14px; }
        .quality-score { font-size: 36px; font-weight: bold; }
        .score-excellent { color: #28a745; }
        .score-good { color: #17a2b8; }
        .score-fair { color: #ffc107; }
        .score-poor { color: #dc3545; }
        .findings-list { list-style-type: none; padding: 0; }
        .findings-list li { background: #e3f2fd; padding: 10px; margin: 5px 0; border-radius: 5px; border-left: 4px solid #2196f3; }
        .recommendations-list { list-style-type: none; padding: 0; }
        .recommendations-list li { background: #fff3e0; padding: 10px; margin: 5px 0; border-radius: 5px; border-left: 4px solid #ff9800; }
        .data-table { width: 100%; border-collapse: collapse; margin: 15px 0; }
        .data-table th, .data-table td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        .data-table th { background-color: #f2f2f2; }
        .ai-insights { background: #f8f9fa; padding: 20px; border-radius: 5px; border: 1px solid #dee2e6; }
        .timestamp { color: #666; font-size: 12px; }
        pre { background: #f4f4f4; padding: 15px; border-radius: 5px; overflow-x: auto; }
    </style>
</head>"""
```

**Lines 262-294:**
- **Lines 263-266:** HTML document structure and metadata
- **Lines 267-293:** Comprehensive CSS styling:
  - Responsive layout with containers
  - Color-coded quality scores
  - Styled metric cards and lists
  - Professional table formatting
  - Special styling for AI insights section

### HTML Body Template

```python
<body>
    <div class="container">
        <div class="header">
            <h1>Data Analysis Report</h1>
            <h2>{{ file_name }}</h2>
            <p class="timestamp">Generated on {{ timestamp }}</p>
        </div>

        <div class="section">
            <h2>Executive Summary</h2>
            
            <div class="metric-grid">
                <div class="metric-card">
                    <div class="metric-value">{{ summary.dataset_overview.total_rows | number_format }}</div>
                    <div class="metric-label">Total Rows</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{{ summary.dataset_overview.total_columns }}</div>
                    <div class="metric-label">Total Columns</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{{ "%.1f" % summary.dataset_overview.file_size_mb }} MB</div>
                    <div class="metric-label">File Size</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value quality-score {{ quality_score_class }}">{{ summary.data_quality_score }}%</div>
                    <div class="metric-label">Data Quality Score</div>
                </div>
            </div>
```

**Lines 295-319:**
- **Lines 296-301:** Report header with file name and generation timestamp
- **Lines 303-319:** Executive summary metrics grid:
  - Dataset dimensions (rows, columns)
  - File size with formatting
  - Color-coded quality score

### Dynamic Content Sections

```python
            {% if summary.key_findings %}
            <h3>Key Findings</h3>
            <ul class="findings-list">
                {% for finding in summary.key_findings %}
                <li>{{ finding }}</li>
                {% endfor %}
            </ul>
            {% endif %}

            {% if summary.recommendations %}
            <h3>Recommendations</h3>
            <ul class="recommendations-list">
                {% for recommendation in summary.recommendations %}
                <li>{{ recommendation }}</li>
                {% endfor %}
            </ul>
            {% endif %}
```

**Lines 321-336:**
- **Lines 321-328:** Conditional key findings section
- **Lines 330-336:** Conditional recommendations section
- Uses Jinja2 template syntax for dynamic content

### Template Rendering and Quality Score Classification

```python
        # Determine quality score class
        quality_score = report_data['executive_summary']['data_quality_score']
        if quality_score >= 90:
            quality_score_class = 'score-excellent'
        elif quality_score >= 75:
            quality_score_class = 'score-good'
        elif quality_score >= 60:
            quality_score_class = 'score-fair'
        else:
            quality_score_class = 'score-poor'
        
        template = Template(html_template)
        
        # Add number formatting filter
        def number_format(value):
            return f"{value:,}"
        
        template.globals['number_format'] = number_format
        
        html_content = template.render(
            file_name=file_name,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            summary=report_data['executive_summary'],
            quality_score_class=quality_score_class,
            ai_insights=report_data['ai_insights'],
            analysis_results=report_data['analysis_results'],
            metadata=report_data['metadata']
        )
        
        html_path = self.output_dir / f"{file_name}_report_{timestamp}.html"
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return str(html_path)
```

**Lines 404-431:**
- **Lines 405-412:** Classify quality score for color coding
- **Line 414:** Create Jinja2 template instance
- **Lines 416-419:** Add custom number formatting filter
- **Lines 421-429:** Render template with all data
- **Lines 431-434:** Write HTML file and return path

---

## JSON and Summary Report Generation

### JSON Report Generation

```python
async def _generate_json_report(self, report_data: Dict[str, Any], file_name: str, timestamp: str) -> str:
    """Generate a JSON report."""
    json_path = self.output_dir / f"{file_name}_report_{timestamp}.json"
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(report_data, f, indent=2, default=str)
    
    return str(json_path)
```

**Lines 433-440:**
- **Line 436:** Create JSON file path with timestamp
- **Lines 438-439:** Write JSON with formatting and string conversion for non-serializable types

### Text Summary Report Generation

```python
async def _generate_summary_report(self, report_data: Dict[str, Any], file_name: str, timestamp: str) -> str:
    """Generate a concise summary report."""
    summary = report_data['executive_summary']
    ai_insights = report_data.get('ai_insights', {})
    
    summary_content = f"""
DATA ANALYSIS SUMMARY REPORT
============================
File: {file_name}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

DATASET OVERVIEW
----------------
Rows: {summary['dataset_overview']['total_rows']:,}
Columns: {summary['dataset_overview']['total_columns']}
File Size: {summary['dataset_overview']['file_size_mb']:.1f} MB
Data Quality Score: {summary['data_quality_score']}%

KEY FINDINGS
------------
"""
    
    for finding in summary['key_findings']:
        summary_content += f"• {finding}\n"
    
    if summary['recommendations']:
        summary_content += "\nRECOMMENDATIONS\n---------------\n"
        for rec in summary['recommendations']:
            summary_content += f"• {rec}\n"
    
    if ai_insights and ai_insights.get('insights'):
        summary_content += f"\nAI INSIGHTS\n-----------\n{ai_insights['insights'][:500]}...\n"
    
    summary_path = self.output_dir / f"{file_name}_summary_{timestamp}.txt"
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write(summary_content)
    
    return str(summary_path)
```

**Lines 442-475:**
- **Lines 445-446:** Extract summary and AI insights data
- **Lines 448-464:** Create formatted text report with sections:
  - Header with file info and timestamp
  - Dataset overview with key metrics
  - Key findings section
- **Lines 466-468:** Add findings with bullet points
- **Lines 470-475:** Add recommendations and truncated AI insights
- **Lines 477-481:** Write text file and return path

---

## Key Design Patterns and Principles

### 1. **API Integration Pattern**
- Structured request/response handling
- Proper error handling and timeout management
- Reusable HTTP session for efficiency

### 2. **Template-Based Reporting**
- Separation of content and presentation
- Dynamic content rendering with Jinja2
- Responsive HTML design with CSS

### 3. **Multi-Format Output**
- HTML for human readability
- JSON for programmatic access
- Text summary for quick review

### 4. **Comprehensive Data Synthesis**
- Combines statistical analysis with AI insights
- Creates executive summaries from raw analysis
- Quality scoring for quick assessment

### 5. **Structured Prompt Engineering**
- Methodical construction of AI prompts
- Context-rich information provision
- Specific instructions for desired output

### 6. **Error Resilience**
- Graceful handling of API failures
- Fallback options when AI insights unavailable
- Detailed error logging for debugging

This report generation system creates professional, comprehensive reports that combine rigorous statistical analysis with AI-powered insights, providing both technical depth and business-oriented recommendations.