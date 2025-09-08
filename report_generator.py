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

logger = logging.getLogger(__name__)

class AmplifyAPIClient:
    """Client for interacting with Amplify API."""
    
    def __init__(self):
        self.api_key = config.amplify_api_key
        self.base_url = config.amplify_base_url
        self.assistant_id = config.amplify_assistant_id
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        })
    
    async def generate_insights(self, analysis_data: Dict[str, Any], file_info: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Generate AI-powered insights from analysis data."""
        try:
            logger.info("Generating AI insights via Amplify API")
            
            # Prepare the prompt for the AI
            prompt = self._create_analysis_prompt(analysis_data, file_info)
            
            payload = {
                "data": {
                    "temperature": 0.7,
                    "max_tokens": 2000,
                    "dataSources": [],
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
                    "options": {
                        "skipRag": True,
                        "model": {"id": "gpt-4o-mini"}
                    }
                }
            }
            endpoint = f"{self.base_url}/chat"
            
            response = self.session.post(
                endpoint,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                logger.info("AI insights generated successfully")
                
                # Handle Amplify API response format
                insights_text = result.get('data', '')
                model_info = result.get('model', 'gpt-4o-mini')
                
                return {
                    'insights': insights_text,
                    'model': model_info,
                    'usage': result.get('usage', {})
                }
            else:
                logger.error(f"Amplify API error: {response.status_code} - {response.text}")
                return self._generate_fallback_insights(analysis_data, file_info)
                
        except Exception as e:
            logger.error(f"Failed to generate AI insights: {e}")
            return self._generate_fallback_insights(analysis_data, file_info)
    
    def _generate_fallback_insights(self, analysis_data: Dict[str, Any], file_info: Dict[str, Any]) -> Dict[str, Any]:
        """Generate basic insights when Amplify API is unavailable."""
        logger.info("Generating fallback insights (API unavailable)")
        
        insights = []
        
        # Data overview insights
        rows = file_info.get('rows', 0)
        cols = file_info.get('columns', 0)
        insights.append(f"Dataset contains {rows:,} records across {cols} dimensions.")
        
        # Data quality insights
        if 'data_quality' in analysis_data:
            quality = analysis_data['data_quality']
            missing_pct = quality.get('missing_values', {}).get('missing_percentage', 0)
            if missing_pct > 0:
                insights.append(f"Data completeness: {100-missing_pct:.1f}% - consider addressing missing values.")
            else:
                insights.append("Data shows excellent completeness with no missing values.")
        
        # Statistical insights
        if 'descriptive_stats' in analysis_data:
            numeric_cols = len(analysis_data['descriptive_stats'])
            insights.append(f"Statistical analysis covers {numeric_cols} numerical variables.")
        
        # Correlation insights
        if 'correlations' in analysis_data:
            strong_corr = sum(1 for corr in analysis_data['correlations'].get('strong_correlations', []))
            if strong_corr > 0:
                insights.append(f"Identified {strong_corr} strong correlations between variables.")
        
        # Time series insights
        if analysis_data.get('time_series_analysis', {}).get('has_time_series', False):
            insights.append("Dataset contains time-series data suitable for trend analysis.")
        
        # Generic recommendations
        insights.extend([
            "Consider performing customer segmentation analysis for targeted insights.",
            "Explore seasonal patterns if temporal data is available.",
            "Monitor key performance indicators for business optimization."
        ])
        
        return {
            'insights': "\n\n".join([f"• {insight}" for insight in insights]),
            'model': 'fallback-generator',
            'usage': {'fallback': True}
        }
    
    def _create_analysis_prompt(self, analysis_data: Dict[str, Any], file_info: Dict[str, Any]) -> str:
        """Create a comprehensive prompt for AI analysis."""
        prompt_parts = []
        
        # File information
        prompt_parts.append(f"Dataset Information:")
        prompt_parts.append(f"- File: {file_info.get('file_name', 'Unknown')}")
        prompt_parts.append(f"- Rows: {file_info.get('rows', 0):,}")
        prompt_parts.append(f"- Columns: {file_info.get('columns', 0)}")
        prompt_parts.append("")
        
        # Data quality summary
        if 'data_quality' in analysis_data:
            quality = analysis_data['data_quality']
            missing_pct = quality.get('missing_values', {}).get('missing_percentage', 0)
            duplicate_pct = quality.get('duplicate_rows', {}).get('percentage', 0)
            
            prompt_parts.append(f"Data Quality:")
            prompt_parts.append(f"- Missing values: {missing_pct:.1f}%")
            prompt_parts.append(f"- Duplicate rows: {duplicate_pct:.1f}%")
            prompt_parts.append("")
        
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
        
        # Distribution analysis
        if 'distribution_analysis' in analysis_data:
            distributions = analysis_data['distribution_analysis']
            prompt_parts.append("Distribution Characteristics:")
            for col, dist_info in list(distributions.items())[:3]:  # First 3 columns
                if isinstance(dist_info, dict):
                    dist_type = dist_info.get('distribution_characteristics', {}).get('distribution_type', 'Unknown')
                    normality = dist_info.get('normality_tests', {}).get('shapiro_wilk', {}).get('is_normal', 'Unknown')
                    prompt_parts.append(f"- {col}: {dist_type}, Normal: {normality}")
            prompt_parts.append("")
        
        prompt_parts.append("Please provide:")
        prompt_parts.append("1. Key findings and insights")
        prompt_parts.append("2. Data quality assessment and recommendations")
        prompt_parts.append("3. Business implications of the statistical findings")
        prompt_parts.append("4. Recommendations for further analysis or data collection")
        prompt_parts.append("5. Any potential issues or concerns identified")
        
        return "\n".join(prompt_parts)

class ReportGenerator:
    """Main report generator class."""
    
    def __init__(self):
        self.config = config
        self.amplify_client = AmplifyAPIClient()
        self.output_dir = Path(self.config.output_directory) / 'reports'
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
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
        
        # Basic recommendations
        recommendations = []
        if missing_pct > 10:
            recommendations.append("Investigate and address high missing value rates")
        if duplicate_pct > 1:
            recommendations.append("Remove or investigate duplicate records")
        if len(strong_corrs) > 0:
            recommendations.append("Explore strong correlations for potential feature engineering")
        
        summary['recommendations'] = recommendations
        
        return summary
    
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
</head>
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
        </div>

        {% if ai_insights and ai_insights.insights %}
        <div class="section">
            <h2>AI-Powered Insights</h2>
            <div class="ai-insights">
                <pre>{{ ai_insights.insights }}</pre>
            </div>
        </div>
        {% endif %}

        <div class="section">
            <h2>Data Quality Assessment</h2>
            {% set quality = analysis_results.data_quality %}
            <div class="metric-grid">
                <div class="metric-card">
                    <div class="metric-value">{{ "%.1f" % quality.missing_values.missing_percentage }}%</div>
                    <div class="metric-label">Missing Values</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{{ quality.duplicate_rows.count }}</div>
                    <div class="metric-label">Duplicate Rows</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{{ quality.data_completeness.complete_rows }}</div>
                    <div class="metric-label">Complete Rows</div>
                </div>
            </div>
        </div>

        {% if analysis_results.correlation_analysis.strong_correlations %}
        <div class="section">
            <h2>Strong Correlations</h2>
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Variable 1</th>
                        <th>Variable 2</th>
                        <th>Pearson Correlation</th>
                        <th>Strength</th>
                    </tr>
                </thead>
                <tbody>
                    {% for corr in analysis_results.correlation_analysis.strong_correlations[:10] %}
                    <tr>
                        <td>{{ corr.variable1 }}</td>
                        <td>{{ corr.variable2 }}</td>
                        <td>{{ "%.3f" % corr.pearson_correlation }}</td>
                        <td>{{ corr.strength }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        {% endif %}

        <div class="section">
            <h2>Analysis Metadata</h2>
            <table class="data-table">
                <tr><td><strong>Analysis Timestamp</strong></td><td>{{ metadata.analysis_timestamp }}</td></tr>
                <tr><td><strong>File Path</strong></td><td>{{ metadata.file_path }}</td></tr>
                <tr><td><strong>Report Version</strong></td><td>{{ metadata.report_version }}</td></tr>
                {% if ai_insights %}
                <tr><td><strong>AI Model Used</strong></td><td>{{ ai_insights.model }}</td></tr>
                {% endif %}
            </table>
        </div>
    </div>
</body>
</html>
"""
        
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
        
        # Create Jinja2 environment with custom filters
        from jinja2 import Environment
        
        def number_format(value):
            if value is None:
                return "0"
            try:
                return f"{int(value):,}"
            except (ValueError, TypeError):
                return str(value)
        
        env = Environment()
        env.filters['number_format'] = number_format
        template = env.from_string(html_template)
        
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
    
    async def _generate_json_report(self, report_data: Dict[str, Any], file_name: str, timestamp: str) -> str:
        """Generate a JSON report."""
        json_path = self.output_dir / f"{file_name}_report_{timestamp}.json"
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, default=str)
        
        return str(json_path)
    
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