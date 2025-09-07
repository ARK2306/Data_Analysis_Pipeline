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

logger = logging.getLogger(__name__)

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
    
    def get_repository_info(self) -> Dict[str, Any]:
        """Get repository information."""
        if not self.repo:
            return {}
        
        try:
            remotes = {}
            for remote in self.repo.remotes:
                remotes[remote.name] = list(remote.urls)
            
            return {
                'current_branch': self.get_current_branch(),
                'is_dirty': self.repo.is_dirty(),
                'untracked_files': len(self.repo.untracked_files),
                'total_commits': len(list(self.repo.iter_commits())),
                'remotes': remotes,
                'last_commit': {
                    'sha': self.repo.head.commit.hexsha,
                    'message': self.repo.head.commit.message.strip(),
                    'author': str(self.repo.head.commit.author),
                    'date': self.repo.head.commit.committed_datetime.isoformat()
                }
            }
        except Exception as e:
            logger.error(f"Failed to get repository info: {e}")
            return {}

class CICDManager:
    """Main CI/CD automation manager."""
    
    def __init__(self):
        self.config = config
        self.git_ops = GitOperations()
        self.pipeline_history: List[Dict[str, Any]] = []
    
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
    
    def _generate_pipeline_id(self) -> str:
        """Generate unique pipeline ID."""
        return f"pipeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
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
            
            step_record = {
                'step': 'commit_artifacts',
                'artifacts_count': len(artifacts_to_commit),
                'artifacts': artifacts_to_commit,
                'success': success,
                'duration_seconds': (datetime.now() - step_start).total_seconds(),
                'timestamp': step_start.isoformat()
            }
            pipeline_record['steps'].append(step_record)
            
            return success
            
        except Exception as e:
            logger.error(f"Error committing analysis artifacts: {e}")
            return False
    
    async def _create_analysis_summary(self, data_file_path: str, analysis_results: Dict[str, Any], 
                                     pipeline_record: Dict[str, Any]) -> Optional[str]:
        """Create a comprehensive analysis summary file."""
        try:
            file_name = Path(data_file_path).stem
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            summary_path = Path(self.config.output_directory) / 'pipeline_summaries' / f"{file_name}_pipeline_{timestamp}.md"
            summary_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Get file info and executive summary
            file_info = analysis_results.get('file_info', {})
            quality_data = analysis_results.get('data_quality', {})
            
            summary_content = f"""# Data Analysis Pipeline Summary

## File Information
- **File**: {file_info.get('file_name', 'Unknown')}
- **Path**: {data_file_path}
- **Size**: {file_info.get('file_size_mb', 0):.2f} MB
- **Rows**: {file_info.get('rows', 0):,}
- **Columns**: {file_info.get('columns', 0)}

## Pipeline Information
- **Pipeline ID**: {pipeline_record['pipeline_id']}
- **Branch**: {pipeline_record.get('branch_name', 'Unknown')}
- **Start Time**: {pipeline_record['start_time']}
- **Status**: {pipeline_record['status']}

## Data Quality Summary
"""
            
            if quality_data:
                missing_pct = quality_data.get('missing_values', {}).get('missing_percentage', 0)
                duplicate_count = quality_data.get('duplicate_rows', {}).get('count', 0)
                complete_pct = quality_data.get('data_completeness', {}).get('complete_percentage', 0)
                
                summary_content += f"""
- **Missing Values**: {missing_pct:.1f}%
- **Duplicate Rows**: {duplicate_count}
- **Complete Rows**: {complete_pct:.1f}%
"""
            
            # Add correlation findings
            corr_data = analysis_results.get('correlation_analysis', {})
            strong_corrs = corr_data.get('strong_correlations', [])
            if strong_corrs:
                summary_content += f"""
## Strong Correlations Found
Total strong correlations: {len(strong_corrs)}

"""
                for i, corr in enumerate(strong_corrs[:5]):  # Top 5
                    summary_content += f"{i+1}. **{corr['variable1']}** vs **{corr['variable2']}**: {corr['pearson_correlation']:.3f}\\n"
            
            # Add steps summary
            summary_content += f"""
## Pipeline Steps
"""
            for step in pipeline_record['steps']:
                status_icon = "✅" if step['success'] else "❌"
                summary_content += f"- {status_icon} **{step['step']}** ({step['duration_seconds']:.2f}s)\\n"
            
            summary_content += f"""
---
*Generated by Data Analysis Pipeline on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
            
            with open(summary_path, 'w', encoding='utf-8') as f:
                f.write(summary_content)
            
            logger.info(f"Created pipeline summary: {summary_path}")
            return str(summary_path)
            
        except Exception as e:
            logger.error(f"Failed to create analysis summary: {e}")
            return None
    
    async def _push_analysis_branch(self, pipeline_record: Dict[str, Any]) -> bool:
        """Push the analysis branch to remote repository."""
        try:
            step_start = datetime.now()
            
            branch_name = pipeline_record.get('branch_name')
            if not branch_name:
                return False
            
            success = self.git_ops.push_branch(
                branch_name=branch_name,
                remote_name=self.config.git_config['remote_name']
            )
            
            step_record = {
                'step': 'push_branch',
                'branch_name': branch_name,
                'remote': self.config.git_config['remote_name'],
                'success': success,
                'duration_seconds': (datetime.now() - step_start).total_seconds(),
                'timestamp': step_start.isoformat()
            }
            pipeline_record['steps'].append(step_record)
            
            return success
            
        except Exception as e:
            logger.error(f"Error pushing analysis branch: {e}")
            return False
    
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
            
            step_record = {
                'step': 'create_pull_request',
                'success': success,
                'pr_url': pr_url if success else None,
                'duration_seconds': (datetime.now() - step_start).total_seconds(),
                'timestamp': step_start.isoformat()
            }
            pipeline_record['steps'].append(step_record)
            
            return success
            
        except Exception as e:
            logger.error(f"Error creating pull request: {e}")
            return False
    
    async def _generate_pipeline_summary(self, pipeline_record: Dict[str, Any]) -> None:
        """Generate a comprehensive pipeline summary."""
        try:
            summary_dir = Path(self.config.output_directory) / 'pipeline_logs'
            summary_dir.mkdir(parents=True, exist_ok=True)
            
            summary_file = summary_dir / f"{pipeline_record['pipeline_id']}_summary.json"
            
            with open(summary_file, 'w', encoding='utf-8') as f:
                json.dump(pipeline_record, f, indent=2, default=str)
            
            logger.info(f"Generated pipeline summary: {summary_file}")
            
        except Exception as e:
            logger.error(f"Failed to generate pipeline summary: {e}")
    
    async def _complete_pipeline(self, pipeline_record: Dict[str, Any], success: bool, message: str) -> bool:
        """Complete the pipeline and update records."""
        try:
            end_time = datetime.now()
            start_time = datetime.fromisoformat(pipeline_record['start_time'])
            duration = (end_time - start_time).total_seconds()
            
            pipeline_record.update({
                'status': 'completed' if success else 'failed',
                'end_time': end_time.isoformat(),
                'duration_seconds': duration,
                'completion_message': message
            })
            
            # Add to pipeline history
            self.pipeline_history.append(pipeline_record)
            
            # Keep only last 50 pipeline records
            self.pipeline_history = self.pipeline_history[-50:]
            
            status_msg = "completed successfully" if success else "failed"
            logger.info(f"Pipeline {pipeline_record['pipeline_id']} {status_msg} in {duration:.2f}s: {message}")
            
            return success
            
        except Exception as e:
            logger.error(f"Error completing pipeline: {e}")
            return False
    
    def get_pipeline_status(self) -> Dict[str, Any]:
        """Get current pipeline status and history."""
        return {
            'total_pipelines': len(self.pipeline_history),
            'recent_pipelines': self.pipeline_history[-10:],  # Last 10 pipelines
            'git_info': self.git_ops.get_repository_info(),
            'config': {
                'branch_name': self.config.git_config['branch_name'],
                'commit_prefix': self.config.git_config['commit_prefix'],
                'remote_name': self.config.git_config['remote_name']
            }
        }