# Data Analysis Pipeline with CI/CD Integration

A comprehensive automated data analysis pipeline that monitors data files, performs statistical analysis, generates AI-powered insights using the Amplify API, and implements CI/CD workflows.

## Features

- **Real-time Data Monitoring**: Automatically detects changes in data files using filesystem watching
- **Comprehensive Statistical Analysis**: Descriptive statistics, correlation analysis, distribution analysis, outlier detection, and hypothesis testing
- **AI-Powered Insights**: Integration with Amplify API for intelligent analysis and recommendations
- **Automated Report Generation**: HTML, JSON, and summary reports with visualizations
- **CI/CD Integration**: Automated Git workflows with branch creation, commits, and pull requests
- **GitHub Actions**: Complete CI/CD pipeline with data validation, analysis, and deployment
- **Error Handling & Logging**: Comprehensive error handling and structured logging throughout

## Project Structure

```
.
├── main.py                     # Entry point and pipeline orchestration
├── config.py                   # Configuration management
├── data_monitor.py             # File monitoring system
├── analysis_engine.py          # Statistical analysis engine
├── report_generator.py         # Amplify API integration and report generation
├── ci_cd_manager.py           # Git automation and CI/CD management
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
├── .github/
│   └── workflows/
│       └── analysis.yml      # GitHub Actions workflow
├── data/                     # Data files directory (monitored)
├── output/                   # Generated reports and visualizations
│   ├── reports/             # HTML, JSON, and summary reports
│   ├── visualizations/      # Generated charts and graphs
│   └── pipeline_logs/       # CI/CD pipeline logs
└── logs/                    # Application logs
```

## Setup Instructions

### 1. Prerequisites

- Python 3.9+
- Git
- Amplify API access
- Optional: GitHub CLI for PR creation

### 2. Installation

```bash
# Clone the repository
git clone <repository-url>
cd data-analysis-pipeline

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env
```

### 3. Configuration

Edit the `.env` file with your settings:

```bash
# Required: Amplify API Configuration
AMPLIFY_API_KEY=your_amplify_api_key_here
AMPLIFY_BASE_URL=https://api.amplify.ai/v1

# Directory Configuration
DATA_DIRECTORY=./data
OUTPUT_DIRECTORY=./output

# Analysis Configuration
CONFIDENCE_LEVEL=0.95
MAX_FILE_SIZE_MB=100
SAMPLE_SIZE_THRESHOLD=1000
CORRELATION_THRESHOLD=0.5

# Git Configuration
GIT_BRANCH=analysis-pipeline
COMMIT_PREFIX=[AUTO]
GIT_REMOTE=origin

# Logging
LOG_LEVEL=INFO
```

### 4. GitHub Actions Setup

Add the following secrets to your GitHub repository:

- `AMPLIFY_API_KEY`: Your Amplify API key

## Usage

### Continuous Monitoring Mode

Start the pipeline to monitor data files continuously:

```bash
python main.py
```

The pipeline will:
- Monitor the `data/` directory for file changes
- Automatically analyze new or modified data files
- Generate reports and visualizations
- Create Git branches and commits
- Optionally create pull requests

### Single File Analysis

Analyze a specific data file:

```bash
python main.py --analyze path/to/your/data.csv
```

### Supported File Formats

- CSV (`.csv`)
- JSON (`.json`)
- Excel (`.xlsx`)
- Parquet (`.parquet`)

## Analysis Features

### Statistical Analysis

- **Descriptive Statistics**: Mean, median, mode, standard deviation, skewness, kurtosis
- **Data Quality Assessment**: Missing values, duplicates, completeness analysis
- **Correlation Analysis**: Pearson and Spearman correlations with significance testing
- **Distribution Analysis**: Normality tests, distribution classification
- **Outlier Detection**: IQR and Z-score methods
- **Hypothesis Testing**: One-sample and two-sample tests
- **Time Series Analysis**: Trend detection and frequency analysis

### Visualizations

- Correlation heatmaps
- Distribution histograms
- Box plots for outlier detection
- Time series plots (when applicable)

### AI-Powered Insights

- Business implications analysis
- Data quality recommendations
- Statistical interpretation
- Action items and next steps

