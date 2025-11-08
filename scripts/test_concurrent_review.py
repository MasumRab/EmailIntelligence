#!/usr/bin/env python3
"""
Test script for concurrent review workflows system
"""

import time
import tempfile
from pathlib import Path
from concurrent_review import ConcurrentReviewManager, ReviewDashboard


def test_review_session_creation():
    """Test creating review sessions."""
    print("Testing review session creation...")

    # Create temporary directory for test files
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        reviews_file = tmp_path / ".test_concurrent_reviews.json"

        # Initialize review manager
        review_manager = ConcurrentReviewManager(reviews_file=reviews_file)

        # Create a review session
        session_id = review_manager.start_review_session(
            document_id="test-doc-1",
            reviewers=["agent-1", "agent-2", "agent-3"]
        )

        print(f"Created session ID: {session_id}")

        # Verify session was created
        assert session_id != "", "Should have created a session ID"

        # Get the session
        session = review_manager.get_review_session(session_id)
        assert session is not None, "Should retrieve created session"
        assert session.session_id == session_id, "Session ID should match"
        assert session.document_id == "test-doc-1", "Document ID should match"
        assert len(session.reviewers) == 3, "Should have 3 reviewers"
        assert session.status == "pending", "Status should be pending"

        # Update session status
        success = review_manager.start_session_review(session_id)
        assert success, "Should start session review"

        session = review_manager.get_review_session(session_id)
        assert session.status == "in_progress", "Status should be in_progress"

        print("✓ Review session creation test passed")


def test_adding_comments():
    """Test adding comments to review sessions."""
    print("\nTesting adding comments to review sessions...")

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        reviews_file = tmp_path / ".test_concurrent_reviews.json"

        # Initialize review manager
        review_manager = ConcurrentReviewManager(reviews_file=reviews_file)

        # Create a review session
        session_id = review_manager.start_review_session(
            document_id="comment-doc-1",
            reviewers=["agent-1", "agent-2"]
        )

        # Add comments
        comment_id_1 = review_manager.add_comment(
            session_id=session_id,
            agent_id="agent-1",
            section_id="section-1",
            comment_text="This section needs more detail.",
            severity="medium"
        )

        comment_id_2 = review_manager.add_comment(
            session_id=session_id,
            agent_id="agent-2",
            section_id="section-2",
            comment_text="There's a typo here: 'recieve' should be 'receive'.",
            severity="high"
        )

        # Verify comments were added
        assert comment_id_1 != "", "Should return comment ID"
        assert comment_id_2 != "", "Should return comment ID"

        # Get session comments
        comments = review_manager.get_session_comments(session_id)
        assert len(comments) == 2, "Should have 2 comments"

        # Find specific comments
        comment_1 = None
        comment_2 = None
        for comment in comments:
            if comment.comment_id == comment_id_1:
                comment_1 = comment
            elif comment.comment_id == comment_id_2:
                comment_2 = comment

        assert comment_1 is not None, "Should find first comment"
        assert comment_2 is not None, "Should find second comment"
        assert comment_1.comment_text == "This section needs more detail.", "Comment text should match"
        assert comment_2.severity == "high", "Severity should match"
        assert comment_1.agent_id == "agent-1", "Agent ID should match"
        assert comment_2.section_id == "section-2", "Section ID should match"

        print("✓ Adding comments test passed")


def test_resolving_comments():
    """Test resolving comments."""
    print("\nTesting resolving comments...")

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        reviews_file = tmp_path / ".test_concurrent_reviews.json"

        # Initialize review manager
        review_manager = ConcurrentReviewManager(reviews_file=reviews_file)

        # Create a review session and add a comment
        session_id = review_manager.start_review_session(
            document_id="resolve-doc-1",
            reviewers=["agent-1"]
        )

        comment_id = review_manager.add_comment(
            session_id=session_id,
            agent_id="agent-1",
            section_id="section-1",
            comment_text="This needs review.",
            severity="medium"
        )

        # Verify comment is open initially
        comments = review_manager.get_session_comments(session_id)
        open_comments = [c for c in comments if c.status == "open"]
        assert len(open_comments) == 1, "Should have 1 open comment"

        # Resolve the comment
        resolved = review_manager.resolve_comment(session_id, comment_id, "agent-2")
        assert resolved, "Should resolve comment successfully"

        # Verify comment is now resolved
        comments = review_manager.get_session_comments(session_id)
        open_comments = [c for c in comments if c.status == "open"]
        resolved_comments = [c for c in comments if c.status == "resolved"]

        assert len(open_comments) == 0, "Should have 0 open comments"
        assert len(resolved_comments) == 1, "Should have 1 resolved comment"
        assert resolved_comments[0].resolved_by == "agent-2", "Resolved by should match"

        print("✓ Resolving comments test passed")


