#!/usr/bin/env python3
"""
Concurrent Review Workflows
Create system for multiple agents to review documentation simultaneously.
"""

import time
import json
import threading
from pathlib import Path
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field
from collections import defaultdict
import uuid


@dataclass
class ReviewComment:
    comment_id: str
    agent_id: str
    section_id: str
    comment_text: str
    severity: str  # "low", "medium", "high", "critical"
    status: str = "open"  # "open", "resolved", "dismissed"
    timestamp: float = 0.0
    resolved_by: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ReviewFeedback:
    feedback_id: str
    agent_id: str
    document_id: str
    overall_rating: int  # 1-5 scale
    feedback_text: str
    timestamp: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ReviewVote:
    vote_id: str
    agent_id: str
    document_id: str
    section_id: str
    vote_type: str  # "approve", "reject", "request_changes"
    comment: str = ""
    timestamp: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ReviewSession:
    session_id: str
    document_id: str
    reviewers: List[str]  # List of agent IDs
    status: str = "pending"  # "pending", "in_progress", "completed"
    start_time: float = 0.0
    end_time: float = 0.0
    comments: List[ReviewComment] = field(default_factory=list)
    feedback: List[ReviewFeedback] = field(default_factory=list)
    votes: List[ReviewVote] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


class ConcurrentReviewManager:
    def __init__(self, reviews_file: Path = None):
        self.reviews_file = reviews_file or Path(".concurrent_reviews.json")
        self.review_sessions: Dict[str, ReviewSession] = {}
        self.agent_reviews: Dict[str, List[str]] = defaultdict(list)  # agent_id -> session_ids
        self.document_reviews: Dict[str, List[str]] = defaultdict(list)  # document_id -> session_ids
        self._lock = threading.RLock()
        self.load_reviews()
        
    def start_review_session(self, document_id: str, reviewers: List[str], 
                           metadata: Dict[str, Any] = None) -> str:
        """Start a new concurrent review session."""
        if metadata is None:
            metadata = {}
            
        session_id = str(uuid.uuid4())
        
        with self._lock:
            session = ReviewSession(
                session_id=session_id,
                document_id=document_id,
                reviewers=reviewers,
                status="pending",
                start_time=time.time(),
                metadata=metadata
            )
            
            self.review_sessions[session_id] = session
            
            # Update indexes
            for reviewer in reviewers:
                self.agent_reviews[reviewer].append(session_id)
            self.document_reviews[document_id].append(session_id)
            
            self._save_reviews()
            
            return session_id
            
    def get_review_session(self, session_id: str) -> Optional[ReviewSession]:
        """Get a review session by ID."""
        with self._lock:
            return self.review_sessions.get(session_id)
            
    def get_sessions_for_agent(self, agent_id: str) -> List[ReviewSession]:
        """Get all review sessions for an agent."""
        with self._lock:
            session_ids = self.agent_reviews.get(agent_id, [])
            return [self.review_sessions[sid] for sid in session_ids if sid in self.review_sessions]
            
    def get_sessions_for_document(self, document_id: str) -> List[ReviewSession]:
        """Get all review sessions for a document."""
        with self._lock:
            session_ids = self.document_reviews.get(document_id, [])
            return [self.review_sessions[sid] for sid in session_ids if sid in self.review_sessions]
            
    def start_session_review(self, session_id: str) -> bool:
        """Mark a review session as in progress."""
        with self._lock:
            session = self.review_sessions.get(session_id)
            if not session:
                return False
                
            session.status = "in_progress"
            session.start_time = time.time()
            self._save_reviews()
            return True
            
    def complete_session_review(self, session_id: str) -> bool:
        """Mark a review session as completed."""
        with self._lock:
            session = self.review_sessions.get(session_id)
            if not session:
                return False
                
            session.status = "completed"
            session.end_time = time.time()
            self._save_reviews()
            return True
            
    def add_comment(self, session_id: str, agent_id: str, section_id: str, 
                   comment_text: str, severity: str = "medium") -> str:
        """Add a comment to a review session."""
        comment_id = str(uuid.uuid4())
        
        with self._lock:
            session = self.review_sessions.get(session_id)
            if not session:
                return ""
                
            comment = ReviewComment(
                comment_id=comment_id,
                agent_id=agent_id,
                section_id=section_id,
                comment_text=comment_text,
                severity=severity,
                timestamp=time.time()
            )
            
            session.comments.append(comment)
            self._save_reviews()
            
            return comment_id
            
    def resolve_comment(self, session_id: str, comment_id: str, resolved_by: str) -> bool:
        """Mark a comment as resolved."""
        with self._lock:
            session = self.review_sessions.get(session_id)
            if not session:
                return False
                
            for comment in session.comments:
                if comment.comment_id == comment_id:
                    comment.status = "resolved"
                    comment.resolved_by = resolved_by
                    self._save_reviews()
                    return True
                    
            return False
            
    def add_feedback(self, session_id: str, agent_id: str, document_id: str,
                    overall_rating: int, feedback_text: str) -> str:
        """Add overall feedback to a review session."""
        feedback_id = str(uuid.uuid4())
        
        with self._lock:
            session = self.review_sessions.get(session_id)
            if not session:
                return ""
                
            feedback = ReviewFeedback(
                feedback_id=feedback_id,
                agent_id=agent_id,
                document_id=document_id,
                overall_rating=overall_rating,
                feedback_text=feedback_text,
                timestamp=time.time()
            )
            
            session.feedback.append(feedback)
            self._save_reviews()
            
            return feedback_id
            
    def add_vote(self, session_id: str, agent_id: str, document_id: str,
                section_id: str, vote_type: str, comment: str = "") -> str:
        """Add a vote to a review session."""
        vote_id = str(uuid.uuid4())
        
        with self._lock:
            session = self.review_sessions.get(session_id)
            if not session:
                return ""
                
            vote = ReviewVote(
                vote_id=vote_id,
                agent_id=agent_id,
                document_id=document_id,
                section_id=section_id,
                vote_type=vote_type,
                comment=comment,
                timestamp=time.time()
            )
            
            session.votes.append(vote)
            self._save_reviews()
            
            return vote_id
            
    def get_session_comments(self, session_id: str) -> List[ReviewComment]:
        """Get all comments for a review session."""
        with self._lock:
            session = self.review_sessions.get(session_id)
            if not session:
                return []
                
            return session.comments[:]
            
    def get_session_feedback(self, session_id: str) -> List[ReviewFeedback]:
        """Get all feedback for a review session."""
        with self._lock:
            session = self.review_sessions.get(session_id)
            if not session:
                return []
                
            return session.feedback[:]
            
    def get_session_votes(self, session_id: str) -> List[ReviewVote]:
        """Get all votes for a review session."""
        with self._lock:
            session = self.review_sessions.get(session_id)
            if not session:
                return []
                
            return session.votes[:]
            
    def get_comment_summary(self, session_id: str) -> Dict[str, Any]:
        """Get a summary of comments for a review session."""
        with self._lock:
            session = self.review_sessions.get(session_id)
            if not session:
                return {}
                
            total_comments = len(session.comments)
            open_comments = len([c for c in session.comments if c.status == "open"])
            resolved_comments = len([c for c in session.comments if c.status == "resolved"])
            
            severity_counts = defaultdict(int)
            for comment in session.comments:
                severity_counts[comment.severity] += 1
                
            return {
                'total_comments': total_comments,
                'open_comments': open_comments,
                'resolved_comments': resolved_comments,
                'severity_breakdown': dict(severity_counts)
            }
            
    def get_voting_results(self, session_id: str) -> Dict[str, Any]:
        """Get voting results for a review session."""
        with self._lock:
            session = self.review_sessions.get(session_id)
            if not session:
                return {}
                
            vote_counts = defaultdict(lambda: defaultdict(int))
            total_votes = defaultdict(int)
            
            for vote in session.votes:
                vote_counts[vote.section_id][vote.vote_type] += 1
                total_votes[vote.section_id] += 1
                
            # Calculate consensus for each section
            consensus_results = {}
            for section_id, votes in vote_counts.items():
                total_section_votes = total_votes[section_id]
                if total_section_votes == 0:
                    consensus_results[section_id] = {
                        'consensus': "no_votes",
                        'confidence': 0.0
                    }
                    continue
                    
                # Find the most common vote type
                most_common_vote = max(votes.items(), key=lambda x: x[1])
                vote_type, count = most_common_vote
                confidence = count / total_section_votes
                
                consensus_results[section_id] = {
                    'consensus': vote_type,
                    'confidence': confidence,
                    'vote_breakdown': dict(votes),
                    'total_votes': total_section_votes
                }
                
            return {
                'total_votes': len(session.votes),
                'section_consensus': consensus_results,
                'reviewers_participated': len(set(vote.agent_id for vote in session.votes))
            }
            
    def get_session_progress(self, session_id: str) -> Dict[str, Any]:
        """Get progress information for a review session."""
        with self._lock:
            session = self.review_sessions.get(session_id)
            if not session:
                return {}
                
            total_reviewers = len(session.reviewers)
            reviewers_with_votes = len(set(vote.agent_id for vote in session.votes))
            reviewers_with_feedback = len(set(feedback.agent_id for feedback in session.feedback))
            
            # Calculate completion percentage based on participation
            participation_rate = (reviewers_with_votes + reviewers_with_feedback) / (2 * total_reviewers) if total_reviewers > 0 else 0
            
            return {
                'session_id': session_id,
                'status': session.status,
                'total_reviewers': total_reviewers,
                'reviewers_with_votes': reviewers_with_votes,
                'reviewers_with_feedback': reviewers_with_feedback,
                'participation_rate': participation_rate,
                'duration_seconds': time.time() - session.start_time if session.start_time > 0 else 0
            }
            
    def get_feedback_summary(self, session_id: str) -> Dict[str, Any]:
        """Get a summary of feedback for a review session."""
        with self._lock:
            session = self.review_sessions.get(session_id)
            if not session:
                return {}
                
            if not session.feedback:
                return {
                    'total_feedback': 0,
                    'average_rating': 0.0
                }
                
            total_feedback = len(session.feedback)
            total_rating = sum(feedback.overall_rating for feedback in session.feedback)
            average_rating = total_rating / total_feedback
            
            rating_counts = defaultdict(int)
            for feedback in session.feedback:
                rating_counts[feedback.overall_rating] += 1
                
            return {
                'total_feedback': total_feedback,
                'average_rating': average_rating,
                'rating_breakdown': dict(rating_counts)
            }
            
    def get_review_consensus(self, session_id: str) -> Dict[str, Any]:
        """Get overall consensus for a review session."""
        with self._lock:
            session = self.review_sessions.get(session_id)
            if not session:
                return {}
                
            # Get voting results
            voting_results = self.get_voting_results(session_id)
            
            # Get feedback summary
            feedback_summary = self.get_feedback_summary(session_id)
            
            # Calculate overall consensus
            total_votes = voting_results.get('total_votes', 0)
            reviewers_participated = voting_results.get('reviewers_participated', 0)
            total_reviewers = len(session.reviewers)
            
            # Consensus level based on participation
            participation_consensus = reviewers_participated / total_reviewers if total_reviewers > 0 else 0
            
            # Approval rate
            approve_votes = sum(
                votes.get('approve', 0) 
                for votes in voting_results.get('section_consensus', {}).values()
            )
            total_section_votes = sum(
                result.get('total_votes', 0)
                for result in voting_results.get('section_consensus', {}).values()
            )
            approval_rate = approve_votes / total_section_votes if total_section_votes > 0 else 0
            
            return {
                'session_id': session_id,
                'participation_consensus': participation_consensus,
                'approval_rate': approval_rate,
                'average_rating': feedback_summary.get('average_rating', 0.0),
                'total_participants': reviewers_participated,
                'total_reviewers': total_reviewers,
                'consensus_strength': (participation_consensus + approval_rate) / 2
            }
            
    def _save_reviews(self):
        """Save review sessions to file."""
        try:
            data = {
                'timestamp': time.time(),
                'review_sessions': {
                    session_id: {
                        'session_id': session.session_id,
                        'document_id': session.document_id,
                        'reviewers': session.reviewers,
                        'status': session.status,
                        'start_time': session.start_time,
                        'end_time': session.end_time,
                        'comments': [
                            {
                                'comment_id': comment.comment_id,
                                'agent_id': comment.agent_id,
                                'section_id': comment.section_id,
                                'comment_text': comment.comment_text,
                                'severity': comment.severity,
                                'status': comment.status,
                                'timestamp': comment.timestamp,
                                'resolved_by': comment.resolved_by,
                                'metadata': comment.metadata
                            }
                            for comment in session.comments
                        ],
                        'feedback': [
                            {
                                'feedback_id': feedback.feedback_id,
                                'agent_id': feedback.agent_id,
                                'document_id': feedback.document_id,
                                'overall_rating': feedback.overall_rating,
                                'feedback_text': feedback.feedback_text,
                                'timestamp': feedback.timestamp,
                                'metadata': feedback.metadata
                            }
                            for feedback in session.feedback
                        ],
                        'votes': [
                            {
                                'vote_id': vote.vote_id,
                                'agent_id': vote.agent_id,
                                'document_id': vote.document_id,
                                'section_id': vote.section_id,
                                'vote_type': vote.vote_type,
                                'comment': vote.comment,
                                'timestamp': vote.timestamp,
                                'metadata': vote.metadata
                            }
                            for vote in session.votes
                        ],
                        'metadata': session.metadata
                    }
                    for session_id, session in self.review_sessions.items()
                }
            }
            
            with open(self.reviews_file, 'w') as f:
                json.dump(data, f, indent=2)
                
        except Exception as e:
            print(f"Error saving reviews: {e}")
            
    def load_reviews(self):
        """Load review sessions from file."""
        try:
            if not self.reviews_file.exists():
                return
                
            with open(self.reviews_file, 'r') as f:
                data = json.load(f)
                
            # Restore review sessions
            self.review_sessions.clear()
            for session_id, session_data in data.get('review_sessions', {}).items():
                comments = [
                    ReviewComment(
                        comment_id=comment_data['comment_id'],
                        agent_id=comment_data['agent_id'],
                        section_id=comment_data['section_id'],
                        comment_text=comment_data['comment_text'],
                        severity=comment_data['severity'],
                        status=comment_data.get('status', 'open'),
                        timestamp=comment_data['timestamp'],
                        resolved_by=comment_data.get('resolved_by', ''),
                        metadata=comment_data.get('metadata', {})
                    )
                    for comment_data in session_data.get('comments', [])
                ]
                
                feedback = [
                    ReviewFeedback(
                        feedback_id=feedback_data['feedback_id'],
                        agent_id=feedback_data['agent_id'],
                        document_id=feedback_data['document_id'],
                        overall_rating=feedback_data['overall_rating'],
                        feedback_text=feedback_data['feedback_text'],
                        timestamp=feedback_data['timestamp'],
                        metadata=feedback_data.get('metadata', {})
                    )
                    for feedback_data in session_data.get('feedback', [])
                ]
                
                votes = [
                    ReviewVote(
                        vote_id=vote_data['vote_id'],
                        agent_id=vote_data['agent_id'],
                        document_id=vote_data['document_id'],
                        section_id=vote_data['section_id'],
                        vote_type=vote_data['vote_type'],
                        comment=vote_data.get('comment', ''),
                        timestamp=vote_data['timestamp'],
                        metadata=vote_data.get('metadata', {})
                    )
                    for vote_data in session_data.get('votes', [])
                ]
                
                session = ReviewSession(
                    session_id=session_data['session_id'],
                    document_id=session_data['document_id'],
                    reviewers=session_data['reviewers'],
                    status=session_data['status'],
                    start_time=session_data['start_time'],
                    end_time=session_data['end_time'],
                    comments=comments,
                    feedback=feedback,
                    votes=votes,
                    metadata=session_data.get('metadata', {})
                )
                
                self.review_sessions[session_id] = session
                
            # Rebuild indexes
            self.agent_reviews.clear()
            self.document_reviews.clear()
            
            for session_id, session in self.review_sessions.items():
                for reviewer in session.reviewers:
                    self.agent_reviews[reviewer].append(session_id)
                self.document_reviews[session.document_id].append(session_id)
                
        except Exception as e:
            print(f"Error loading reviews: {e}")


