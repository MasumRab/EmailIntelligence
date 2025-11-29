"""
Speckit Command Factory

Implements the command factory pattern to create speckit commands
that can be integrated with the existing launcher system.
"""

import argparse
from typing import Optional, Dict, Any
from pathlib import Path
import sys

# Add project root to sys.path for imports
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from src.speckit import speckit_analyse, speckit_checkist


class SpeckitCommand:
    """Base class for speckit commands"""
    
    def __init__(self, args: argparse.Namespace):
        self.args = args
    
    def execute(self) -> int:
        """Execute the command and return exit code"""
        raise NotImplementedError("Subclasses must implement execute method")
    
    def cleanup(self):
        """Perform any necessary cleanup"""
        pass


class SpeckitAnalyseCommand(SpeckitCommand):
    """Speckit Analyse Command Implementation"""
    
    def execute(self) -> int:
        """Execute the speckit analyse command"""
        try:
            # Prepare arguments for speckit_analyse
            user_feedback = getattr(self.args, 'feedback', None)
            analysis_type = getattr(self.args, 'analysis_type', 'comprehensive')
            output_format = getattr(self.args, 'output_format', 'json')
            
            # Execute the analyse function
            result = speckit_analyse(
                user_feedback=user_feedback,
                analysis_type=analysis_type,
                output_format=output_format
            )
            
            # Output the result
            if output_format == 'json':
                import json
                print(json.dumps(result, indent=2))
            elif output_format == 'markdown':
                print(result.get('markdown_output', ''))
            else:
                print(result.get('text_output', str(result)))
                
            return 0
        except Exception as e:
            print(f"Error executing speckit.analyse: {e}", file=sys.stderr)
            return 1


class SpeckitCheckistCommand(SpeckitCommand):
    """Speckit Checklist Command Implementation"""
    
    def execute(self) -> int:
        """Execute the speckit checkist command"""
        try:
            # Prepare arguments for speckit_checkist
            user_feedback = getattr(self.args, 'feedback', None)
            checklist_type = getattr(self.args, 'checklist_type', 'development')
            output_format = getattr(self.args, 'output_format', 'json')
            
            # Execute the checkist function
            result = speckit_checkist(
                user_feedback=user_feedback,
                checklist_type=checklist_type,
                output_format=output_format
            )
            
            # Output the result
            if output_format == 'json':
                import json
                print(json.dumps(result, indent=2))
            elif output_format == 'markdown':
                print(result.get('markdown_output', ''))
            else:
                print(result.get('text_output', str(result)))
                
            return 0
        except Exception as e:
            print(f"Error executing speckit.checkist: {e}", file=sys.stderr)
            return 1


class SpeckitCommandFactory:
    """Factory for creating speckit commands"""
    
    @staticmethod
    def create_command(command_name: str, args: argparse.Namespace) -> Optional[SpeckitCommand]:
        """
        Create a speckit command based on the command name.
        
        Args:
            command_name: Name of the command to create
            args: Arguments for the command
            
        Returns:
            Created command instance or None if command name is not recognized
        """
        command_map = {
            'speckit.analyse': SpeckitAnalyseCommand,
            'speckit.checkist': SpeckitCheckistCommand,
            'analyse': SpeckitAnalyseCommand,
            'checkist': SpeckitCheckistCommand,
        }
        
        command_class = command_map.get(command_name)
        if command_class:
            return command_class(args)
        else:
            return None


def get_command_factory():
    """Get the speckit command factory instance"""
    return SpeckitCommandFactory()


def add_speckit_arguments(parser: argparse.ArgumentParser):
    """Add speckit-specific arguments to the argument parser."""
    # Create a subparser for speckit commands
    speckit_parser = parser.add_subparsers(dest='speckit_command', help='Speckit commands')
    
    # Analyse command
    analyse_parser = speckit_parser.add_parser('analyse', help='Analyse user feedback and codebase')
    analyse_parser.add_argument('--feedback', type=str, help='User feedback to analyse')
    analyse_parser.add_argument('--type', dest='analysis_type', choices=['comprehensive', 'feedback', 'codebase'], 
                               default='comprehensive', help='Type of analysis to perform')
    analyse_parser.add_argument('--format', dest='output_format', choices=['json', 'text', 'markdown'], 
                               default='json', help='Output format')
    
    # Checkist command  
    checkist_parser = speckit_parser.add_parser('checkist', help='Generate checklists based on feedback')
    checkist_parser.add_argument('--feedback', type=str, help='User feedback to generate checklist from')
    checkist_parser.add_argument('--type', dest='checklist_type', choices=['development', 'review', 'deployment', 'feedback'], 
                                default='development', help='Type of checklist to generate')
    checkist_parser.add_argument('--format', dest='output_format', choices=['json', 'text', 'markdown'], 
                               default='json', help='Output format')
    
    return speckit_parser