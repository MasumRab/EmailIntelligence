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
class TranslationSegment:
    segment_id: str
    source_text: str
    source_language: str
    target_language: str
    translated_text: str = ""
    translation_status: str = "pending"  # "pending", "in_progress", "completed", "failed"
    translation_agent: str = ""
    translation_time: float = 0.0
    confidence_score: float = 0.0  # 0.0 to 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TranslationMemoryEntry:
    source_text: str
    target_text: str
    source_language: str
    target_language: str
    confidence_score: float
    last_used: float = 0.0
    usage_count: int = 1
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TranslationJob:
    job_id: str
    document_id: str
    source_language: str
    target_language: str
    segments: List[TranslationSegment]
    status: str = "pending"  # "pending", "in_progress", "completed", "failed"
    start_time: float = 0.0
    end_time: float = 0.0
    assigned_agents: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TranslationQualityReport:
    report_id: str
    job_id: str
    segment_id: str
    quality_score: float  # 0.0 to 1.0
    issues: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)
    reviewer: str = ""
    timestamp: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


class DistributedTranslationManager:
    def __init__(self, translation_file: Path = None):
        self.translation_file = translation_file or Path(".distributed_translation.json")
        self.translation_jobs: Dict[str, TranslationJob] = {}
        self.translation_memory: Dict[str, TranslationMemoryEntry] = {}
        self.quality_reports: Dict[str, TranslationQualityReport] = {}
        self.language_pairs: Dict[str, List[str]] = defaultdict(list)  # source -> targets
        self.agent_capabilities: Dict[str, List[str]] = defaultdict(list)  # agent_id -> language_pairs
        self._lock = threading.RLock()
        self.load_translation_data()

    def register_agent_capability(self, agent_id: str, source_language: str,
                                target_language: str) -> bool:
        """Register an agent's translation capability."""
        language_pair = f"{source_language}-{target_language}"

        with self._lock:
            if language_pair not in self.agent_capabilities[agent_id]:
                self.agent_capabilities[agent_id].append(language_pair)

            # Update language pairs
            if target_language not in self.language_pairs[source_language]:
                self.language_pairs[source_language].append(target_language)

            self._save_translation_data()
            return True

    def create_translation_job(self, document_id: str, source_language: str,
                              target_language: str, source_segments: List[str],
                              metadata: Dict[str, Any] = None) -> str:
        """Create a new translation job."""
        if metadata is None:
            metadata = {}

        job_id = str(uuid.uuid4())

        # Create segments
        segments = []
        for i, source_text in enumerate(source_segments):
            segment_id = f"{job_id}-seg-{i}"
            segment = TranslationSegment(
                segment_id=segment_id,
                source_text=source_text,
                source_language=source_language,
                target_language=target_language
            )
            segments.append(segment)

        with self._lock:
            job = TranslationJob(
                job_id=job_id,
                document_id=document_id,
                source_language=source_language,
                target_language=target_language,
                segments=segments,
                status="pending",
                metadata=metadata
            )

            self.translation_jobs[job_id] = job
            self._save_translation_data()

            return job_id

    def get_translation_job(self, job_id: str) -> Optional[TranslationJob]:
        """Get a translation job by ID."""
        with self._lock:
            return self.translation_jobs.get(job_id)

    def start_translation_job(self, job_id: str, agent_ids: List[str]) -> bool:
        """Start a translation job with assigned agents."""
        with self._lock:
            job = self.translation_jobs.get(job_id)
            if not job:
                return False

            job.status = "in_progress"
            job.start_time = time.time()
            job.assigned_agents = agent_ids[:]
            self._save_translation_data()
            return True

    def complete_translation_job(self, job_id: str) -> bool:
        """Mark a translation job as completed."""
        with self._lock:
            job = self.translation_jobs.get(job_id)
            if not job:
                return False

            job.status = "completed"
            job.end_time = time.time()
            self._save_translation_data()
            return True

    def get_available_agents(self, source_language: str, target_language: str) -> List[str]:
        """Get agents capable of translating between the specified languages."""
        language_pair = f"{source_language}-{target_language}"

        with self._lock:
            available_agents = [
                agent_id for agent_id, capabilities in self.agent_capabilities.items()
                if language_pair in capabilities
            ]
            return available_agents

    def translate_segment(self, job_id: str, segment_id: str, agent_id: str,
                         translated_text: str, confidence_score: float = 0.8) -> bool:
        """Translate a segment."""
        with self._lock:
            job = self.translation_jobs.get(job_id)
            if not job:
                return False

            # Find the segment
            segment = None
            for seg in job.segments:
                if seg.segment_id == segment_id:
                    segment = seg
                    break

            if not segment:
                return False

            # Update segment
            segment.translated_text = translated_text
            segment.translation_status = "completed"
            segment.translation_agent = agent_id
            segment.translation_time = time.time() - job.start_time if job.start_time > 0 else 0
            segment.confidence_score = confidence_score

            # Add to translation memory
            self._add_to_translation_memory(
                segment.source_text, translated_text,
                segment.source_language, segment.target_language,
                confidence_score
            )

            self._save_translation_data()
            return True

    def _add_to_translation_memory(self, source_text: str, target_text: str,
                                  source_language: str, target_language: str,
                                  confidence_score: float):
        """Add a translation to the translation memory."""
        # Create a hash key for the entry
        key = hashlib.md5(f"{source_text}-{source_language}-{target_language}".encode()).hexdigest()

        entry = TranslationMemoryEntry(
            source_text=source_text,
            target_text=target_text,
            source_language=source_language,
            target_language=target_language,
            confidence_score=confidence_score,
            last_used=time.time(),
            usage_count=1
        )

        self.translation_memory[key] = entry

    def lookup_translation_memory(self, source_text: str, source_language: str,
                                target_language: str) -> Optional[TranslationMemoryEntry]:
        """Look up a translation in the translation memory."""
        key = hashlib.md5(f"{source_text}-{source_language}-{target_language}".encode()).hexdigest()

        with self._lock:
            entry = self.translation_memory.get(key)
            if entry:
                entry.last_used = time.time()
                entry.usage_count += 1
                self._save_translation_data()
                return entry

            return None

    def get_job_progress(self, job_id: str) -> Dict[str, Any]:
        """Get progress information for a translation job."""
        with self._lock:
            job = self.translation_jobs.get(job_id)
            if not job:
                return {}

            total_segments = len(job.segments)
            completed_segments = len([s for s in job.segments if s.translation_status == "completed"])
            in_progress_segments = len([s for s in job.segments if s.translation_status == "in_progress"])
            pending_segments = len([s for s in job.segments if s.translation_status == "pending"])

            return {
                'job_id': job_id,
                'status': job.status,
                'total_segments': total_segments,
                'completed_segments': completed_segments,
                'in_progress_segments': in_progress_segments,
                'pending_segments': pending_segments,
                'progress_percentage': (completed_segments / total_segments * 100) if total_segments > 0 else 0,
                'assigned_agents': job.assigned_agents[:],
                'duration_seconds': time.time() - job.start_time if job.start_time > 0 else 0
            }

    def get_job_quality_metrics(self, job_id: str) -> Dict[str, Any]:
        """Get quality metrics for a translation job."""
        with self._lock:
            job = self.translation_jobs.get(job_id)
            if not job:
                return {}

            # Get quality reports for this job
            job_reports = [
                report for report in self.quality_reports.values()
                if report.job_id == job_id
            ]

            if not job_reports:
                return {
                    'total_segments': len(job.segments),
                    'segments_with_quality_reports': 0,
                    'average_quality_score': 0.0
                }

            # Calculate metrics
            total_reports = len(job_reports)
            total_quality_score = sum(report.quality_score for report in job_reports)
            average_quality_score = total_quality_score / total_reports if total_reports > 0 else 0.0

            # Count issues
            total_issues = sum(len(report.issues) for report in job_reports)

            return {
                'total_segments': len(job.segments),
                'segments_with_quality_reports': total_reports,
                'average_quality_score': average_quality_score,
                'total_issues': total_issues,
                'reports_per_segment': total_reports / len(job.segments) if job.segments else 0
            }

    def add_quality_report(self, job_id: str, segment_id: str, quality_score: float,
                          issues: List[str] = None, suggestions: List[str] = None,
                          reviewer: str = "") -> str:
        """Add a quality report for a translated segment."""
        if issues is None:
            issues = []
        if suggestions is None:
            suggestions = []

        report_id = str(uuid.uuid4())

        with self._lock:
            report = TranslationQualityReport(
                report_id=report_id,
                job_id=job_id,
                segment_id=segment_id,
                quality_score=quality_score,
                issues=issues[:],
                suggestions=suggestions[:],
                reviewer=reviewer,
                timestamp=time.time()
            )

            self.quality_reports[report_id] = report
            self._save_translation_data()

            return report_id

    def get_quality_reports(self, job_id: str) -> List[TranslationQualityReport]:
        """Get all quality reports for a translation job."""
        with self._lock:
            return [
                report for report in self.quality_reports.values()
                if report.job_id == job_id
            ]

    def get_translation_memory_stats(self) -> Dict[str, Any]:
        """Get statistics about the translation memory."""
        with self._lock:
            total_entries = len(self.translation_memory)

            # Group by language pair
            language_stats = defaultdict(int)
            for entry in self.translation_memory.values():
                pair = f"{entry.source_language}-{entry.target_language}"
                language_stats[pair] += 1

            # Calculate average confidence
            if total_entries > 0:
                total_confidence = sum(entry.confidence_score for entry in self.translation_memory.values())
                average_confidence = total_confidence / total_entries
            else:
                average_confidence = 0.0

            return {
                'total_entries': total_entries,
                'language_pairs': dict(language_stats),
                'average_confidence': average_confidence,
                'supported_language_pairs': dict(self.language_pairs)
            }

    def get_agent_translation_stats(self, agent_id: str) -> Dict[str, Any]:
        """Get translation statistics for an agent."""
        with self._lock:
            # Find segments translated by this agent
            agent_segments = []
            for job in self.translation_jobs.values():
                for segment in job.segments:
                    if segment.translation_agent == agent_id:
                        agent_segments.append(segment)

            total_segments = len(agent_segments)
            if total_segments == 0:
                return {
                    'agent_id': agent_id,
                    'total_segments_translated': 0,
                    'average_confidence': 0.0,
                    'language_pairs': []
                }

            # Calculate average confidence
            total_confidence = sum(segment.confidence_score for segment in agent_segments)
            average_confidence = total_confidence / total_segments if total_segments > 0 else 0.0

            # Get language pairs
            language_pairs = list(set(
                f"{segment.source_language}-{segment.target_language}"
                for segment in agent_segments
            ))

            return {
                'agent_id': agent_id,
                'total_segments_translated': total_segments,
                'average_confidence': average_confidence,
                'language_pairs': language_pairs
            }

    def get_parallel_translation_plan(self, job_id: str) -> List[List[str]]:
        """Get a plan for parallel segment translation."""
        with self._lock:
            job = self.translation_jobs.get(job_id)
            if not job:
                return []

            # For simplicity, we'll divide segments evenly among agents
            # In a real system, this would consider segment complexity, agent performance, etc.
            if not job.assigned_agents:
                # If no agents assigned, return all segments in one group
                return [[segment.segment_id for segment in job.segments]]

            # Divide segments among agents
            num_agents = len(job.assigned_agents)
            segments_per_agent = max(1, len(job.segments) // num_agents)

            waves = []
            for i in range(0, len(job.segments), segments_per_agent):
                wave_segments = job.segments[i:i + segments_per_agent]
                wave_ids = [segment.segment_id for segment in wave_segments]
                waves.append(wave_ids)

            return waves

    def _save_translation_data(self):
        """Save translation data to file."""
        try:
            data = {
                'timestamp': time.time(),
                'translation_jobs': {
                    job_id: {
                        'job_id': job.job_id,
                        'document_id': job.document_id,
                        'source_language': job.source_language,
                        'target_language': job.target_language,
                        'segments': [
                            {
                                'segment_id': segment.segment_id,
                                'source_text': segment.source_text,
                                'source_language': segment.source_language,
                                'target_language': segment.target_language,
                                'translated_text': segment.translated_text,
                                'translation_status': segment.translation_status,
                                'translation_agent': segment.translation_agent,
                                'translation_time': segment.translation_time,
                                'confidence_score': segment.confidence_score,
                                'metadata': segment.metadata
                            }
                            for segment in job.segments
                        ],
                        'status': job.status,
                        'start_time': job.start_time,
                        'end_time': job.end_time,
                        'assigned_agents': job.assigned_agents,
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
                        'last_used': entry.last_used,
                        'usage_count': entry.usage_count,
                        'metadata': entry.metadata
                    }
                    for key, entry in self.translation_memory.items()
                },
                'quality_reports': {
                    report_id: {
                        'report_id': report.report_id,
                        'job_id': report.job_id,
                        'segment_id': report.segment_id,
                        'quality_score': report.quality_score,
                        'issues': report.issues,
                        'suggestions': report.suggestions,
                        'reviewer': report.reviewer,
                        'timestamp': report.timestamp,
                        'metadata': report.metadata
                    }
                    for report_id, report in self.quality_reports.items()
                },
                'language_pairs': dict(self.language_pairs),
                'agent_capabilities': {
                    agent_id: capabilities[:]
                    for agent_id, capabilities in self.agent_capabilities.items()
                }
            }

            with open(self.translation_file, 'w') as f:
                json.dump(data, f, indent=2)

        except Exception as e:
            print(f"Error saving translation data: {e}")

    def load_translation_data(self):
        """Load translation data from file."""
        try:
            if not self.translation_file.exists():
                return

            with open(self.translation_file, 'r') as f:
                data = json.load(f)

            # Restore translation jobs
            self.translation_jobs.clear()
            for job_id, job_data in data.get('translation_jobs', {}).items():
                segments = [
                    TranslationSegment(
                        segment_id=segment_data['segment_id'],
                        source_text=segment_data['source_text'],
                        source_language=segment_data['source_language'],
                        target_language=segment_data['target_language'],
                        translated_text=segment_data.get('translated_text', ''),
                        translation_status=segment_data.get('translation_status', 'pending'),
                        translation_agent=segment_data.get('translation_agent', ''),
                        translation_time=segment_data.get('translation_time', 0.0),
                        confidence_score=segment_data.get('confidence_score', 0.0),
                        metadata=segment_data.get('metadata', {})
                    )
                    for segment_data in job_data.get('segments', [])
                ]

                job = TranslationJob(
                    job_id=job_data['job_id'],
                    document_id=job_data['document_id'],
                    source_language=job_data['source_language'],
                    target_language=job_data['target_language'],
                    segments=segments,
                    status=job_data.get('status', 'pending'),
                    start_time=job_data.get('start_time', 0.0),
                    end_time=job_data.get('end_time', 0.0),
                    assigned_agents=job_data.get('assigned_agents', []),
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
                    last_used=entry_data.get('last_used', 0.0),
                    usage_count=entry_data.get('usage_count', 1),
                    metadata=entry_data.get('metadata', {})
                )
                self.translation_memory[key] = entry

            # Restore quality reports
            self.quality_reports.clear()
            for report_id, report_data in data.get('quality_reports', {}).items():
                report = TranslationQualityReport(
                    report_id=report_data['report_id'],
                    job_id=report_data['job_id'],
                    segment_id=report_data['segment_id'],
                    quality_score=report_data['quality_score'],
                    issues=report_data.get('issues', []),
                    suggestions=report_data.get('suggestions', []),
                    reviewer=report_data.get('reviewer', ''),
                    timestamp=report_data['timestamp'],
                    metadata=report_data.get('metadata', {})
                )
                self.quality_reports[report_id] = report

            # Restore language pairs
            self.language_pairs.clear()
            for source_lang, target_langs in data.get('language_pairs', {}).items():
                self.language_pairs[source_lang] = target_langs[:]

            # Restore agent capabilities
            self.agent_capabilities.clear()
            for agent_id, capabilities in data.get('agent_capabilities', {}).items():
                self.agent_capabilities[agent_id] = capabilities[:]

        except Exception as e:
            print(f"Error loading translation data: {e}")


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
        quality_metrics = self.translation_manager.get_job_quality_metrics(job_id)

        print(f"\nTranslation Job Overview - {job_id}")
        print("=" * 40)
        print(f"Document ID: {job.document_id}")
        print(f"Languages: {job.source_language} → {job.target_language}")
        print(f"Status: {job.status}")
        print(f"Assigned Agents: {len(job.assigned_agents)} ({', '.join(job.assigned_agents)})")
        print(f"Duration: {progress.get('duration_seconds', 0):.1f} seconds")

        print(f"\nProgress:")
        print(f"  Total Segments: {progress.get('total_segments', 0)}")
        print(f"  Completed: {progress.get('completed_segments', 0)}")
        print(f"  In Progress: {progress.get('in_progress_segments', 0)}")
        print(f"  Pending: {progress.get('pending_segments', 0)}")
        print(f"  Progress: {progress.get('progress_percentage', 0):.1f}%")

        print(f"\nQuality Metrics:")
        print(f"  Average Quality Score: {quality_metrics.get('average_quality_score', 0):.2f}")
        print(f"  Segments with Reports: {quality_metrics.get('segments_with_quality_reports', 0)}/{quality_metrics.get('total_segments', 0)}")
        print(f"  Total Issues: {quality_metrics.get('total_issues', 0)}")

        # Show parallel translation plan
        plan = self.translation_manager.get_parallel_translation_plan(job_id)
        print(f"\nParallel Translation Plan:")
        for i, wave in enumerate(plan, 1):
            print(f"  Wave {i}: {len(wave)} segments")

    def display_translation_memory_stats(self):
        """Display translation memory statistics."""
        stats = self.translation_manager.get_translation_memory_stats()

        print(f"\nTranslation Memory Statistics")
        print("=" * 32)
        print(f"Total Entries: {stats.get('total_entries', 0)}")
        print(f"Average Confidence: {stats.get('average_confidence', 0):.2f}")

        language_pairs = stats.get('language_pairs', {})
        if language_pairs:
            print(f"\nEntries by Language Pair:")
            for pair, count in language_pairs.items():
                print(f"  {pair}: {count}")

        supported_pairs = stats.get('supported_language_pairs', {})
        if supported_pairs:
            print(f"\nSupported Language Pairs:")
            for source, targets in supported_pairs.items():
                print(f"  {source} → {', '.join(targets)}")

    def display_agent_stats(self, agent_id: str):
        """Display statistics for a translation agent."""
        stats = self.translation_manager.get_agent_translation_stats(agent_id)

        print(f"\nAgent Translation Statistics - {agent_id}")
        print("=" * 42)
        print(f"Total Segments Translated: {stats.get('total_segments_translated', 0)}")
        print(f"Average Confidence: {stats.get('average_confidence', 0):.2f}")

        language_pairs = stats.get('language_pairs', [])
        if language_pairs:
            print(f"Language Pairs: {', '.join(language_pairs)}")

    def display_quality_reports(self, job_id: str):
        """Display quality reports for a translation job."""
        reports = self.translation_manager.get_quality_reports(job_id)

        print(f"\nQuality Reports - Job {job_id}")
        print("=" * 32)

        if not reports:
            print("No quality reports found")
            return

        for i, report in enumerate(reports, 1):
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(report.timestamp))
            print(f"\n{i}. Segment: {report.segment_id}")
            print(f"   Reviewer: {report.reviewer}")
            print(f"   Time: {timestamp}")
            print(f"   Quality Score: {report.quality_score:.2f}")

            if report.issues:
                print(f"   Issues:")
                for issue in report.issues:
                    print(f"     - {issue}")

            if report.suggestions:
                print(f"   Suggestions:")
                for suggestion in report.suggestions:
                    print(f"     - {suggestion}")

    def display_job_segments(self, job_id: str):
        """Display segments for a translation job."""
        job = self.translation_manager.get_translation_job(job_id)
        if not job:
            print(f"Translation job '{job_id}' not found")
            return

        print(f"\nTranslation Segments - Job {job_id}")
        print("=" * 35)

        for i, segment in enumerate(job.segments, 1):
            print(f"\n{i}. Status: {segment.translation_status}")
            print(f"   Source ({segment.source_language}): {segment.source_text[:100]}{'...' if len(segment.source_text) > 100 else ''}")
            if segment.translated_text:
                print(f"   Target ({segment.target_language}): {segment.translated_text[:100]}{'...' if len(segment.translated_text) > 100 else ''}")
            print(f"   Confidence: {segment.confidence_score:.2f}")
            if segment.translation_agent:
                print(f"   Translated by: {segment.translation_agent}")
            if segment.translation_time > 0:
                print(f"   Translation Time: {segment.translation_time:.2f}s")


def main():
    # Example usage
    print("Distributed Translation Pipelines")
    print("=" * 35)

    # Create translation manager and dashboard
    translation_manager = DistributedTranslationManager()
    dashboard = TranslationDashboard(translation_manager)

    print("Distributed translation system initialized")
    print("System ready for parallel translation workflows")

    # Example of what the workflow would look like:
    print("\nExample workflow:")
    print("  1. Register agents with translation capabilities")
    print("  2. Create translation jobs for multi-language docs")
    print("  3. Assign segments to agents for parallel translation")
    print("  4. Use translation memory to reduce redundant work")
    print("  5. Track quality and performance metrics")


if __name__ == "__main__":
    main()