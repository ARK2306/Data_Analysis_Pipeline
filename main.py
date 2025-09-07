#!/usr/bin/env python3
"""
Data Analysis Pipeline with CI/CD Integration
Entry point for the automated data analysis system.
"""

import asyncio
import logging
import signal
import sys
from pathlib import Path
from typing import Optional

from config import config
from data_monitor import DataMonitor
from analysis_engine import AnalysisEngine
from report_generator import ReportGenerator
from ci_cd_manager import CICDManager

logger = logging.getLogger(__name__)

class DataAnalysisPipeline:
    """Main pipeline orchestrator."""
    
    def __init__(self):
        self.config = config
        self.monitor: Optional[DataMonitor] = None
        self.analysis_engine: Optional[AnalysisEngine] = None
        self.report_generator: Optional[ReportGenerator] = None
        self.cicd_manager: Optional[CICDManager] = None
        self.running = False
        
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
    
    async def stop(self) -> None:
        """Stop the pipeline gracefully."""
        logger.info("Stopping data analysis pipeline...")
        self.running = False
        
        if self.monitor:
            await self.monitor.stop()
        
        logger.info("Pipeline stopped successfully")
    
    def handle_signal(self, signum, frame):
        """Handle shutdown signals."""
        logger.info(f"Received signal {signum}, shutting down...")
        self.running = False

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

if __name__ == "__main__":
    asyncio.run(main())