def test_adding_feedback():
    """Test adding feedback to review sessions."""
    print("\nTesting adding feedback to review sessions...")

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        reviews_file = tmp_path / ".test_concurrent_reviews.json"

        # Initialize review manager
        review_manager = ConcurrentReviewManager(reviews_file=reviews_file)

        # Create a review session
        session_id = review_manager.start_review_session(
            document_id="feedback-doc-1",
            reviewers=["agent-1", "agent-2"]
        )

        # Add feedback
        feedback_id_1 = review_manager.add_feedback(
            session_id=session_id,
            agent_id="agent-1",
            document_id="feedback-doc-1",
            overall_rating=4,
            feedback_text="Good documentation overall, but needs more examples."
        )

        feedback_id_2 = review_manager.add_feedback(
            session_id=session_id,
            agent_id="agent-2",
            document_id="feedback-doc-1",
            overall_rating=5,
            feedback_text="Excellent work, very clear and comprehensive."
        )

        # Verify feedback was added
        assert feedback_id_1 != "", "Should return feedback ID"
        assert feedback_id_2 != "", "Should return feedback ID"

        # Get session feedback
        feedback_list = review_manager.get_session_feedback(session_id)
        assert len(feedback_list) == 2, "Should have 2 feedback items"

        # Get feedback summary
        feedback_summary = review_manager.get_feedback_summary(session_id)
        assert feedback_summary['total_feedback'] == 2, "Should have 2 feedback items"
        assert feedback_summary['average_rating'] == 4.5, "Average rating should be 4.5"

        print("✓ Adding feedback test passed")


def test_adding_votes():
    """Test adding votes to review sessions."""
    print("\nTesting adding votes to review sessions...")

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        reviews_file = tmp_path / ".test_concurrent_reviews.json"

        # Initialize review manager
        review_manager = ConcurrentReviewManager(reviews_file=reviews_file)

        # Create a review session
        session_id = review_manager.start_review_session(
            document_id="vote-doc-1",
            reviewers=["agent-1", "agent-2", "agent-3"]
        )

        # Add votes
        vote_id_1 = review_manager.add_vote(
            session_id=session_id,
            agent_id="agent-1",
            document_id="vote-doc-1",
            section_id="section-1",
            vote_type="approve"
        )

        vote_id_2 = review_manager.add_vote(
            session_id=session_id,
            agent_id="agent-2",
            document_id="vote-doc-1",
            section_id="section-1",
            vote_type="request_changes",
            comment="Need more details in this section"
        )

        vote_id_3 = review_manager.add_vote(
            session_id=session_id,
            agent_id="agent-3",
            document_id="vote-doc-1",
            section_id="section-2",
            vote_type="approve"
        )

        # Verify votes were added
        assert vote_id_1 != "", "Should return vote ID"
        assert vote_id_2 != "", "Should return vote ID"
        assert vote_id_3 != "", "Should return vote ID"

        # Get session votes
        votes = review_manager.get_session_votes(session_id)
        assert len(votes) == 3, "Should have 3 votes"

        # Get voting results
        voting_results = review_manager.get_voting_results(session_id)
        assert voting_results['total_votes'] == 3, "Should have 3 total votes"
        assert voting_results['reviewers_participated'] == 3, "Should have 3 reviewers participated"

        print("✓ Adding votes test passed")


