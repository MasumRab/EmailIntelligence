#!/usr/bin/env python3
"""
Distributed Translation Pipelines
Implement parallel translation workflows for multi-language docs.
"""

import time
import json
import threading
from pathlib import Path
from typing import Dict, List, Optional, Any, Set, Tuple
from dataclasses import dataclass, field
from collections import defaultdict
import uuid
import hashlib


@dataclass
class TranslationUnit:
    unit_id: str
    source_text: str
    source_language: str
    target_language: str
    translated_text: str = ""
    status: str = "pending"  # "pending", "in_progress", "completed", "failed"
    assigned_agent: str = ""
    translation_time: float = 0.0
    quality_score: float = 0.0  # 0.0 to 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TranslationMemoryEntry:
    source_text: str
    target_text: str
    source_language: str
    target_language: str
    confidence_score: float
    usage_count: int = 1
    last_used: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TranslationJob:
    job_id: str
    document_id: str
    source_language: str
    target_languages: List[str]
    status: str = "pending"  # "pending", "in_progress", "completed", "failed"
    start_time: float = 0.0
    end_time: float = 0.0
    translation_units: List[TranslationUnit] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TranslationQualityReport:
    job_id: str
    target_language: str
    total_units: int
    translated_units: int
    failed_units: int
    average_quality_score: float
    consistency_score: float
    terminology_accuracy: float
    metadata: Dict[str, Any] = field(default_factory=dict)


