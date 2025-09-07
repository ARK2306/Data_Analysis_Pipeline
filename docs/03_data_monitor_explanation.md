# data_monitor.py - Complete Line-by-Line Code Explanation

## Overview
The `data_monitor.py` file implements real-time file system monitoring using the watchdog library. It detects when data files are created or modified and triggers the analysis pipeline automatically.

## Detailed Code Breakdown

### Imports and Dependencies

```python
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
```

**Lines 1-12:**
- **Lines 1-3:** Module docstring explaining the file's purpose
- **Line 5:** `asyncio` for asynchronous operations
- **Line 6:** `logging` for structured logging
- **Line 7:** `os` for operating system interactions
- **Line 8:** `pathlib.Path` for modern path handling
- **Line 9:** Type hints for callback functions and sets
- **Lines 10-11:** Watchdog library components for file system monitoring
- **Line 13:** Import global configuration

```python
logger = logging.getLogger(__name__)
```

**Line 15:** Create module-specific logger for tracking file monitoring events

---

## DataFileHandler Class

### Handler Initialization

```python
class DataFileHandler(FileSystemEventHandler):
    """Handler for data file system events."""
    
    def __init__(self, callback: Callable[[str], Awaitable[None]]):
        super().__init__()
        self.callback = callback
        self.supported_extensions = config.supported_file_types
        self.processing_files: Set[str] = set()
```

**Lines 17-24:**
- **Line 17:** Inherit from watchdog's FileSystemEventHandler
- **Line 20:** Constructor takes an async callback function
- **Line 21:** Call parent constructor
- **Line 22:** Store callback for processing file changes
- **Line 23:** Get supported file types from configuration
- **Line 24:** Track files currently being processed to prevent duplicates

### File Type Validation

```python
def _is_supported_file(self, file_path: str) -> bool:
    """Check if file type is supported for analysis."""
    return any(file_path.lower().endswith(ext) for ext in self.supported_extensions)
```

**Lines 26-28:**
- **Line 27:** Check if file extension matches supported types
- **Line 28:** Use `any()` with generator expression for efficient checking
- Case-insensitive comparison using `lower()`

### File Processing Logic

```python
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
```

**Lines 30-48:**
- **Lines 31-32:** First check if file type is supported
- **Lines 35-41:** Calculate and check file size limits:
  - Convert bytes to megabytes
  - Compare against configured maximum
  - Log warning if file is too large
- **Lines 42-43:** Handle file access errors (permissions, file not found)
- **Lines 45-46:** Prevent duplicate processing of same file
- **Line 48:** Return True if all checks pass

### Event Handler Methods

#### File Modification Handler

```python
def on_modified(self, event):
    """Handle file modification events."""
    if not isinstance(event, FileModifiedEvent) or event.is_directory:
        return
    
    self._handle_file_change(event.src_path, "modified")
```

**Lines 50-55:**
- **Line 52:** Check if event is file modification (not directory)
- **Line 53:** Exit early if it's a directory event
- **Line 55:** Forward to common file change handler

#### File Creation Handler

```python
def on_created(self, event):
    """Handle file creation events."""
    if not isinstance(event, FileCreatedEvent) or event.is_directory:
        return
    
    self._handle_file_change(event.src_path, "created")
```

**Lines 57-62:**
- Similar to modification handler but for file creation events
- Ensures both new files and modified files trigger analysis

#### Common File Change Handler

```python
def _handle_file_change(self, file_path: str, event_type: str):
    """Handle file change events."""
    if not self._should_process_file(file_path):
        return
    
    logger.info(f"Data file {event_type}: {file_path}")
    
    # Add to processing set to prevent duplicate processing
    self.processing_files.add(file_path)
    
    # Schedule async callback
    asyncio.create_task(self._process_file_async(file_path))
```

**Lines 64-75:**
- **Line 66:** Validate file should be processed
- **Line 69:** Log the file change event
- **Line 72:** Add to processing set (prevents duplicates)
- **Line 75:** Schedule asynchronous processing task

#### Asynchronous File Processing

```python
async def _process_file_async(self, file_path: str):
    """Process file changes asynchronously."""
    try:
        await self.callback(file_path)
    except Exception as e:
        logger.error(f"Error processing file {file_path}: {e}")
    finally:
        # Remove from processing set when done
        self.processing_files.discard(file_path)
```

**Lines 77-85:**
- **Line 80:** Execute the callback function (analysis pipeline)
- **Lines 81-82:** Log any processing errors
- **Lines 83-85:** Always remove file from processing set (cleanup)

---

## DataMonitor Class

### Monitor Initialization

```python
class DataMonitor:
    """Main data monitoring class."""
    
    def __init__(self, watch_directory: str, callback: Callable[[str], Awaitable[None]]):
        self.watch_directory = Path(watch_directory)
        self.callback = callback
        self.observer: Observer = None
        self.handler: DataFileHandler = None
        self.running = False
```

