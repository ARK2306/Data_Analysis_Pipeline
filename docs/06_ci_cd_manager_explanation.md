# ci_cd_manager.py - Complete Line-by-Line Code Explanation

## Overview
The `ci_cd_manager.py` file handles Git automation and CI/CD pipeline management. It creates branches, commits analysis results, pushes changes, and optionally creates pull requests for automated workflows.

## Detailed Code Breakdown

### Imports and Dependencies

```python
"""
CI/CD automation manager for Git operations and pipeline management.
Handles automated commits, branch creation, and pull request management.
"""

import asyncio
import json
import logging
import os
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
import git
from git import Repo, InvalidGitRepositoryError

from config import config
```

**Lines 1-16:**
- **Lines 1-4:** Module docstring explaining Git automation capabilities
- **Line 6:** `asyncio` for asynchronous operations
- **Line 7:** `json` for JSON data handling
- **Line 8:** `logging` for structured logging
- **Line 9:** `os` for operating system operations
- **Line 10:** `subprocess` for running external commands (GitHub CLI)
- **Line 11:** `datetime` for timestamps
- **Line 12:** `pathlib.Path` for file operations
- **Line 13:** Type hints for better code documentation
- **Line 14:** `git` library for Python Git operations
- **Line 15:** Git repository classes and exceptions
- **Line 17:** Import global configuration

---

## GitOperations Class

### Git Repository Initialization

```python
class GitOperations:
    """Git operations wrapper with error handling."""
    
    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path).resolve()
        self.repo: Optional[Repo] = None
        self._initialize_repo()
    
    def _initialize_repo(self) -> bool:
        """Initialize or connect to existing Git repository."""
        try:
            self.repo = Repo(self.repo_path)
            logger.info(f"Connected to Git repository: {self.repo_path}")
            return True
        except InvalidGitRepositoryError:
            logger.warning(f"Not a Git repository: {self.repo_path}")
            try:
                self.repo = Repo.init(self.repo_path)
                logger.info(f"Initialized new Git repository: {self.repo_path}")
                return True
            except Exception as e:
                logger.error(f"Failed to initialize Git repository: {e}")
                return False
        except Exception as e:
            logger.error(f"Git repository error: {e}")
            return False
```

**Lines 21-44:**
- **Line 24:** Store resolved repository path
- **Line 25:** Initialize repository reference as None
- **Line 26:** Call initialization helper method
- **Lines 28-44:** Repository initialization logic:
  - Try to connect to existing repository
  - If not a Git repo, initialize new one
  - Handle all possible Git errors gracefully

### Repository State Methods

```python
def is_repo_clean(self) -> bool:
    """Check if repository has uncommitted changes."""
    if not self.repo:
        return False
    return not self.repo.is_dirty() and len(self.repo.untracked_files) == 0

def get_current_branch(self) -> str:
    """Get current branch name."""
    if not self.repo:
        return "unknown"
    return self.repo.active_branch.name
```

**Lines 46-55:**
- **Lines 46-49:** Check for uncommitted changes or untracked files
- **Lines 51-55:** Get current branch name safely

### Branch Management

```python
def create_branch(self, branch_name: str, checkout: bool = True) -> bool:
    """Create a new branch."""
    try:
        if not self.repo:
            return False
        
        # Check if branch already exists
        existing_branches = [branch.name for branch in self.repo.branches]
        if branch_name in existing_branches:
            if checkout:
                self.repo.git.checkout(branch_name)
            logger.info(f"Checked out existing branch: {branch_name}")
            return True
        
        # Create new branch
        new_branch = self.repo.create_head(branch_name)
        if checkout:
            new_branch.checkout()
        
        logger.info(f"Created and checked out branch: {branch_name}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to create branch {branch_name}: {e}")
        return False
```

**Lines 57-81:**
- **Lines 62-67:** Check if branch already exists and checkout if requested
- **Lines 69-73:** Create new branch and optionally checkout
- **Lines 75-81:** Error handling with logging

### File Staging and Commits

