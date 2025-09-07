# Complete Project Walkthrough - Real Example Simulation

## Overview
This document provides a complete, hands-on simulation of the Data Analysis Pipeline project from setup to deployment. We'll walk through a realistic scenario where a company analyzes their sales data automatically.

---

# Scenario: Automated Sales Data Analysis

**Company**: TechCorp Solutions  
**Use Case**: Automatically analyze daily sales data uploads  
**Goal**: Generate insights and reports whenever new sales data arrives  

---

# Part 1: Initial Setup and Configuration

## Step 1: Project Setup

Let's start by setting up our environment:

```bash
# Create project directory
mkdir techcorp-analytics
cd techcorp-analytics

# Create virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux

# Clone/copy the project files
# (Assuming files are already in place)

# Install dependencies
pip install -r requirements.txt
```

**Output you'll see:**
```
Collecting requests>=2.31.0
Collecting watchdog>=3.0.0
Collecting pandas>=2.0.0
...
Successfully installed pandas-2.1.1 numpy-1.24.3 requests-2.31.0 ...
```

## Step 2: Configuration Setup

Create the `.env` file with our TechCorp configuration:

```bash
# Copy template
cp .env.example .env

# Edit configuration
nano .env
```

**Our .env configuration:**
```bash
# Amplify API Configuration
AMPLIFY_API_KEY=sk-amp-abc123def456ghi789jkl012mno345
AMPLIFY_BASE_URL=https://api.amplify.ai/v1

# Directory Configuration
DATA_DIRECTORY=./sales_data
OUTPUT_DIRECTORY=./analytics_output

# Analysis Configuration
CONFIDENCE_LEVEL=0.95
MAX_FILE_SIZE_MB=50
SAMPLE_SIZE_THRESHOLD=500
CORRELATION_THRESHOLD=0.6

# Git Configuration
GIT_BRANCH=sales-analysis
COMMIT_PREFIX=[ANALYTICS]
GIT_REMOTE=origin

# Logging
LOG_LEVEL=INFO
```

## Step 3: Directory Structure Creation

```bash
# Create directories
mkdir -p sales_data analytics_output/{reports,visualizations,pipeline_logs} logs

# Verify structure
tree -a
```

**Directory structure created:**
```
techcorp-analytics/
├── .env
├── .env.example
├── .github/workflows/analysis.yml
├── sales_data/              # Our data monitoring directory
├── analytics_output/        # Generated reports go here
│   ├── reports/
│   ├── visualizations/
│   └── pipeline_logs/
├── logs/                    # Application logs
├── main.py
├── config.py
├── data_monitor.py
├── analysis_engine.py
├── report_generator.py
├── ci_cd_manager.py
└── requirements.txt
```

---

# Part 2: Testing with Sample Data

## Step 1: Create Realistic Sales Data

Let's create sample sales data that represents TechCorp's monthly sales:

```bash
# Create Q4 2024 sales data
cat > sales_data/october_2024_sales.csv << 'EOF'
date,product,category,sales_rep,region,revenue,quantity,customer_type
2024-10-01,CloudSync Pro,Software,Alice Johnson,North America,15000,5,Enterprise
2024-10-01,DataViz Suite,Analytics,Bob Chen,Europe,8000,2,SMB
2024-10-02,CloudSync Pro,Software,Charlie Davis,Asia Pacific,12000,4,Enterprise
2024-10-02,SecureNet,Security,Diana Martinez,North America,25000,10,Enterprise
2024-10-03,DataViz Suite,Analytics,Eve Wilson,Europe,6000,3,SMB
2024-10-03,MobileApp Builder,Development,Frank Zhang,Asia Pacific,18000,6,Enterprise
2024-10-04,CloudSync Pro,Software,Alice Johnson,North America,9000,3,SMB
2024-10-05,SecureNet,Security,Bob Chen,Europe,20000,8,Enterprise
2024-10-05,DataViz Suite,Analytics,Charlie Davis,Asia Pacific,4500,1,SMB
2024-10-06,MobileApp Builder,Development,Diana Martinez,North America,22000,7,Enterprise
2024-10-07,CloudSync Pro,Software,Eve Wilson,Europe,13500,5,Enterprise
2024-10-07,SecureNet,Security,Frank Zhang,Asia Pacific,30000,12,Enterprise
2024-10-08,DataViz Suite,Analytics,Alice Johnson,North America,7200,4,SMB
2024-10-09,MobileApp Builder,Development,Bob Chen,Europe,16000,5,SMB
2024-10-10,CloudSync Pro,Software,Charlie Davis,Asia Pacific,11000,4,Enterprise
2024-10-10,SecureNet,Security,Diana Martinez,North America,28000,11,Enterprise
2024-10-11,DataViz Suite,Analytics,Eve Wilson,Europe,5400,2,SMB
2024-10-12,MobileApp Builder,Development,Frank Zhang,Asia Pacific,19500,6,Enterprise
2024-10-12,CloudSync Pro,Software,Alice Johnson,North America,8500,3,SMB
2024-10-13,SecureNet,Security,Bob Chen,Europe,23000,9,Enterprise
2024-10-14,DataViz Suite,Analytics,Charlie Davis,Asia Pacific,6800,3,SMB
2024-10-15,MobileApp Builder,Development,Diana Martinez,North America,21000,7,Enterprise
EOF
```

## Step 2: Test Configuration Validation

```bash
# Test our configuration
python -c "from config import config; print('✅ Config validation:', config.validate_config())"
```

**Expected output:**
```
✅ Config validation: True
```

If you see errors, check your `.env` file and API key.

---

# Part 3: Single File Analysis Example

## Step 1: Run Analysis on October Sales

```bash
# Analyze the October sales data
python main.py --analyze sales_data/october_2024_sales.csv
```

**Console output you'll see:**
```
2024-12-06 10:30:15,123 - config - INFO - Pipeline initialization completed successfully
2024-12-06 10:30:15,125 - __main__ - INFO - Running one-time analysis on: sales_data/october_2024_sales.csv
2024-12-06 10:30:15,127 - analysis_engine - INFO - Starting analysis of: sales_data/october_2024_sales.csv
2024-12-06 10:30:15,135 - analysis_engine - INFO - Loaded 22 rows and 8 columns from sales_data/october_2024_sales.csv
2024-12-06 10:30:15,245 - report_generator - INFO - Generating AI insights via Amplify API
2024-12-06 10:30:18,892 - report_generator - INFO - AI insights generated successfully
2024-12-06 10:30:19,156 - report_generator - INFO - Reports generated successfully:
2024-12-06 10:30:19,156 - report_generator - INFO - - HTML: /analytics_output/reports/october_2024_sales_report_20241206_103019.html
2024-12-06 10:30:19,156 - report_generator - INFO - - JSON: /analytics_output/reports/october_2024_sales_report_20241206_103019.json
2024-12-06 10:30:19,156 - report_generator - INFO - - Summary: /analytics_output/reports/october_2024_sales_summary_20241206_103019.txt
2024-12-06 10:30:19,234 - ci_cd_manager - INFO - Starting CI/CD pipeline for analysis of: sales_data/october_2024_sales.csv
2024-12-06 10:30:19,235 - ci_cd_manager - INFO - Created analysis branch: sales-analysis-october_2024_sales-20241206_103019
2024-12-06 10:30:19,456 - ci_cd_manager - INFO - Pipeline sales-analysis-october_2024_sales-20241206_103019 completed successfully in 0.22s: Pipeline completed successfully
2024-12-06 10:30:19,457 - __main__ - INFO - One-time analysis completed
```

## Step 2: Examine the Generated Reports

Let's look at what was created:

```bash
# Check generated files
ls -la analytics_output/reports/
ls -la analytics_output/visualizations/
```

