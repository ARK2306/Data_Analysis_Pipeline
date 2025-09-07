# Complete Setup Guide and Project Overview

## Project Overview

### What We Built
The **Data Analysis Pipeline with CI/CD Integration** is a comprehensive, automated system that:

1. **Monitors data files** in real-time using filesystem watching
2. **Performs statistical analysis** including descriptive statistics, correlations, distributions, outliers, and hypothesis testing
3. **Generates AI-powered insights** using the Amplify API
4. **Creates comprehensive reports** in HTML, JSON, and text formats with visualizations
5. **Automates Git workflows** with branch creation, commits, and pull requests
6. **Implements CI/CD pipelines** using GitHub Actions for validation and deployment

### Architecture Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────────┐
│   Data Files    │───▶│  Data Monitor    │───▶│  Analysis Engine    │
│  (.csv, .json,  │    │ (File Watching)  │    │ (Statistical Calc)  │
│  .xlsx, .parquet│    └──────────────────┘    └─────────────────────┘
└─────────────────┘                                        │
                                                          ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────────┐
│  GitHub Actions │◀───│  CI/CD Manager   │◀───│  Report Generator   │
│  (Automated     │    │ (Git Operations) │    │ (Amplify API +      │
│   Validation)   │    └──────────────────┘    │  HTML/JSON Reports) │
└─────────────────┘                            └─────────────────────┘
```

### Key Components

1. **main.py** - Pipeline orchestrator and entry point
2. **config.py** - Centralized configuration management
3. **data_monitor.py** - Real-time file system monitoring
4. **analysis_engine.py** - Comprehensive statistical analysis
5. **report_generator.py** - AI insights and report generation
6. **ci_cd_manager.py** - Git automation and CI/CD integration
7. **GitHub Actions** - Automated testing and deployment

---

## Complete Setup Instructions

### Prerequisites

#### Required Software
- **Python 3.9+** - Core runtime environment
- **Git** - Version control operations
- **Amplify API Account** - For AI-powered insights

#### Optional Software
- **GitHub CLI (gh)** - For automated pull request creation
- **Docker** - For containerized deployment (optional)

#### Required API Access
- **Amplify API Key** - Contact Amplify for access credentials

### Step 1: Environment Setup

#### 1.1 Clone or Download Project
```bash
# If using Git
git clone <your-repository-url>
cd data-analysis-pipeline

# Or download and extract the project files
```

#### 1.2 Create Python Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

#### 1.3 Install Dependencies
```bash
# Install all required packages
pip install -r requirements.txt

# Verify installation
pip list | grep -E "(requests|pandas|numpy|scipy|matplotlib|seaborn|plotly|watchdog|GitPython|jinja2)"
```

### Step 2: Configuration Setup

#### 2.1 Create Environment File
```bash
# Copy the example environment file
cp .env.example .env

# Edit the .env file with your settings
nano .env  # or use your preferred editor
```

#### 2.2 Configure Environment Variables
Edit `.env` file with your specific settings:

```bash
# REQUIRED: Amplify API Configuration
AMPLIFY_API_KEY=your_actual_api_key_here
AMPLIFY_BASE_URL=https://api.amplify.ai/v1

# Directory Configuration (customize as needed)
DATA_DIRECTORY=./data
OUTPUT_DIRECTORY=./output

# Analysis Configuration (can use defaults)
CONFIDENCE_LEVEL=0.95
MAX_FILE_SIZE_MB=100
SAMPLE_SIZE_THRESHOLD=1000
CORRELATION_THRESHOLD=0.5

# Git Configuration (customize for your workflow)
GIT_BRANCH=analysis-pipeline
COMMIT_PREFIX=[AUTO]
GIT_REMOTE=origin

# Logging Configuration
LOG_LEVEL=INFO
```

### Step 3: Directory Structure Setup

#### 3.1 Create Required Directories
```bash
# Create data directory for monitoring
mkdir -p data

# Create output directories (will be created automatically, but can pre-create)
mkdir -p output/reports
mkdir -p output/visualizations
mkdir -p output/pipeline_logs
mkdir -p logs
```

#### 3.2 Verify Directory Structure
```bash
# Your directory should look like this:
tree -a
```
```
.
├── .env                          # Your configuration
├── .env.example                  # Configuration template
├── .github/
│   └── workflows/
│       └── analysis.yml          # GitHub Actions workflow
├── README.md                     # Project documentation
├── requirements.txt              # Python dependencies
├── main.py                      # Entry point
├── config.py                    # Configuration management
├── data_monitor.py              # File monitoring
├── analysis_engine.py           # Statistical analysis
├── report_generator.py          # AI insights & reporting
├── ci_cd_manager.py             # Git automation
├── data/                        # Data files directory
├── output/                      # Generated outputs
│   ├── reports/                 # HTML, JSON, text reports
│   ├── visualizations/          # Charts and graphs
│   └── pipeline_logs/           # CI/CD logs
├── logs/                        # Application logs
└── docs/                        # Code explanations
```

### Step 4: Git Repository Setup

#### 4.1 Initialize Git Repository (if needed)
```bash
# If not already a Git repository
git init

# Add remote repository
git remote add origin <your-repository-url>

# Set up main branch
git branch -M main
```

#### 4.2 Configure Git User (if needed)
```bash
# Set your Git user information
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

### Step 5: GitHub Actions Setup

#### 5.1 GitHub Repository Secrets
In your GitHub repository, add these secrets:

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Add **Repository Secret**:
   - **Name**: `AMPLIFY_API_KEY`
   - **Value**: Your actual Amplify API key

#### 5.2 Enable GitHub Pages (Optional)
1. Go to **Settings** → **Pages**
2. Select **Source**: GitHub Actions
3. This enables automatic deployment of analysis results

### Step 6: Verification and Testing

#### 6.1 Test Configuration
```bash
# Test configuration validation
python -c "from config import config; print('Config valid:', config.validate_config())"
```

#### 6.2 Create Test Data File
```bash
# Create a simple CSV test file
cat > data/test_data.csv << EOF
name,age,salary,department
Alice,25,50000,Engineering
Bob,30,60000,Marketing
Charlie,35,70000,Engineering
Diana,28,55000,Marketing
Eve,32,65000,Engineering
EOF
```

#### 6.3 Test Single File Analysis
```bash
# Run analysis on test file
python main.py --analyze data/test_data.csv

# Check if reports were generated
ls output/reports/
ls output/visualizations/
```

#### 6.4 Test Continuous Monitoring
```bash
# Start the pipeline (will run until interrupted)
python main.py

# In another terminal, add or modify files in the data/ directory
echo "Frank,29,58000,Sales" >> data/test_data.csv

# Check logs for processing activity
tail -f logs/pipeline.log
```

### Step 7: GitHub Actions Testing

#### 7.1 Trigger GitHub Actions
```bash
# Commit and push changes to trigger the workflow
git add .
git commit -m "Initial setup and test data"
git push origin main

# Or manually trigger the workflow on GitHub:
# Go to Actions → Data Analysis Pipeline → Run workflow
```

#### 7.2 Monitor GitHub Actions
1. Go to **Actions** tab in your GitHub repository
2. Click on the running workflow
3. Monitor each job's progress
4. Check for any failures or warnings

---

## Troubleshooting Common Issues

### Issue 1: Import Errors
**Problem**: `ModuleNotFoundError` when running the pipeline

**Solutions**:
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Check Python path
python -c "import sys; print(sys.path)"
```

### Issue 2: Amplify API Authentication
**Problem**: API authentication failures

**Solutions**:
1. Verify API key in `.env` file
2. Check API key has correct permissions
3. Test API connection:
```bash
python -c "
import requests
from config import config
response = requests.get(f'{config.amplify_base_url}/test', 
                       headers={'Authorization': f'Bearer {config.amplify_api_key}'})
print('Status:', response.status_code)
"
```

### Issue 3: Git Operations Failing
**Problem**: Git commands fail during CI/CD

**Solutions**:
```bash
# Check Git configuration
git config --list | grep user

# Verify repository status
git status

# Check remote configuration
git remote -v

# Test Git operations manually
git checkout -b test-branch
git add .
git commit -m "test commit"
git push origin test-branch
```

### Issue 4: File Monitoring Not Working
**Problem**: Files not being processed when changed

**Solutions**:
1. Check file permissions:
```bash
ls -la data/
```

2. Verify file formats are supported:
```bash
python -c "from config import config; print('Supported:', config.supported_file_types)"
```

3. Check file size limits:
```bash
python -c "from config import config; print('Max size (MB):', config.analysis_config['max_file_size_mb'])"
```

### Issue 5: GitHub Actions Failing
**Problem**: Workflow fails in GitHub Actions

**Common Solutions**:
1. **Secret missing**: Verify `AMPLIFY_API_KEY` is set in repository secrets
2. **Dependency issues**: Check if all dependencies are in `requirements.txt`
3. **Permission issues**: Ensure repository has Actions enabled
4. **File path issues**: Use absolute paths in workflow

### Issue 6: Memory Issues with Large Files
**Problem**: Out of memory errors with large datasets

**Solutions**:
1. Reduce file size limit:
```bash
# In .env file
MAX_FILE_SIZE_MB=50
```

2. Increase sample size threshold:
```bash
# In .env file
SAMPLE_SIZE_THRESHOLD=500
```

3. Monitor memory usage:
```bash
# Check memory during analysis
python -c "
import psutil
import os
process = psutil.Process(os.getpid())
print(f'Memory usage: {process.memory_info().rss / 1024 / 1024:.1f} MB')
"
```

---

## Usage Scenarios

### Scenario 1: Development and Testing
```bash
# 1. Start continuous monitoring
python main.py

# 2. Add test files to data/ directory
# 3. Monitor logs for processing
# 4. Check generated reports in output/
```

### Scenario 2: One-off Analysis
```bash
# Analyze specific file
python main.py --analyze path/to/your/data.csv

# Check results
ls output/reports/
ls output/visualizations/
```

### Scenario 3: Automated CI/CD Workflow
```bash
# 1. Add data files to repository
git add data/new_dataset.csv
git commit -m "Add new dataset for analysis"
git push origin main

# 2. GitHub Actions automatically:
#    - Validates data files
#    - Runs analysis
#    - Generates reports
#    - Deploys to GitHub Pages (if enabled)
```

### Scenario 4: Manual GitHub Actions Trigger
1. Go to GitHub repository
2. Click **Actions** → **Data Analysis Pipeline**
3. Click **Run workflow**
4. Choose options:
   - **Analyze specific file**: Enter file path
   - **Run full analysis**: Check the box

---

## Performance Optimization

### For Large Datasets
1. **Increase file size limits** carefully
2. **Use sampling** for very large files
3. **Enable multiprocessing** for multiple files
4. **Monitor memory usage** during processing

### For High-Frequency Updates
1. **Add processing delays** to prevent overload
2. **Implement queuing** for multiple simultaneous changes
3. **Use file locking** to prevent conflicts
4. **Monitor system resources**

### For CI/CD Performance
1. **Cache dependencies** in GitHub Actions
2. **Parallelize analysis** of multiple files
3. **Use artifacts** to persist results between jobs
4. **Optimize Docker images** if using containerization

---

## Security Considerations

### API Key Security
- **Never commit API keys** to version control
- **Use GitHub Secrets** for CI/CD
- **Rotate keys regularly**
- **Monitor API usage** for anomalies

### File Access Security
- **Validate file types** before processing
- **Implement size limits** to prevent DoS
- **Sanitize file paths** to prevent directory traversal
- **Use isolated environments** for processing

### Repository Security
- **Review automated commits** before merging
- **Use branch protection** rules
- **Enable required reviews** for pull requests
- **Monitor repository access** logs

This comprehensive setup guide provides everything needed to deploy and operate the Data Analysis Pipeline successfully in various environments and use cases.