```python
def add_files(self, file_patterns: List[str] = None) -> bool:
    """Add files to staging area."""
    try:
        if not self.repo:
            return False
        
        if file_patterns is None:
            file_patterns = ['.']
        
        for pattern in file_patterns:
            self.repo.git.add(pattern)
        
        logger.info(f"Added files to staging: {file_patterns}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to add files: {e}")
        return False

def commit_changes(self, message: str, author_name: str = None, author_email: str = None) -> bool:
    """Commit staged changes."""
    try:
        if not self.repo:
            return False
        
        # Check if there are changes to commit
        if not self.repo.is_dirty() and len(self.repo.untracked_files) == 0:
            logger.info("No changes to commit")
            return True
        
        # Configure commit author if provided
        if author_name and author_email:
            with self.repo.config_writer() as git_config:
                git_config.set_value("user", "name", author_name)
                git_config.set_value("user", "email", author_email)
        
        # Commit changes
        self.repo.git.add('-A')  # Add all changes including deletions
        commit = self.repo.index.commit(message)
        
        logger.info(f"Committed changes: {commit.hexsha[:8]} - {message}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to commit changes: {e}")
        return False
```

**Lines 83-120:**
- **Lines 83-98:** File staging with pattern support (default: all files)
- **Lines 100-120:** Commit creation with optional author configuration:
  - Check for changes before committing
  - Configure Git author if provided
  - Add all changes and create commit
  - Log commit SHA and message

### Remote Operations

```python
def push_branch(self, branch_name: str = None, remote_name: str = "origin") -> bool:
    """Push branch to remote repository."""
    try:
        if not self.repo:
            return False
        
        if branch_name is None:
            branch_name = self.get_current_branch()
        
        # Check if remote exists
        if remote_name not in [remote.name for remote in self.repo.remotes]:
            logger.warning(f"Remote '{remote_name}' not found")
            return False
        
        # Push branch
        origin = self.repo.remote(remote_name)
        push_info = origin.push(f"{branch_name}:{branch_name}")
        
        logger.info(f"Pushed branch {branch_name} to {remote_name}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to push branch {branch_name}: {e}")
        return False
```

**Lines 122-144:**
- **Lines 126-127:** Use current branch if none specified
- **Lines 129-132:** Validate remote exists
- **Lines 134-137:** Push branch to remote
- **Lines 139-144:** Error handling

---

## CICDManager Class

### CI/CD Manager Initialization

```python
class CICDManager:
    """Main CI/CD automation manager."""
    
    def __init__(self):
        self.config = config
        self.git_ops = GitOperations()
        self.pipeline_history: List[Dict[str, Any]] = []
```

**Lines 167-173:**
- **Line 170:** Store configuration reference
- **Line 171:** Create Git operations instance
- **Line 172:** Initialize pipeline history tracking

### Main Pipeline Handler

```python
async def handle_analysis_complete(self, data_file_path: str, report_path: str, analysis_results: Dict[str, Any]) -> bool:
    """Handle completion of data analysis and trigger CI/CD pipeline."""
    try:
        logger.info(f"Starting CI/CD pipeline for analysis of: {data_file_path}")
        
        pipeline_id = self._generate_pipeline_id()
        pipeline_start_time = datetime.now()
        
        # Create pipeline record
        pipeline_record = {
            'pipeline_id': pipeline_id,
            'data_file': data_file_path,
            'report_path': report_path,
            'start_time': pipeline_start_time.isoformat(),
            'status': 'running',
            'steps': []
        }
        
        # Step 1: Create analysis branch
        branch_created = await self._create_analysis_branch(data_file_path, pipeline_record)
        if not branch_created:
            return await self._complete_pipeline(pipeline_record, False, "Failed to create analysis branch")
        
        # Step 2: Generate and commit analysis artifacts
        artifacts_committed = await self._commit_analysis_artifacts(
            data_file_path, report_path, analysis_results, pipeline_record
        )
        if not artifacts_committed:
            return await self._complete_pipeline(pipeline_record, False, "Failed to commit analysis artifacts")
        
        # Step 3: Push changes to remote
        pushed = await self._push_analysis_branch(pipeline_record)
        if not pushed:
            return await self._complete_pipeline(pipeline_record, False, "Failed to push analysis branch")
        
        # Step 4: Create pull request (if GitHub CLI is available)
        pr_created = await self._create_pull_request(data_file_path, analysis_results, pipeline_record)
        
        # Step 5: Generate pipeline summary
        await self._generate_pipeline_summary(pipeline_record)
        
        return await self._complete_pipeline(pipeline_record, True, "Pipeline completed successfully")
        
    except Exception as e:
        logger.error(f"CI/CD pipeline failed: {e}")
        return False
```

