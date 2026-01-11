# Task ID: 018

**Title:** Configure Branch Protection Rules and Merge Guards

**Status:** deferred

**Dependencies:** None

**Priority:** high

**Description:** Implement branch protection rules and merge guards to prevent cross-branch overwrites and enforce merge policies on critical branches.

**Details:**

Configure repository settings (e.g., in GitHub, GitLab, Bitbucket) for the 'scientific' branch and other critical branches (e.g., 'main', 'develop'). Enforce rules such as: require pull requests, require a minimum number of approving reviews, require status checks to pass (including the new import validation [e.g., from Task 18] and pre-merge validations from Task 19), prevent force pushes, and restrict who can merge. Set up merge guards to prevent merging if specified conditions are not met.

### Tags:
- `work_type:configuration`
- `work_type:security`
- `component:vcs-management`
- `component:branch-protection`
- `scope:devops`
- `scope:security`
- `purpose:stability`
- `purpose:security-enforcement`

**Test Strategy:**

Attempt to directly push to a protected branch without a pull request; verify it's denied. Open a Pull Request and attempt to merge it without satisfying all configured requirements (e.g., missing approvals, failing CI/CD checks); verify the merge is blocked. Ensure that only authorized personnel can bypass or modify these rules.

## Subtasks

### 20.1. Identify Critical Branches and Gather Protection Requirements

**Status:** done  
**Dependencies:** None  

Determine which branches are considered critical for the project (e.g., 'main', 'develop', 'scientific') and solicit specific protection needs from relevant teams/stakeholders, including specific requirements related to 'scientific' branch recovery (as per Task 23 context).

**Details:**

Review existing documentation and consult with development, QA, operations, and scientific teams to identify all branches requiring protection. Document specific needs for pull requests, required approval counts, mandatory status checks, restrictions on force pushes, and merge permissions. Focus on 'main', 'develop', and 'scientific' branches initially.

### 20.2. Design Detailed Branch Protection Policies for Critical Branches

**Status:** done  
**Dependencies:** 20.1  

Based on the identified critical branches and gathered requirements, define comprehensive and detailed branch protection policies, including specific merge conditions, required status checks (integrating Task 18 and 19), and access controls for each identified critical branch.

**Details:**

For each critical branch (e.g., 'main', 'develop', 'scientific'): specify the minimum number of required approving reviews, list all mandatory status checks (e.g., CI/CD pipeline passing, unit tests, integration tests, Task 18's import validation, Task 19's pre-merge validations), determine restrictions on force pushes, and identify groups or individuals allowed to perform merges or bypass certain rules. Document these policies clearly.
<info added on 2025-11-12T18:44:23.081Z>
Based on the analysis of the .github/workflows/pull_request.yml CI/CD workflow, the detailed branch protection policies for critical branches (e.g., 'main', 'develop', 'scientific') will specifically include: GitHub Branch Protection requiring pull requests; a minimum of 2 approving reviews; mandatory status checks including existing basic CI checks, import validation (Task 18), critical file validation (Task 19), and security scans, all of which must pass before merging; restricted force pushes; and designated groups or individuals for merge permissions or rule bypass.
</info added on 2025-11-12T18:44:23.081Z>

### 20.3. Implement Branch Protection Rules and Merge Guards in VCS

**Status:** pending  
**Dependencies:** None  

Implement the defined branch protection policies and merge guards within the chosen Version Control System (e.g., GitHub, GitLab, Bitbucket) settings for all identified critical branches, specifically integrating the CI/CD checks from Tasks 18 and 19.

**Details:**

Access the repository settings in the VCS. For each critical branch ('main', 'develop', 'scientific', etc.): enable 'Require pull request reviews before merging' and set the required count; enable 'Require status checks to pass before merging' and select all relevant checks, including those from Task 18 (automated import validation) and Task 19 (pre-merge validations); enable 'Require branches to be up to date before merging'; restrict force pushes; and configure access controls for merging and pushing as per the defined policies.

### 20.4. Test Implemented Branch Protection and Merge Guard Enforcement

**Status:** pending  
**Dependencies:** None  

Thoroughly test the implemented branch protection rules and merge guards to ensure they correctly enforce the defined policies and effectively block unauthorized or non-compliant actions while allowing valid ones.

**Details:**

Perform a series of test scenarios: 1. Attempt a direct push to a protected branch without a pull request; verify it's denied. 2. Open a Pull Request (PR) for a protected branch. 3. Attempt to merge the PR without the required number of approvals; verify it's blocked. 4. Attempt to merge the PR when a required status check (e.g., from Task 18 or 19) is failing; verify it's blocked. 5. Attempt to merge the PR as an unauthorized user; verify it's blocked. 6. Verify that authorized users can merge a PR that meets all conditions. 7. Attempt a force push to a protected branch; verify it's denied. Document all test cases and results.