def test_comment_summary():
    """Test comment summary functionality."""
    print("\nTesting comment summary functionality...")

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        reviews_file = tmp_path / ".test_concurrent_reviews.json"

        # Initialize review manager
        review_manager = ConcurrentReviewManager(reviews_file=reviews_file)

        # Create a review session and add comments
        session_id = review_manager.start_review_session(
            document_id="summary-doc-1",
            reviewers=["agent-1", "agent-2"]
        )

        # Add various comments with different severities
        review_manager.add_comment(
            session_id=session_id,
            agent_id="agent-1",
            section_id="section-1",
            comment_text="Low priority issue",
            severity="low"
        )

        review_manager.add_comment(
            session_id=session_id,
            agent_id="agent-2",
            section_id="section-1",
            comment_text="High priority issue",
            severity="high"
        )

        review_manager.add_comment(
            session_id=session_id,
            agent_id="agent-1",
            section_id="section-2",
            comment_text="Medium priority issue",
            severity="medium"
        )

        # Add one more comment and resolve it
        comment_id = review_manager.add_comment(
            session_id=session_id,
            agent_id="agent-2",
            section_id="section-2",
            comment_text="Another issue",
            severity="low"
        )
        review_manager.resolve_comment(session_id, comment_id, "agent-1")

        # Get comment summary
        comment_summary = review_manager.get_comment_summary(session_id)

        print(f"Comment summary: {comment_summary}")

        assert comment_summary['total_comments'] == 4, "Should have 4 total comments"
        assert comment_summary['resolved_comments'] == 1, "Should have 1 resolved comment"
        assert comment_summary['open_comments'] == 3, "Should have 3 open comments"
        assert comment_summary['severity_breakdown']['low'] == 2, "Should have 2 low severity comments"
        assert comment_summary['severity_breakdown']['medium'] == 1, "Should have 1 medium severity comment"
        assert comment_summary['severity_breakdown']['high'] == 1, "Should have 1 high severity comment"

        print("✓ Comment summary functionality test passed")


def test_voting_results():
    """Test voting results calculation."""
    print("\nTesting voting results calculation...")

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        reviews_file = tmp_path / ".test_concurrent_reviews.json"

        # Initialize review manager
        review_manager = ConcurrentReviewManager(reviews_file=reviews_file)

        # Create a review session and add votes
        session_id = review_manager.start_review_session(
            document_id="voting-results-doc-1",
            reviewers=["agent-1", "agent-2", "agent-3", "agent-4"]
        )

        # Add votes for section-1
        review_manager.add_vote(
            session_id=session_id,
            agent_id="agent-1",
            document_id="voting-results-doc-1",
            section_id="section-1",
            vote_type="approve"
        )

        review_manager.add_vote(
            session_id=session_id,
            agent_id="agent-2",
            document_id="voting-results-doc-1",
            section_id="section-1",
            vote_type="approve"
        )

        review_manager.add_vote(
            session_id=session_id,
            agent_id="agent-3",
            document_id="voting-results-doc-1",
            section_id="section-1",
            vote_type="reject"
        )

        # Add votes for section-2
        review_manager.add_vote(
            session_id=session_id,
            agent_id="agent-1",
            document_id="voting-results-doc-1",
            section_id="section-2",
            vote_type="approve"
        )

        review_manager.add_vote(
            session_id=session_id,
            agent_id="agent-4",
            document_id="voting-results-doc-1",
            section_id="section-2",
            vote_type="approve"
        )

        # Get voting results
        voting_results = review_manager.get_voting_results(session_id)

        print(f"Voting results: {voting_results}")

        assert voting_results['total_votes'] == 5, "Should have 5 total votes"
        assert voting_results['reviewers_participated'] == 4, "Should have 4 reviewers participated"

        section_consensus = voting_results['section_consensus']
        assert 'section-1' in section_consensus, "Should have consensus for section-1"
        assert 'section-2' in section_consensus, "Should have consensus for section-2"

        # Section-1 should have approve: 2, reject: 1
        section1_results = section_consensus['section-1']
        assert section1_results['total_votes'] == 3, "Section-1 should have 3 votes"
        assert section1_results['vote_breakdown']['approve'] == 2, "Section-1 should have 2 approve votes"
        assert section1_results['vote_breakdown']['reject'] == 1, "Section-1 should have 1 reject vote"

        # Section-2 should have approve: 2
        section2_results = section_consensus['section-2']
        assert section2_results['total_votes'] == 2, "Section-2 should have 2 votes"
        assert section2_results['vote_breakdown']['approve'] == 2, "Section-2 should have 2 approve votes"

        print("✓ Voting results calculation test passed")