**Lines 175-215:**
- **Lines 178-186:** Initialize pipeline tracking record
- **Lines 188-215:** Execute pipeline steps sequentially:
  1. Create analysis branch
  2. Commit analysis artifacts
  3. Push to remote
  4. Create pull request (optional)
  5. Generate summary
- Each step includes error handling and early termination

### Branch Creation Step

```python
async def _create_analysis_branch(self, data_file_path: str, pipeline_record: Dict[str, Any]) -> bool:
    """Create a new branch for the analysis."""
    try:
        step_start = datetime.now()
        
        file_name = Path(data_file_path).stem
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        branch_name = f"{self.config.git_config['branch_name']}-{file_name}-{timestamp}"
        
        success = self.git_ops.create_branch(branch_name, checkout=True)
        
        step_record = {
            'step': 'create_branch',
            'branch_name': branch_name,
            'success': success,
            'duration_seconds': (datetime.now() - step_start).total_seconds(),
            'timestamp': step_start.isoformat()
        }
        pipeline_record['steps'].append(step_record)
        
        if success:
            pipeline_record['branch_name'] = branch_name
            logger.info(f"Created analysis branch: {branch_name}")
        else:
            logger.error(f"Failed to create analysis branch: {branch_name}")
        
        return success
        
    except Exception as e:
        logger.error(f"Error creating analysis branch: {e}")
        return False
```

**Lines 221-248:**
- **Line 224:** Generate unique branch name with timestamp
- **Line 226:** Create and checkout branch
- **Lines 228-234:** Record step metrics (duration, timestamp, success)
- **Lines 236-242:** Update pipeline record and log result

### Artifact Commitment Step

```python
async def _commit_analysis_artifacts(self, data_file_path: str, report_path: str, 
                                   analysis_results: Dict[str, Any], pipeline_record: Dict[str, Any]) -> bool:
    """Commit all analysis artifacts to the repository."""
    try:
        step_start = datetime.now()
        
        # Collect all artifacts to commit
        artifacts_to_commit = []
        
        # Add report files
        if report_path and os.path.exists(report_path):
            artifacts_to_commit.append(report_path)
            
            # Add related files (JSON, summary, visualizations)
            report_dir = Path(report_path).parent
            report_stem = Path(report_path).stem.replace('_report_', '_')
            
            for pattern in ['*.json', '*.txt']:
                related_files = list(report_dir.glob(f"{report_stem}*"))
                artifacts_to_commit.extend([str(f) for f in related_files if f.exists()])
        
        # Add visualization files
        viz_results = analysis_results.get('visualizations', {})
        if 'generated_files' in viz_results:
            for viz_file in viz_results['generated_files']:
                if os.path.exists(viz_file):
                    artifacts_to_commit.append(viz_file)
        
        # Create analysis summary
        summary_file = await self._create_analysis_summary(data_file_path, analysis_results, pipeline_record)
        if summary_file:
            artifacts_to_commit.append(summary_file)
        
        # Add files to git
        if artifacts_to_commit:
            success = self.git_ops.add_files(artifacts_to_commit)
            if success:
                # Create commit message
                file_name = Path(data_file_path).name
                commit_message = f"{self.config.git_config['commit_prefix']} Analysis results for {file_name}\\n\\nGenerated by automated data analysis pipeline"
                
                success = self.git_ops.commit_changes(
                    message=commit_message,
                    author_name="Data Analysis Pipeline",
                    author_email="pipeline@analysis.local"
                )
        else:
            logger.warning("No artifacts found to commit")
            success = True
```