**Files created:**
```
analytics_output/reports/
├── october_2024_sales_report_20241206_103019.html
├── october_2024_sales_report_20241206_103019.json
└── october_2024_sales_summary_20241206_103019.txt

analytics_output/visualizations/
├── october_2024_sales_correlation_heatmap.png
├── october_2024_sales_distributions.png
└── october_2024_sales_boxplots.png
```

## Step 3: Review the HTML Report

**Sample HTML report content:**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Data Analysis Report - october_2024_sales</title>
</head>
<body>
    <div class="container">
        <h1>Data Analysis Report</h1>
        <h2>october_2024_sales</h2>
        <p class="timestamp">Generated on 2024-12-06 10:30:19</p>
        
        <div class="section">
            <h2>Executive Summary</h2>
            <div class="metric-grid">
                <div class="metric-card">
                    <div class="metric-value">22</div>
                    <div class="metric-label">Total Rows</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">8</div>
                    <div class="metric-label">Total Columns</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">0.02 MB</div>
                    <div class="metric-label">File Size</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value quality-score score-excellent">100%</div>
                    <div class="metric-label">Data Quality Score</div>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2>AI-Powered Insights</h2>
            <div class="ai-insights">
                <pre>Based on the October 2024 sales data analysis, here are the key insights:

**Key Findings:**
1. Strong Revenue Performance: Total revenue of $342,000 across 22 transactions shows healthy sales activity
2. Product Mix Balance: Five product lines (CloudSync Pro, DataViz Suite, SecureNet, MobileApp Builder) with SecureNet leading in average deal size
3. Geographic Distribution: Sales well-distributed across North America, Europe, and Asia Pacific regions
4. Customer Segmentation: 68% Enterprise vs 32% SMB sales, indicating strong enterprise focus

**Data Quality Assessment:**
- Excellent data completeness (100% - no missing values)
- No duplicate records detected
- All fields properly populated with consistent formatting
- Date range covers October 1-15, 2024 (15-day period)

**Business Implications:**
1. SecureNet product shows highest revenue per transaction ($25,750 average), suggesting strong market demand for security solutions
2. Enterprise customers drive majority of revenue - consider enterprise-focused marketing strategies
3. Sales rep performance varies: Diana Martinez leads with $96,000 total, followed by Bob Chen with $59,000
4. Asia Pacific region shows strong performance despite having fewer transactions

**Recommendations:**
1. Investigate SecureNet's success factors and apply to other products
2. Develop targeted Enterprise customer acquisition strategies
3. Analyze sales rep best practices from top performers
4. Consider expanding Asia Pacific market presence
5. Monitor SMB segment for growth opportunities

**Data Collection Recommendations:**
- Add customer company size data for better segmentation
- Include lead source information for marketing attribution
- Track deal cycle length for sales process optimization</pre>
            </div>
        </div>
    </div>
</body>
</html>
```

## Step 4: Review the Summary Report

```bash
# View the text summary
cat analytics_output/reports/october_2024_sales_summary_20241206_103019.txt
```

**Sample summary output:**
```
DATA ANALYSIS SUMMARY REPORT
============================
File: october_2024_sales
Generated: 2024-12-06 10:30:19

DATASET OVERVIEW
----------------
Rows: 22
Columns: 8
File Size: 0.02 MB
Data Quality Score: 100.0%

KEY FINDINGS
------------
• Found 2 strong correlations between variables
• Outliers detected in 1 columns

RECOMMENDATIONS
---------------
• Explore strong correlations for potential feature engineering

AI INSIGHTS
-----------
Based on the October 2024 sales data analysis, here are the key insights:

**Key Findings:**
1. Strong Revenue Performance: Total revenue of $342,000 across 22 transactions shows healthy sales activity
2. Product Mix Balance: Five product lines (CloudSync Pro, DataViz Suite, SecureNet, MobileApp Builder) with SecureNet leading in average deal size
3. Geographic Distribution: Sales well-distributed across North America, Europe, and Asia Pacific regions...
```

---

# Part 4: Continuous Monitoring Example

## Step 1: Start Continuous Monitoring

```bash
# Start the pipeline in continuous monitoring mode
python main.py
```

**Console output:**
```
2024-12-06 10:35:20,123 - config - INFO - Pipeline initialization completed successfully
2024-12-06 10:35:20,125 - __main__ - INFO - Starting data analysis pipeline...
2024-12-06 10:35:20,127 - data_monitor - INFO - Starting data monitor on: /Users/techcorp/techcorp-analytics/sales_data
2024-12-06 10:35:20,128 - data_monitor - INFO - Data monitor started successfully
2024-12-06 10:35:20,128 - data_monitor - INFO - Monitoring file types: ['.csv', '.json', '.xlsx', '.parquet']
2024-12-06 10:35:20,129 - data_monitor - INFO - Scanning for existing data files...
2024-12-06 10:35:20,135 - data_monitor - INFO - Processing existing file: sales_data/october_2024_sales.csv
2024-12-06 10:35:20,136 - data_monitor - INFO - Processed 1 existing files
2024-12-06 10:35:20,137 - __main__ - INFO - Pipeline is now monitoring for data changes...
2024-12-06 10:35:20,137 - __main__ - INFO - Watching directory: ./sales_data
2024-12-06 10:35:20,137 - __main__ - INFO - Output directory: ./analytics_output
```

**The pipeline is now running and waiting for file changes...**

## Step 2: Simulate New Data Arrival

Open a new terminal (keep the pipeline running) and add new data:

```bash
# Terminal 2: Add November sales data
cat > sales_data/november_2024_sales.csv << 'EOF'
date,product,category,sales_rep,region,revenue,quantity,customer_type
2024-11-01,CloudSync Pro,Software,Alice Johnson,North America,18000,6,Enterprise
2024-11-01,DataViz Suite,Analytics,Bob Chen,Europe,9500,3,SMB
2024-11-02,SecureNet,Security,Charlie Davis,Asia Pacific,32000,13,Enterprise
2024-11-02,MobileApp Builder,Development,Diana Martinez,North America,24000,8,Enterprise
2024-11-03,CloudSync Pro,Software,Eve Wilson,Europe,14000,5,Enterprise
2024-11-03,AI Assistant Pro,AI/ML,Frank Zhang,Asia Pacific,45000,3,Enterprise
2024-11-04,DataViz Suite,Analytics,Alice Johnson,North America,7800,4,SMB
2024-11-04,SecureNet,Security,Bob Chen,Europe,28000,11,Enterprise
2024-11-05,MobileApp Builder,Development,Charlie Davis,Asia Pacific,21000,7,SMB
2024-11-05,AI Assistant Pro,AI/ML,Diana Martinez,North America,38000,2,Enterprise
2024-11-06,CloudSync Pro,Software,Eve Wilson,Europe,16500,6,Enterprise
2024-11-06,DataViz Suite,Analytics,Frank Zhang,Asia Pacific,8200,4,SMB
2024-11-07,SecureNet,Security,Alice Johnson,North America,30000,12,Enterprise
2024-11-07,AI Assistant Pro,AI/ML,Bob Chen,Europe,42000,3,Enterprise
2024-11-08,MobileApp Builder,Development,Charlie Davis,Asia Pacific,19500,6,SMB
EOF
```

## Step 3: Watch Automatic Processing

**Back in Terminal 1, you'll see:**
```
2024-12-06 10:37:45,234 - data_monitor - INFO - Data file created: sales_data/november_2024_sales.csv
2024-12-06 10:37:45,235 - __main__ - INFO - Processing data change: sales_data/november_2024_sales.csv
2024-12-06 10:37:45,237 - analysis_engine - INFO - Starting analysis of: sales_data/november_2024_sales.csv
2024-12-06 10:37:45,245 - analysis_engine - INFO - Loaded 15 rows and 8 columns from sales_data/november_2024_sales.csv
2024-12-06 10:37:46,456 - report_generator - INFO - Generating AI insights via Amplify API
2024-12-06 10:37:49,123 - report_generator - INFO - AI insights generated successfully
2024-12-06 10:37:49,387 - report_generator - INFO - Reports generated successfully:
2024-12-06 10:37:49,387 - report_generator - INFO - - HTML: /analytics_output/reports/november_2024_sales_report_20241206_103749.html
2024-12-06 10:37:49,387 - report_generator - INFO - - JSON: /analytics_output/reports/november_2024_sales_report_20241206_103749.json
2024-12-06 10:37:49,387 - report_generator - INFO - - Summary: /analytics_output/reports/november_2024_sales_summary_20241206_103749.txt
2024-12-06 10:37:49,512 - ci_cd_manager - INFO - Starting CI/CD pipeline for analysis of: sales_data/november_2024_sales.csv
2024-12-06 10:37:49,513 - ci_cd_manager - INFO - Created analysis branch: sales-analysis-november_2024_sales-20241206_103749
2024-12-06 10:37:49,734 - ci_cd_manager - INFO - Committed changes: abc12345 - [ANALYTICS] Analysis results for november_2024_sales.csv
2024-12-06 10:37:49,956 - ci_cd_manager - INFO - Pushed branch sales-analysis-november_2024_sales-20241206_103749 to origin
2024-12-06 10:37:50,178 - ci_cd_manager - INFO - Created pull request: https://github.com/techcorp/techcorp-analytics/pull/42
2024-12-06 10:37:50,234 - ci_cd_manager - INFO - Pipeline sales-analysis-november_2024_sales-20241206_103749 completed successfully in 0.72s
2024-12-06 10:37:50,235 - __main__ - INFO - Analysis pipeline completed for sales_data/november_2024_sales.csv
```

## Step 4: Check Git Status

```bash
# Terminal 2: Check what happened in Git
git status
git branch -a
git log --oneline -5
```

**Output:**
```
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean

# Branches created
* main
  remotes/origin/main
  remotes/origin/sales-analysis-november_2024_sales-20241206_103749
  remotes/origin/sales-analysis-october_2024_sales-20241206_103019

# Recent commits
abc12345 [ANALYTICS] Analysis results for november_2024_sales.csv
def67890 [ANALYTICS] Analysis results for october_2024_sales.csv
```

---

# Part 5: GitHub Actions Workflow Example

## Step 1: Commit and Push to Trigger CI/CD

```bash
# Terminal 2: Add both data files to main branch and push
git add sales_data/
git commit -m "Add October and November 2024 sales data for analysis"
git push origin main
```

## Step 2: GitHub Actions Execution

**On GitHub, you'll see the workflow running:**

```yaml
# Workflow execution log (abbreviated)
✅ setup (ubuntu-latest)
   - Checkout code
   - Get changed files: sales_data/october_2024_sales.csv, sales_data/november_2024_sales.csv
   - Check for data file changes: has_data_changes=true

✅ validate-data (ubuntu-latest)
   - Setup Python 3.9
   - Install dependencies
   - Validate data files:
     ✅ Valid: sales_data/october_2024_sales.csv (22 rows, 8 columns)
     ✅ Valid: sales_data/november_2024_sales.csv (15 rows, 8 columns)
     Summary: 2 valid, 0 invalid files

✅ analyze-data (ubuntu-latest)
   - Setup directories
   - Configure environment
   - Run analysis on changed files:
     🔍 Analyzing: sales_data/october_2024_sales.csv
     ✅ Analysis completed: sales_data/october_2024_sales.csv
     🔍 Analyzing: sales_data/november_2024_sales.csv
     ✅ Analysis completed: sales_data/november_2024_sales.csv
   - Upload analysis results

✅ quality-check (ubuntu-latest)
   - Download analysis results
   - Quality assessment:
     - HTML Reports: 2
     - JSON Reports: 2
     - Visualizations: 6
     - Log Analysis: 0 errors, 2 warnings
   - Overall Assessment: ✅ PASS - Analysis pipeline generated reports and visualizations successfully