def test_session_progress():
    """Test session progress tracking."""
    print("\nTesting session progress tracking...")

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        reviews_file = tmp_path / ".test_concurrent_reviews.json"

        # Initialize review manager
        review_manager = ConcurrentReviewManager(reviews_file=reviews_file)

        # Create a review session
        session_id = review_manager.start_review_session(
            document_id="progress-doc-1",
            reviewers=["agent-1", "agent-2", "agent-3"]
        )

        # Get initial progress
        progress = review_manager.get_session_progress(session_id)

        print(f"Initial progress: {progress}")

        assert progress['total_reviewers'] == 3, "Should have 3 total reviewers"
        assert progress['reviewers_with_votes'] == 0, "Should have 0 reviewers with votes initially"
        assert progress['reviewers_with_feedback'] == 0, "Should have 0 reviewers with feedback initially"

        # Add some votes and feedback
        review_manager.add_vote(
            session_id=session_id,
            agent_id="agent-1",
            document_id="progress-doc-1",
            section_id="section-1",
            vote_type="approve"
        )

        review_manager.add_feedback(
            session_id=session_id,
            agent_id="agent-2",
            document_id="progress-doc-1",
            overall_rating=4,
            feedback_text="Good work"
        )

        # Get updated progress
        updated_progress = review_manager.get_session_progress(session_id)

        print(f"Updated progress: {updated_progress}")

        assert updated_progress['reviewers_with_votes'] == 1, "Should have 1 reviewer with votes"
        assert updated_progress['reviewers_with_feedback'] == 1, "Should have 1 reviewer with feedback"
        assert updated_progress['participation_rate'] > 0, "Participation rate should be > 0"

        print("✓ Session progress tracking test passed")


def test_review_consensus():
    """Test review consensus calculation."""
    print("\nTesting review consensus calculation...")

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        reviews_file = tmp_path / ".test_concurrent_reviews.json"

        # Initialize review manager
        review_manager = ConcurrentReviewManager(reviews_file=reviews_file)

        # Start a review session
        reviewers = ["agent-1", "agent-2", "agent-3"]
        session_id = review_manager.start_review_session(
            document_id="consensus-test-doc",
            reviewers=reviewers
        )

        # Add votes from all reviewers
        review_manager.add_vote(
            session_id=session_id,
            agent_id="agent-1",
            document_id="consensus-test-doc",
            section_id="section-1",
            vote_type="approve"
        )

        review_manager.add_vote(
            session_id=session_id,
            agent_id="agent-2",
            document_id="consensus-test-doc",
            section_id="section-1",
            vote_type="approve"
        )

        review_manager.add_vote(
            session_id=session_id,
            agent_id="agent-3",
            document_id="consensus-test-doc",
            section_id="section-1",
            vote_type="approve"
        )

        # Add feedback from all reviewers
        for i, agent in enumerate(reviewers, 1):
            review_manager.add_feedback(
                session_id=session_id,
                agent_id=agent,
                document_id="consensus-test-doc",
                overall_rating=5,
                feedback_text=f"Excellent work from {agent}"
            )

        # Get consensus
        consensus = review_manager.get_review_consensus(session_id)
        assert consensus['total_participants'] == 3, "Should have 3 participants"
        assert consensus['total_reviewers'] == 3, "Should have 3 total reviewers"
        assert consensus['participation_consensus'] == 1.0, "Participation consensus should be 100%"
        assert consensus['average_rating'] == 5.0, "Average rating should be 5.0"

        print("✓ Review consensus calculation test passed")


