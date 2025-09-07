# main.py - Complete Line-by-Line Code Explanation

## Overview
The `main.py` file serves as the entry point for the Data Analysis Pipeline. It orchestrates all components and provides both continuous monitoring and one-time analysis capabilities.

## Detailed Code Breakdown

### Imports and Dependencies

```python
#!/usr/bin/env python3
```
**Line 1:** Shebang line - tells the system to use Python 3 interpreter when executing this file directly

```python
"""
Data Analysis Pipeline with CI/CD Integration
Entry point for the automated data analysis system.
"""
```
**Lines 2-5:** Module docstring providing a brief description of the file's purpose

```python
import asyncio
import logging
import signal
import sys
from pathlib import Path
from typing import Optional
```
**Lines 7-12:** Standard library imports:
- `asyncio`: For asynchronous programming and concurrent operations
- `logging`: For structured logging throughout the application
- `signal`: For handling system signals (SIGINT, SIGTERM) for graceful shutdown
- `sys`: For system-specific parameters and functions
- `pathlib.Path`: For object-oriented filesystem path handling
- `typing.Optional`: For type hints indicating optional values

```python
from config import config
from data_monitor import DataMonitor
from analysis_engine import AnalysisEngine
from report_generator import ReportGenerator
from ci_cd_manager import CICDManager
```
**Lines 14-18:** Import custom modules:
- `config`: Configuration management system
- `DataMonitor`: File system monitoring component
- `AnalysisEngine`: Statistical analysis component
- `ReportGenerator`: Report generation with AI insights
- `CICDManager`: Git and CI/CD automation

```python
logger = logging.getLogger(__name__)
```
**Line 20:** Create a logger instance for this module using Python's standard logging

---

## Main Pipeline Class

### Class Definition and Initialization

```python
class DataAnalysisPipeline:
    """Main pipeline orchestrator."""
    
    def __init__(self):
        self.config = config
        self.monitor: Optional[DataMonitor] = None
        self.analysis_engine: Optional[AnalysisEngine] = None
        self.report_generator: Optional[ReportGenerator] = None
        self.cicd_manager: Optional[CICDManager] = None
        self.running = False
```

