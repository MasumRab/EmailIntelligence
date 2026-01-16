# Branch-Specific Agent Guidelines Summary & Consistency Review

**Document Version**: 1.0  
**Last Updated**: 2025-11-12  
**Status**: DRAFT - Consistency Issues Identified

---

## Branch-Specific Extensions

For branch-specific agent guidance, check for `AGENTS_{branch-name}.md` files:

- `AGENTS_scientific.md` - Scientific branch extensions
- `AGENTS_orchestration-tools.md` - Orchestration tools branch extensions  
- `AGENTS_[branch-name].md` - Other branch-specific guides (as they exist)

These files extend the core guidance in AGENTS.md with branch-specific commands, workflows, and considerations. If a file exists for your current branch, it supplements the main guide.

---

## Executive Summary

This document consolidates branch-specific agent guidelines across the EmailIntelligence project and identifies inconsistencies that need resolution. The project uses three primary branches with distinct purposes and agent access controls.

---

## Branch Classification

### 1. **orchestration-tools** (Current Branch)
- **Purpose**: Central source of truth for development environment tooling, configuration management, scripts, and Git hooks
- **Project Type**: `library` (orchestration/infrastructure)
- **Agent Scope**: Full access to all orchestration files, setup scripts, and configurations
- **Special Role**: NOT merged with other branches; synchronized via Git hooks

### 2. **main**
- **Purpose**: Core application development and integration
- **Project Type**: `application`
- **Agent Scope**: Access to application code (src/, tests/) and core configurations
- **Restrictions**: Blocks access to orchestration scripts and specifications

### 3. **scientific**
- **Purpose**: FastAPI backend, email processing, AI analysis, and API routes
- **Project Type**: `backend-service`
- **Agent Scope**: Backend-specific code and services
- **Restrictions**: Blocks access to orchestration scripts, deployment configs, and setup utilities

---

## Context Control Profiles

### Orchestration-Tools Profile
```json
{
  "id": "orchestration-tools",
  "branch_patterns": ["orchestration-tools", "orchestration-tools-*", "001-agent-context-control"],
  "allowed_files": [
    "scripts/**", "specs/**", "src/**", "tests/**", "docs/**",
    "*.md", "*.py", "*.sh", "*.yml", "*.yaml", "*.json"
  ],
  "blocked_files": [".git/**", "__pycache__/**", "*.pyc", ".pytest_cache/**", "node_modules/**"],
  "max_context_length": 8192,
  "enable_code_execution": true,
  "enable_file_writing": true,
  "enable_shell_commands": true
}
```

### Main Profile
```json
{
  "id": "main",
  "branch_patterns": ["main", "master"],
  "allowed_files": [
    "src/**", "tests/**", "docs/**", "*.md", "*.py", "*.sh",
    "*.yml", "*.yaml", "*.json", "setup.py", "pyproject.toml",
    "requirements*.txt", "uv.lock", ".github/**", "CLAUDE.md", "README.md"
  ],
  "blocked_files": [
    ".git/**", "__pycache__/**", "*.pyc", ".pytest_cache/**",
    "node_modules/**", "scripts/**", "specs/**", ".context-control/**",
    ".specify/**", ".taskmaster/**"
  ],
  "max_context_length": 8192,
  "enable_code_execution": true,
  "enable_file_writing": true,
  "enable_shell_commands": true
}
```

### Scientific Profile
```json
{
  "id": "scientific",
  "branch_patterns": ["scientific", "scientific-*"],
  "allowed_files": [
    "src/**", "tests/**", "docs/**", "*.md", "*.py", "*.sh",
    "*.yml", "*.yaml", "*.json", "setup.py", "pyproject.toml",
    "requirements*.txt", "uv.lock", ".github/**", "CLAUDE.md", "README.md",
    "Dockerfile.backend", "docker-compose.yml"
  ],
  "blocked_files": [
    ".git/**", "__pycache__/**", "*.pyc", ".pytest_cache/**",
    "node_modules/**", "scripts/**", "specs/**", ".context-control/**",
    ".specify/**", ".taskmaster/**", "deployment/**", "setup/**"
  ],
  "max_context_length": 8192,
  "enable_code_execution": true,
  "enable_file_writing": true,
  "enable_shell_commands": true
}
```

---

## Agent Guideline Documents

### AGENTS.md (Main Orchestration-Tools Version)
- **Location**: `/AGENTS.md` (orchestration-tools branch)
- **Scope**: Task Master commands, MCP integration, project structure
- **Branch Directives**: 
  - Explicitly tells agents working on `scientific` to use branch-specific AGENTS.md
  - Applies Task Master CLI workflow to orchestration-tools and main branches
  - Jules-specific guidance (NOT compatible, refer to Jules documentation)

### AGENTS.md (Scientific Branch Version)
- **Location**: `scientific` branch
- **Scope**: Context contamination prevention guidelines, additional code conventions
- **Focus Areas**:
  - TypeScript code style (2 spaces, double quotes, trailing commas)
  - Architecture principles (feature organization, dependency injection)
  - Context contamination prevention with 6 detailed sections
  - No Task Master commands listed

