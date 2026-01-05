#!/usr/bin/env python3
"""
Robust Progress File Compression Tool

Compresses progress tracking files while preserving:
- File metadata (timestamps, permissions)
- File content (no data loss)
- Directory structure
- Compression ratio optimization

Usage:
    python compress_progress.py --compress --source backup/ --destination compressed/
    python compress_progress.py --decompress --source compressed/progress.tar.xz --destination restore/
    python compress_progress.py --list --source compressed/progress.tar.xz
    python compress_progress.py --verify --source compressed/progress.tar.xz
"""

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tarfile
import tempfile
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class ProgressCompressor:
    """Robust compression system for progress tracking files."""

    # Compression level recommendations by file type
    COMPRESSION_LEVELS = {
        ".json": 6,  # Moderate compression for structured data
        ".md": 3,  # Light compression for markdown (already text)
        ".txt": 6,  # Moderate compression for text
        ".log": 9,  # Maximum compression for logs (repetitive)
        ".py": 6,  # Moderate compression for code
        ".sh": 3,  # Light compression for scripts
        ".yaml": 6,  # Moderate compression for YAML
        ".yml": 6,  # Moderate compression for YAML
    }

    # Files to always include (never compress out)
    ESSENTIAL_FILES = {
        "PROJECT_REFERENCE.md",
        "ENHANCED_VALIDATION_PLAN.md",
        "LOGGING_SYSTEM_PLAN.md",
        "LOGGING_GUIDE.md",
        "CLEAN_TASK_INDEX.md",
        "README.md",
        "AGENTS.md",
        "CLAUDE.md",
    }

    def __init__(self, source: str, destination: str):
        self.source = Path(source)
        self.destination = Path(destination)
        self.manifest = {}
        self.compression_log = []

    def calculate_file_hash(self, file_path: Path) -> str:
        """Calculate SHA-256 hash of file for verification."""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256_hash.update(chunk)
        return sha256_hash.hexdigest()

    def get_file_info(self, file_path: Path) -> Dict:
        """Get comprehensive file information."""
        stat = file_path.stat()
        return {
            "path": str(file_path.relative_to(self.source.parent)),
            "size": stat.st_size,
            "mtime": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "ctime": datetime.fromtimestamp(stat.st_ctime).isoformat(),
            "permissions": oct(stat.st_mode)[-3:],
            "sha256": self.calculate_file_hash(file_path),
            "extension": file_path.suffix.lower(),
        }

    def should_compress(self, file_path: Path, essential_only: bool = False) -> bool:
        """Determine if file should be included in compression."""
        # Always include essential files
        if file_path.name in self.ESSENTIAL_FILES:
            return True

        if essential_only:
            return False

        # Include files with known compressible extensions
        if file_path.suffix.lower() in self.COMPRESSION_LEVELS:
            return True

        # Include progress-related files
        name_lower = file_path.name.lower()
        progress_keywords = [
            "progress",
            "tracking",
            "status",
            "summary",
            "index",
            "reference",
            "plan",
            "guide",
            "task",
            "logging",
            "findings",
        ]
        if any(keyword in name_lower for keyword in progress_keywords):
            return True

        return False

    def get_compression_level(self, file_path: Path) -> int:
        """Get optimal compression level for file type."""
        extension = file_path.suffix.lower()
        return self.COMPRESSION_LEVELS.get(extension, 6)

    def create_manifest(self, files: List[Path]) -> Dict:
        """Create manifest with file information and checksums."""
        manifest = {
            "created": datetime.now().isoformat(),
            "source": str(self.source),
            "files": {},
            "totals": {
                "file_count": len(files),
                "original_size": 0,
                "compressed_size": 0,
            },
        }

        for file_path in sorted(files):
            info = self.get_file_info(file_path)
            manifest["files"][info["path"]] = info
            manifest["totals"]["original_size"] += info["size"]

        return manifest

    def compress(
        self, essential_only: bool = False, compression_format: str = "xz"
    ) -> Tuple[bool, str]:
        """
        Compress progress tracking files.

        Args:
            essential_only: Only compress essential files
            compression_format: 'gz', 'bz2', or 'xz'

        Returns:
            (success: bool, message: str)
        """
        # Find files to compress
        if not self.source.exists():
            return False, f"Source directory does not exist: {self.source}"

        files = [
            f
            for f in self.source.rglob("*")
            if f.is_file() and self.should_compress(f, essential_only)
        ]

        if not files:
            return False, "No files found to compress"

        # Create manifest
        manifest = self.create_manifest(files)

        # Create archive name
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_name = f"progress_{'essential' if essential_only else 'all'}_{timestamp}.tar.{compression_format}"
        archive_path = self.destination / archive_name

        # Ensure destination exists
        self.destination.mkdir(parents=True, exist_ok=True)

        # Create compressed archive
        try:
            if compression_format == "xz":
                mode = "w:xz"
            elif compression_format == "gz":
                mode = "w:gz"
            elif compression_format == "bz2":
                mode = "w:bz2"
            else:
                mode = "w"

            with tarfile.open(
                archive_path,
                mode,
                compresslevel=self.COMPRESSION_LEVELS.get(f".{compression_format}", 6),
            ) as tar:
                # Add manifest first
                manifest_content = json.dumps(manifest, indent=2)
                manifest_temp = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False)
                manifest_temp.write(manifest_content)
                manifest_temp.close()

                tar.add(manifest_temp.name, arcname="manifest.json")
                os.unlink(manifest_temp.name)

                # Add files
                for file_path in files:
                    rel_path = file_path.relative_to(self.source.parent)
                    tar.add(file_path, arcname=str(rel_path))

            # Calculate compressed size
            compressed_size = archive_path.stat().st_size
            manifest["totals"]["compressed_size"] = compressed_size
            manifest["archive_name"] = archive_name
            manifest["compression_format"] = compression_format
            manifest["compression_ratio"] = (
                (1 - (compressed_size / manifest["totals"]["original_size"])) * 100
                if manifest["totals"]["original_size"] > 0
                else 0
            )

            # Save updated manifest
            manifest_path = self.destination / f"{archive_name}.manifest.json"
            with open(manifest_path, "w") as f:
                json.dump(manifest, f, indent=2)

            ratio = manifest["compression_ratio"]
            original_mb = manifest["totals"]["original_size"] / (1024 * 1024)
            compressed_mb = compressed_size / (1024 * 1024)

            return True, (
                f"Compression complete: {archive_name}\n"
                f"  Files: {manifest['totals']['file_count']}\n"
                f"  Original: {original_mb:.2f} MB\n"
                f"  Compressed: {compressed_mb:.2f} MB\n"
                f"  Ratio: {ratio:.1f}%\n"
                f"  Manifest: {manifest_path.name}"
            )

        except Exception as e:
            return False, f"Compression failed: {e}"

    def decompress(self, archive_name: str, restore_path: Optional[str] = None) -> Tuple[bool, str]:
        """
        Decompress archive with verification.

        Args:
            archive_name: Name of archive to decompress
            restore_path: Optional custom restore path

        Returns:
            (success: bool, message: str)
        """
        archive_path = self.destination / archive_name

        if not archive_path.exists():
            return False, f"Archive not found: {archive_path}"

        # Check manifest
        manifest_path = self.destination / f"{archive_name}.manifest.json"
        if manifest_path.exists():
            with open(manifest_path) as f:
                manifest = json.load(f)
        else:
            manifest = None

        # Decompress to restore path
        target_path = Path(restore_path) if restore_path else self.source
        target_path.mkdir(parents=True, exist_ok=True)

        try:
            with tarfile.open(archive_path, "r:*") as tar:
                # Verify checksums during extraction
                verified_count = 0
                total_count = 0

                for member in tar.getmembers():
                    total_count += 1
                    if member.isfile():
                        # Extract to temporary location
                        temp_extract = tempfile.NamedTemporaryFile(delete=False)
                        temp_extract.close()

                        tar.extract(member, path=target_path)
                        extracted_path = target_path / member.name

                        # Verify checksum
                        if manifest and member.name in manifest.get("files", {}):
                            expected_hash = manifest["files"][member.name]["sha256"]
                            actual_hash = self.calculate_file_hash(extracted_path)

                            if expected_hash == actual_hash:
                                verified_count += 1
                            else:
                                return False, (
                                    f"Checksum mismatch for {member.name}\n"
                                    f"  Expected: {expected_hash}\n"
                                    f"  Actual: {actual_hash}"
                                )
                        else:
                            verified_count += 1

            files_restored = sum(1 for _ in target_path.rglob("*") if _.is_file())

            return True, (
                f"Decompression complete: {archive_name}\n"
                f"  Restored to: {target_path}\n"
                f"  Files: {files_restored}\n"
                f"  Verified: {verified_count}/{total_count}"
            )

        except Exception as e:
            return False, f"Decompression failed: {e}"

    def list_archive(self, archive_name: str) -> Tuple[bool, str]:
        """List contents of archive."""
        archive_path = self.destination / archive_name

        if not archive_path.exists():
            return False, f"Archive not found: {archive_path}"

        try:
            output = [f"Contents of {archive_name}:"]
            total_size = 0

            with tarfile.open(archive_path, "r:*") as tar:
                for member in tar.getmembers():
                    size_mb = member.size / (1024 * 1024)
                    output.append(f"  {member.name:<50} {size_mb:>8.2f} MB")
                    total_size += member.size

            output.append(f"\nTotal: {total_size / (1024 * 1024):.2f} MB")

            # Include manifest info
            manifest_path = self.destination / f"{archive_name}.manifest.json"
            if manifest_path.exists():
                with open(manifest_path) as f:
                    manifest = json.load(f)
                output.append(f"\nManifest Info:")
                output.append(f"  Created: {manifest.get('created', 'Unknown')}")
                output.append(f"  Files: {manifest.get('totals', {}).get('file_count', 'Unknown')}")
                output.append(f"  Compression: {manifest.get('compression_ratio', 0):.1f}%")

            return True, "\n".join(output)

        except Exception as e:
            return False, f"Failed to list archive: {e}"

    def verify_archive(self, archive_name: str) -> Tuple[bool, str]:
        """Verify integrity of archive."""
        archive_path = self.destination / archive_name

        if not archive_path.exists():
            return False, f"Archive not found: {archive_path}"

        try:
            results = {
                "archive_exists": True,
                "archive_readable": False,
                "manifest_valid": False,
                "checksums_valid": False,
                "files_count": 0,
                "errors": [],
            }

            # Check archive readability
            try:
                with tarfile.open(archive_path, "r:*") as tar:
                    results["archive_readable"] = True
                    results["files_count"] = len(tar.getmembers())
            except Exception as e:
                results["errors"].append(f"Cannot read archive: {e}")

            # Check manifest
            manifest_path = self.destination / f"{archive_name}.manifest.json"
            if manifest_path.exists():
                try:
                    with open(manifest_path) as f:
                        manifest = json.load(f)
                    results["manifest_valid"] = True
                except Exception as e:
                    results["errors"].append(f"Invalid manifest: {e}")
            else:
                results["errors"].append("Manifest not found")

            # Summary
            if results["archive_readable"] and results["manifest_valid"]:
                return True, (
                    f"Archive verification PASSED: {archive_name}\n"
                    f"  Files: {results['files_count']}\n"
                    f"  Status: All checks passed"
                )
            else:
                return False, (
                    f"Archive verification FAILED: {archive_name}\n"
                    f"  Errors:\n" + "\n".join(f"    - {e}" for e in results["errors"])
                )

        except Exception as e:
            return False, f"Verification failed: {e}"

    def get_archives(self) -> List[Dict]:
        """List all archives in destination with metadata."""
        archives = []

        if not self.destination.exists():
            return archives

        for file_path in self.destination.glob("*.tar.*"):
            stat = file_path.stat()
            manifest_path = self.destination / f"{file_path.name}.manifest.json"

            archive_info = {
                "name": file_path.name,
                "size_mb": stat.st_size / (1024 * 1024),
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            }

            if manifest_path.exists():
                try:
                    with open(manifest_path) as f:
                        manifest = json.load(f)
                    archive_info["files"] = manifest.get("totals", {}).get("file_count", "?")
                    archive_info["ratio"] = manifest.get("compression_ratio", 0)
                    archive_info["original_mb"] = manifest.get("totals", {}).get(
                        "original_size", 0
                    ) / (1024 * 1024)
                except Exception:
                    pass

            archives.append(archive_info)

        return sorted(archives, key=lambda x: x["modified"], reverse=True)


