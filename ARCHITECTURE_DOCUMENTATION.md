# Data Analysis Pipeline - Architecture Documentation

## 🏗️ System Overview

This is an automated data analysis pipeline that monitors data files, performs comprehensive statistical analysis, generates AI-powered insights using Amplify API, and creates detailed reports with visualizations. The system includes CI/CD integration for automated processing and GitHub Actions workflows.

---

## 📁 Core Files Documentation

### 1. `main.py` - Pipeline Orchestrator

**Purpose**: Entry point that coordinates the entire data analysis workflow.

**Key Components**:

```python
async def run_analysis_once(file_path: str):
    """Runs complete analysis pipeline for a single file"""
    # 1. Initialize pipeline components
    # 2. Run statistical analysis  
    # 3. Generate AI insights
    # 4. Create reports and visualizations
    # 5. Execute CI/CD workflow
```

**Architecture**:
- **DataPipeline Class**: Main coordinator that manages all components
- **Component Integration**: Connects AnalysisEngine, ReportGenerator, and CICDManager
- **Error Handling**: Comprehensive logging and graceful failure handling
- **Async Processing**: Non-blocking operations for large datasets

**Key Functions**:
- `initialize_pipeline()`: Sets up all components and validates configuration
- `run_continuous_monitoring()`: Watches for file changes and triggers analysis
- `run_analysis_once()`: Processes a single file through the complete pipeline

---

### 2. `analysis_engine.py` - Statistical Analysis Core

**Purpose**: Performs comprehensive statistical analysis on datasets including descriptive statistics, correlation analysis, distribution analysis, outlier detection, and hypothesis testing.

**Key Components**:

```python
class AnalysisEngine:
    async def analyze_file(self, file_path: str) -> Dict[str, Any]:
        """Complete analysis workflow"""
        # 1. Load and validate data
        # 2. Generate file information
        # 3. Assess data quality
        # 4. Compute descriptive statistics  
        # 5. Perform correlation analysis
        # 6. Analyze distributions
        # 7. Detect outliers
        # 8. Run hypothesis tests
        # 9. Time series analysis (if applicable)
        # 10. Create visualizations
```

**Statistical Methods Implemented**:

1. **Data Quality Assessment**:
   ```python
   def _analyze_data_quality(self, data: pd.DataFrame) -> Dict[str, Any]:
       # Missing value analysis
       # Duplicate detection  
       # Data completeness metrics
       # Column-wise quality assessment
   ```

2. **Descriptive Statistics**:
   ```python
   def _calculate_descriptive_stats(self, data: pd.DataFrame) -> Dict[str, Any]:
       # Basic statistics (mean, std, min, max, quartiles)
       # Advanced statistics (skewness, kurtosis, variance)
       # Categorical analysis (value counts, entropy)
   ```

3. **Correlation Analysis**:
   ```python
   def _perform_correlation_analysis(self, data: pd.DataFrame) -> Dict[str, Any]:
       # Pearson correlation matrix
       # Spearman correlation matrix  
       # Strong correlation identification (>0.5 threshold)
   ```

4. **Distribution Analysis**:
   ```python
   def _analyze_distributions(self, data: pd.DataFrame) -> Dict[str, Any]:
       # Normality tests (Shapiro-Wilk, Kolmogorov-Smirnov)
       # Distribution characteristics (skewness, kurtosis)
       # Distribution type classification
   ```

5. **Outlier Detection**:
   ```python
   def _detect_outliers(self, data: pd.DataFrame) -> Dict[str, Any]:
       # IQR method (Interquartile Range)
       # Z-score method (3 standard deviations)
       # Outlier percentage and values
   ```

**Configuration Parameters** (from `config.py`):
- `CONFIDENCE_LEVEL`: Statistical confidence level (default: 0.95)
- `CORRELATION_THRESHOLD`: Minimum correlation to be considered strong (default: 0.5)
- `MAX_FILE_SIZE_MB`: Maximum file size for processing (default: 100MB)

---

### 3. `report_generator.py` - AI-Powered Report Generation

**Purpose**: Generates comprehensive HTML, JSON, and text reports with AI-powered business insights using Amplify API integration.

**Key Components**:

#### AmplifyAPIClient Class:
```python
class AmplifyAPIClient:
    def __init__(self):
        self.api_key = config.amplify_api_key
        self.base_url = config.amplify_base_url  # https://prod-api.vanderbilt.ai
        self.session = requests.Session()
        
    async def generate_insights(self, analysis_data, file_info):
        """Generates AI insights using Amplify API"""
        # 1. Create analysis prompt with statistical data
        # 2. Make API request to Amplify /chat endpoint
        # 3. Parse response and extract insights
        # 4. Fallback to template insights if API fails
```

#### API Request Format:
```python
payload = {
    "data": {
        "temperature": 0.7,
        "max_tokens": 2000,
        "dataSources": [],  # Required empty array
        "messages": [
            {
                "role": "system", 
                "content": "You are a data analyst AI assistant..."
            },
            {
                "role": "user",
                "content": prompt  # Statistical analysis summary
            }
        ],
        "options": {
            "skipRag": True,
            "model": {"id": "gpt-4o-mini"}
        }
    }
}
```

#### Report Generation Process:
```python
class ReportGenerator:
    async def generate_report(self, analysis_results, file_path):
        """Complete report generation workflow"""
        # 1. Generate AI insights via Amplify API
        # 2. Create executive summary
        # 3. Generate HTML report with Jinja2 templates
        # 4. Create JSON data export
        # 5. Generate text summary
        # 6. Save all reports to output directory
```

#### Jinja2 Template System:
```python
# Custom filters for number formatting
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
```

**Report Types Generated**:
1. **HTML Report**: Interactive report with visualizations and AI insights
2. **JSON Report**: Complete analysis data in structured format  
3. **Text Summary**: Executive summary for quick review

---

### 4. `config.py` - Configuration Management

**Purpose**: Centralized configuration management with environment variable support and validation.

```python
class Config:
    """Configuration management for the data analysis pipeline"""
    
    def __init__(self):
        self.setup_logging()
        
    @property
    def amplify_api_key(self) -> str:
        """Get Amplify API key from environment variables"""
        return os.getenv('AMPLIFY_API_KEY', '')
    
    @property  
    def amplify_base_url(self) -> str:
        """Get Amplify API base URL"""
        return os.getenv('AMPLIFY_BASE_URL', 'https://api.amplify.ai/v1')
        
    @property
    def analysis_config(self) -> Dict[str, Any]:
        """Configuration for statistical analysis"""
        return {
            'confidence_level': float(os.getenv('CONFIDENCE_LEVEL', '0.95')),
            'max_file_size_mb': int(os.getenv('MAX_FILE_SIZE_MB', '100')),
            'sample_size_threshold': int(os.getenv('SAMPLE_SIZE_THRESHOLD', '1000')),
            'correlation_threshold': float(os.getenv('CORRELATION_THRESHOLD', '0.5'))
        }
```

**Configuration Categories**:
- **Amplify API**: API key, base URL, assistant ID
- **Directory Paths**: Data input and output directories
- **Analysis Parameters**: Statistical thresholds and limits
- **Git Configuration**: Branch names, commit prefixes, remote settings
- **Logging**: Log levels and file locations

---

### 5. `ci_cd_manager.py` - Automated CI/CD Integration  

**Purpose**: Manages Git operations, branch creation, automated commits, and CI/CD pipeline execution.

**Key Components**:

```python
class CICDManager:
    async def execute_pipeline(self, analysis_results, file_path):
        """Complete CI/CD workflow"""
        # 1. Create unique analysis branch
        # 2. Stage generated reports and visualizations  
        # 3. Create automated commit with analysis summary
        # 4. Push branch to remote repository
        # 5. Create pull request (if GitHub CLI available)
        # 6. Generate pipeline summary and logs
```

#### Git Workflow:
```python
def create_analysis_branch(self, file_name: str) -> str:
    """Creates a unique branch for analysis results"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  
    branch_name = f"analysis-pipeline-{file_name}-{timestamp}"
    
    # Create and checkout new branch
    self.repo.git.checkout('-b', branch_name)
    return branch_name
```

#### Automated Commit Process:
```python
def commit_analysis_results(self, files: List[str], message: str):
    """Commits analysis results with automated message"""
    # Stage files
    self.repo.index.add(files)
    
    # Create commit with standardized message format
    commit_message = f"[AUTO] {message}\n\nGenerated by automated data analysis pipeline"
    self.repo.index.commit(commit_message)
```

**Pipeline Outputs**:
- **Analysis Branches**: Unique branches for each analysis run
- **Pipeline Summaries**: Markdown summaries of analysis results
- **Pipeline Logs**: JSON logs with execution details and performance metrics

