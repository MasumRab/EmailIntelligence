#!/usr/bin/env python3
"""
Task Content Extractor - Canonical Implementation
Extracts and normalizes task content for duplication analysis
"""

import re
import logging
import json
from pathlib import Path
from typing import Dict, Optional, Tuple
import chardet

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TaskContentExtractor:
    """Canonical task content extraction with comprehensive error handling"""

    def __init__(self, root_dir: str):
        self.root_dir = Path(root_dir)
        self.stats = {
            'files_processed': 0,
            'extraction_errors': 0,
            'encoding_issues': 0,
            'empty_files': 0
        }

    def detect_encoding(self, file_path: Path) -> str:
        """Detect file encoding for robust reading"""
        try:
            with open(file_path, 'rb') as f:
                raw_data = f.read()
                result = chardet.detect(raw_data)
                return result['encoding'] or 'utf-8'
        except Exception as e:
            logger.warning(f"Encoding detection failed for {file_path}: {e}")
            return 'utf-8'

    def read_file_safely(self, file_path: Path) -> Optional[str]:
        """Read file with encoding detection and error handling"""
        try:
            encoding = self.detect_encoding(file_path)
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()

            if not content.strip():
                self.stats['empty_files'] += 1
                logger.warning(f"Empty file: {file_path}")
                return None

            self.stats['files_processed'] += 1
            return content

        except UnicodeDecodeError as e:
            self.stats['encoding_issues'] += 1
            logger.error(f"Encoding error for {file_path}: {e}")
            return None
        except Exception as e:
            self.stats['extraction_errors'] += 1
            logger.error(f"Failed to read {file_path}: {e}")
            return None

    def extract_frontmatter(self, content: str) -> Tuple[str, Dict]:
        """Extract YAML frontmatter and return content without it"""
        frontmatter = {}

        # Match YAML frontmatter (--- to ---)
        frontmatter_match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)

        if frontmatter_match:
            try:
                # Simple YAML parsing (could be enhanced with pyyaml)
                frontmatter_text = frontmatter_match.group(1)
                content = frontmatter_match.group(2)

                # Extract key fields
                for line in frontmatter_text.split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        frontmatter[key.strip()] = value.strip().strip('\'"')

            except Exception as e:
                logger.warning(f"Frontmatter parsing error: {e}")

        return content, frontmatter

    def normalize_content(self, content: str) -> str:
        """Normalize content for consistent comparison"""
        # Remove markdown headers that are just titles
        content = re.sub(r'^#\s+Task:.*$', '', content, flags=re.MULTILINE)
        content = re.sub(r'^##\s+Priority.*$', '', content, flags=re.MULTILINE)
        content = re.sub(r'^##\s+Description.*$', '', content, flags=re.MULTILINE)

        # Remove common boilerplate
        content = re.sub(r'^##\s+Current Implementation.*$', '', content, flags=re.MULTILINE)
        content = re.sub(r'^##\s+Requirements.*$', '', content, flags=re.MULTILINE)
        content = re.sub(r'^##\s+Acceptance Criteria.*$', '', content, flags=re.MULTILINE)

        # Normalize whitespace
        content = re.sub(r'\s+', ' ', content)
        content = content.strip()

        # Remove extra whitespace around punctuation
        content = re.sub(r'\s*([.!?])\s*', r'\1 ', content)

        return content

    def extract_task_content(self, file_path: Path) -> Optional[Dict]:
        """Main extraction method returning structured data"""
        raw_content = self.read_file_safely(file_path)
        if not raw_content:
            return None

        try:
            # Extract frontmatter
            content, frontmatter = self.extract_frontmatter(raw_content)

            # Normalize content
            normalized_content = self.normalize_content(content)

            return {
                'file_path': str(file_path),
                'raw_content': raw_content,
                'normalized_content': normalized_content,
                'frontmatter': frontmatter,
                'content_length': len(normalized_content),
                'word_count': len(normalized_content.split())
            }

        except Exception as e:
            logger.error(f"Content extraction failed for {file_path}: {e}")
            return None

    def process_directory(self, directory: str) -> Dict[str, Dict]:
        """Process all task files in a directory"""
        task_dir = self.root_dir / directory
        if not task_dir.exists():
            logger.error(f"Directory not found: {task_dir}")
            return {}

        results = {}
        task_files = list(task_dir.rglob("task-*.md"))

        logger.info(f"Processing {len(task_files)} task files in {directory}")

        for file_path in task_files:
            result = self.extract_task_content(file_path)
            if result:
                results[str(file_path)] = result

        logger.info(f"Successfully processed {len(results)} files")
        return results

def main():
    """Command-line interface for testing"""
    import argparse

    parser = argparse.ArgumentParser(description='Extract task content for duplication analysis')
    parser.add_argument('--input-dir', required=True, help='Directory containing task files')
    parser.add_argument('--output', help='Output JSON file')

    args = parser.parse_args()

    extractor = TaskContentExtractor('/home/masum/github')
    results = extractor.process_directory(args.input_dir)

    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)

    print(f"Processed {len(results)} task files")
    print(f"Stats: {extractor.stats}")

if __name__ == "__main__":
    main()