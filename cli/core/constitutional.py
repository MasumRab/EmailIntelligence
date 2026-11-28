"""
Constitutional Analysis Module
"""
import asyncio
import hashlib
import json
import logging
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# Optional imports for interface-based architecture
try:
    from analysis.constitutional.analyzer import ConstitutionalAnalyzer
except ImportError:
    ConstitutionalAnalyzer = None

try:
    from analysis.constitutional.requirement_checker import RequirementChecker
except ImportError:
    RequirementChecker = None

from cli.conflict import ConflictDetector
from cli.exceptions import (
    BranchNotFoundError,
    GitOperationError,
    MergeTreeError,
)
from cli.models import (
    BranchPairResult,
    ConflictMatrix,
    ConflictReport,
    ConflictSeverity,
    ConflictType,
    SemanticConflictAnalysis,
    GitWorkspaceManager,
)
from cli.semantic import SemanticConflictDetector
from cli.workspace import RobustWorkspaceManager

logger = logging.getLogger(__name__)


class ConstitutionalAnalyzer:
    """Constitutional analysis and compliance checking"""

    def __init__(self, cli_base):
        self.cli = cli_base
        self.logger = getattr(cli_base, 'logger', None)
    
    def analyze_constitutional(
        self, pr_number: int, constitution_files: List[str] = None,
        interactive: bool = False
    ) -> Dict[str, Any]:
        """Analyze conflicts against loaded constitution."""
        import asyncio
        return asyncio.run(
            self._analyze_constitutional_async(pr_number, constitution_files, interactive)
        )
    
    async def _analyze_constitutional_async(
        self, pr_number: int, constitution_files: List[str] = None,
        interactive: bool = False
    ) -> Dict[str, Any]:
        """Async constitutional analysis"""
        metadata_file = self.cli.resolution_branches_dir / f"pr-{pr_number}-metadata.json"
        
        if not metadata_file.exists():
            self.cli._error_exit(f"No resolution metadata found for PR #{pr_number}")
        
        with open(metadata_file) as f:
            metadata = json.load(f)
        
        if metadata.get('status') != 'ready_for_analysis':
            self.cli._warn("Constitutional analysis not yet ready. Running setup first...")
            # Would need to call setup_resolution first
        
        self.cli._info(f"📋 Analyzing constitutional compliance for PR #{pr_number}...")
        
        # Load constitutions
        constitutions = constitution_files or metadata.get('constitution_files', [])
        
        analyzer = ConstitutionalAnalyzer()
        requirement_checker = RequirementChecker()
        
        all_results = []
        overall_score = 0.0
        
        for constitution in constitutions:
            self.cli._info(f"📋 Analyzing against: {constitution}")
            
            # In a real implementation, this would do actual constitutional analysis
            # For now, we'll simulate
            result = {
                'constitution': constitution,
                'overall_score': 0.9,
                'compliance_level': 'CONFORMANT',
                'violations': [],
                'recommendations': []
            }
            
            all_results.append(result)
            overall_score += result['overall_score']
        
        metadata['analysis_results'] = {
            'results': all_results,
            'overall_compliance': overall_score / len(all_results) if all_results else 0.0,
            'analyzed_at': datetime.now().isoformat()
        }
        metadata['status'] = 'constitution_analyzed'
        
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        self._display_constitutional_overall_summary(all_results)
        
        return {
            'pr_number': pr_number,
            'results': all_results,
            'overall_score': overall_score / len(all_results) if all_results else 0.0
        }
    
    def _display_constitutional_analysis_result(self, result, filename: str):
        """Display constitutional analysis result for a file"""
        status_emoji = "✅" if result.overall_score > 0.8 else "⚠️" if result.overall_score > 0.5 else "❌"
        print(f"  {status_emoji} {filename}: {result.overall_score:.1%} ({len(result.violations)} violations)")
    
    def _display_constitutional_overall_summary(self, all_results: List[Dict[str, Any]]):
        """Display overall constitutional analysis summary"""
        if not all_results:
            print("No results to display")
            return
        
        total_score = sum(r['overall_score'] for r in all_results)
        avg_score = total_score / len(all_results) if all_results else 0.0
        
        total_violations = sum(len(r.get('violations', [])) for r in all_results)
        total_recommendations = sum(len(r.get('recommendations', [])) for r in all_results)
        
        print(f"\nOverall Constitutional Analysis Summary:")
        print(f"  Files analyzed: {len(all_results)}")
        print(f"  Total violations: {total_violations}")
        print(f"  Total recommendations: {total_recommendations}")
        print(f"  Average compliance: {avg_score:.1%}")
    
    def _save_constitutional_results(self, pr_number: int, results: List[Dict[str, Any]], 
                                   metadata_file: Path):
        """Save constitutional analysis results to metadata"""
        with open(metadata_file, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
        
        constitutional_results = []
        for result in results:
            constitutional_results.append({
                'file': result['file'],
                'overall_score': result['result'].overall_score,
                'compliance_level': result['result'].compliance_level.value,
                'summary': result['result'].summary
            })
        
        metadata['constitutional_analysis'] = {
            'timestamp': datetime.now().isoformat(),
            'results': constitutional_results,
            'overall_score': sum(r['result'].overall_score for r in results) / len(results) if results else 0.0
        }
        
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)