**Lines 250-291:**
- **Lines 256-268:** Collect all analysis artifacts:
  - Main report file
  - Related JSON and summary files
  - Visualization files
- **Lines 270-274:** Add visualization files from analysis results
- **Lines 276-278:** Create pipeline summary document
- **Lines 280-291:** Commit all artifacts with descriptive message

### Pull Request Creation

```python
async def _create_pull_request(self, data_file_path: str, analysis_results: Dict[str, Any], 
                             pipeline_record: Dict[str, Any]) -> bool:
    """Create a pull request using GitHub CLI if available."""
    try:
        step_start = datetime.now()
        
        # Check if GitHub CLI is available
        try:
            result = subprocess.run(['gh', '--version'], capture_output=True, text=True, timeout=5)
            if result.returncode != 0:
                logger.info("GitHub CLI not available, skipping PR creation")
                return True
        except (subprocess.TimeoutExpired, FileNotFoundError):
            logger.info("GitHub CLI not available, skipping PR creation")
            return True
        
        # Create PR title and body
        file_name = Path(data_file_path).name
        branch_name = pipeline_record.get('branch_name', 'analysis-branch')
        
        pr_title = f"Analysis results for {file_name}"
        
        # Create PR body with analysis summary
        file_info = analysis_results.get('file_info', {})
        quality_data = analysis_results.get('data_quality', {})
        
        pr_body = f"""## Automated Data Analysis Results

### Dataset Overview
- **File**: {file_name}
- **Rows**: {file_info.get('rows', 0):,}
- **Columns**: {file_info.get('columns', 0)}
- **Size**: {file_info.get('file_size_mb', 0):.2f} MB

### Data Quality
- **Missing Values**: {quality_data.get('missing_values', {}).get('missing_percentage', 0):.1f}%
- **Duplicate Rows**: {quality_data.get('duplicate_rows', {}).get('count', 0)}

### Analysis Artifacts Included
"""
        
        # List artifacts
        for step in pipeline_record['steps']:
            if step['step'] == 'commit_artifacts' and 'artifacts' in step:
                pr_body += "\\n".join([f"- `{Path(artifact).name}`" for artifact in step['artifacts'][:10]])
                break
        
        pr_body += f"""

### Pipeline Information
- **Pipeline ID**: {pipeline_record['pipeline_id']}
- **Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---
*This PR was created automatically by the Data Analysis Pipeline*
"""
        
        # Create PR using GitHub CLI
        cmd = [
            'gh', 'pr', 'create',
            '--title', pr_title,
            '--body', pr_body,
            '--head', branch_name,
            '--draft'  # Create as draft initially
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        success = result.returncode == 0
        
        if success:
            pr_url = result.stdout.strip()
            logger.info(f"Created pull request: {pr_url}")
            pipeline_record['pull_request_url'] = pr_url
        else:
            logger.warning(f"Failed to create PR: {result.stderr}")
```

**Lines 362-426:**
- **Lines 367-374:** Check GitHub CLI availability
- **Lines 376-398:** Create PR title and comprehensive description:
  - Dataset overview with metrics
  - Data quality summary
  - List of included artifacts
- **Lines 409-422:** Execute GitHub CLI command to create draft PR
- **Lines 424-430:** Handle PR creation result

---

## Key Design Patterns and Principles

### 1. **Pipeline Pattern**
- Sequential execution of CI/CD steps
- Each step validates before proceeding
- Comprehensive error handling at each stage

### 2. **State Management**
- Detailed tracking of pipeline execution
- Step-by-step recording with metrics
- Pipeline history for monitoring

### 3. **Error Resilience**
- Graceful handling of missing Git repository
- GitHub CLI availability checking
- Fallback options when tools unavailable

### 4. **Automation Philosophy**
- Minimal manual intervention required
- Self-contained pipeline execution
- Comprehensive logging for debugging

### 5. **Version Control Integration**
- Proper Git workflow with branches
- Meaningful commit messages
- Professional PR descriptions

This CI/CD manager provides robust automation for integrating analysis results into version control workflows while maintaining flexibility and error resilience.