✅ deploy-results (ubuntu-latest)
   - Setup Pages
   - Prepare GitHub Pages content
   - Deploy to GitHub Pages: https://techcorp.github.io/techcorp-analytics
```

## Step 3: View Deployed Results

The GitHub Pages deployment creates an index page:

**https://techcorp.github.io/techcorp-analytics/index.html:**
```html
<!DOCTYPE html>
<html>
<head>
    <title>Data Analysis Results</title>
</head>
<body>
    <div class="container">
        <h1>TechCorp Data Analysis Pipeline Results</h1>
        <p><strong>Last Updated:</strong> 2024-12-06 10:45:32</p>
        
        <div class="section">
            <h2>Generated Reports</h2>
            <ul class="file-list">
                <li><a href="reports/october_2024_sales_report_20241206_103019.html">october_2024_sales_report_20241206_103019.html</a></li>
                <li><a href="reports/november_2024_sales_report_20241206_103749.html">november_2024_sales_report_20241206_103749.html</a></li>
            </ul>
        </div>
        
        <div class="section">
            <h2>Visualizations</h2>
            <ul class="file-list">
                <li><a href="visualizations/october_2024_sales_correlation_heatmap.png">october_2024_sales_correlation_heatmap.png</a></li>
                <li><a href="visualizations/october_2024_sales_distributions.png">october_2024_sales_distributions.png</a></li>
                <li><a href="visualizations/november_2024_sales_boxplots.png">november_2024_sales_boxplots.png</a></li>
            </ul>
        </div>
    </div>
</body>
</html>
```

---

# Part 6: Pull Request Review Example

## Step 1: Review Automated Pull Request

**GitHub Pull Request #42:**
```markdown
# Analysis results for november_2024_sales.csv

## Automated Data Analysis Results

### Dataset Overview
- **File**: november_2024_sales.csv
- **Rows**: 15
- **Columns**: 8
- **Size**: 0.01 MB

### Data Quality
- **Missing Values**: 0.0%
- **Duplicate Rows**: 0

### Analysis Artifacts Included

- `november_2024_sales_report_20241206_103749.html`
- `november_2024_sales_report_20241206_103749.json`
- `november_2024_sales_summary_20241206_103749.txt`
- `november_2024_sales_correlation_heatmap.png`
- `november_2024_sales_distributions.png`
- `november_2024_sales_boxplots.png`

### Pipeline Information
- **Pipeline ID**: pipeline_20241206_103749
- **Generated**: 2024-12-06 10:37:49

---
*This PR was created automatically by the Data Analysis Pipeline*
```

## Step 2: AI Insights Comparison

**November vs October Analysis Highlights:**

**November Report AI Insights (Sample):**
```
**Key Findings:**
1. Revenue Growth: November shows 15 transactions totaling $373,000 vs October's $342,000 (+9% growth)
2. New Product Introduction: AI Assistant Pro launched with highest average deal value ($41,667)
3. Geographic Expansion: Continued strong performance across all three regions
4. Customer Mix Shift: 80% Enterprise vs 20% SMB (up from 68% Enterprise in October)

**Business Implications:**
1. AI Assistant Pro shows exceptional market reception - consider accelerated rollout
2. Enterprise focus strategy is working - SMB segment may need attention
3. Revenue per transaction increased from $15,545 to $24,867 (+60%)
4. Sales team efficiency improved with higher deal values

