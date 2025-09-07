"""
Data file monitoring system using watchdog for real-time file change detection.
"""

import asyncio
import logging
import os
from pathlib import Path
from typing import Callable, Awaitable, Set
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent, FileCreatedEvent

from config import config

logger = logging.getLogger(__name__)

class DataFileHandler(FileSystemEventHandler):
    """Handler for data file system events."""
    
    def __init__(self, callback: Callable[[str], Awaitable[None]]):
        super().__init__()
        self.callback = callback
        self.supported_extensions = config.supported_file_types
        self.processing_files: Set[str] = set()
        
    def _is_supported_file(self, file_path: str) -> bool:
        """Check if file type is supported for analysis."""
        return any(file_path.lower().endswith(ext) for ext in self.supported_extensions)
    
    def _should_process_file(self, file_path: str) -> bool:
        """Determine if file should be processed."""
        if not self._is_supported_file(file_path):
            return False
        
        # Check file size
        try:
            file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
            max_size = config.analysis_config['max_file_size_mb']
            if file_size_mb > max_size:
                logger.warning(f"File {file_path} too large ({file_size_mb:.1f}MB > {max_size}MB)")
                return False
        except OSError:
            return False
        
        # Avoid processing the same file multiple times
        if file_path in self.processing_files:
            return False
        
        return True
    
    def on_modified(self, event):
        """Handle file modification events."""
        if not isinstance(event, FileModifiedEvent) or event.is_directory:
            return
        
        self._handle_file_change(event.src_path, "modified")
    
    def on_created(self, event):
        """Handle file creation events."""
        if not isinstance(event, FileCreatedEvent) or event.is_directory:
            return
        
        self._handle_file_change(event.src_path, "created")
    
    def _handle_file_change(self, file_path: str, event_type: str):
        """Handle file change events."""
        if not self._should_process_file(file_path):
            return
        
        logger.info(f"Data file {event_type}: {file_path}")
        
        # Add to processing set to prevent duplicate processing
        self.processing_files.add(file_path)
        
        # Schedule async callback
        asyncio.create_task(self._process_file_async(file_path))
    
    async def _process_file_async(self, file_path: str):
        """Process file changes asynchronously."""
        try:
            await self.callback(file_path)
        except Exception as e:
            logger.error(f"Error processing file {file_path}: {e}")
        finally:
            # Remove from processing set when done
            self.processing_files.discard(file_path)

class DataMonitor:
    """Main data monitoring class."""
    
    def __init__(self, watch_directory: str, callback: Callable[[str], Awaitable[None]]):
        self.watch_directory = Path(watch_directory)
        self.callback = callback
        self.observer: Observer = None
        self.handler: DataFileHandler = None
        self.running = False
        
    async def start(self) -> None:
        """Start monitoring the data directory."""
        try:
            # Ensure watch directory exists
            self.watch_directory.mkdir(parents=True, exist_ok=True)
            
            logger.info(f"Starting data monitor on: {self.watch_directory}")
            
            # Create event handler
            self.handler = DataFileHandler(self.callback)
            
            # Set up observer
            self.observer = Observer()
            self.observer.schedule(
                self.handler, 
                str(self.watch_directory), 
                recursive=True
            )
            
            # Start observer
            self.observer.start()
            self.running = True
            
            logger.info(f"Data monitor started successfully")
            logger.info(f"Monitoring file types: {config.supported_file_types}")
            
            # Process existing files
            await self._process_existing_files()
            
        except Exception as e:
            logger.error(f"Failed to start data monitor: {e}")
            raise
    
    async def stop(self) -> None:
        """Stop monitoring."""
        if self.observer and self.running:
            logger.info("Stopping data monitor...")
            self.observer.stop()
            self.observer.join()
            self.running = False
            logger.info("Data monitor stopped")
    
    async def _process_existing_files(self) -> None:
        """Process any existing data files in the directory."""
        try:
            logger.info("Scanning for existing data files...")
            processed_count = 0
            
            for file_path in self.watch_directory.rglob('*'):
                if file_path.is_file() and self.handler._should_process_file(str(file_path)):
                    logger.info(f"Processing existing file: {file_path}")
                    await self._process_file_with_delay(str(file_path))
                    processed_count += 1
            
            if processed_count > 0:
                logger.info(f"Processed {processed_count} existing files")
            else:
                logger.info("No existing data files found")
                
        except Exception as e:
            logger.error(f"Error processing existing files: {e}")
    
    async def _process_file_with_delay(self, file_path: str):
        """Process file with a small delay to avoid overwhelming the system."""
        try:
            await asyncio.sleep(0.1)  # Small delay between file processing
            await self.callback(file_path)
        except Exception as e:
            logger.error(f"Error processing existing file {file_path}: {e}")
    
    def get_status(self) -> dict:
        """Get monitor status information."""
        return {
            'running': self.running,
            'watch_directory': str(self.watch_directory),
            'supported_file_types': config.supported_file_types,
            'max_file_size_mb': config.analysis_config['max_file_size_mb'],
            'processing_files_count': len(self.handler.processing_files) if self.handler else 0
        }

class ManualTrigger:
    """Manual trigger for testing and one-off analysis."""
    
    def __init__(self, callback: Callable[[str], Awaitable[None]]):
        self.callback = callback
    
    async def trigger_analysis(self, file_path: str) -> bool:
        """Manually trigger analysis for a specific file."""
        try:
            if not os.path.exists(file_path):
                logger.error(f"File does not exist: {file_path}")
                return False
            
            # Check if file type is supported
            handler = DataFileHandler(self.callback)
            if not handler._should_process_file(file_path):
                logger.error(f"File type not supported or file too large: {file_path}")
                return False
            
            logger.info(f"Manually triggering analysis for: {file_path}")
            await self.callback(file_path)
            return True
            
        except Exception as e:
            logger.error(f"Manual trigger failed for {file_path}: {e}")
            return False