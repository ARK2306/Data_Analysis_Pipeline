# config.py - Complete Line-by-Line Code Explanation

## Overview
The `config.py` file provides centralized configuration management for the entire Data Analysis Pipeline. It handles environment variables, logging setup, directory creation, and configuration validation.

## Detailed Code Breakdown

### Imports and Dependencies

```python
import os
import logging
from typing import Dict, Any, List
from dotenv import load_dotenv
```

**Lines 1-4:** Import necessary modules:
- `os`: Operating system interface for environment variables and file operations
- `logging`: Python's standard logging framework
- `typing`: Type hints for better code documentation and IDE support
- `dotenv`: Load environment variables from .env files

```python
load_dotenv()
```

**Line 6:** Load environment variables from a `.env` file in the current directory. This allows configuration without hardcoding values or setting system environment variables.

---

## Config Class Definition

### Class Initialization

```python
class Config:
    """Configuration management for the data analysis pipeline."""
    
    def __init__(self):
        self.setup_logging()
```

**Lines 8-12:**
- **Line 8:** Define the main configuration class
- **Line 9:** Class docstring explaining its purpose
- **Lines 11-12:** Constructor that automatically sets up logging when config is created

---

## API Configuration Properties

### Amplify API Key

```python
@property
def amplify_api_key(self) -> str:
    """Get Amplify API key from environment variables."""
    api_key = os.getenv('AMPLIFY_API_KEY')
    if not api_key:
        raise ValueError("AMPLIFY_API_KEY environment variable not set")
    return api_key
```

**Lines 14-20:**
- **Line 14:** Python property decorator - makes this method accessible as an attribute
- **Line 15:** Method signature with return type annotation
- **Line 17:** Get API key from environment variable
- **Lines 18-19:** Validation - raise error if API key is missing (critical for operation)
- **Line 20:** Return the API key

### Amplify Base URL

```python
@property
def amplify_base_url(self) -> str:
    """Get Amplify API base URL."""
    return os.getenv('AMPLIFY_BASE_URL', 'https://api.amplify.ai/v1')
```

**Lines 22-25:**
- **Line 24:** Get base URL from environment with default fallback
- Default ensures the system works even without explicit configuration

---

## Directory Configuration Properties

### Data Directory

```python
@property
def data_directory(self) -> str:
    """Directory to monitor for data files."""
    return os.getenv('DATA_DIRECTORY', './data')
```

**Lines 27-30:**
- **Line 29:** Get data directory path with default of `./data`
- This is where the pipeline will monitor for new/changed data files

### Output Directory

```python
@property
def output_directory(self) -> str:
    """Directory for generated reports and visualizations."""
    return os.getenv('OUTPUT_DIRECTORY', './output')
```

**Lines 32-35:**
- **Line 34:** Get output directory path with default of `./output`
- This is where reports, visualizations, and analysis results are saved

---

## Logging Configuration

### Log Level

```python
@property
def log_level(self) -> str:
    """Logging level."""
    return os.getenv('LOG_LEVEL', 'INFO')
```

**Lines 37-40:**
- **Line 39:** Get logging level with INFO as default
- Supports standard Python logging levels: DEBUG, INFO, WARNING, ERROR, CRITICAL

---

## File Type Configuration

### Supported File Types

```python
@property
def supported_file_types(self) -> List[str]:
    """Supported data file extensions."""
    return ['.csv', '.json', '.xlsx', '.parquet']
```

**Lines 42-45:**
- **Line 44:** Return list of supported file extensions
- These are the file types the pipeline can automatically process
- Hard-coded for consistency and reliability

---

## Analysis Configuration

### Analysis Parameters

```python
@property
def analysis_config(self) -> Dict[str, Any]:
    """Configuration for statistical analysis."""
    return {
        'confidence_level': float(os.getenv('CONFIDENCE_LEVEL', '0.95')),
        'max_file_size_mb': int(os.getenv('MAX_FILE_SIZE_MB', '100')),
        'sample_size_threshold': int(os.getenv('SAMPLE_SIZE_THRESHOLD', '1000')),
        'correlation_threshold': float(os.getenv('CORRELATION_THRESHOLD', '0.5'))
    }
```

**Lines 47-54:**
- **Line 49:** Statistical confidence level (default 95%)
- **Line 50:** Maximum file size for processing (default 100MB)
- **Line 51:** Minimum sample size for certain statistical tests (default 1000)
- **Line 52:** Correlation threshold for identifying "strong" correlations (default 0.5)