class DistributedTranslationManager:
    def __init__(self, translation_file: Path = None):
        self.translation_file = translation_file or Path(".distributed_translations.json")
        self.translation_jobs: Dict[str, TranslationJob] = {}
        self.translation_memory: Dict[str, TranslationMemoryEntry] = {}
        self.agent_assignments: Dict[str, List[str]] = defaultdict(list)  # agent_id -> job_ids
        self.language_pairs: Dict[str, List[str]] = defaultdict(list)  # source_lang -> target_langs
        self.agent_capabilities: Dict[str, List[Tuple[str, str]]] = defaultdict(list)  # agent_id -> [(source, target)]
        self._lock = threading.RLock()
        self.load_translations()

    def register_agent_capability(self, agent_id: str, source_lang: str, target_lang: str):
        """Register an agent's translation capability."""
        with self._lock:
            self.agent_capabilities[agent_id].append((source_lang, target_lang))
            if target_lang not in self.language_pairs[source_lang]:
                self.language_pairs[source_lang].append(target_lang)

    def create_translation_job(self, document_id: str, source_language: str,
                             target_languages=None, target_language=None, source_segments=None, metadata: Dict[str, Any] = None) -> str:
        """Create a new translation job (flexible signature)."""
        if target_language and not target_languages:
            target_languages = [target_language]
        if not isinstance(target_languages, list):
            target_languages = [target_languages]
        job_id = self.start_translation_job(document_id, source_language, target_languages, metadata)
        if source_segments:
            self.add_translation_units(job_id, source_segments)
        return job_id

    def get_translation_memory_stats(self) -> Dict[str, Any]:
        """Get translation memory statistics."""
        with self._lock:
            return {
                'total_entries': len(self.translation_memory),
                'language_pairs': dict(self.language_pairs)
            }

    def start_translation_job(self, document_id: str, source_language: str,
                            target_languages: List[str], metadata: Dict[str, Any] = None) -> str:
        """Start a new translation job."""
        if metadata is None:
            metadata = {}

        job_id = str(uuid.uuid4())

        with self._lock:
            job = TranslationJob(
                job_id=job_id,
                document_id=document_id,
                source_language=source_language,
                target_languages=target_languages,
                status="pending",
                start_time=time.time(),
                metadata=metadata
            )

            self.translation_jobs[job_id] = job

            # Update language pairs
            for target_lang in target_languages:
                if target_lang not in self.language_pairs[source_language]:
                    self.language_pairs[source_language].append(target_lang)

            self._save_translations()

            return job_id

    def get_translation_job(self, job_id: str) -> Optional[TranslationJob]:
        """Get a translation job by ID."""
        with self._lock:
            return self.translation_jobs.get(job_id)

    def add_translation_units(self, job_id: str, source_texts: List[str]) -> List[str]:
        """Add translation units to a job."""
        unit_ids = []

        with self._lock:
            job = self.translation_jobs.get(job_id)
            if not job:
                return unit_ids

            # Create translation units for each target language
            for source_text in source_texts:
                for target_lang in job.target_languages:
                    unit_id = str(uuid.uuid4())
                    unit = TranslationUnit(
                        unit_id=unit_id,
                        source_text=source_text,
                        source_language=job.source_language,
                        target_language=target_lang
                    )
                    job.translation_units.append(unit)
                    unit_ids.append(unit_id)

            self._save_translations()

            return unit_ids

    def start_job_processing(self, job_id: str) -> bool:
        """Mark a translation job as in progress."""
        with self._lock:
            job = self.translation_jobs.get(job_id)
            if not job:
                return False

            job.status = "in_progress"
            job.start_time = time.time()
            self._save_translations()
            return True

    def complete_job(self, job_id: str) -> bool:
        """Mark a translation job as completed."""
        with self._lock:
            job = self.translation_jobs.get(job_id)
            if not job:
                return False

            job.status = "completed"
            job.end_time = time.time()
            self._save_translations()
            return True

    def assign_unit_to_agent(self, unit_id: str, agent_id: str) -> bool:
        """Assign a translation unit to an agent."""
        with self._lock:
            # Find the unit across all jobs
            unit = None
            job = None

            for j in self.translation_jobs.values():
                for u in j.translation_units:
                    if u.unit_id == unit_id:
                        unit = u
                        job = j
                        break
                if unit:
                    break

            if not unit or not job:
                return False

            unit.status = "in_progress"
            unit.assigned_agent = agent_id

            # Update agent assignments
            if job.job_id not in self.agent_assignments[agent_id]:
                self.agent_assignments[agent_id].append(job.job_id)

            self._save_translations()
            return True

    def complete_translation_unit(self, unit_id: str, translated_text: str,
                                quality_score: float = 0.8) -> bool:
        """Mark a translation unit as completed."""
        with self._lock:
            # Find the unit across all jobs
            unit = None
            for job in self.translation_jobs.values():
                for u in job.translation_units:
                    if u.unit_id == unit_id:
                        unit = u
                        break
                if unit:
                    break

            if not unit:
                return False

            unit.translated_text = translated_text
            unit.status = "completed"
            unit.translation_time = time.time() - unit.translation_time if unit.translation_time > 0 else 0
            unit.quality_score = quality_score

            # Add to translation memory
            self._add_to_translation_memory(
                unit.source_text, translated_text,
                unit.source_language, unit.target_language,
                quality_score
            )

            self._save_translations()
            return True

    def fail_translation_unit(self, unit_id: str, error_message: str = "") -> bool:
        """Mark a translation unit as failed."""
        with self._lock:
            # Find the unit across all jobs
            unit = None
            for job in self.translation_jobs.values():
                for u in job.translation_units:
                    if u.unit_id == unit_id:
                        unit = u
                        break
                if unit:
                    break

            if not unit:
                return False

            unit.status = "failed"
            unit.metadata['error_message'] = error_message
            self._save_translations()
            return True

    def _add_to_translation_memory(self, source_text: str, target_text: str,
                                 source_lang: str, target_lang: str, confidence_score: float):
        """Add a translation to the translation memory."""
        # Create a key for the translation memory entry
        key = hashlib.md5(f"{source_text}_{source_lang}_{target_lang}".encode()).hexdigest()

        if key in self.translation_memory:
            # Update existing entry
            entry = self.translation_memory[key]
            # Weighted average of confidence scores
            new_confidence = (entry.confidence_score * entry.usage_count + confidence_score) / (entry.usage_count + 1)
            entry.confidence_score = new_confidence
            entry.usage_count += 1
            entry.last_used = time.time()
        else:
            # Create new entry
            entry = TranslationMemoryEntry(
                source_text=source_text,
                target_text=target_text,
                source_language=source_lang,
                target_language=target_lang,
                confidence_score=confidence_score,
                usage_count=1,
                last_used=time.time()
            )
            self.translation_memory[key] = entry

    def lookup_translation_memory(self, source_text: str, source_lang: str,
                                target_lang: str) -> Optional[TranslationMemoryEntry]:
        """Look up a translation in the translation memory."""
        key = hashlib.md5(f"{source_text}_{source_lang}_{target_lang}".encode()).hexdigest()

        with self._lock:
            return self.translation_memory.get(key)

    def get_job_progress(self, job_id: str) -> Dict[str, Any]:
        """Get progress information for a translation job."""
        with self._lock:
            job = self.translation_jobs.get(job_id)
            if not job:
                return {}

            total_units = len(job.translation_units)
            completed_units = len([u for u in job.translation_units if u.status == "completed"])
            failed_units = len([u for u in job.translation_units if u.status == "failed"])
            in_progress_units = len([u for u in job.translation_units if u.status == "in_progress"])
            pending_units = len([u for u in job.translation_units if u.status == "pending"])

            # Calculate progress by language
            language_progress = {}
            for target_lang in job.target_languages:
                lang_units = [u for u in job.translation_units if u.target_language == target_lang]
                total_lang = len(lang_units)
                completed_lang = len([u for u in lang_units if u.status == "completed"])
                progress_percent = (completed_lang / total_lang * 100) if total_lang > 0 else 0
                language_progress[target_lang] = {
                    'total_units': total_lang,
                    'completed_units': completed_lang,
                    'progress_percentage': progress_percent
                }

            return {
                'job_id': job_id,
                'status': job.status,
                'total_units': total_units,
                'completed_units': completed_units,
                'failed_units': failed_units,
                'in_progress_units': in_progress_units,
                'pending_units': pending_units,
                'progress_percentage': (completed_units / total_units * 100) if total_units > 0 else 0,
                'language_progress': language_progress,
                'duration_seconds': time.time() - job.start_time if job.start_time > 0 else 0
            }

    def get_agent_assignments(self, agent_id: str) -> List[TranslationJob]:
        """Get all translation jobs assigned to an agent."""
        with self._lock:
            job_ids = self.agent_assignments.get(agent_id, [])
            return [self.translation_jobs[jid] for jid in job_ids if jid in self.translation_jobs]

    def get_language_pairs(self, source_language: str) -> List[str]:
        """Get supported target languages for a source language."""
        with self._lock:
            return self.language_pairs.get(source_language, [])

    def get_jobs_for_document(self, document_id: str) -> List[TranslationJob]:
        """Get all translation jobs for a document."""
        with self._lock:
            return [job for job in self.translation_jobs.values() if job.document_id == document_id]

    def get_translation_quality_report(self, job_id: str, target_language: str) -> TranslationQualityReport:
        """Generate a quality report for a translation job and language."""
        with self._lock:
            job = self.translation_jobs.get(job_id)
            if not job:
                return TranslationQualityReport(job_id, target_language, 0, 0, 0, 0.0, 0.0, 0.0)

            # Get units for the specific language
            lang_units = [u for u in job.translation_units if u.target_language == target_language]

            total_units = len(lang_units)
            translated_units = len([u for u in lang_units if u.status == "completed"])
            failed_units = len([u for u in lang_units if u.status == "failed"])

            if total_units == 0:
                return TranslationQualityReport(job_id, target_language, 0, 0, 0, 0.0, 0.0, 0.0)

            # Calculate average quality score
            completed_units = [u for u in lang_units if u.status == "completed"]
            if completed_units:
                avg_quality = sum(u.quality_score for u in completed_units) / len(completed_units)
            else:
                avg_quality = 0.0

            # Calculate consistency score (simplified)
            consistency_score = self._calculate_consistency_score(lang_units)

            # Calculate terminology accuracy (simplified)
            terminology_accuracy = self._calculate_terminology_accuracy(lang_units)

            return TranslationQualityReport(
                job_id=job_id,
                target_language=target_language,
                total_units=total_units,
                translated_units=translated_units,
                failed_units=failed_units,
                average_quality_score=avg_quality,
                consistency_score=consistency_score,
                terminology_accuracy=terminology_accuracy
            )

    def _calculate_consistency_score(self, units: List[TranslationUnit]) -> float:
        """Calculate consistency score for translated units."""
        # Simplified consistency check - look for repeated source texts
        source_texts = defaultdict(list)
        for unit in units:
            if unit.status == "completed":
                source_texts[unit.source_text].append(unit.translated_text)

        if not source_texts:
            return 0.0

        # Check if same source texts have consistent translations
        consistent_count = 0
        total_repeated = 0

        for source_text, translations in source_texts.items():
            if len(translations) > 1:
                total_repeated += 1
                # Check if all translations are the same
                if len(set(translations)) == 1:
                    consistent_count += 1

        return (consistent_count / total_repeated * 100) if total_repeated > 0 else 100.0

    def _calculate_terminology_accuracy(self, units: List[TranslationUnit]) -> float:
        """Calculate terminology accuracy score."""
        # Simplified terminology check
        completed_units = [u for u in units if u.status == "completed"]
        if not completed_units:
            return 0.0

        # For now, we'll use a placeholder - in a real system, this would check
        # against a terminology database or glossary
        return 95.0  # Assume 95% accuracy as placeholder

    def get_translation_statistics(self) -> Dict[str, Any]:
        """Get overall translation statistics."""
        with self._lock:
            total_jobs = len(self.translation_jobs)
            completed_jobs = len([j for j in self.translation_jobs.values() if j.status == "completed"])
            in_progress_jobs = len([j for j in self.translation_jobs.values() if j.status == "in_progress"])

            # Calculate total units and completion
            total_units = 0
            completed_units = 0
            failed_units = 0

            for job in self.translation_jobs.values():
                total_units += len(job.translation_units)
                completed_units += len([u for u in job.translation_units if u.status == "completed"])
                failed_units += len([u for u in job.translation_units if u.status == "failed"])

            # Language coverage
            language_coverage = dict(self.language_pairs)

            # Translation memory size
            tm_size = len(self.translation_memory)

            return {
                'total_jobs': total_jobs,
                'completed_jobs': completed_jobs,
                'in_progress_jobs': in_progress_jobs,
                'completion_rate': (completed_jobs / total_jobs * 100) if total_jobs > 0 else 0,
                'total_units': total_units,
                'completed_units': completed_units,
                'failed_units': failed_units,
                'unit_completion_rate': (completed_units / total_units * 100) if total_units > 0 else 0,
                'failed_unit_rate': (failed_units / total_units * 100) if total_units > 0 else 0,
                'language_coverage': language_coverage,
                'translation_memory_size': tm_size
            }

    def _save_translations(self):
        """Save translation jobs and memory to file."""
        try:
            data = {
                'timestamp': time.time(),
                'translation_jobs': {
                    job_id: {
                        'job_id': job.job_id,
                        'document_id': job.document_id,
                        'source_language': job.source_language,
                        'target_languages': job.target_languages,
                        'status': job.status,
                        'start_time': job.start_time,
                        'end_time': job.end_time,
                        'translation_units': [
                            {
                                'unit_id': unit.unit_id,
                                'source_text': unit.source_text,
                                'source_language': unit.source_language,
                                'target_language': unit.target_language,
                                'translated_text': unit.translated_text,
                                'status': unit.status,
                                'assigned_agent': unit.assigned_agent,
                                'translation_time': unit.translation_time,
                                'quality_score': unit.quality_score,
                                'metadata': unit.metadata
                            }
                            for unit in job.translation_units
                        ],
                        'metadata': job.metadata
                    }
                    for job_id, job in self.translation_jobs.items()
                },
                'translation_memory': {
                    key: {
                        'source_text': entry.source_text,
                        'target_text': entry.target_text,
                        'source_language': entry.source_language,
                        'target_language': entry.target_language,
                        'confidence_score': entry.confidence_score,
                        'usage_count': entry.usage_count,
                        'last_used': entry.last_used,
                        'metadata': entry.metadata
                    }
                    for key, entry in self.translation_memory.items()
                },
                'agent_assignments': dict(self.agent_assignments),
                'language_pairs': dict(self.language_pairs)
            }

            with open(self.translation_file, 'w') as f:
                json.dump(data, f, indent=2)

        except Exception as e:
            print(f"Error saving translations: {e}")

    def load_translations(self):
        """Load translation jobs and memory from file."""
        try:
            if not self.translation_file.exists():
                return

            with open(self.translation_file, 'r') as f:
                data = json.load(f)

            # Restore translation jobs
            self.translation_jobs.clear()
            for job_id, job_data in data.get('translation_jobs', {}).items():
                units = [
                    TranslationUnit(
                        unit_id=unit_data['unit_id'],
                        source_text=unit_data['source_text'],
                        source_language=unit_data['source_language'],
                        target_language=unit_data['target_language'],
                        translated_text=unit_data['translated_text'],
                        status=unit_data['status'],
                        assigned_agent=unit_data['assigned_agent'],
                        translation_time=unit_data['translation_time'],
                        quality_score=unit_data['quality_score'],
                        metadata=unit_data.get('metadata', {})
                    )
                    for unit_data in job_data.get('translation_units', [])
                ]

                job = TranslationJob(
                    job_id=job_data['job_id'],
                    document_id=job_data['document_id'],
                    source_language=job_data['source_language'],
                    target_languages=job_data['target_languages'],
                    status=job_data['status'],
                    start_time=job_data['start_time'],
                    end_time=job_data['end_time'],
                    translation_units=units,
                    metadata=job_data.get('metadata', {})
                )

                self.translation_jobs[job_id] = job

            # Restore translation memory
            self.translation_memory.clear()
            for key, entry_data in data.get('translation_memory', {}).items():
                entry = TranslationMemoryEntry(
                    source_text=entry_data['source_text'],
                    target_text=entry_data['target_text'],
                    source_language=entry_data['source_language'],
                    target_language=entry_data['target_language'],
                    confidence_score=entry_data['confidence_score'],
                    usage_count=entry_data['usage_count'],
                    last_used=entry_data['last_used'],
                    metadata=entry_data.get('metadata', {})
                )
                self.translation_memory[key] = entry

            # Restore indexes
            self.agent_assignments.clear()
            for agent_id, job_ids in data.get('agent_assignments', {}).items():
                self.agent_assignments[agent_id] = job_ids

            self.language_pairs.clear()
            for source_lang, target_langs in data.get('language_pairs', {}).items():
                self.language_pairs[source_lang] = target_langs

        except Exception as e:
            print(f"Error loading translations: {e}")