## CI/CD Pipeline

### Automated Workflows

1. **Data Validation**: Validates data files and checks quality
2. **Analysis Execution**: Runs statistical analysis on changed files
3. **Report Generation**: Creates comprehensive reports with AI insights
4. **Quality Assessment**: Evaluates pipeline success and output quality
5. **Deployment**: Optionally deploys results to GitHub Pages

### Git Integration

- Automatic branch creation for each analysis
- Structured commit messages
- Pull request creation with analysis summaries
- Pipeline history tracking

## GitHub Actions Triggers

- **Push to main/develop**: Analyzes changed data files
- **Pull Request**: Validates data files and runs analysis
- **Manual Trigger**: 
  - Analyze specific file: `workflow_dispatch` with `data_file` input
  - Full analysis: `workflow_dispatch` with `full_analysis: true`

## Monitoring and Logging

### Application Logs

Logs are written to:
- `logs/pipeline.log`: Main application log
- Console output: Real-time feedback

### Log Levels

- `ERROR`: Critical errors that prevent analysis
- `WARNING`: Issues that don't prevent analysis but need attention
- `INFO`: General information about pipeline execution
- `DEBUG`: Detailed debugging information

### Error Handling

- Graceful handling of file format issues
- API timeout and error recovery
- Git operation error handling
- Comprehensive error reporting in CI/CD

## API Integration

### Amplify API

The pipeline integrates with Amplify API to generate AI-powered insights:

```python
# Example API request structure
{
    "messages": [
        {
            "role": "system",
            "content": "You are a data analyst AI assistant..."
        },
        {
            "role": "user", 
            "content": "Statistical analysis data..."
        }
    ],
    "max_tokens": 2000,
    "temperature": 0.7,
    "model": "claude-3-sonnet-20240229"
}
```

## Performance Considerations

### File Size Limits

- Default maximum file size: 100MB
- Configurable via `MAX_FILE_SIZE_MB` environment variable
- Large files are automatically skipped with warnings

### Memory Management

- Streaming data processing for large files
- Automatic memory cleanup after analysis
- Configurable sample size thresholds

### Rate Limiting

- Built-in delays between file processing
- API request throttling
- Concurrent analysis limitations

## Troubleshooting

### Common Issues

1. **Import Errors**: Install dependencies with `pip install -r requirements.txt`
2. **API Authentication**: Verify `AMPLIFY_API_KEY` in `.env` file
3. **Git Permissions**: Ensure Git is configured and repository has write access
4. **File Format Issues**: Check file format compatibility and size limits

### Debug Mode

Enable debug logging:

```bash
export LOG_LEVEL=DEBUG
python main.py
```

### Manual Testing

Test individual components:

```python
# Test analysis engine
from analysis_engine import AnalysisEngine
engine = AnalysisEngine()
result = await engine.analyze_file('path/to/test.csv')

# Test report generation
from report_generator import ReportGenerator
generator = ReportGenerator()
report = await generator.generate_report('path/to/test.csv', result)
```

## Development

### Adding New Analysis Features

1. Extend `AnalysisEngine` class in `analysis_engine.py`
2. Add new analysis methods following existing patterns
3. Update report templates in `report_generator.py`
4. Add tests and documentation

### Custom Visualizations

1. Add visualization functions to `analysis_engine.py`
2. Update `_generate_visualizations()` method
3. Ensure proper file path management

### CI/CD Customization

1. Modify `.github/workflows/analysis.yml`
2. Add custom validation steps
3. Configure deployment targets

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Make changes and add tests
4. Commit changes: `git commit -am 'Add new feature'`
5. Push to branch: `git push origin feature/new-feature`
6. Create Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:

1. Check the troubleshooting section above
2. Review application logs in `logs/pipeline.log`
3. Create an issue in the GitHub repository
4. Check GitHub Actions logs for CI/CD issues

## Changelog

### Version 1.0.1
- Updated GitHub Actions to latest versions (fixed deprecated actions)
- Enhanced CI/CD pipeline stability
- Added comprehensive dataset integration guide

### Version 1.0.0
- Initial release with core analysis pipeline
- Amplify API integration
- GitHub Actions CI/CD
- Comprehensive error handling and logging