**Lines 87-95:**
- **Line 90:** Constructor takes directory path and callback
- **Line 91:** Convert directory to Path object
- **Line 92:** Store callback function
- **Lines 93-94:** Initialize observer and handler as None
- **Line 95:** Track running state

### Monitor Start Method

```python
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
```

**Lines 97-128:**
- **Line 101:** Create watch directory if it doesn't exist
- **Line 103:** Log monitoring start
- **Line 106:** Create file event handler
- **Lines 108-113:** Configure watchdog observer:
  - Schedule handler for directory
  - Set recursive monitoring (subdirectories too)
- **Lines 115-117:** Start observer and set running flag
- **Lines 119-120:** Log success and configuration
- **Line 123:** Process any existing files in directory
- **Lines 125-128:** Error handling with re-raising

### Monitor Stop Method

```python
async def stop(self) -> None:
    """Stop monitoring."""
    if self.observer and self.running:
        logger.info("Stopping data monitor...")
        self.observer.stop()
        self.observer.join()
        self.running = False
        logger.info("Data monitor stopped")
```

**Lines 130-137:**
- **Line 131:** Check if observer exists and is running
- **Line 133:** Stop the observer
- **Line 134:** Wait for observer thread to finish
- **Line 135:** Set running flag to False
- **Line 136:** Log successful stop

### Existing Files Processing

```python
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
```

**Lines 139-156:**
- **Line 142:** Log scanning start
- **Lines 145-149:** Recursively find all files in directory:
  - Use `rglob('*')` for recursive file search
  - Check if it's a file and should be processed
  - Process with delay to prevent overwhelming
- **Lines 151-154:** Log processing results
- **Lines 155-156:** Error handling

### Delayed File Processing

```python
async def _process_file_with_delay(self, file_path: str):
    """Process file with a small delay to avoid overwhelming the system."""
    try:
        await asyncio.sleep(0.1)  # Small delay between file processing
        await self.callback(file_path)
    except Exception as e:
        logger.error(f"Error processing existing file {file_path}: {e}")
```

**Lines 158-164:**
- **Line 161:** Small delay to prevent system overload
- **Line 162:** Execute callback (analysis pipeline)
- **Lines 163-164:** Error handling with logging

### Status Information

```python
def get_status(self) -> dict:
    """Get monitor status information."""
    return {
        'running': self.running,
        'watch_directory': str(self.watch_directory),
        'supported_file_types': config.supported_file_types,
        'max_file_size_mb': config.analysis_config['max_file_size_mb'],
        'processing_files_count': len(self.handler.processing_files) if self.handler else 0
    }
```

**Lines 166-174:**
- Returns dictionary with current monitor status
- Includes running state, configuration, and active processing count
- Useful for debugging and monitoring

---

## ManualTrigger Class

### Manual Trigger for Testing

```python
class ManualTrigger:
    """Manual trigger for testing and one-off analysis."""
    
    def __init__(self, callback: Callable[[str], Awaitable[None]]):
        self.callback = callback
```

**Lines 176-180:**
- **Line 177:** Utility class for manual file processing
- **Line 179:** Store callback function

### Manual Analysis Trigger

```python
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
```

**Lines 182-201:**
- **Lines 185-187:** Check if file exists
- **Lines 189-193:** Validate file can be processed
- **Lines 195-197:** Execute callback and return success
- **Lines 198-201:** Error handling

---

## Key Design Patterns

### 1. **Observer Pattern**
- FileSystemEventHandler observes file system changes
- Callbacks notify interested parties of changes
- Loose coupling between monitoring and processing

### 2. **Async/Await Pattern**
- Non-blocking file processing
- Concurrent handling of multiple file changes
- Prevents UI/system freezing during analysis

### 3. **Strategy Pattern**
- Different handlers for different event types
- Configurable file filtering strategies
- Easy to extend with new file types

### 4. **State Management**
- Tracks processing files to prevent duplicates
- Maintains running state for clean shutdown
- Status reporting for monitoring

### 5. **Error Handling**
- Try-catch blocks at every level
- Graceful degradation when files can't be processed
- Detailed logging for debugging

## Monitoring Philosophy

### Real-time Processing
- Immediate response to file changes
- No polling - event-driven architecture
- Minimal system resource usage

### Reliability
- Duplicate processing prevention
- File size limits prevent memory issues
- Graceful error handling

### Flexibility
- Configurable file types and size limits
- Recursive directory monitoring
- Manual trigger capability for testing

### Performance
- Asynchronous processing prevents blocking
- Delayed processing prevents system overload
- Efficient file type checking

This monitoring system provides a robust foundation for real-time data analysis by efficiently detecting file changes while preventing common issues like duplicate processing and system overload.