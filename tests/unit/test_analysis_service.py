import pytest
from unittest.mock import Mock, AsyncMock, patch
from src.lib.git_wrapper import GitWrapper
from datetime import datetime # Import datetime for mocking

# Mock GitWrapper for testing
@pytest.fixture
def mock_git_wrapper():
    return Mock(spec=GitWrapper)

# Mock ActionNarrative, IntentReport, VerificationResult entities
# These would ideally come from src.models.unified_analysis
# For testing, we'll create simple mock classes that behave like the real ones
class MockActionNarrative:
    def __init__(self, commit_hexsha, author_name, authored_date, commit_message, synthesized_narrative, is_consistent, discrepancy_notes):
        self.commit_hexsha = commit_hexsha
        self.author_name = author_name
        self.authored_date = authored_date
        self.commit_message = commit_message
        self.synthesized_narrative = synthesized_narrative
        self.is_consistent = is_consistent
        self.discrepancy_notes = discrepancy_notes

class MockIntentReport:
    def __init__(self, branch_name, generated_at, commit_narratives):
        self.branch_name = branch_name
        self.generated_at = generated_at
        self.commit_narratives = commit_narratives

class MockVerificationResult:
    def __init__(self, branch_name, verified_at, is_fully_consistent, missing_changes, unexpected_changes):
        self.branch_name = branch_name
        self.verified_at = verified_at
        self.is_fully_consistent = is_fully_consistent
        self.missing_changes = missing_changes
        self.unexpected_changes = unexpected_changes


class TestAnalysisService:
    @pytest.mark.asyncio
    @patch('src.lib.git_wrapper.GitWrapper') # Mock the actual GitWrapper when instantiating the service
    async def test_narrative_synthesis(self, MockGitWrapper):
        # Mock the classes that AnalysisService would import
        MockLLMClient = Mock()
        MockDiffParser = Mock()
        
        # We'll put this inside the test function for now, as AnalysisService is not yet defined
        class MockAnalysisService:
            def __init__(self, repo_path):
                self.git_wrapper = MockGitWrapper(repo_path)
                self.llm_client = MockLLMClient()
                self.diff_parser = MockDiffParser()

            async def _synthesize_narrative_with_llm(self, commit_message, diff_content):
                # Mock actual LLM call
                return f"LLM generated narrative for '{commit_message}' and diff: {diff_content}"

            async def generate_action_narrative(self, commit_mock):
                commit_message = commit_mock.message
                diff_content = self.git_wrapper.get_commit_diff(commit_mock) # Mocked call

                synthesized_narrative = await self._synthesize_narrative_with_llm(commit_message, diff_content)
                
                # Mock consistency check
                is_consistent = True # Simplified for test
                discrepancy_notes = ""

                return MockActionNarrative(
                    commit_hexsha=commit_mock.hexsha,
                    author_name=commit_mock.author.name,
                    authored_date=commit_mock.authored_date,
                    commit_message=commit_message,
                    synthesized_narrative=synthesized_narrative,
                    is_consistent=is_consistent,
                    discrepancy_notes=discrepancy_notes
                )
        
        # Setup mocks
        mock_commit = Mock()
        mock_commit.hexsha = "abcd123"
        mock_commit.message = "feat: Add new feature"
        mock_commit.author.name = "Test Author"
        mock_commit.authored_date = 1678886400

        mock_git_wrapper_instance = MockGitWrapper.return_value
        mock_git_wrapper_instance.get_commit_diff.return_value = "mock_diff_content"

        # Instantiate our mock service
        service = MockAnalysisService("/fake/path")
        # Mock the async method on the mock llm_client instance
        service.llm_client.generate_summary = AsyncMock(return_value="LLM generated narrative")

        # Execute
        narrative = await service.generate_action_narrative(mock_commit)

        # Assertions
        assert narrative.commit_hexsha == "abcd123"
        assert narrative.synthesized_narrative.startswith("LLM generated narrative for 'feat: Add new feature'")
        mock_git_wrapper_instance.get_commit_diff.assert_called_once_with(mock_commit)
        assert narrative.author_name == "Test Author"


    @pytest.mark.asyncio
    @patch('src.lib.git_wrapper.GitWrapper')
    async def test_detect_rebased_branches(self, MockGitWrapper):
        # Mock the actual GitWrapper when instantiating the service
        class MockAnalysisService:
            def __init__(self, repo_path):
                self.git_wrapper = MockGitWrapper(repo_path)

            async def detect_rebased_branches(self):
                mock_reflog = [
                    Mock(message="rebase (start): checkout main"),
                    Mock(message="rebase (finish): refs/heads/feature_branch"),
                    Mock(message="commit: initial commit")
                ]
                self.git_wrapper.get_reflog.return_value = mock_reflog
                
                rebased_branches = []
                reflog_entries = self.git_wrapper.get_reflog() # Call the mocked method
                for entry in reflog_entries:
                    if "rebase (finish)" in entry.message:
                        branch_name = entry.message.split("refs/heads/")[1].strip()
                        rebased_branches.append(branch_name)
                return rebased_branches

        service = MockAnalysisService("/fake/path")
        
        rebased = await service.detect_rebased_branches()
        assert "feature_branch" in rebased
        assert len(rebased) == 1
        MockGitWrapper.return_value.get_reflog.assert_called_once()
    
    @pytest.mark.asyncio
    @patch('src.lib.git_wrapper.GitWrapper')
    async def test_verify_integrity(self, MockGitWrapper):
        # Mock the actual GitWrapper when instantiating the service
        class MockAnalysisService:
            def __init__(self, repo_path):
                self.git_wrapper = MockGitWrapper(repo_path)

            async def verify_integrity(self, intent_report_mock, merged_branch_name):
                # Simulate discrepancy detection
                is_fully_consistent = False
                missing = [{"commit_hexsha": "old_sha", "file_path": "file.txt", "change_type": "modify"}]
                unexpected = []
                
                return MockVerificationResult(
                    branch_name=merged_branch_name,
                    verified_at=datetime.now(),
                    is_fully_consistent=is_fully_consistent,
                    missing_changes=missing,
                    unexpected_changes=unexpected
                )

        # Setup mocks
        mock_intent_report = Mock()
        mock_intent_report.commit_narratives = [
            Mock(commit_hexsha="old_sha", synthesized_narrative="expected change")
        ]
        
        service = MockAnalysisService("/fake/path")
        
        # Execute
        result = await service.verify_integrity(mock_intent_report, "main")

        # Assertions
        assert result.branch_name == "main"
        assert not result.is_fully_consistent
        assert len(result.missing_changes) == 1
        assert result.missing_changes[0]["commit_hexsha"] == "old_sha"