---

### 6. `data_monitor.py` - File System Monitoring

**Purpose**: Monitors data directories for file changes and triggers analysis pipeline automatically.

```python
class DataFileHandler(FileSystemEventHandler):
    """Handles file system events for data files"""
    
    def on_created(self, event):
        """Triggered when new data file is added"""
        if self._is_valid_data_file(event.src_path):
            # Queue file for analysis
            asyncio.create_task(self.pipeline.process_file(event.src_path))
            
    def on_modified(self, event):  
        """Triggered when data file is modified"""
        if self._is_valid_data_file(event.src_path):
            # Re-analyze modified file
            asyncio.create_task(self.pipeline.process_file(event.src_path))
```

**Monitored File Types**:
- `.csv` - Comma-separated values
- `.json` - JSON data files
- `.xlsx` - Excel files  
- `.parquet` - Parquet files

---

## 🔧 Environment Configuration (`.env`)

```env
# Amplify API Configuration
AMPLIFY_API_KEY=amp-v1-nLqH-10eWxoaNZ1BxJH813XrWUR7j_A72mNZOlqv5kM
AMPLIFY_BASE_URL=https://prod-api.vanderbilt.ai
AMPLIFY_ASSISTANT_ID=astp/6f59dc1c-de32-4e76-84a0-f362334307e3

# Directory Configuration  
DATA_DIRECTORY=./sales_data
OUTPUT_DIRECTORY=./analysis_output

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

---

## 🚀 GitHub Actions Workflow (`.github/workflows/analysis.yml`)

**Purpose**: Automated CI/CD pipeline that runs analysis on GitHub Actions runners.

```yaml
name: Data Analysis Pipeline

on:
  push:
    branches: [ main ]
    paths: ['sales_data/**']  # Triggers on data file changes

jobs:
  analyze-data:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.9, 3.10, 3.11]
        
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
        cache: pip
        
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        
    - name: Run analysis pipeline
      run: |
        # Process changed files through analysis pipeline
        python -c "
        import asyncio
        from main import run_analysis_once
        # Analysis logic here
        "
        
    - name: Upload analysis results
      uses: actions/upload-artifact@v4
      with:
        name: analysis-results-${{ matrix.python-version }}
        path: ./analytics_output/
```

**Workflow Features**:
- **Multi-Python Version Testing**: Tests on Python 3.9, 3.10, 3.11
- **Automated Triggering**: Runs on pushes to `sales_data/**` paths  
- **Artifact Generation**: Uploads analysis results as downloadable artifacts
- **Environment Setup**: Configures analysis environment variables
- **Error Handling**: Continues pipeline execution even if some analyses fail

---

## 📊 Data Flow Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌───────────────────┐
│   Data Files    │───▶│  Data Monitor    │───▶│  Analysis Engine  │
│   (.csv, .json) │    │  (file watcher)  │    │  (statistics)     │
└─────────────────┘    └──────────────────┘    └───────────────────┘
                                                           │
                                                           ▼
┌─────────────────┐    ┌──────────────────┐    ┌───────────────────┐
│   GitHub Repo   │◀───│   CI/CD Manager  │◀───│  Report Generator │
│   (branches)    │    │   (git ops)      │    │  (AI insights)    │
└─────────────────┘    └──────────────────┘    └───────────────────┘
                                                           │
                                                           ▼
                                               ┌───────────────────┐
                                               │   Amplify API     │
                                               │   (gpt-4o-mini)   │  
                                               └───────────────────┘
```

---

## 🎯 Usage Examples

### 1. Manual Analysis
```bash
# Analyze a single file
python -c "import asyncio; from main import run_analysis_once; asyncio.run(run_analysis_once('sales_data/data.csv'))"

# Run continuous monitoring
python main.py
```

### 2. API Integration Test
```python
from report_generator import AmplifyAPIClient

client = AmplifyAPIClient()
result = await client.generate_insights(analysis_data, file_info)
print(f"Model used: {result['model']}")
print(f"Insights: {result['insights'][:200]}...")
```

### 3. Configuration Validation  
```python
from config import config

# Check configuration
if config.validate_config():
    print("✅ Configuration valid")
    print(f"API Base URL: {config.amplify_base_url}")
    print(f"Data Directory: {config.data_directory}")
```

---

This architecture provides a complete, scalable data analysis pipeline with AI-powered insights, automated CI/CD, and comprehensive reporting capabilities.