### CLAUDE.md
- **Location**: Root level across branches
- **Scope**: Claude-specific features, MCP configuration, tool allowlist
- **Content**: Same across branches (Claude Code features are universal)
- **Integration**: Auto-loaded alongside AGENTS.md for context

### .specify/memory/constitution.md
- **Location**: `.specify/memory/constitution.md`
- **Scope**: Orchestration tools verification and review principles
- **Key Principles**:
  - Verification-first development
  - Goal-task consistency
  - Role-based access control
  - Context-aware verification
  - Token optimization

---

## Critical Consistency Issues Identified

### ⚠️ Issue #1: Branch-Specific AGENTS.md Guidelines Not Synchronized

**Problem**:
- orchestration-tools/main version includes Task Master commands and full workflow
- scientific version focuses on code conventions and context contamination prevention
- Scientific branch AGENTS.md does NOT mention Task Master commands
- No clear indication of whether Task Master applies to scientific branch

**Impact**: Agents on scientific branch may not know about Task Master task management capabilities

**Status**: 🔴 **CRITICAL**

**Recommendation**: 
1. Add Task Master command section to scientific branch AGENTS.md (if applicable)
2. Or explicitly document that scientific branch uses different task management
3. Update orchestration-tools AGENTS.md to clarify Task Master availability per branch

---

### ⚠️ Issue #2: Inconsistent File Access Control

**Problem**:
- `AGENTS.md` and `CLAUDE.md` are **NOT explicitly listed** in main/scientific blocked_files
- However, both branches show them in allowed_files through `*.md` pattern
- orchestration-tools shows full access to `specs/**` but main/scientific block it

**Impact**: Potential security or access control bypass; agents may see configurations they shouldn't

**Status**: 🟡 **HIGH**

