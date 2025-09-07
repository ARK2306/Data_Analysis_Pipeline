import os
import logging
from typing import Dict, Any, List
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration management for the data analysis pipeline."""
    
    def __init__(self):
        self.setup_logging()
        
    @property
    def amplify_api_key(self) -> str:
        """Get Amplify API key from environment variables."""
        api_key = os.getenv('AMPLIFY_API_KEY')
        if not api_key:
            raise ValueError("AMPLIFY_API_KEY environment variable not set")
        return api_key
    
    @property
    def amplify_base_url(self) -> str:
        """Get Amplify API base URL."""
        return os.getenv('AMPLIFY_BASE_URL', 'https://api.amplify.ai/v1')
    
    @property
    def data_directory(self) -> str:
        """Directory to monitor for data files."""
        return os.getenv('DATA_DIRECTORY', './data')
    
    @property
    def output_directory(self) -> str:
        """Directory for generated reports and visualizations."""
        return os.getenv('OUTPUT_DIRECTORY', './output')
    
    @property
    def log_level(self) -> str:
        """Logging level."""
        return os.getenv('LOG_LEVEL', 'INFO')
    
    @property
    def supported_file_types(self) -> List[str]:
        """Supported data file extensions."""
        return ['.csv', '.json', '.xlsx', '.parquet']
    
    @property
    def analysis_config(self) -> Dict[str, Any]:
        """Configuration for statistical analysis."""
        return {
            'confidence_level': float(os.getenv('CONFIDENCE_LEVEL', '0.95')),
            'max_file_size_mb': int(os.getenv('MAX_FILE_SIZE_MB', '100')),
            'sample_size_threshold': int(os.getenv('SAMPLE_SIZE_THRESHOLD', '1000')),
            'correlation_threshold': float(os.getenv('CORRELATION_THRESHOLD', '0.5'))
        }
    
    @property
    def git_config(self) -> Dict[str, str]:
        """Git configuration for CI/CD."""
        return {
            'branch_name': os.getenv('GIT_BRANCH', 'analysis-pipeline'),
            'commit_prefix': os.getenv('COMMIT_PREFIX', '[AUTO]'),
            'remote_name': os.getenv('GIT_REMOTE', 'origin')
        }
    
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
            
    def validate_config(self) -> bool:
        """Validate configuration settings."""
        try:
            self.amplify_api_key
            self.create_directories()
            return True
        except Exception as e:
            logging.error(f"Configuration validation failed: {e}")
            return False

config = Config()