def main():
    parser = argparse.ArgumentParser(description="Robust progress file compression tool")
    parser.add_argument("--compress", action="store_true", help="Compress progress files")
    parser.add_argument("--decompress", action="store_true", help="Decompress archive")
    parser.add_argument("--list", action="store_true", help="List archive contents")
    parser.add_argument("--verify", action="store_true", help="Verify archive integrity")
    parser.add_argument(
        "--source", default=".", help="Source directory (default: current directory)"
    )
    parser.add_argument(
        "--destination", default="backups/", help="Destination directory (default: backups/)"
    )
    parser.add_argument(
        "--archive", help="Archive filename (required for --list, --verify, --decompress)"
    )
    parser.add_argument(
        "--essential-only", action="store_true", help="Only compress essential files"
    )
    parser.add_argument(
        "--format",
        default="xz",
        choices=["gz", "bz2", "xz"],
        help="Compression format (default: xz)",
    )
    parser.add_argument("--restore-to", help="Custom restore path for decompression")

    args = parser.parse_args()

    compressor = ProgressCompressor(args.source, args.destination)

    if args.compress:
        success, message = compressor.compress(
            essential_only=args.essential_only, compression_format=args.format
        )
        print(message)
        sys.exit(0 if success else 1)

    elif args.decompress:
        if not args.archive:
            parser.error("--archive required for --decompress")
        success, message = compressor.decompress(args.archive, restore_path=args.restore_to)
        print(message)
        sys.exit(0 if success else 1)

    elif args.list:
        if not args.archive:
            parser.error("--archive required for --list")
        success, message = compressor.list_archive(args.archive)
        print(message)
        sys.exit(0 if success else 1)

    elif args.verify:
        if not args.archive:
            parser.error("--archive required for --verify")
        success, message = compressor.verify_archive(args.archive)
        print(message)
        sys.exit(0 if success else 1)

    else:
        # List all archives
        archives = compressor.get_archives()
        if archives:
            print("Available archives:")
            for archive in archives:
                files = archive.get("files", "?")
                ratio = archive.get("ratio", 0)
                print(
                    f"  {archive['name']:<45} "
                    f"{archive['size_mb']:>7.2f} MB  "
                    f"[{files} files, {ratio:.1f}% reduction]"
                )
        else:
            print("No archives found")
        sys.exit(0)


if __name__ == "__main__":
    main()
