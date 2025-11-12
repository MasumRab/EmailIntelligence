import git
from datetime import datetime
from typing import List, Dict, Any, Optional

from src.lib.git_wrapper import GitWrapper
from src.models.unified_analysis import ActionNarrative, IntentReport, VerificationResult

# Placeholder for LLMClient and DiffParser, which would be implemented in src/lib/
class LLMClient:
    async def generate_summary(self, text: str) -> str:
        # Mock LLM response for now
        return f"LLM Summary: {text[:100]}..."

class DiffParser:
    def prioritize_code_changes(self, diff_content: str) -> str:
        # Mock diff prioritization for now
        return f"Prioritized diff: {diff_content[:100]}..."

class AnalysisService:
    def __init__(self, repo_path: str):
        self.git_wrapper = GitWrapper(repo_path)
        self.llm_client = LLMClient()
        self.diff_parser = DiffParser()

    async def generate_action_narrative(self, commit: git.Commit) -> ActionNarrative:
        commit_message = commit.message
        diff_content = self.git_wrapper.get_commit_diff(commit)

        # Prioritize code changes
        prioritized_diff = self.diff_parser.prioritize_code_changes(str(diff_content))

        # Use LLM to generate human-like summary
        llm_input = f"Commit Message: {commit_message}\nPrioritized Diff: {prioritized_diff}"
        synthesized_narrative = await self.llm_client.generate_summary(llm_input)

        # Determine consistency (simplified for initial implementation)
        is_consistent = True # Placeholder logic
        discrepancy_notes = ""

        return ActionNarrative(
            commit_hexsha=commit.hexsha,
            author_name=commit.author.name,
            authored_date=commit.authored_date,
            commit_message=commit_message,
            synthesized_narrative=synthesized_narrative,
            is_consistent=is_consistent,
            discrepancy_notes=discrepancy_notes
        )

    async def generate_intent_report(self, branch_name: str, revision_range: Optional[str] = None) -> IntentReport:
        commits = self.git_wrapper.get_commits(revision_range or branch_name)
        
        commit_narratives: List[ActionNarrative] = []
        for commit in commits:
            narrative = await self.generate_action_narrative(commit)
            commit_narratives.append(narrative)
        
        return IntentReport(
            branch_name=branch_name,
            generated_at=datetime.now(),
            commit_narratives=commit_narratives
        )

    async def detect_rebased_branches(self) -> List[str]:
        reflog_entries = self.git_wrapper.get_reflog()
        rebased_branches = []
        for entry in reflog_entries:
            if "rebase (finish)" in entry.message:
                # Extract branch name from reflog message
                match = re.search(r"refs/heads/(\S+)", entry.message)
                if match:
                    branch_name = match.group(1)
                    if branch_name not in rebased_branches:
                        rebased_branches.append(branch_name)
        return rebased_branches

    async def verify_integrity(self, intent_report: IntentReport, merged_branch_name: str) -> VerificationResult:
        # Placeholder for actual verification logic
        # This would involve comparing the intent_report against the actual merged_branch_name state
        # For now, simulate a discrepancy
        is_fully_consistent = False
        missing_changes = [
            {"commit_hexsha": "mock_missing_sha", "file_path": "mock_file.txt", "change_type": "modify"}
        ]
        unexpected_changes = []

        return VerificationResult(
            branch_name=merged_branch_name,
            verified_at=datetime.now(),
            is_fully_consistent=is_fully_consistent,
            missing_changes=missing_changes,
            unexpected_changes=unexpected_changes
        )
