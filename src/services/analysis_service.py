import git
import re
from datetime import datetime
from typing import List, Dict, Any, Optional
from tqdm.asyncio import tqdm # Import tqdm for async operations

from src.lib.git_wrapper import GitWrapper
from src.models.unified_analysis import ActionNarrative, IntentReport, VerificationResult

# Placeholder for LLMClient and DiffParser, which would be implemented in src/lib/
class LLMClient:
    async def generate_summary(self, text: str) -> str:
        # Mock LLM response for now
        return f"LLM Summary: {text[:100]}..."

class DiffParser:
    def prioritize_code_changes(self, diff_content: str) -> str:
        """
        TODO: Implement a full-featured diff prioritization logic.

        This method should analyze the raw Git diff content and identify the most
        semantically significant changes, filtering out noise and less impactful
        modifications.

        Key considerations for a full implementation:
        1.  **Language-Specific Parsing:** Utilize AST (Abstract Syntax Tree) parsing
            for different programming languages (e.g., Python's `ast` module, Tree-sitter)
            to understand the code structure.
        2.  **Filtering Noise:**
            *   **Whitespace/Formatting:** Ignore changes that are purely whitespace,
                indentation, or minor formatting (e.g., from linters).
            *   **Comment-Only Changes:** Prioritize changes to executable code over
                changes to comments, unless comments are critical documentation.
        3.  **Focus on Semantic Changes:** Identify changes that alter the meaning or
            behavior of the code, such as:
            *   Modifications to function/method signatures (parameters, return types).
            *   Changes in class or interface definitions (adding/removing members, inheritance).
            *   Alterations to control flow statements (if/else conditions, loop bounds).
            *   Changes in variable declarations or assignments that impact logic.
            *   Modifications to API endpoints or data models.
            *   Changes in configuration files that alter system behavior.
        4.  **Heuristics:** Develop heuristics to weigh the importance of different
            types of changes. For example, a change in a core algorithm might be
            more significant than a change in a UI string.
        5.  **Contextual Analysis:** Consider the context of the change (e.g., changes
            in a test file vs. a production file).

        The output should be a concise, structured representation of the most important
        code changes, suitable for input to an LLM for narrative generation.
        """
        # Mock diff prioritization for now
        return f"Prioritized diff: {diff_content[:100]}..."

    def parse_diff_for_changes(self, diff_content: str) -> List[Dict[str, Any]]:
        """
        TODO: Implement robust diff parsing and intent inference.

        This method should parse a diff content to extract detailed changes
        (additions, deletions, modifications) and infer the high-level intent
        behind these changes.

        Key considerations for a full implementation:
        1.  **Granular Change Detection:** Instead of just 'modify', identify
            'add', 'delete', 'rename', 'move' for files, and more granular
            changes within files (e.g., 'function_added', 'variable_changed').
        2.  **Intent Inference:** Based on patterns of changes, infer the intent:
            *   **New Feature:** Adding new files, classes, functions, or significant
                blocks of code.
            *   **Bug Fix:** Changes concentrated in a specific area, especially
                within conditional logic or error handling.
            *   **Refactoring:** Restructuring code without changing external behavior.
            *   **Performance Optimization:** Changes related to algorithms, data structures.
            *   **Documentation/Tests:** Changes primarily in documentation or test files.
        3.  **Structured Output:** Each change should be a dict with:
            *   `file_path`: Path to the affected file.
            *   `change_type`: Granular type of change (e.g., 'add', 'delete', 'modify', 'rename', 'refactor').
            *   `inferred_intent`: High-level intent (e.g., 'new_feature', 'bug_fix').
            *   `line_numbers`: Specific line ranges affected.
            *   `code_snippet`: Relevant code snippets for context.
        4.  **Diff Parsing Libraries:** Consider using existing libraries that
            can parse Git diffs more effectively than simple string splitting.
        """
        changes = []
        current_file = None
        for line in diff_content.splitlines():
            if line.startswith("--- a/"):
                current_file = line[6:].strip()
            elif line.startswith("+++ b/"):
                if current_file:
                    # Assuming any change in a file means a 'modify' for now
                    changes.append({"file_path": current_file, "change_type": "modify"})
                current_file = None # Reset
        return changes


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
        commits = list(self.git_wrapper.get_commits(revision_range or branch_name)) # Convert to list to get length for tqdm
        
        commit_narratives: List[ActionNarrative] = []
        for commit in tqdm(commits, desc=f"Generating narratives for {branch_name}"):
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
            # As per spec, detect rebased branches by looking for "rebase (finish)" messages
            if "rebase (finish)" in entry.message:
                # Extract branch name from reflog message
                # Example: "rebase (finish): refs/heads/feature_branch"
                match = re.search(r"refs/heads/(\S+)", entry.message)
                if match:
                    branch_name = match.group(1)
                    if branch_name not in rebased_branches: # Avoid duplicates
                        rebased_branches.append(branch_name)
        return rebased_branches

    async def verify_integrity(self, intent_report: IntentReport, merged_branch_name: str) -> VerificationResult:
        missing_changes: List[Dict[str, Any]] = []
        unexpected_changes: List[Dict[str, Any]] = []
        is_fully_consistent = True

        # Get the actual state of the merged branch
        merged_branch_commits = list(self.git_wrapper.get_commits(merged_branch_name))
        
        # Simplified comparison:
        # For each narrative in the intent report, check if a similar change exists in the merged branch.
        # This is a very basic implementation and would need significant refinement for real-world use.
        
        # Collect all changes from the intent report
        expected_changes_map: Dict[str, List[Dict[str, Any]]] = {} # {commit_hexsha: [changes]}
        for narrative in tqdm(intent_report.commit_narratives, desc="Processing expected changes"):
            commit = self.git_wrapper.get_commit_by_hexsha(narrative.commit_hexsha)
            diff_content = str(self.git_wrapper.get_commit_diff(commit))
            expected_changes_map[narrative.commit_hexsha] = self.diff_parser.parse_diff_for_changes(diff_content)

        # Collect all changes from the merged branch
        actual_changes_map: Dict[str, List[Dict[str, Any]]] = {}
        for commit in tqdm(merged_branch_commits, desc="Processing actual changes"):
            diff_content = str(self.git_wrapper.get_commit_diff(commit))
            actual_changes_map[commit.hexsha] = self.diff_parser.parse_diff_for_changes(diff_content)

        # Compare expected vs actual changes
        # This is a very naive comparison and needs to be improved.
        # It currently just checks if commit SHAs exist and if their changes are present.
        # A robust implementation would compare actual file contents and diffs.

        expected_commit_shas = {n.commit_hexsha for n in intent_report.commit_narratives}
        actual_commit_shas = {c.hexsha for c in merged_branch_commits}

        # Check for missing commits/changes
        for expected_sha in expected_commit_shas:
            if expected_sha not in actual_commit_shas:
                is_fully_consistent = False
                # Add all changes from this missing commit to missing_changes
                for change in expected_changes_map.get(expected_sha, []):
                    missing_changes.append({
                        "commit_hexsha": expected_sha,
                        "file_path": change["file_path"],
                        "change_type": change["change_type"]
                    })
            else:
                # If commit exists, compare its changes (simplified)
                # This part needs a proper diff comparison
                pass # Placeholder for detailed change comparison

        # Check for unexpected commits/changes
        for actual_sha in actual_commit_shas:
            if actual_sha not in expected_commit_shas:
                is_fully_consistent = False
                # Add all changes from this unexpected commit to unexpected_changes
                for change in actual_changes_map.get(actual_sha, []):
                    unexpected_changes.append({
                        "commit_hexsha": actual_sha,
                        "file_path": change["file_path"],
                        "change_type": change["change_type"]
                    })
            else:
                # If commit exists, compare its changes (simplified)
                pass # Placeholder for detailed change comparison


        # If any discrepancies were found, set is_fully_consistent to False
        if missing_changes or unexpected_changes:
            is_fully_consistent = False
        else:
            is_fully_consistent = True # If no simple missing/unexpected commits, assume consistent for now


        return VerificationResult(
            branch_name=merged_branch_name,
            verified_at=datetime.now(),
            is_fully_consistent=is_fully_consistent,
            missing_changes=missing_changes,
            unexpected_changes=unexpected_changes
        )
