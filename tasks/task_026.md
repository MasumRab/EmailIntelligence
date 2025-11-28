# Task ID: 26

**Title:** Restore Critical AI Agent and Workflow Documentation

**Status:** pending

**Dependencies:** 15 ✓

**Priority:** medium

**Description:** Restore multiple crucial documentation files, including AGENTS.md, GEMINI.md, CRUSH.md, IFLOW.md, LLXPRT.md, and associated workflow guides, which were lost due to a destructive revert.

**Details:**

1.  **Identify Target Files and Commit:** Pinpoint the specific versions of `AGENTS.md`, `GEMINI.md`, `CRUSH.md`, `IFLOW.md`, `LLXPRT.md`, and all relevant workflow guides that existed immediately prior to the destructive commit `2abe41e3` (or any subsequent commits that further removed them).
2.  **Utilize Version Control for Recovery:** Systematically use Git commands such as `git log --oneline --grep="2abe41e3" -- <file-path>`, `git reflog`, and `git checkout <commit-hash> -- <file-path>` to recover the content of each identified file. Prioritize recovering the most accurate and complete versions.
3.  **Content Reconstruction and Enhancement:** For any sections or entire documents where direct Git recovery is insufficient or content is significantly outdated, collaborate with product owners, AI engineers, and subject matter experts to reconstruct, rewrite, or update the information to reflect the current system state, agent capabilities, and operational procedures.
4.  **Documentation Scope and Focus:**
    *   **AGENTS.md:** Ensure this document comprehensively covers the overall AI agent architecture, available agents, their core functionalities, and common usage patterns.
    *   **GEMINI.md, CRUSH.md, IFLOW.md, LLXPRT.md:** For each model-specific documentation, detail their integration points, specific input/output requirements, model-specific instructions, known limitations, and best practices for their deployment and utilization.
    *   **Workflow Guides:** Recover and update critical development, deployment, and operational workflow guides that involve AI agents, detailing step-by-step procedures, required tools, and troubleshooting tips.
5.  **Adherence to Standards:** Ensure all restored and updated documentation adheres to the project's current documentation standards, including Markdown formatting, consistent terminology, clear headings, and well-structured code examples.
6.  **Placement:** Integrate the recovered and updated documentation into the appropriate and accessible directories within the project repository (e.g., `docs/agents/`, `docs/workflows/` or project root).

### Tags:
- `work_type:documentation-recovery`
- `work_type:content-restoration`
- `component:ai-agents`
- `component:workflow-guides`
- `scope:documentation`
- `scope:knowledge-management`
- `purpose:information-integrity`
- `purpose:developer-enablement`

**Test Strategy:**

1.  **File Presence and Location:** Verify that all specified documentation files (`AGENTS.md`, `GEMINI.md`, `CRUSH.md`, `IFLOW.md`, `LLXPRT.md`, and identified workflow guides) are present in their designated locations within the repository.
2.  **Content Accuracy and Completeness:** Conduct a thorough manual review of each restored document by at least two independent developers or subject matter experts. Validate that the content accurately reflects the current system architecture, agent functionalities, model behavior, and established workflows. Check for completeness against the expected scope of each document.
3.  **Readability and Clarity:** Assess the documentation for clarity, conciseness, and ease of understanding for both new and experienced team members. Ensure consistent language, grammar, and style.
4.  **Internal Consistency and Linking:** Verify that all internal links within and between the documentation files are functional and point to the correct sections or documents. Ensure cross-references are accurate.
5.  **Format and Standards Compliance:** Confirm that all documentation adheres to the defined project documentation standards, including Markdown syntax, code block formatting, and overall structure.
6.  **Stakeholder Review:** Obtain formal sign-off or feedback from relevant stakeholders (e.g., product owners, lead AI engineers, team leads) to ensure the restored documentation meets their operational and informational needs.

## Subtasks

### 26.1. Identify Target Document Versions and Commits

**Status:** pending  
**Dependencies:** None  

Precisely identify the specific versions of AGENTS.md, GEMINI.md, CRUSH.md, IFLOW.md, LLXPRT.md, and all relevant workflow guides that existed immediately prior to the destructive commit '2abe41e3', or any subsequent commits that further removed them. This involves deep diving into Git history.

**Details:**

Utilize Git commands such as `git log --oneline --grep="2abe41e3" -- <file-path>`, `git reflog`, and `git blame` to pinpoint the last known good commit hashes for each critical document before their removal. Document these commit hashes and file paths.

### 26.2. Recover Initial Content of All Documentation Files

**Status:** pending  
**Dependencies:** 26.1  

Systematically use Git commands to recover the content of each identified document file from its last known good version. Place these recovered files in a temporary recovery directory for initial review.

**Details:**

For each document identified in subtask 1, execute `git checkout <commit-hash> -- <file-path>` to retrieve its content. Ensure all specified files (AGENTS.md, GEMINI.md, CRUSH.md, IFLOW.md, LLXPRT.md, and workflow guides) are recovered successfully. Store them in a dedicated 'recovered_docs' folder.

### 26.3. Perform Comprehensive Content Review, Reconstruction, and Update

**Status:** pending  
**Dependencies:** None  

Thoroughly review the recovered content of each document. For any sections or entire documents where direct Git recovery is insufficient or content is significantly outdated, collaborate with product owners, AI engineers, and subject matter experts to reconstruct, rewrite, or update the information to reflect the current system state, agent capabilities, and operational procedures.

**Details:**

Review AGENTS.md for architecture and functionalities. For GEMINI.md, CRUSH.md, IFLOW.md, LLXPRT.md, update integration points, I/O requirements, and best practices. Update workflow guides with current step-by-step procedures and tools. Schedule meetings with SMEs for content validation and input.

### 26.4. Ensure Documentation Standards Adherence and Proper Placement

**Status:** pending  
**Dependencies:** None  

Integrate the reviewed and updated documentation into the appropriate and accessible directories within the project repository. Ensure all restored and updated documentation adheres to the project's current documentation standards.

**Details:**

Move the finalized documents to their designated locations (e.g., `docs/agents/`, `docs/workflows/` or project root). Verify Markdown formatting, consistent terminology, clear headings, and well-structured code examples. Perform a spell check and grammar review.

### 26.5. Conduct Stakeholder Validation and Final Approval

**Status:** pending  
**Dependencies:** 26.4  

Present the fully restored, updated, and formatted documentation to relevant stakeholders (Product Owners, AI Engineers, and potentially users) for final review, validation, and official approval, ensuring all critical information is present and accurate.

**Details:**

Organize a final review session or circulate the updated documentation for formal sign-off. Collect any last-minute feedback and implement necessary minor revisions. Obtain explicit confirmation from stakeholders that the documentation accurately reflects the current system and meets their needs.
