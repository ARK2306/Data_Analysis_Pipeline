# Retail Transactional Dataset Integration Guide

## Dataset Overview
**Source**: [Kaggle - Retail Transactional Dataset](https://www.kaggle.com/datasets/bhavikjikadara/retail-transactional-dataset)
**Size**: ~25 MB (25,984,799 bytes)
**Format**: ZIP file containing CSV
**License**: CC BY 4.0

## Dataset Structure

### Customer Demographics
- `Customer ID` - Unique identifier
- `Name` - Customer name
- `Email` - Email address
- `Phone` - Contact number
- `Address` - Location information
- `Age` - Customer age
- `Gender` - Demographics
- `Income` - Income level
- `Customer Segment` - Business classification

### Transaction Data
- `Last Purchase Date` - Most recent transaction
- `Total Purchases` - Number of transactions
- `Amount Spent` - Total spend value

### Product Information
- `Product Category` - Product classification
- `Product Brand` - Brand information
- `Product Type` - Specific product type

### Additional Metrics
- `Feedback` - Customer satisfaction
- `Shipping Method` - Delivery type
- `Payment Method` - Payment type
- `Order Status` - Transaction status

## Integration Steps

### Step 1: Download Dataset from Kaggle

#### Option A: Using Kaggle CLI (Recommended)
```bash
# Install kaggle CLI (if not already installed)
pip install kaggle

# Configure Kaggle API credentials
# 1. Go to kaggle.com → Account → API → Create New API Token
# 2. Download kaggle.json file
# 3. Place in ~/.kaggle/ directory (create if doesn't exist)
# 4. Set permissions: chmod 600 ~/.kaggle/kaggle.json

# Download dataset
kaggle datasets download -d bhavikjikadara/retail-transactional-dataset -p ./sales_data --unzip
```

#### Option B: Manual Download
1. Go to the [dataset page](https://www.kaggle.com/datasets/bhavikjikadara/retail-transactional-dataset)
2. Click "Download" button
3. Extract ZIP file
4. Move CSV file to `./sales_data/` directory

### Step 2: File Placement
```bash
# Ensure correct directory structure
mkdir -p sales_data

# Move your downloaded CSV file to:
# ./sales_data/retail_transactional_dataset.csv
```

### Step 3: Trigger Automated Analysis

#### Automatic CI/CD Trigger
```bash
# Simply commit and push the new dataset
git add sales_data/retail_transactional_dataset.csv
git commit -m "Add retail transactional dataset for analysis"
git push origin main
```

**That's it! The CI/CD pipeline will automatically:**
- ✅ Validate the dataset structure
- ✅ Run comprehensive statistical analysis
- ✅ Generate visualizations and reports
- ✅ Create quality assessment
- ✅ Deploy results (if Pages enabled)

## Expected Analysis Results

### Statistical Analysis
- **Customer Demographics**: Age distribution, gender breakdown, income analysis
- **Transaction Patterns**: Purchase frequency, spending behavior, seasonal trends
- **Product Performance**: Category analysis, brand preferences, product type insights
- **Customer Segmentation**: Behavioral clusters, value-based grouping
- **Correlation Analysis**: Relationships between demographics and spending

### Visualizations Generated
- Customer age distribution histograms
- Spending patterns by segment
- Product category performance charts
- Geographic distribution maps (if location data available)
- Customer lifetime value analysis
- Payment method preferences
- Shipping method analysis

### Business Insights (AI-Generated)
- Customer acquisition recommendations
- Inventory optimization suggestions
- Marketing campaign targeting
- Revenue optimization strategies
- Customer retention insights

## Manual Analysis (Optional)
If you want to run analysis manually instead of using CI/CD:

```bash
# Activate virtual environment
source venv/bin/activate

# Run analysis on specific file
python main.py --analyze sales_data/retail_transactional_dataset.csv
```

## Viewing Results

### GitHub Actions Artifacts
1. Go to your repository → Actions tab
2. Click on the latest workflow run
3. Download artifacts:
   - `analysis-results-3.9` - Complete analysis outputs
   - `analysis-summary` - Executive summary
   - `quality-report` - Quality assessment

### GitHub Pages (If Enabled)
1. Enable Pages: Repository → Settings → Pages → Source: GitHub Actions
2. View deployed results at: `https://yourusername.github.io/your-repo-name`

## Troubleshooting

### Common Issues

#### Dataset Too Large
```bash
# Check file size
ls -lh sales_data/retail_transactional_dataset.csv

# If >100MB, the pipeline will skip it
# Solution: Update MAX_FILE_SIZE_MB in .env file
```

#### API Rate Limits
```bash
# If Amplify API fails, check logs
cat logs/pipeline.log | grep ERROR

# Solution: Add delays between requests or check API key
```

#### Memory Issues
```bash
# For large datasets, the pipeline automatically samples
# Check SAMPLE_SIZE_THRESHOLD in .env (default: 1000 rows)
```

### Validation Errors
```bash
# Check data validation step in GitHub Actions
# Common fixes:
# - Ensure CSV has headers
# - Remove empty rows
# - Check for special characters in column names
```

## Advanced Configuration

### Environment Variables (.env)
```bash
# Analysis Configuration
CONFIDENCE_LEVEL=0.95           # Statistical confidence
MAX_FILE_SIZE_MB=100           # Maximum file size
SAMPLE_SIZE_THRESHOLD=1000     # Sampling threshold
CORRELATION_THRESHOLD=0.5      # Correlation significance

# API Configuration (Optional)
AMPLIFY_API_KEY=your_key_here  # For AI insights
```

### Custom Analysis Parameters
The pipeline automatically detects:
- Numerical columns → Statistical analysis
- Categorical columns → Frequency analysis
- Date columns → Time series analysis
- Text columns → Basic text analysis

## Success Indicators

### Pipeline Success
- ✅ All GitHub Actions jobs complete
- ✅ Quality report shows "PASS" status  
- ✅ Analysis artifacts generated
- ✅ No critical errors in logs

### Quality Metrics
- HTML Reports: Generated
- JSON Reports: Generated  
- Visualizations: Created
- Error Count: 0
- Warning Count: Minimal

## Next Steps After Analysis

1. **Review Results**: Download and examine generated reports
2. **Business Actions**: Implement insights from AI recommendations
3. **Iterate**: Add more datasets to compare trends
4. **Share**: Use GitHub Pages to share results with stakeholders
5. **Automate**: Set up regular data updates for continuous monitoring

## Dataset-Specific Analysis Opportunities

### Customer Segmentation
- RFM Analysis (Recency, Frequency, Monetary)
- Demographics-based clustering
- Behavioral pattern recognition

### Revenue Optimization
- Customer lifetime value prediction
- Cross-selling opportunities
- Price sensitivity analysis

### Marketing Intelligence
- Channel effectiveness analysis
- Customer acquisition cost optimization
- Retention strategy development

### Operations Insights
- Shipping method efficiency
- Payment method preferences
- Order fulfillment optimization

---

**Pro Tip**: The analysis pipeline is designed to handle various data formats and sizes automatically. Simply add your dataset and let the CI/CD do the heavy lifting!