**Lines 22-31:** 
- **Line 22:** Define the main pipeline orchestrator class
- **Line 25:** Initialize with global config object
- **Lines 26-30:** Initialize component references as None (they'll be created during initialization)
- **Line 31:** Track running state of the pipeline

### Pipeline Initialization

```python
async def initialize(self) -> bool:
    """Initialize all pipeline components."""
    try:
        logger.info("Initializing Data Analysis Pipeline...")
        
        # Validate configuration
        if not self.config.validate_config():
            logger.error("Configuration validation failed")
            return False
        
        # Initialize components
        self.analysis_engine = AnalysisEngine()
        self.report_generator = ReportGenerator()
        self.cicd_manager = CICDManager()
        
        # Initialize data monitor with callback
        self.monitor = DataMonitor(
            watch_directory=self.config.data_directory,
            callback=self.on_data_change
        )
        
        logger.info("Pipeline initialization completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Failed to initialize pipeline: {e}")
        return False
```

**Lines 33-56:**
- **Line 33:** Async method that returns boolean indicating success/failure
- **Line 36:** Log the start of initialization
- **Lines 38-41:** Validate configuration before proceeding
- **Lines 43-45:** Create instances of core components
- **Lines 47-51:** Create DataMonitor with callback to handle file changes
- **Lines 53-56:** Error handling with logging and return status

### Data Change Handler

```python
async def on_data_change(self, file_path: str) -> None:
    """Handle data file changes."""
    try:
        logger.info(f"Processing data change: {file_path}")
        
        # Run statistical analysis
        analysis_results = await self.analysis_engine.analyze_file(file_path)
        
        if analysis_results:
            # Generate AI-powered report
            report_path = await self.report_generator.generate_report(
                file_path, analysis_results
            )
            
            # Commit changes and create PR if enabled
            if report_path:
                await self.cicd_manager.handle_analysis_complete(
                    file_path, report_path, analysis_results
                )
                
            logger.info(f"Analysis pipeline completed for {file_path}")
        else:
            logger.warning(f"Analysis failed for {file_path}")
            
    except Exception as e:
        logger.error(f"Error processing data change for {file_path}: {e}")
```

**Lines 58-79:**
- **Line 58:** Async callback method triggered when files change
- **Line 61:** Log the file being processed
- **Line 64:** Run statistical analysis on the changed file
- **Lines 66-71:** If analysis successful, generate reports with AI insights
- **Lines 73-77:** If report generated, trigger CI/CD automation
- **Lines 78-82:** Error handling with detailed logging

### Pipeline Start Method

```python
async def start(self) -> None:
    """Start the pipeline."""
    if not await self.initialize():
        logger.error("Failed to initialize pipeline")
        return
    
    self.running = True
    logger.info("Starting data analysis pipeline...")
    
    try:
        # Start file monitoring
        await self.monitor.start()
        
        logger.info("Pipeline is now monitoring for data changes...")
        logger.info(f"Watching directory: {self.config.data_directory}")
        logger.info(f"Output directory: {self.config.output_directory}")
        
        # Keep the pipeline running
        while self.running:
            await asyncio.sleep(1)
            
    except Exception as e:
        logger.error(f"Pipeline error: {e}")
    finally:
        await self.stop()
```

**Lines 81-103:**
- **Lines 83-85:** Initialize pipeline and exit if initialization fails
- **Line 87:** Set running flag to True
- **Lines 91-94:** Start the file monitoring system
- **Lines 96-98:** Log pipeline status and configuration
- **Lines 100-101:** Keep pipeline alive with sleep loop
- **Lines 102-105:** Error handling and cleanup

### Pipeline Stop Method

```python
async def stop(self) -> None:
    """Stop the pipeline gracefully."""
    logger.info("Stopping data analysis pipeline...")
    self.running = False
    
    if self.monitor:
        await self.monitor.stop()
    
    logger.info("Pipeline stopped successfully")
```

**Lines 105-113:**
- **Line 107:** Log shutdown start
- **Line 108:** Set running flag to False
- **Lines 110-111:** Stop file monitoring if it exists
- **Line 113:** Log successful shutdown

### Signal Handler

```python
def handle_signal(self, signum, frame):
    """Handle shutdown signals."""
    logger.info(f"Received signal {signum}, shutting down...")
    self.running = False
```

**Lines 115-118:**
- **Line 115:** Handle system signals (SIGINT/SIGTERM) for graceful shutdown
- **Line 117:** Log signal reception
- **Line 118:** Set running flag to False to trigger shutdown

---

## Utility Functions

### Single File Analysis

```python
async def run_analysis_once(file_path: str) -> None:
    """Run analysis on a single file (for testing or manual execution)."""
    try:
        logger.info(f"Running one-time analysis on: {file_path}")
        
        pipeline = DataAnalysisPipeline()
        if not await pipeline.initialize():
            logger.error("Failed to initialize pipeline")
            return
        
        await pipeline.on_data_change(file_path)
        logger.info("One-time analysis completed")
        
    except Exception as e:
        logger.error(f"One-time analysis failed: {e}")
```

**Lines 120-135:**
- **Line 120:** Async function for analyzing single files
- **Line 123:** Log the file being analyzed
- **Lines 125-129:** Create and initialize a temporary pipeline
- **Line 131:** Run the analysis callback directly
- **Lines 132-135:** Error handling and logging

---

## Main Entry Point

### Main Function

```python
async def main():
    """Main entry point."""
    try:
        # Check for command line arguments
        if len(sys.argv) > 1:
            if sys.argv[1] == '--analyze' and len(sys.argv) > 2:
                # Run analysis on specific file
                await run_analysis_once(sys.argv[2])
                return
            elif sys.argv[1] == '--help':
                print("""
Data Analysis Pipeline - Usage:

python main.py                    # Start continuous monitoring
python main.py --analyze <file>   # Analyze single file
python main.py --help            # Show this help
                """)
                return
        
        # Start continuous pipeline
        pipeline = DataAnalysisPipeline()
        
        # Set up signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, pipeline.handle_signal)
        signal.signal(signal.SIGTERM, pipeline.handle_signal)
        
        await pipeline.start()
        
    except KeyboardInterrupt:
        logger.info("Pipeline interrupted by user")
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        sys.exit(1)
```

**Lines 137-167:**
- **Lines 140-152:** Command line argument processing:
  - `--analyze <file>`: Run single file analysis
  - `--help`: Show usage information
- **Line 155:** Create main pipeline instance
- **Lines 157-159:** Set up signal handlers for graceful shutdown
- **Line 161:** Start the pipeline
- **Lines 163-167:** Error handling for keyboard interrupts and exceptions

### Script Execution Guard

```python
if __name__ == "__main__":
    asyncio.run(main())
```

**Lines 169-170:**
- **Line 169:** Ensure main() only runs when script is executed directly
- **Line 170:** Run the async main function using asyncio

---

## Key Design Patterns

### 1. **Async/Await Pattern**
- All I/O operations are asynchronous to prevent blocking
- Enables concurrent processing of multiple files
- Allows graceful handling of long-running operations

### 2. **Observer Pattern**
- DataMonitor observes file system changes
- Pipeline acts as observer receiving change notifications
- Loose coupling between monitoring and processing

### 3. **Pipeline Pattern**
- Data flows through stages: Monitor → Analyze → Report → CI/CD
- Each stage is independent and can be tested separately
- Easy to add new stages or modify existing ones

### 4. **Error Handling Strategy**
- Try-catch blocks at every level
- Detailed logging for debugging
- Graceful degradation when components fail

### 5. **Configuration Management**
- Centralized configuration through config module
- Environment variable support
- Validation before pipeline starts

This architecture provides a robust, scalable, and maintainable data analysis pipeline that can handle both continuous monitoring and on-demand analysis scenarios.