Each parameter has type conversion (float/int) and sensible defaults.

---

## Git Configuration

### Git Parameters

```python
@property
def git_config(self) -> Dict[str, str]:
    """Git configuration for CI/CD."""
    return {
        'branch_name': os.getenv('GIT_BRANCH', 'analysis-pipeline'),
        'commit_prefix': os.getenv('COMMIT_PREFIX', '[AUTO]'),
        'remote_name': os.getenv('GIT_REMOTE', 'origin')
    }
```

**Lines 56-62:**
- **Line 58:** Branch name pattern for automated branches
- **Line 59:** Prefix for automated commit messages
- **Line 60:** Git remote name (usually 'origin')

These settings control how the CI/CD manager interacts with Git repositories.

---

## Logging Setup Method

### Setup Logging Configuration

```python
def setup_logging(self) -> None:
    """Configure logging for the application."""
    os.makedirs('logs', exist_ok=True)
    
    logging.basicConfig(
        level=getattr(logging, self.log_level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/pipeline.log'),
            logging.StreamHandler()
        ]
    )
```

**Lines 64-75:**
- **Line 66:** Create logs directory if it doesn't exist
- **Line 68:** Configure Python's logging system
- **Line 69:** Set logging level dynamically using getattr to convert string to logging constant
- **Line 70:** Define log message format with timestamp, logger name, level, and message
- **Lines 71-74:** Configure two handlers:
  - **Line 72:** File handler - writes logs to `logs/pipeline.log`
  - **Line 73:** Stream handler - writes logs to console (stdout)

This dual logging approach provides both persistent logs and real-time console output.

---

## Directory Management

### Create Necessary Directories

```python
def create_directories(self) -> None:
    """Create necessary directories if they don't exist."""
    directories = [
        self.data_directory,
        self.output_directory,
        'logs',
        f"{self.output_directory}/reports",
        f"{self.output_directory}/visualizations"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
```

**Lines 77-87:**
- **Lines 79-84:** List of all directories needed by the pipeline
- **Lines 86-87:** Create each directory with `exist_ok=True` (no error if directory already exists)

This ensures the pipeline has all necessary directories before starting operations.

---

## Configuration Validation

### Validate Configuration Method

```python
def validate_config(self) -> bool:
    """Validate configuration settings."""
    try:
        self.amplify_api_key
        self.create_directories()
        return True
    except Exception as e:
        logging.error(f"Configuration validation failed: {e}")
        return False
```

**Lines 89-96:**
- **Line 92:** Attempt to access the API key property (which will raise an error if not set)
- **Line 93:** Create necessary directories
- **Line 94:** Return True if everything succeeds
- **Lines 95-96:** Catch any exceptions and log them, return False

This validation runs before the pipeline starts to catch configuration issues early.

---

## Global Configuration Instance

### Module-Level Configuration

```python
config = Config()
```

**Line 98:** Create a global configuration instance that can be imported by other modules.

This singleton pattern ensures all modules use the same configuration instance.

---

## Key Design Patterns

### 1. **Singleton Pattern**
- Single global config instance shared across all modules
- Consistent configuration throughout the application
- Easy to modify configuration in one place

### 2. **Property Pattern**
- Configuration values accessed as properties, not methods
- Lazy evaluation - values computed when accessed
- Clean, readable syntax: `config.amplify_api_key` instead of `config.get_amplify_api_key()`

### 3. **Environment Variable Pattern**
- All configuration can be set via environment variables
- Sensible defaults for development
- Supports different configurations for dev/test/production

### 4. **Validation Pattern**
- Early validation prevents runtime errors
- Clear error messages for missing configuration
- Fail-fast approach - catch issues before they cause problems

### 5. **Directory Management**
- Automatic creation of required directories
- No manual setup required
- Consistent file organization

## Configuration Philosophy

### Security
- API keys and sensitive data come from environment variables
- No hardcoded secrets in source code
- Support for `.env` files for local development

### Flexibility
- Most settings can be overridden via environment variables
- Sensible defaults for quick setup
- Type conversion handles string environment variables

### Reliability
- Validation ensures required configuration is present
- Error handling with clear messages
- Automatic directory creation prevents runtime errors

### Maintainability
- Centralized configuration management
- Clear separation of different configuration types
- Well-documented properties with docstrings

This configuration system provides a robust foundation that supports both development and production deployments while maintaining security and flexibility.