class ReviewDashboard:
    def __init__(self, review_manager: ConcurrentReviewManager):
        self.review_manager = review_manager
        
    def display_session_overview(self, session_id: str):
        """Display overview of a review session."""
        session = self.review_manager.get_review_session(session_id)
        if not session:
            print(f"Review session '{session_id}' not found")
            return
            
        progress = self.review_manager.get_session_progress(session_id)
        consensus = self.review_manager.get_review_consensus(session_id)
        comment_summary = self.review_manager.get_comment_summary(session_id)
        voting_results = self.review_manager.get_voting_results(session_id)
        
        print(f"\nReview Session Overview - {session_id}")
        print("=" * 45)
        print(f"Document ID: {session.document_id}")
        print(f"Status: {session.status}")
        print(f"Reviewers: {len(session.reviewers)} ({', '.join(session.reviewers)})")
        print(f"Duration: {progress.get('duration_seconds', 0):.1f} seconds")
        
        print(f"\nProgress:")
        print(f"  Participation Rate: {progress.get('participation_rate', 0):.1%}")
        print(f"  Reviewers with Votes: {progress.get('reviewers_with_votes', 0)}/{len(session.reviewers)}")
        print(f"  Reviewers with Feedback: {progress.get('reviewers_with_feedback', 0)}/{len(session.reviewers)}")
        
        print(f"\nConsensus:")
        print(f"  Participation Consensus: {consensus.get('participation_consensus', 0):.1%}")
        print(f"  Approval Rate: {consensus.get('approval_rate', 0):.1%}")
        print(f"  Average Rating: {consensus.get('average_rating', 0):.1f}/5")
        print(f"  Consensus Strength: {consensus.get('consensus_strength', 0):.1%}")
        
        print(f"\nComments:")
        print(f"  Total: {comment_summary.get('total_comments', 0)}")
        print(f"  Open: {comment_summary.get('open_comments', 0)}")
        print(f"  Resolved: {comment_summary.get('resolved_comments', 0)}")
        print(f"  Severity Breakdown: {comment_summary.get('severity_breakdown', {})}")
        
        print(f"\nVoting Results:")
        print(f"  Total Votes: {voting_results.get('total_votes', 0)}")
        print(f"  Reviewers Participated: {voting_results.get('reviewers_participated', 0)}/{len(session.reviewers)}")
        
        section_consensus = voting_results.get('section_consensus', {})
        if section_consensus:
            print(f"  Section Consensus:")
            for section_id, result in section_consensus.items():
                print(f"    {section_id}: {result.get('consensus', 'no_votes')} "
                      f"({result.get('confidence', 0):.1%} confidence)")
                
    def display_session_comments(self, session_id: str):
        """Display comments for a review session."""
        session = self.review_manager.get_review_session(session_id)
        if not session:
            print(f"Review session '{session_id}' not found")
            return
            
        comments = self.review_manager.get_session_comments(session_id)
        
        print(f"\nReview Comments - Session {session_id}")
        print("=" * 40)
        
        if not comments:
            print("No comments found")
            return
            
        for i, comment in enumerate(comments, 1):
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(comment.timestamp))
            print(f"\n{i}. [{comment.severity.upper()}] {comment.agent_id} on {comment.section_id}")
            print(f"   Status: {comment.status}")
            print(f"   Time: {timestamp}")
            print(f"   Comment: {comment.comment_text}")
            if comment.status == "resolved":
                print(f"   Resolved by: {comment.resolved_by}")
                
    def display_session_votes(self, session_id: str):
        """Display votes for a review session."""
        session = self.review_manager.get_review_session(session_id)
        if not session:
            print(f"Review session '{session_id}' not found")
            return
            
        votes = self.review_manager.get_session_votes(session_id)
        
        print(f"\nReview Votes - Session {session_id}")
        print("=" * 35)
        
        if not votes:
            print("No votes found")
            return
            
        # Group votes by section
        section_votes = defaultdict(list)
        for vote in votes:
            section_votes[vote.section_id].append(vote)
            
        for section_id, section_vote_list in section_votes.items():
            print(f"\nSection: {section_id}")
            vote_counts = defaultdict(int)
            for vote in section_vote_list:
                vote_counts[vote.vote_type] += 1
                
            for vote_type, count in vote_counts.items():
                print(f"  {vote_type}: {count}")
                
            print(f"  Total: {len(section_vote_list)}")
            
            # Show individual votes
            print(f"  Individual Votes:")
            for vote in section_vote_list:
                timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(vote.timestamp))
                print(f"    {vote.agent_id}: {vote.vote_type} - {timestamp}")
                if vote.comment:
                    print(f"      Comment: {vote.comment}")
                    
    def display_session_feedback(self, session_id: str):
        """Display feedback for a review session."""
        session = self.review_manager.get_review_session(session_id)
        if not session:
            print(f"Review session '{session_id}' not found")
            return
            
        feedback_list = self.review_manager.get_session_feedback(session_id)
        feedback_summary = self.review_manager.get_feedback_summary(session_id)
        
        print(f"\nReview Feedback - Session {session_id}")
        print("=" * 37)
        
        print(f"Average Rating: {feedback_summary.get('average_rating', 0):.1f}/5")
        print(f"Total Feedback: {feedback_summary.get('total_feedback', 0)}")
        print(f"Rating Breakdown: {feedback_summary.get('rating_breakdown', {})}")
        
        if not feedback_list:
            print("\nNo detailed feedback found")
            return
            
        print(f"\nDetailed Feedback:")
        for i, feedback in enumerate(feedback_list, 1):
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(feedback.timestamp))
            print(f"\n{i}. {feedback.agent_id} - {feedback.overall_rating}/5")
            print(f"   Time: {timestamp}")
            print(f"   Feedback: {feedback.feedback_text}")
            
    def display_agent_review_sessions(self, agent_id: str):
        """Display all review sessions for an agent."""
        sessions = self.review_manager.get_sessions_for_agent(agent_id)
        
        print(f"\nReview Sessions for Agent {agent_id}")
        print("=" * 38)
        
        if not sessions:
            print("No review sessions found")
            return
            
        for session in sessions:
            progress = self.review_manager.get_session_progress(session.session_id)
            print(f"\nSession: {session.session_id}")
            print(f"  Document: {session.document_id}")
            print(f"  Status: {session.status}")
            print(f"  Participation: {progress.get('participation_rate', 0):.1%}")


def main():
    # Example usage
    print("Concurrent Review Workflows")
    print("=" * 28)
    
    # Create review manager and dashboard
    review_manager = ConcurrentReviewManager()
    dashboard = ReviewDashboard(review_manager)
    
    print("Concurrent review system initialized")
    print("System ready for multiple agents to review documentation simultaneously")
    
    # Example of what the workflow would look like:
    print("\nExample workflow:")
    print("  1. Start concurrent review sessions with multiple reviewers")
    print("  2. Agents add comments, votes, and feedback in parallel")
    print("  3. Track progress and participation in real-time")
    print("  4. Calculate consensus and voting results")
    print("  5. Resolve comments and finalize reviews")


if __name__ == "__main__":
    main()