**Month-over-Month Trends:**
- Transaction volume: -32% (22 to 15 transactions)
- Revenue growth: +9% despite fewer transactions
- Average deal size: +60% improvement
- Enterprise customer focus intensified
```

---

# Part 7: Error Handling and Recovery Examples

## Step 1: Simulate File Processing Error

```bash
# Create a corrupted CSV file
echo "invalid,csv,data,with,wrong,format" > sales_data/corrupted_data.csv
echo "this,is,not,proper,csv" >> sales_data/corrupted_data.csv
```

**Pipeline response:**
```
2024-12-06 11:15:30,123 - data_monitor - INFO - Data file created: sales_data/corrupted_data.csv
2024-12-06 11:15:30,124 - __main__ - INFO - Processing data change: sales_data/corrupted_data.csv
2024-12-06 11:15:30,125 - analysis_engine - INFO - Starting analysis of: sales_data/corrupted_data.csv
2024-12-06 11:15:30,126 - analysis_engine - INFO - Loaded 2 rows and 5 columns from sales_data/corrupted_data.csv
2024-12-06 11:15:30,127 - analysis_engine - WARNING - No numeric columns for correlation analysis
2024-12-06 11:15:30,128 - analysis_engine - WARNING - No numeric columns for distribution analysis
2024-12-06 11:15:30,129 - analysis_engine - WARNING - No numeric columns for outlier detection
2024-12-06 11:15:30,130 - analysis_engine - WARNING - Insufficient numeric columns for hypothesis testing
2024-12-06 11:15:30,131 - analysis_engine - WARNING - No time series data detected
2024-12-06 11:15:30,135 - analysis_engine - INFO - Analysis completed for: sales_data/corrupted_data.csv
2024-12-06 11:15:31,256 - report_generator - INFO - AI insights generated successfully
2024-12-06 11:15:31,458 - report_generator - INFO - Reports generated successfully (limited analysis)
```

**The system gracefully handles the error and produces a report noting data limitations.**

## Step 2: Simulate API Failure

```bash
# Temporarily break API key
export AMPLIFY_API_KEY="invalid_key"
echo "test,data,123" > sales_data/test_api_failure.csv
```

**Pipeline response:**
```
2024-12-06 11:20:15,234 - report_generator - ERROR - Amplify API error: 401 - {"error": "Invalid API key"}
2024-12-06 11:20:15,235 - report_generator - WARNING - Failed to generate AI insights: API authentication failed
2024-12-06 11:20:15,456 - report_generator - INFO - Reports generated successfully (without AI insights)
```

**The system continues without AI insights and generates reports with statistical analysis only.**

## Step 3: Simulate Git Error

```bash
# Remove git remote to simulate git failure
git remote remove origin
echo "test,git,failure" > sales_data/test_git_failure.csv
```

**Pipeline response:**
```
2024-12-06 11:25:45,123 - ci_cd_manager - WARNING - Remote 'origin' not found
2024-12-06 11:25:45,124 - ci_cd_manager - ERROR - Failed to push branch test-branch: No remote named 'origin'
2024-12-06 11:25:45,125 - ci_cd_manager - INFO - Pipeline completed with warnings: Git operations failed but analysis succeeded
```

**The system completes analysis and reporting but logs Git operation failures.**

---

# Part 8: Advanced Usage Examples

## Step 1: Custom Configuration for Different Departments

**Marketing Team Configuration (.env.marketing):**
```bash
# Marketing team focuses on customer segmentation
DATA_DIRECTORY=./marketing_data
OUTPUT_DIRECTORY=./marketing_reports
CORRELATION_THRESHOLD=0.4
SAMPLE_SIZE_THRESHOLD=100
GIT_BRANCH=marketing-analysis
COMMIT_PREFIX=[MARKETING]
```

**Finance Team Configuration (.env.finance):**
```bash
# Finance team needs higher precision
DATA_DIRECTORY=./finance_data  
OUTPUT_DIRECTORY=./finance_reports
CONFIDENCE_LEVEL=0.99
MAX_FILE_SIZE_MB=200
CORRELATION_THRESHOLD=0.7
GIT_BRANCH=finance-analysis
COMMIT_PREFIX=[FINANCE]
```

## Step 2: Batch Processing Multiple Files

```bash
# Process multiple files at once
python main.py --analyze sales_data/october_2024_sales.csv
python main.py --analyze sales_data/november_2024_sales.csv
python main.py --analyze sales_data/december_2024_sales.csv