**Inconsistent Access**:
| File | Orchestration-Tools | Main | Scientific |
|------|-------------------|------|-----------|
| scripts/** | ✅ Allowed | ❌ Blocked | ❌ Blocked |
| specs/** | ✅ Allowed | ❌ Blocked | ❌ Blocked |
| .context-control/** | ✅ Allowed* | ❌ Blocked | ❌ Blocked |
| .specify/** | ✅ Allowed* | ❌ Blocked | ❌ Blocked |
| .taskmaster/** | ✅ Allowed* | ❌ Blocked | ❌ Blocked |
| AGENTS.md | ✅ Allowed | ✅ Allowed | ✅ Allowed |
| CLAUDE.md | ✅ Allowed | ✅ Allowed | ✅ Allowed |

*Not explicitly listed but falls under broader patterns

**Recommendation**:
1. Explicitly list AGENTS.md and CLAUDE.md in allowed_files for all branches
2. Explicitly list .context-control/, .specify/, .taskmaster/ in orchestration-tools allowed_files
3. Add explanatory comments to profiles clarifying why scientific blocks certain files

---

### ⚠️ Issue #3: Context Contamination Prevention Guidelines Missing from Orchestration-Tools

**Problem**:
- Scientific branch AGENTS.md includes detailed context contamination prevention guidelines (6 sections)
- Orchestration-tools AGENTS.md does not mention context contamination prevention
- constitution.md mentions context contamination prevention as a core principle
- But orchestration-tools branch lacks practical implementation guidelines

**Impact**: Agents working on orchestration-tools may not follow context isolation best practices

**Status**: 🟡 **MEDIUM**

**Recommendation**:
1. Replicate context contamination prevention guidelines to orchestration-tools AGENTS.md
2. Or create separate CONTEXT_CONTAMINATION_PREVENTION.md referenced from AGENTS.md
3. Add task isolation and tool state management guidance specific to orchestration work

---

### ⚠️ Issue #4: Code Style Guidance Only in Scientific Branch

**Problem**:
- Scientific AGENTS.md includes code style rules (TypeScript, 2 spaces, double quotes, trailing commas)
- Orchestration-tools AGENTS.md does NOT include code style guidance
- Main branch AGENTS.md (truncated in search) may lack style guidance
- No unified code style specification across branches

**Impact**: Inconsistent code formatting across branches; lack of clear standards for orchestration tools

**Status**: 🟡 **MEDIUM**

**Recommendation**:
1. Create unified CODING_STANDARDS.md with branch-specific sections
2. Reference from each branch's AGENTS.md
3. Include Python style (for orchestration-tools/main) and TypeScript style (for scientific)

---

### ⚠️ Issue #5: Task Master Scope Ambiguity for Scientific Branch

**Problem**:
- Orchestration-tools/main AGENTS.md prominently features Task Master CLI commands
- Scientific branch AGENTS.md makes no mention of Task Master
- Constitution.md references "goals and tasks" but unclear if Task Master is the implementation vehicle
- Agents on scientific branch may not know they have task management available

**Impact**: Scientific branch agents may not utilize centralized task tracking

**Status**: 🟡 **MEDIUM**

**Recommendation**:
1. Clarify whether scientific branch uses Task Master
2. If yes: Add Task Master section to scientific AGENTS.md with any science-specific adaptations
3. If no: Document the alternative task management approach for scientific branch
4. Update orchestration-tools AGENTS.md to explicitly state Task Master scope across branches

---

### ⚠️ Issue #6: Claude-Specific Guidance Not Branch-Aware

**Problem**:
- CLAUDE.md is identical across branches
- Contains Claude Code features that may not apply to agents not using Claude Code
- No indication of non-Claude agent support (e.g., GPT-4, Gemini, Grok via OpenRouter)
- MCP configuration assumes Claude Code environment

**Impact**: Non-Claude agents may be confused by Claude-specific instructions; unclear if MCP applies universally

**Status**: 🟠 **MEDIUM**

**Recommendation**:
1. Update CLAUDE.md header to clarify it's for Claude Code users
2. Add section "For Non-Claude Agents" with alternative workflow guidance
3. Or create separate MCP_INTEGRATION.md that's agent-agnostic
4. Update AGENTS.md to link to appropriate guides based on agent type

---

### ⚠️ Issue #7: Inconsistent .context-control Profile Coverage

**Problem**:
- Profiles exist for orchestration-tools, main, and scientific
- `branch_patterns` in orchestration-tools includes "001-agent-context-control"
- No profiles exist for other feature branches (e.g., orchestration-tools-changes, orchestration-tools-clean)
- Convention for feature branch profile naming unclear

**Impact**: Agents working on feature branches may not have proper context control applied

**Status**: 🟠 **MEDIUM**

**Recommendation**:
1. Create profiles for orchestration-tools-* branches (or update main pattern to catch them)
2. Document pattern-matching logic in `.context-control/README.md`
3. Add fallback/default profile for unmapped branches
4. Create guide for adding profiles when new branches are established

---

### ⚠️ Issue #8: Agent Settings Redundancy

**Problem**:
- All profiles define identical `agent_settings` and `project_config` sections
- Settings are duplicated across 3 profiles (8192 context length, same enable flags)
- No per-branch customization of agent capabilities (all have same permissions)
- Unclear if agent capabilities should differ by branch

**Impact**: Maintenance burden; risk of inconsistency if one profile is updated but others aren't; possible incorrect capabilities per branch

**Status**: 🟠 **LOW-MEDIUM**

**Recommendation**:
1. Create shared default settings in `.context-control/defaults.json`
2. Override only branch-specific settings in individual profiles
3. Add documentation explaining intentional differences in agent capabilities
4. Consider: Should scientific branch agents have different execution permissions than orchestration-tools?

---

## Consistency Verification Checklist

- [ ] **Issue #1**: Branch AGENTS.md files synchronized for Task Master usage
- [ ] **Issue #2**: File access control explicitly documented in all profiles
- [ ] **Issue #3**: Context contamination prevention guidelines present in all branch guidelines
- [ ] **Issue #4**: Code style guidance available for all branches
- [ ] **Issue #5**: Task Master scope clearly documented for each branch
- [ ] **Issue #6**: Claude vs. non-Claude agent guidance separated
- [ ] **Issue #7**: Profile coverage includes all active branches
- [ ] **Issue #8**: Agent settings centralized and branch-specific overrides documented

---

## Recommendations Summary

### High Priority (Resolve Before Next Release)
1. **Synchronize AGENTS.md across branches** - Ensure Task Master scope is clear for scientific branch
2. **Consolidate file access control** - Explicitly list all protected files in context profiles
3. **Add context contamination guidance to all branches** - Essential for agent quality

### Medium Priority (Implement in Next Phase)
4. **Create unified coding standards** - Branch-specific style guides in one location
5. **Clarify Claude vs. non-Claude agent support** - Update CLAUDE.md and MCP documentation
6. **Expand profile coverage** - Add missing branch patterns

### Low Priority (Quality Improvements)
7. **Refactor agent settings** - Extract shared configuration
8. **Create configuration documentation** - `.context-control/README.md` explaining profile system

---

## Files Requiring Updates

### Must Update
- [ ] `AGENTS.md` (scientific branch) - Add Task Master section or clarify scope
- [ ] `.context-control/profiles/*.json` - Explicit file listing and comments
- [ ] `CLAUDE.md` - Add non-Claude agent guidance section

### Should Update
- [ ] Create `CODING_STANDARDS.md` with branch-specific sections
- [ ] Create `.context-control/README.md` documenting profile system
- [ ] Create `MCP_INTEGRATION.md` (agent-agnostic)
- [ ] Add `CONTEXT_CONTAMINATION_PREVENTION.md` (referenced from all AGENTS.md files)

### Consider Creating
- [ ] `.specify/branch-guidelines.md` - Single source of truth for branch-agent mapping
- [ ] `.context-control/defaults.json` - Shared agent settings template

---

## Next Steps

1. **Review and Prioritize**: Team review of identified issues and recommendations
2. **Assign Ownership**: Designate branch maintainers responsible for guidelines
3. **Implementation Plan**: Create tasks for each inconsistency fix
4. **Verification**: Test context control profiles work as documented
5. **Documentation**: Update all relevant README files to reflect standardization

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-11-12 | Amp AI | Initial consistency review and issue identification |