def test_review_persistence():
    """Test review data persistence."""
    print("\nTesting review data persistence...")

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        reviews_file = tmp_path / ".test_persistence_reviews.json"

        # Initialize review manager and add data
        review_manager1 = ConcurrentReviewManager(reviews_file=reviews_file)

        # Create a review session
        session_id = review_manager1.start_review_session(
            document_id="persistence-doc-1",
            reviewers=["agent-1", "agent-2"]
        )

        # Add some data
        review_manager1.add_comment(
            session_id=session_id,
            agent_id="agent-1",
            section_id="section-1",
            comment_text="Persistence test comment",
            severity="medium"
        )

        review_manager1.add_feedback(
            session_id=session_id,
            agent_id="agent-2",
            document_id="persistence-doc-1",
            overall_rating=4,
            feedback_text="Persistence test feedback"
        )

        review_manager1.add_vote(
            session_id=session_id,
            agent_id="agent-1",
            document_id="persistence-doc-1",
            section_id="section-1",
            vote_type="approve"
        )

        # Create new review manager and load data
        review_manager2 = ConcurrentReviewManager(reviews_file=reviews_file)

        # Verify data was loaded correctly
        loaded_session = review_manager2.get_review_session(session_id)
        assert loaded_session is not None, "Should load session"
        assert loaded_session.document_id == "persistence-doc-1", "Document ID should match"

        # Check comments
        comments = review_manager2.get_session_comments(session_id)
        assert len(comments) == 1, "Should have loaded 1 comment"
        assert comments[0].comment_text == "Persistence test comment", "Comment text should match"

        # Check feedback
        feedback = review_manager2.get_session_feedback(session_id)
        assert len(feedback) == 1, "Should have loaded 1 feedback"
        assert feedback[0].feedback_text == "Persistence test feedback", "Feedback text should match"

        # Check votes
        votes = review_manager2.get_session_votes(session_id)
        assert len(votes) == 1, "Should have loaded 1 vote"
        assert votes[0].vote_type == "approve", "Vote type should match"

        print("✓ Review data persistence test passed")


def test_review_dashboard():
    """Test review dashboard functionality."""
    print("\nTesting review dashboard functionality...")

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        reviews_file = tmp_path / ".test_concurrent_reviews.json"

        # Initialize review manager and dashboard
        review_manager = ConcurrentReviewManager(reviews_file=reviews_file)
        dashboard = ReviewDashboard(review_manager)

        # Create a review session
        session_id = review_manager.start_review_session(
            document_id="dashboard-doc-1",
            reviewers=["agent-1", "agent-2", "agent-3"]
        )

        # Add some data
        review_manager.add_comment(
            session_id=session_id,
            agent_id="agent-1",
            section_id="section-1",
            comment_text="Dashboard test comment",
            severity="high"
        )

        review_manager.add_feedback(
            session_id=session_id,
            agent_id="agent-2",
            document_id="dashboard-doc-1",
            overall_rating=3,
            feedback_text="Dashboard test feedback"
        )

        review_manager.add_vote(
            session_id=session_id,
            agent_id="agent-3",
            document_id="dashboard-doc-1",
            section_id="section-1",
            vote_type="request_changes",
            comment="Needs more detail"
        )

        # Test dashboard methods (should not crash)
        dashboard.display_session_overview(session_id)
        dashboard.display_session_comments(session_id)
        dashboard.display_session_votes(session_id)
        dashboard.display_session_feedback(session_id)
        dashboard.display_agent_review_sessions("agent-1")

        print("✓ Review dashboard functionality test passed")


def main():
    """Run all tests."""
    print("Running Concurrent Review Workflows Tests")
    print("=" * 45)

    try:
        test_review_session_creation()
        test_adding_comments()
        test_resolving_comments()
        test_adding_feedback()
        test_adding_votes()
        test_comment_summary()
        test_voting_results()
        test_session_progress()
        test_review_consensus()
        test_review_persistence()
        test_review_dashboard()

        print("\n" + "=" * 45)
        print("All tests passed! ✓")

    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        raise


if __name__ == "__main__":
    main()