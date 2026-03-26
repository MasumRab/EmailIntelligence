#!/usr/bin/env python3
"""
Automated Fix Suggestions
Provide automatic corrections for common documentation issues.
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class IssueType(Enum):
    BROKEN_LINK = "broken_link"
    FORMATTING = "formatting"
    CONSISTENCY = "consistency"
    SPELLING = "spelling"
    GRAMMAR = "grammar"
    STRUCTURE = "structure"


class FixConfidence(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class FixSuggestion:
    issue_type: IssueType
    file_path: str
    line_number: Optional[int]
    original_text: str
    suggested_text: str
    confidence: FixConfidence
    description: str
    auto_apply: bool = False  # Whether the fix can be automatically applied
    suggestion_id: str = ""


class FixSuggestionEngine:
    def __init__(self):
        self.fix_patterns = self._load_fix_patterns()
        self.applied_fixes = []
        self.suggestion_log = []
        
    def _load_fix_patterns(self) -> Dict:
        """Load fix patterns and rules."""
        # In a real implementation, this would load from a configuration file
        return {
            'link_fixes': [
                {
                    'pattern': r'\[([^\]]+)\]\(([^)]+)\.md\)',
                    'replacement': r'[\1](\2)',
                    'description': 'Remove .md extension from markdown links',
                    'confidence': FixConfidence.HIGH,
                    'auto_apply': True
                }
            ],
            'formatting_fixes': [
                {
                    'pattern': r'(\s+)##(\s+)',
                    'replacement': r'\n## ',
                    'description': 'Fix heading spacing',
                    'confidence': FixConfidence.HIGH,
                    'auto_apply': True
                },
                {
                    'pattern': r'(\*\*[^*]+\*\*)(\*\*[^*]+\*\*)',
                    'replacement': r'\1 \2',
                    'description': 'Add space between bold text',
                    'confidence': FixConfidence.MEDIUM,
                    'auto_apply': False
                }
            ],
            'consistency_fixes': [
                {
                    'pattern': r'APIs',
                    'replacement': r'APIs',
                    'description': 'Ensure consistent API spelling',
                    'confidence': FixConfidence.HIGH,
                    'auto_apply': True
                }
            ]
        }
        
    def suggest_link_fixes(self, content: str, file_path: str) -> List[FixSuggestion]:
        """Suggest fixes for link-related issues."""
        suggestions = []
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Check for broken links
            link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
            links = re.findall(link_pattern, line)
            
            for text, url in links:
                suggestion = self._check_broken_link(url, file_path)
                if suggestion:
                    suggestion.line_number = i
                    suggestions.append(suggestion)
                    
            # Check for common link formatting issues
            for pattern_info in self.fix_patterns.get('link_fixes', []):
                matches = re.finditer(pattern_info['pattern'], line)
                for match in matches:
                    suggestion = FixSuggestion(
                        issue_type=IssueType.BROKEN_LINK,
                        file_path=file_path,
                        line_number=i,
                        original_text=match.group(0),
                        suggested_text=re.sub(pattern_info['pattern'], pattern_info['replacement'], match.group(0)),
                        confidence=FixConfidence[pattern_info['confidence'].upper()],
                        description=pattern_info['description'],
                        auto_apply=pattern_info['auto_apply'],
                        suggestion_id=f"link_{len(suggestions)}"
                    )
                    suggestions.append(suggestion)
                    
        return suggestions
        
    def _check_broken_link(self, url: str, file_path: str) -> Optional[FixSuggestion]:
        """Check if a link is broken and suggest fix."""
        # Check relative links
        if not url.startswith('http'):
            current_dir = Path(file_path).parent
            link_path = current_dir / url
            
            if not link_path.exists():
                # Try common fixes
                if url.endswith('.md'):
                    # Try without .md extension
                    alt_path = current_dir / url[:-3]
                    if alt_path.exists():
                        return FixSuggestion(
                            issue_type=IssueType.BROKEN_LINK,
                            file_path=file_path,
                            line_number=None,
                            original_text=url,
                            suggested_text=str(alt_path.relative_to(current_dir)),
                            confidence=FixConfidence.HIGH,
                            description="Remove .md extension to fix broken link",
                            auto_apply=True
                        )
                        
        return None
        
    def suggest_formatting_fixes(self, content: str, file_path: str) -> List[FixSuggestion]:
        """Suggest fixes for formatting issues."""
        suggestions = []
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Check for formatting issues
            for pattern_info in self.fix_patterns.get('formatting_fixes', []):
                matches = re.finditer(pattern_info['pattern'], line)
                for match in matches:
                    suggestion = FixSuggestion(
                        issue_type=IssueType.FORMATTING,
                        file_path=file_path,
                        line_number=i,
                        original_text=match.group(0),
                        suggested_text=re.sub(pattern_info['pattern'], pattern_info['replacement'], match.group(0)),
                        confidence=FixConfidence[pattern_info['confidence'].upper()],
                        description=pattern_info['description'],
                        auto_apply=pattern_info['auto_apply'],
                        suggestion_id=f"format_{len(suggestions)}"
                    )
                    suggestions.append(suggestion)
                    
        return suggestions
        
    def suggest_consistency_fixes(self, content: str, file_path: str) -> List[FixSuggestion]:
        """Suggest fixes for consistency issues."""
        suggestions = []
        
        # Check for consistency issues
        for pattern_info in self.fix_patterns.get('consistency_fixes', []):
            matches = re.finditer(pattern_info['pattern'], content)
            for match in matches:
                suggestion = FixSuggestion(
                    issue_type=IssueType.CONSISTENCY,
                    file_path=file_path,
                    line_number=None,
                    original_text=match.group(0),
                    suggested_text=re.sub(pattern_info['pattern'], pattern_info['replacement'], match.group(0)),
                    confidence=FixConfidence[pattern_info['confidence'].upper()],
                    description=pattern_info['description'],
                    auto_apply=pattern_info['auto_apply'],
                    suggestion_id=f"consistency_{len(suggestions)}"
                )
                suggestions.append(suggestion)
                
        return suggestions
        
    def suggest_spelling_fixes(self, content: str, file_path: str) -> List[FixSuggestion]:
        """Suggest fixes for spelling issues."""
        # This would integrate with a spell checker library
        # For now, we'll return an empty list
        return []
        
    def suggest_grammar_fixes(self, content: str, file_path: str) -> List[FixSuggestion]:
        """Suggest fixes for grammar issues."""
        # This would integrate with a grammar checker library
        # For now, we'll return an empty list
        return []
        
    def generate_fix_suggestions(self, file_path: Path) -> List[FixSuggestion]:
        """Generate all fix suggestions for a file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            return [FixSuggestion(
                issue_type=IssueType.FORMATTING,
                file_path=str(file_path),
                line_number=None,
                original_text="",
                suggested_text="",
                confidence=FixConfidence.LOW,
                description=f"Could not read file: {str(e)}"
            )]
            
        all_suggestions = []
        
        # Generate suggestions for different issue types
        all_suggestions.extend(self.suggest_link_fixes(content, str(file_path)))
        all_suggestions.extend(self.suggest_formatting_fixes(content, str(file_path)))
        all_suggestions.extend(self.suggest_consistency_fixes(content, str(file_path)))
        all_suggestions.extend(self.suggest_spelling_fixes(content, str(file_path)))
        all_suggestions.extend(self.suggest_grammar_fixes(content, str(file_path)))
        
        # Log suggestions
        self.suggestion_log.extend(all_suggestions)
        
        return all_suggestions
        
    def apply_fix_suggestion(self, file_path: Path, suggestion: FixSuggestion) -> bool:
        """Apply a fix suggestion to a file."""
        if not suggestion.auto_apply and suggestion.confidence != FixConfidence.HIGH:
            return False  # Don't auto-apply low confidence suggestions
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Apply the fix
            if suggestion.line_number:
                lines = content.split('\n')
                if 1 <= suggestion.line_number <= len(lines):
                    lines[suggestion.line_number - 1] = lines[suggestion.line_number - 1].replace(
                        suggestion.original_text, suggestion.suggested_text
                    )
                    new_content = '\n'.join(lines)
                else:
                    return False
            else:
                new_content = content.replace(suggestion.original_text, suggestion.suggested_text)
                
            # Write back to file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
                
            # Log applied fix
            self.applied_fixes.append({
                'file_path': str(file_path),
                'suggestion_id': suggestion.suggestion_id,
                'applied_at': __import__('time').time()
            })
            
            return True
            
        except Exception as e:
            print(f"Error applying fix to {file_path}: {e}")
            return False
            
    def apply_all_high_confidence_fixes(self, file_path: Path) -> int:
        """Apply all high confidence fixes to a file."""
        suggestions = self.generate_fix_suggestions(file_path)
        applied_count = 0
        
        for suggestion in suggestions:
            if suggestion.confidence == FixConfidence.HIGH and suggestion.auto_apply:
                if self.apply_fix_suggestion(file_path, suggestion):
                    applied_count += 1
                    
        return applied_count
        
    def get_suggestion_statistics(self) -> Dict:
        """Get statistics about fix suggestions."""
        total_suggestions = len(self.suggestion_log)
        applied_fixes = len(self.applied_fixes)
        
        # Group by issue type
        issue_types = {}
        for suggestion in self.suggestion_log:
            issue_type = suggestion.issue_type.value
            if issue_type not in issue_types:
                issue_types[issue_type] = 0
            issue_types[issue_type] += 1
            
        # Group by confidence
        confidence_levels = {}
        for suggestion in self.suggestion_log:
            confidence = suggestion.confidence.value
            if confidence not in confidence_levels:
                confidence_levels[confidence] = 0
            confidence_levels[confidence] += 1
            
        return {
            'total_suggestions': total_suggestions,
            'applied_fixes': applied_fixes,
            'success_rate': (applied_fixes / total_suggestions * 100) if total_suggestions > 0 else 0,
            'issue_types': issue_types,
            'confidence_levels': confidence_levels
        }
        
    def get_fix_accuracy(self) -> float:
        """Get the accuracy rate of applied fixes."""
        if not self.applied_fixes:
            return 0.0
            
        # In a real system, this would track whether applied fixes were later reverted
        # For now, we'll assume all applied fixes are correct
        return 100.0


def main():
    # Example usage
    print("Automated Fix Suggestions System")
    print("=" * 35)
    
    # Create fix suggestion engine
    engine = FixSuggestionEngine()
    
    print("Fix suggestion engine initialized")
    print("System ready to provide automatic corrections for common documentation issues")
    
    # Example of what the workflow would look like:
    print("\nExample workflow:")
    print("  1. Analyze documentation files for common issues")
    print("  2. Generate fix suggestions with confidence levels")
    print("  3. Automatically apply high-confidence fixes")
    print("  4. Present medium/low-confidence fixes for review")
    print("  5. Track fix accuracy and improve suggestions")


if __name__ == "__main__":
    main()