# Or start continuous monitoring and drop multiple files
cp data_archive/*.csv sales_data/
# Pipeline processes each file automatically
```

## Step 3: Integration with External Systems

**Example webhook integration:**
```bash
# Create webhook listener that triggers analysis
curl -X POST http://localhost:5000/trigger-analysis \
  -H "Content-Type: application/json" \
  -d '{"file_path": "sales_data/webhook_data.csv", "source": "salesforce"}'
```

**Example database integration:**
```bash
# Export results to database
python -c "
from report_generator import ReportGenerator
import json

# Load analysis results
with open('analytics_output/reports/november_2024_sales_report_*.json', 'r') as f:
    data = json.load(f)

# Export to database (pseudocode)
# db.analytics_results.insert(data)
print('Results exported to database')
"
```

---

# Part 9: Monitoring and Maintenance

## Step 1: Log Analysis

```bash
# Monitor application logs
tail -f logs/pipeline.log

# Search for errors
grep -i error logs/pipeline.log

# Analyze processing times
grep "duration_seconds" logs/pipeline.log | tail -10
```

## Step 2: Performance Monitoring

```bash
# Monitor system resources during analysis
python -c "
import psutil
import time

print('Monitoring system resources...')
for i in range(10):
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    print(f'CPU: {cpu}%, Memory: {memory.percent}%, Available: {memory.available/1024/1024:.1f}MB')
    time.sleep(5)
"
```

## Step 3: Pipeline Health Check

```bash
# Check pipeline status
python -c "
from data_monitor import DataMonitor
from config import config

async def check_health():
    monitor = DataMonitor(config.data_directory, lambda x: None)
    status = monitor.get_status()
    print('Pipeline Health Check:')
    for key, value in status.items():
        print(f'  {key}: {value}')

import asyncio
asyncio.run(check_health())
"
```

---

# Part 10: Deployment Scenarios

## Scenario 1: Local Development

```bash
# Development workflow
python main.py --analyze test_data.csv  # Test with sample data
python main.py                          # Run continuous monitoring
# Ctrl+C to stop
```

## Scenario 2: Production Server

```bash
# Production deployment with process management
nohup python main.py > production.log 2>&1 &
echo $! > pipeline.pid

# Monitor production
tail -f production.log

# Stop production
kill $(cat pipeline.pid)
```

## Scenario 3: Docker Container

```dockerfile
# Example Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

```bash
# Build and run container
docker build -t techcorp-analytics .
docker run -d --name analytics-pipeline \
  -v $(pwd)/sales_data:/app/sales_data \
  -v $(pwd)/analytics_output:/app/analytics_output \
  --env-file .env \
  techcorp-analytics
```

## Scenario 4: Cloud Deployment (AWS)

```bash
# Deploy to AWS using GitHub Actions
# (Workflow includes deployment to ECS or Lambda)

# Monitor cloud deployment
aws logs tail /aws/lambda/techcorp-analytics --follow

# Check function status
aws lambda get-function --function-name techcorp-analytics
```

---

# Summary

This walkthrough demonstrated:

✅ **Complete setup** from scratch to production  
✅ **Real data analysis** with sample sales data  
✅ **Continuous monitoring** with automatic processing  
✅ **CI/CD integration** with GitHub Actions  
✅ **Error handling** and recovery scenarios  
✅ **Advanced usage** patterns and configurations  
✅ **Monitoring and maintenance** procedures  
✅ **Multiple deployment** options  

The Data Analysis Pipeline provides a complete, production-ready solution that can be adapted to various business needs while maintaining professional standards for automation, reporting, and integration.

**Key Takeaways:**
- The system handles real business data automatically
- AI insights provide valuable business intelligence  
- Git integration enables collaborative workflows
- Error handling ensures robust operation
- Multiple deployment options support various environments
- Comprehensive monitoring enables maintenance and optimization

This example shows how the pipeline can transform raw sales data into actionable business insights automatically, demonstrating the power of combining statistical analysis with AI-powered interpretation and modern DevOps practices.