class TranslationDashboard:
    def __init__(self, translation_manager: DistributedTranslationManager):
        self.translation_manager = translation_manager

    def display_job_overview(self, job_id: str):
        """Display overview of a translation job."""
        job = self.translation_manager.get_translation_job(job_id)
        if not job:
            print(f"Translation job '{job_id}' not found")
            return

        progress = self.translation_manager.get_job_progress(job_id)

        print(f"\nTranslation Job Overview - {job_id}")
        print("=" * 40)
        print(f"Document ID: {job.document_id}")
        print(f"Source Language: {job.source_language}")
        print(f"Target Languages: {', '.join(job.target_languages)}")
        print(f"Status: {job.status}")
        print(f"Duration: {progress.get('duration_seconds', 0):.1f} seconds")

        print(f"\nProgress:")
        print(f"  Total Units: {progress.get('total_units', 0)}")
        print(f"  Completed: {progress.get('completed_units', 0)}")
        print(f"  Failed: {progress.get('failed_units', 0)}")
        print(f"  In Progress: {progress.get('in_progress_units', 0)}")
        print(f"  Pending: {progress.get('pending_units', 0)}")
        print(f"  Overall Progress: {progress.get('progress_percentage', 0):.1f}%")

        print(f"\nLanguage Progress:")
        language_progress = progress.get('language_progress', {})
        for lang, lang_progress in language_progress.items():
            print(f"  {lang}: {lang_progress['completed_units']}/{lang_progress['total_units']} "
                  f"({lang_progress['progress_percentage']:.1f}%)")

    def display_translation_quality(self, job_id: str):
        """Display quality reports for a translation job."""
        job = self.translation_manager.get_translation_job(job_id)
        if not job:
            print(f"Translation job '{job_id}' not found")
            return

        print(f"\nTranslation Quality Reports - {job_id}")
        print("=" * 38)

        for target_lang in job.target_languages:
            report = self.translation_manager.get_translation_quality_report(job_id, target_lang)

            print(f"\nLanguage: {target_lang}")
            print(f"  Total Units: {report.total_units}")
            print(f"  Translated: {report.translated_units}")
            print(f"  Failed: {report.failed_units}")
            print(f"  Average Quality Score: {report.average_quality_score:.1f}/100")
            print(f"  Consistency Score: {report.consistency_score:.1f}/100")
            print(f"  Terminology Accuracy: {report.terminology_accuracy:.1f}/100")

    def display_translation_statistics(self):
        """Display overall translation statistics."""
        stats = self.translation_manager.get_translation_statistics()

        print(f"\nTranslation Statistics")
        print("=" * 22)
        print(f"Total Jobs: {stats['total_jobs']}")
        print(f"Completed Jobs: {stats['completed_jobs']}")
        print(f"In Progress Jobs: {stats['in_progress_jobs']}")
        print(f"Job Completion Rate: {stats['completion_rate']:.1f}%")

        print(f"\nTranslation Units:")
        print(f"  Total Units: {stats['total_units']}")
        print(f"  Completed Units: {stats['completed_units']}")
        print(f"  Failed Units: {stats['failed_units']}")
        print(f"  Unit Completion Rate: {stats['unit_completion_rate']:.1f}%")
        print(f"  Failed Unit Rate: {stats['failed_unit_rate']:.1f}%")

        print(f"\nLanguage Coverage:")
        for source_lang, target_langs in stats['language_coverage'].items():
            print(f"  {source_lang} → {', '.join(target_langs)}")

        print(f"\nTranslation Memory:")
        print(f"  Entries: {stats['translation_memory_size']}")

    def display_agent_assignments(self, agent_id: str):
        """Display translation jobs assigned to an agent."""
        jobs = self.translation_manager.get_agent_assignments(agent_id)

        print(f"\nTranslation Jobs for Agent {agent_id}")
        print("=" * 38)

        if not jobs:
            print("No translation jobs assigned")
            return

        for job in jobs:
            progress = self.translation_manager.get_job_progress(job.job_id)
            print(f"\nJob: {job.job_id}")
            print(f"  Document: {job.document_id}")
            print(f"  Languages: {job.source_language} → {', '.join(job.target_languages)}")
            print(f"  Status: {job.status}")
            print(f"  Progress: {progress.get('progress_percentage', 0):.1f}%")

    def display_translation_memory_stats(self):
        """Display translation memory statistics."""
        with self.translation_manager._lock:
            tm_size = len(self.translation_manager.translation_memory)

            # Get quality distribution
            quality_ranges = defaultdict(int)
            for entry in self.translation_manager.translation_memory.values():
                quality_range = int(entry.quality_score / 10) * 10  # Group by 10s
                quality_ranges[f"{quality_range}-{quality_range+9}"] += 1

            # Get most used entries
            sorted_entries = sorted(
                self.translation_manager.translation_memory.values(),
                key=lambda x: x.usage_count,
                reverse=True
            )[:5]  # Top 5 most used

        print(f"\nTranslation Memory Statistics")
        print("=" * 30)
        print(f"Total Entries: {tm_size}")

        print(f"\nQuality Distribution:")
        for range_name, count in sorted(quality_ranges.items()):
            print(f"  {range_name}%: {count} entries")

        print(f"\nMost Used Entries:")
        for i, entry in enumerate(sorted_entries, 1):
            print(f"  {i}. {entry.source_text[:50]}... → {entry.target_text[:50]}...")
            print(f"     Quality: {entry.quality_score:.1f}%, Used: {entry.usage_count} times")


def main():
    # Example usage
    print("Distributed Translation Pipelines")
    print("=" * 33)

    # Create translation manager and dashboard
    translation_manager = DistributedTranslationManager()
    dashboard = TranslationDashboard(translation_manager)

    print("Distributed translation system initialized")
    print("System ready for parallel translation workflows")

    # Example of what the workflow would look like:
    print("\nExample workflow:")
    print("  1. Start translation jobs for multiple languages")
    print("  2. Distribute translation units to agents")
    print("  3. Leverage translation memory for consistency")
    print("  4. Track progress and quality across languages")
    print("  5. Generate quality reports and statistics")


if __name__ == "__main__":
    main()