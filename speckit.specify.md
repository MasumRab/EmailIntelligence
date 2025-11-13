# Spec-Kit Specification: Unified PR Resolution CLI with LLM Orchestration

**Feature ID**: `002-pr-resolution-cli-unified`
**Created**: 2025-11-12
**Updated**: 2025-11-12
**Status**: Draft - Ready for `/speckit.clarify`
**Extends**: EmailIntelligence CLI v2.0 (spec `001-pr-resolution-improvements`)

---

## Overview

### Primary Goal
Consolidate and refactor existing PR resolution scripts into a unified CLI tool with LLM orchestration capabilities, supporting LangChain integration and TOML-based configuration for Gemini CLI and other LLM providers.

### Current State Analysis

#### Existing Components to Consolidate
**EmailIntelligence CLI** (`emailintelligence_cli.py` - 1,418 lines):
- ✅ Resolution workspace setup (`setup-resolution`)
- ✅ Constitutional analysis framework (`analyze-constitutional`)
- ✅ Strategy development (`develop-spec-kit-strategy`)
- ✅ Content alignment execution (`align-content`)
- ✅ Resolution validation (`validate-resolution`)

**Bash Scripts** (scripts/bash/):
- ✅ `create-pr-resolution-spec.sh` (366 lines) - Interactive specification creation
- ✅ `gh-pr-ci-integration.sh` (483 lines) - GitHub PR and CI/CD integration
- ✅ `pr-test-executor.sh` - Testing framework execution

**PowerShell Scripts** (scripts/powershell/):
- ✅ `create-pr-resolution-spec.ps1` (367 lines) - Windows specification creation

**Source Modules** (src/):
- ✅ `src/resolution/` - Resolution engine components
- ✅ `src/specification/` - Specification templates
- ✅ `src/integration/` - Task Master integration
- ✅ `src/validation/` - Validation frameworks

### Gaps Identified
- ❌ Scripts are fragmented across bash/PowerShell/Python
- ❌ No unified LLM orchestration layer
- ❌ Limited LangChain integration
- ❌ No TOML-based configuration for LLM providers
- ❌ Missing Gemini CLI compatibility
- ❌ No multi-provider LLM fallback system
- ❌ Limited prompt template management
- ❌ No LLM response caching and optimization

### Success Criteria
- [ ] Unified CLI consolidates all bash/PowerShell/Python scripts
- [ ] LangChain integration enables multi-provider LLM orchestration
- [ ] TOML configuration supports Gemini CLI, Groq CLI, and other providers
- [ ] Interactive specification wizard reduces creation time by 70%
- [ ] Constitutional validation catches 95%+ policy violations
- [ ] Multi-strategy comparison provides 3+ resolution options
- [ ] LLM response caching reduces API costs by 60%
- [ ] Automated test generation achieves 80%+ coverage
- [ ] Enhancement preservation rate exceeds 95%

---

## User Stories

### Story 1: Unified CLI Consolidation
**As a** developer using PR resolution tools
**I want** a single unified CLI that consolidates all scripts
**So that** I have one consistent interface regardless of platform

**Acceptance Criteria:**
- [ ] All bash script functionality migrated to Python CLI
- [ ] All PowerShell script functionality available in CLI
- [ ] Cross-platform compatibility (Windows, Linux, macOS)
- [ ] Backward compatibility with existing script interfaces
- [ ] Unified configuration system

**Implementation Notes:**
- Consolidate `create-pr-resolution-spec.sh/ps1` into CLI
- Integrate `gh-pr-ci-integration.sh` functionality
- Merge `pr-test-executor.sh` capabilities
- Maintain script wrappers for backward compatibility

---

### Story 2: LLM Orchestration with LangChain
**As a** developer using AI-powered resolution
**I want** LangChain integration for multi-provider LLM support
**So that** I can use any LLM provider with consistent interfaces

**Acceptance Criteria:**
- [ ] LangChain integration for LLM orchestration
- [ ] Support for OpenAI, Anthropic, Google, Groq, Mistral
- [ ] Prompt template management via LangChain
- [ ] LLM response caching and optimization
- [ ] Fallback provider chain for reliability

**Implementation Notes:**
- Use LangChain's `ChatOpenAI`, `ChatAnthropic`, `ChatGoogleGenerativeAI`
- Implement `PromptTemplate` for constitutional analysis
- Add `CacheBackedEmbeddings` for response caching
- Create provider fallback chain with retry logic

---

### Story 3: TOML-Based Configuration
**As a** developer configuring LLM providers
**I want** TOML-based configuration like Gemini CLI and Groq CLI
**So that** I can easily manage multiple LLM providers

**Acceptance Criteria:**
- [ ] TOML configuration file support
- [ ] Compatible with Gemini CLI config format
- [ ] Compatible with Groq CLI config format
- [ ] Environment variable override support
- [ ] Provider-specific settings (temperature, max_tokens, etc.)

**Implementation Notes:**
- Use `tomli`/`tomllib` for TOML parsing
- Support `.emailintelligence.toml` configuration
- Allow per-provider configuration sections
- Enable environment variable substitution

---

### Story 4: Interactive Specification Creation
**As a** developer facing complex PR conflicts
**I want** an interactive wizard to guide specification creation
**So that** I can systematically document conflicts without missing critical details

**Acceptance Criteria:**
- [ ] Wizard prompts for all required specification sections
- [ ] Real-time validation ensures completeness
- [ ] Generated specifications follow spec-kit template standards
- [ ] Integration with existing `setup-resolution` workflow
- [ ] Specifications are saved in standardized format
- [ ] LLM-assisted specification generation

**Implementation Notes:**
- Consolidate bash/PowerShell interactive prompts
- Use LangChain for AI-assisted specification generation
- Validate against specification schema
- Auto-populate from git metadata and GitHub API

---

### Story 2: Constitutional Rule Templates
**As a** team lead enforcing organizational standards  
**I want** pre-built constitutional rule templates  
**So that** I can quickly apply standard policies to PR resolutions

**Acceptance Criteria:**
- [ ] Template library includes common rule categories
- [ ] Templates are customizable and extensible
- [ ] Rules can be combined and prioritized
- [ ] Validation provides clear compliance scoring
- [ ] Critical violations halt resolution automatically

**Implementation Notes:**
- Create `.emailintelligence/constitutions/templates/` directory
- Provide templates for: security, performance, code-quality, architecture
- Extend `analyze-constitutional` to support template selection
- Add `--template` flag for quick rule application

---

### Story 3: Multi-Strategy Comparison
**As a** developer evaluating resolution approaches  
**I want** to compare multiple resolution strategies side-by-side  
**So that** I can choose the optimal approach for my specific conflict

**Acceptance Criteria:**
- [ ] Generate 3+ distinct resolution strategies
- [ ] Compare strategies across key metrics (time, risk, complexity)
- [ ] Provide recommendation based on project context
- [ ] Allow interactive strategy selection
- [ ] Support custom strategy weighting

**Implementation Notes:**
- Extend `develop-spec-kit-strategy` with `--compare` flag
- Generate strategies: conservative, balanced, aggressive
- Display comparison table with metrics
- Add `--recommend` flag for AI-powered recommendation

---

### Story 4: Task Master MCP Integration
**As a** developer working on complex resolutions  
**I want** automatic task creation and tracking  
**So that** I can manage resolution phases systematically

**Acceptance Criteria:**
- [ ] Automatic task creation from resolution phases
- [ ] Task dependencies reflect resolution workflow
- [ ] Progress tracking integrated with CLI
- [ ] Parallel development support via worktrees
- [ ] Task completion triggers validation

**Implementation Notes:**
- Add MCP client integration to CLI
- Create tasks for each strategy phase
- Map task dependencies from phase relationships
- Add `--task-master` flag to enable integration
- Provide task status in CLI output

---

### Story 5: Automated Test Generation
**As a** quality assurance engineer  
**I want** automated test generation from specifications  
**So that** I can ensure resolution quality without manual test writing

**Acceptance Criteria:**
- [ ] Generate unit tests for conflict resolution logic
- [ ] Create integration tests for workflow validation
- [ ] Produce enhancement preservation tests
- [ ] Generate performance benchmarks
- [ ] Tests follow project testing conventions

**Implementation Notes:**
- Add `generate-tests` command to CLI
- Parse specification to identify testable components
- Use templates for test generation
- Support multiple test frameworks (pytest, unittest)
- Integrate with existing validation framework

---

### Story 6: Enhanced Preservation Validation
**As a** developer preserving feature enhancements  
**I want** comprehensive validation of feature preservation  
**So that** I can ensure no functionality is lost during resolution

**Acceptance Criteria:**
- [ ] Automated feature detection in both branches
- [ ] Preservation rate calculation and reporting
- [ ] Regression detection for lost functionality
- [ ] Enhancement integration validation
- [ ] Detailed preservation report generation

**Implementation Notes:**
- Extend `validate-resolution` with `--preservation` flag
- Implement feature detection heuristics
- Compare pre/post resolution functionality
- Generate preservation report
- Fail validation if preservation < 95%

---

### Consolidated Architecture

#### Component Consolidation Map

**From Bash Scripts → Unified CLI**:
```
create-pr-resolution-spec.sh (366 lines)
  → eai create-specification
  → Consolidates interactive prompts
  → Adds LLM-assisted generation

gh-pr-ci-integration.sh (483 lines)
  → eai github-integration
  → Adds GitHub API client
  → Integrates CI/CD status checking

pr-test-executor.sh
  → eai execute-tests
  → Consolidates test execution
  → Adds test result analysis
```

**From PowerShell Scripts → Unified CLI**:
```
create-pr-resolution-spec.ps1 (367 lines)
  → Same as bash consolidation
  → Cross-platform Python implementation
  → Maintains Windows compatibility
```

**From Source Modules → CLI Integration**:
```
src/resolution/ → Core resolution engine
src/specification/ → Template system
src/integration/ → Task Master MCP
src/validation/ → Validation framework
```

---

### LLM Orchestration Layer

#### LangChain Integration Architecture

```python
from langchain.chat_models import (
    ChatOpenAI,
    ChatAnthropic,
    ChatGoogleGenerativeAI
)
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.cache import SQLiteCache
from langchain.callbacks import get_openai_callback

class LLMOrchestrator:
    """Unified LLM orchestration with multi-provider support"""
    
    def __init__(self, config: dict):
        self.providers = self._initialize_providers(config)
        self.cache = SQLiteCache(database_path=".emailintelligence/llm_cache.db")
        self.fallback_chain = self._create_fallback_chain()
    
    def _initialize_providers(self, config):
        """Initialize LLM providers from TOML config"""
        providers = {}
        
        if config.get('openai', {}).get('enabled'):
            providers['openai'] = ChatOpenAI(
                model=config['openai']['model'],
                temperature=config['openai'].get('temperature', 0.7),
                api_key=config['openai']['api_key']
            )
        
        if config.get('anthropic', {}).get('enabled'):
            providers['anthropic'] = ChatAnthropic(
                model=config['anthropic']['model'],
                temperature=config['anthropic'].get('temperature', 0.7),
                api_key=config['anthropic']['api_key']
            )
        
        if config.get('google', {}).get('enabled'):
            providers['google'] = ChatGoogleGenerativeAI(
                model=config['google']['model'],
                temperature=config['google'].get('temperature', 0.7),
                google_api_key=config['google']['api_key']
            )
        
        if config.get('groq', {}).get('enabled'):
            providers['groq'] = ChatOpenAI(
                model=config['groq']['model'],
                base_url="https://api.groq.com/openai/v1",
                api_key=config['groq']['api_key']
            )
        
        return providers
    
    def generate_with_fallback(self, prompt, **kwargs):
        """Generate response with provider fallback"""
        for provider_name in self.fallback_chain:
            try:
                provider = self.providers.get(provider_name)
                if provider:
                    chain = LLMChain(llm=provider, prompt=prompt)
                    return chain.run(**kwargs)
            except Exception as e:
                print(f"Provider {provider_name} failed: {e}")
                continue
        raise Exception("All LLM providers failed")
```

---

### TOML Configuration System

#### Configuration File: `.emailintelligence.toml`

```toml
# EmailIntelligence Unified CLI Configuration
# Compatible with Gemini CLI and Groq CLI formats

[general]
default_provider = "anthropic"
enable_caching = true
cache_ttl = 3600  # 1 hour
fallback_enabled = true

# OpenAI Configuration (GPT-4, GPT-3.5)
[openai]
enabled = true
model = "gpt-4o"
api_key = "${OPENAI_API_KEY}"
temperature = 0.7
max_tokens = 4096
timeout = 60

# Anthropic Configuration (Claude)
[anthropic]
enabled = true
model = "claude-3-5-sonnet-20241022"
api_key = "${ANTHROPIC_API_KEY}"
temperature = 0.7
max_tokens = 4096
timeout = 60

# Google Configuration (Gemini) - Gemini CLI Compatible
[google]
enabled = true
model = "gemini-1.5-pro"
api_key = "${GOOGLE_API_KEY}"
temperature = 0.7
max_tokens = 4096
timeout = 60

# Groq Configuration - Groq CLI Compatible
[groq]
enabled = true
model = "llama-3.1-70b-versatile"
api_key = "${GROQ_API_KEY}"
temperature = 0.7
max_tokens = 4096
timeout = 30

# Mistral Configuration
[mistral]
enabled = false
model = "mistral-large-latest"
api_key = "${MISTRAL_API_KEY}"
temperature = 0.7
max_tokens = 4096

# Perplexity Configuration (Research)
[perplexity]
enabled = true
model = "llama-3.1-sonar-large-128k-online"
api_key = "${PERPLEXITY_API_KEY}"
temperature = 0.7
max_tokens = 4096

# Provider Fallback Chain
[fallback]
chain = ["anthropic", "openai", "google", "groq"]
retry_attempts = 3
retry_delay = 2  # seconds

# Prompt Templates
[prompts]
constitutional_analysis = "templates/constitutional_analysis.txt"
strategy_generation = "templates/strategy_generation.txt"
specification_creation = "templates/specification_creation.txt"

# GitHub Integration
[github]
enabled = true
token = "${GITHUB_TOKEN}"
repo = "${GITHUB_REPO}"
fetch_pr_context = true
fetch_ci_status = true

# Task Master Integration
[taskmaster]
enabled = true
mcp_server = "task-master-ai"
auto_create_tasks = true

---

### Enhanced CLI Commands with LLM Orchestration

#### 1. `create-specification` (Consolidated & LLM-Enhanced)
```bash
eai create-specification --pr <number> [--interactive] [--template <name>] [--llm-assist] [--provider <name>]
```

**Purpose**: Interactive specification creation wizard (consolidates bash/PowerShell scripts)  
**Output**: Generates `specs/<pr-number>-resolution/spec.md`  
**Features**:
- Interactive prompts (from create-pr-resolution-spec.sh/ps1)
- LLM-assisted generation via LangChain
- Template-based initialization
- Real-time validation
- Auto-population from git metadata and GitHub API
- Multi-provider LLM support

**Workflow**:
1. Prompt for PR number and basic info
2. Fetch GitHub PR context (from gh-pr-ci-integration.sh)
3. Analyze git branches for conflict details
4. Use LLM to generate specification sections
5. Guide through specification sections interactively
6. Validate completeness against schema
7. Save to standardized location

**LLM Integration Example**:
```python
# Use LangChain for specification generation
spec_prompt = PromptTemplate(
    input_variables=["pr_context", "conflict_analysis"],
    template="""Generate a comprehensive PR resolution specification:
    
    PR Context: {pr_context}
    Conflict Analysis: {conflict_analysis}
    
    Create a detailed specification following spec-kit methodology with:
    1. Merge scenario information
    2. Conflict characteristics
    3. Resolution requirements
    4. Strategy options
    5. Risk assessment
    ..."""
)

orchestrator = LLMOrchestrator(config)
chain = LLMChain(llm=orchestrator.get_provider(), prompt=spec_prompt)
specification = chain.run(pr_context=context, conflict_analysis=analysis)
```

---

#### 2. `github-integration` (Consolidated from gh-pr-ci-integration.sh)
```bash
eai github-integration --pr <number> [--fetch-context] [--fetch-ci] [--ci-system <name>]
```

**Purpose**: GitHub PR and CI/CD integration (consolidates 483 lines from gh-pr-ci-integration.sh)  
**Output**: Enhanced PR context with GitHub and CI/CD data  
**Features**:
- Fetch GitHub PR metadata via GitHub API
- Get CI/CD status (GitHub Actions, GitLab CI, Jenkins, Azure DevOps)
- Calculate PR complexity score
- Analyze review status
- Merge with testing framework data
- Export to JSON for further processing

**Implementation**:
- Consolidates all functionality from gh-pr-ci-integration.sh
- Uses PyGithub or requests for GitHub API
- Integrates with testing framework
- Supports multiple CI/CD systems
- Provides enhanced PR data for LLM context

**Example Output**:
```json
{
  "pr_metadata": {
    "number": 123,
    "title": "Add authentication system",
    "state": "open",
    "mergeable": true,
    "complexity_score": 2.5
  },
  "ci_status": {
    "overall_status": "success",
    "ready_for_merge": true
  }
}
```

---

#### 3. `compare-strategies` (LLM-Enhanced)
```bash
eai compare-strategies --pr <number> [--strategies <count>] [--recommend] [--provider <name>]
```

**Purpose**: Generate and compare multiple resolution strategies using LLM  
**Output**: Strategy comparison table and AI-powered recommendation  
**Features**:
- Generate 3-5 distinct strategies via LLM
- Compare across metrics (time, risk, complexity, preservation)
- AI-powered recommendation using LangChain
- Interactive strategy selection
- Provider fallback for reliability
- TOML-configured strategy templates

**LLM Integration Example**:
```python
# Multi-strategy generation with LangChain
strategy_prompt = PromptTemplate(
    input_variables=["conflict_data", "constitutional_rules", "pr_context"],
    template="""Generate 3 distinct PR resolution strategies:
    
    Conflict Data: {conflict_data}
    Constitutional Rules: {constitutional_rules}
    PR Context: {pr_context}
    
    For each strategy (Conservative, Balanced, Aggressive), provide:
    1. Approach name and description
    2. Risk assessment (Low/Medium/High)
    3. Time estimate (hours)
    4. Complexity score (1-10)
    5. Enhancement preservation rate (%)
    6. Constitutional compliance score (%)
    7. Recommended execution steps
    ..."""
)

# Use fallback chain for reliability
orchestrator = LLMOrchestrator(config)
strategies = orchestrator.generate_with_fallback(
    prompt=strategy_prompt,
    conflict_data=data,
    constitutional_rules=rules,
    pr_context=context
)
```

---

#### 4. `execute-tests` (Consolidated from pr-test-executor.sh)
```bash
eai execute-tests --pr <number> [--phase <baseline|improved>] [--framework <name>]
```

**Purpose**: Execute comprehensive testing framework (consolidates pr-test-executor.sh)  
**Output**: Test results with metrics and analysis  
**Features**:
- Baseline vs improved testing methodology
- Automated data collection
- Performance metrics calculation
- Test result analysis
- Integration with validation framework

**Implementation**:
- Consolidates pr-test-executor.sh functionality
- Supports multiple test frameworks
- Provides detailed test reports
- Integrates with CI/CD systems

---

### LLM-Powered Features

#### Constitutional Analysis with LLM
```python
constitutional_prompt = PromptTemplate(
    input_variables=["code_changes", "rules"],
    template="""Analyze code changes for constitutional compliance:
    
    Code Changes: {code_changes}
    Constitutional Rules: {rules}
    
    Provide:
    1. Compliance score (0-1)
    2. Violations found
    3. Recommendations for fixes
    4. Risk assessment
    ..."""
)

---

## SOLID Principles Implementation

### Architecture Design Principles

The unified PR resolution CLI will be built following SOLID principles to ensure modularity, flexibility, and maintainability across all subfeatures.

---

### 1. Single Responsibility Principle (SRP)

**Each module has one reason to change**

#### Module Responsibilities

**LLM Provider Module** (`src/llm/providers/`)
```python
# Each provider has single responsibility: communicate with its API
class OpenAIProvider:
    """Responsible only for OpenAI API communication"""
    def generate(self, prompt: str, **kwargs) -> str:
        pass

class AnthropicProvider:
    """Responsible only for Anthropic API communication"""
    def generate(self, prompt: str, **kwargs) -> str:
        pass

class GoogleProvider:
    """Responsible only for Google Gemini API communication"""
    def generate(self, prompt: str, **kwargs) -> str:
        pass
```

**Configuration Module** (`src/config/`)
```python
class TOMLConfigLoader:
    """Responsible only for loading TOML configuration"""
    def load(self, path: str) -> dict:
        pass

class EnvironmentVariableResolver:
    """Responsible only for resolving environment variables"""
    def resolve(self, config: dict) -> dict:
        pass

class ConfigValidator:
    """Responsible only for validating configuration"""
    def validate(self, config: dict) -> bool:
        pass
```

**Specification Module** (`src/specification/`)
```python
class SpecificationGenerator:
    """Responsible only for generating specifications"""
    def generate(self, pr_context: dict) -> str:
        pass

class SpecificationValidator:
    """Responsible only for validating specifications"""
    def validate(self, spec: str) -> bool:
        pass

class SpecificationPersister:
    """Responsible only for saving specifications"""
    def save(self, spec: str, path: str) -> None:
        pass
```

---

### 2. Open/Closed Principle (OCP)

**Open for extension, closed for modification**

#### Extensible Provider System

```python
from abc import ABC, abstractmethod

class LLMProvider(ABC):
    """Base provider interface - closed for modification"""
    
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate response from LLM"""
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """Get provider name"""
        pass
    
    @abstractmethod
    def get_capabilities(self) -> dict:
        """Get provider capabilities"""
        pass

# New providers extend without modifying base
class GroqProvider(LLMProvider):
    """Groq provider - extends base interface"""
    def generate(self, prompt: str, **kwargs) -> str:
        # Groq-specific implementation
        pass
    
    def get_name(self) -> str:
        return "groq"
    
    def get_capabilities(self) -> dict:
        return {"max_tokens": 4096, "streaming": True}

class CustomProvider(LLMProvider):
    """Custom provider - extends base interface"""
    def generate(self, prompt: str, **kwargs) -> str:
        # Custom implementation
        pass
```

#### Extensible Strategy System

```python
class ResolutionStrategy(ABC):
    """Base strategy interface"""
    
    @abstractmethod
    def analyze(self, conflict: dict) -> dict:
        pass
    
    @abstractmethod
    def generate_plan(self, analysis: dict) -> dict:
        pass
    
    @abstractmethod
    def estimate_effort(self, plan: dict) -> dict:
        pass

# Strategies extend without modifying base
class ConservativeStrategy(ResolutionStrategy):
    """Conservative resolution approach"""
    pass

class BalancedStrategy(ResolutionStrategy):
    """Balanced resolution approach"""
    pass

class AggressiveStrategy(ResolutionStrategy):
    """Aggressive resolution approach"""
    pass

# Custom strategies can be added
class CustomStrategy(ResolutionStrategy):
    """User-defined custom strategy"""
    pass
```

---

### 3. Liskov Substitution Principle (LSP)

**Subtypes must be substitutable for their base types**

#### Provider Substitutability

```python
class LLMOrchestrator:
    """Orchestrator works with any LLMProvider implementation"""
    
    def __init__(self, provider: LLMProvider):
        self.provider = provider  # Any LLMProvider subtype works
    
    def generate_specification(self, context: dict) -> str:
        # Works with any provider implementation
        prompt = self._create_prompt(context)
        return self.provider.generate(prompt)

# All providers are substitutable
orchestrator1 = LLMOrchestrator(OpenAIProvider())
orchestrator2 = LLMOrchestrator(AnthropicProvider())
orchestrator3 = LLMOrchestrator(GroqProvider())
# All work identically from orchestrator's perspective
```

#### Strategy Substitutability

```python
class StrategyExecutor:
    """Executor works with any ResolutionStrategy implementation"""
    
    def execute(self, strategy: ResolutionStrategy, conflict: dict) -> dict:
        # Works with any strategy implementation
        analysis = strategy.analyze(conflict)
        plan = strategy.generate_plan(analysis)
        effort = strategy.estimate_effort(plan)
        return {"analysis": analysis, "plan": plan, "effort": effort}

# All strategies are substitutable
executor = StrategyExecutor()
result1 = executor.execute(ConservativeStrategy(), conflict)
result2 = executor.execute(BalancedStrategy(), conflict)
result3 = executor.execute(CustomStrategy(), conflict)
# All work identically from executor's perspective
```

---

### 4. Interface Segregation Principle (ISP)

**Clients should not depend on interfaces they don't use**

#### Segregated Interfaces

```python
# Instead of one large interface
class LLMProviderBad:
    def generate(self): pass
    def stream(self): pass
    def embed(self): pass
    def fine_tune(self): pass
    def moderate(self): pass
    # Not all providers support all features!

# Segregate into focused interfaces
class TextGenerator(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        pass

class StreamingGenerator(ABC):
    @abstractmethod
    def stream(self, prompt: str) -> Iterator[str]:
        pass

class Embedder(ABC):
    @abstractmethod
    def embed(self, text: str) -> List[float]:
        pass

class ContentModerator(ABC):
    @abstractmethod
    def moderate(self, text: str) -> dict:
        pass

# Providers implement only what they support
class OpenAIProvider(TextGenerator, StreamingGenerator, Embedder, ContentModerator):
    """Supports all features"""
    pass

class GroqProvider(TextGenerator, StreamingGenerator):
    """Supports only generation and streaming"""
    pass

class PerplexityProvider(TextGenerator):
    """Supports only generation"""
    pass
```

#### Segregated Configuration Interfaces

```python
class ConfigLoader(ABC):
    @abstractmethod
    def load(self, path: str) -> dict:
        pass

class ConfigValidator(ABC):
    @abstractmethod
    def validate(self, config: dict) -> bool:
        pass

class ConfigPersister(ABC):
    @abstractmethod
    def save(self, config: dict, path: str) -> None:
        pass

# Clients use only what they need
class ReadOnlyConfigClient:
    def __init__(self, loader: ConfigLoader):
        self.loader = loader  # Only needs loading

class ConfigEditorClient:
    def __init__(self, loader: ConfigLoader, validator: ConfigValidator, persister: ConfigPersister):
        self.loader = loader
        self.validator = validator
        self.persister = persister  # Needs all three
```

---

### 5. Dependency Inversion Principle (DIP)

**Depend on abstractions, not concretions**

#### Dependency Injection Architecture

```python
# High-level module depends on abstraction
class SpecificationCreator:
    """High-level specification creation logic"""
    
    def __init__(
        self,
        llm_provider: LLMProvider,  # Abstraction
        github_client: GitHubClient,  # Abstraction
        config_loader: ConfigLoader,  # Abstraction
        validator: SpecificationValidator  # Abstraction
    ):
        self.llm = llm_provider
        self.github = github_client
        self.config = config_loader
        self.validator = validator
    
    def create(self, pr_number: int) -> str:
        # High-level logic using abstractions
        config = self.config.load(".emailintelligence.toml")
        pr_context = self.github.get_pr_context(pr_number)
        spec = self.llm.generate(self._create_prompt(pr_context))
        
        if self.validator.validate(spec):
            return spec
        raise ValueError("Invalid specification")

# Dependency injection at runtime
creator = SpecificationCreator(
    llm_provider=AnthropicProvider(),  # Concrete implementation
    github_client=PyGithubClient(),  # Concrete implementation
    config_loader=TOMLConfigLoader(),  # Concrete implementation
    validator=SchemaValidator()  # Concrete implementation
)
```

#### Factory Pattern for Dependency Creation

```python
class ProviderFactory:
    """Factory creates providers based on configuration"""
    
    @staticmethod
    def create(provider_name: str, config: dict) -> LLMProvider:
        """Create provider from configuration"""
        providers = {
            "openai": OpenAIProvider,
            "anthropic": AnthropicProvider,
            "google": GoogleProvider,
            "groq": GroqProvider,
        }
        
        provider_class = providers.get(provider_name)
        if not provider_class:
            raise ValueError(f"Unknown provider: {provider_name}")
        
        return provider_class(config)

class OrchestratorFactory:
    """Factory creates orchestrator with dependencies"""
    
    @staticmethod
    def create(config_path: str) -> LLMOrchestrator:
        """Create orchestrator with all dependencies"""
        config_loader = TOMLConfigLoader()
        config = config_loader.load(config_path)
        
        provider = ProviderFactory.create(
            config['general']['default_provider'],
            config
        )
        
        cache = SQLiteCache(config['general']['cache_path'])
        
        return LLMOrchestrator(provider, cache)
```

---

### Modular Architecture Design

#### Component Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     CLI Interface Layer                      │
│  (eai create-specification, compare-strategies, etc.)       │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────┴────────────────────────────────────────┐
│                  Application Service Layer                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │Specification │  │   Strategy   │  │   GitHub     │      │
│  │   Creator    │  │  Comparator  │  │ Integration  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────┴────────────────────────────────────────┐
│                    Domain Logic Layer                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Resolution   │  │Constitutional│  │ Enhancement  │      │
│  │  Strategies  │  │   Analysis   │  │ Preservation │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────┴────────────────────────────────────────┐
│                 Infrastructure Layer                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │LLM Providers │  │   Config     │  │    Cache     │      │
│  │ (OpenAI,etc) │  │   Loaders    │  │   Storage    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

#### Module Structure

---

## Outstanding TODOs & Task Master Research Integration

### Overview

This section identifies outstanding TODOs, unresolved decisions, and areas requiring research. These items should be expanded and researched using Task Master MCP integration to ensure comprehensive implementation planning.

---

### Task Master Integration for TODO Management

#### Automated TODO Discovery

```python
class TODODiscovery:
    """Discover and catalog TODOs across codebase"""
    
    def scan_codebase(self, patterns: List[str] = None) -> List[dict]:
        """Scan for TODO, FIXME, XXX, HACK markers"""
        if patterns is None:
            patterns = [r'TODO', r'FIXME', r'XXX', r'HACK', r'TKTK']
        
        todos = []
        for pattern in patterns:
            results = self._search_files(pattern)
            todos.extend(self._parse_results(results))
        
        return todos
    
    def create_taskmaster_tasks(self, todos: List[dict]) -> None:
        """Create Task Master tasks for each TODO"""
        for todo in todos:
            task = {
                "title": f"Resolve TODO: {todo['description']}",
                "file": todo['file'],
                "line": todo['line'],
                "priority": self._assess_priority(todo),
                "research_required": self._needs_research(todo)
            }
            self.taskmaster.add_task(task)
```

#### Research-Enhanced TODO Resolution

```python
class ResearchEnhancedTODO:
    """Resolve TODOs with LLM research assistance"""
    
    def research_todo(self, todo: dict) -> dict:
        """Research TODO using LLM providers"""
        research_prompt = f"""
        Research and provide implementation guidance for:
        
        TODO: {todo['description']}
        Context: {todo['context']}
        File: {todo['file']}
        
        Provide:
        1. Technical approach options
        2. Best practices
        3. Potential pitfalls
        4. Implementation estimate
        5. Dependencies
        """
        
        research = self.llm_orchestrator.generate(research_prompt)
        return self._parse_research(research)
```

---

### Identified Outstanding TODOs

#### 1. **LLM Provider Integration TODOs**

**TODO-LLM-001: Provider Fallback Logic**
- **Location**: `src/infrastructure/llm/orchestrator.py` (to be created)
- **Description**: Implement intelligent fallback logic when primary provider fails
- **Priority**: HIGH
- **Research Required**: Yes
- **Task Master Action**: Create research task for fallback strategies

**Research Questions**:
- What are best practices for LLM provider fallback?
- How to handle partial failures (e.g., rate limits vs. errors)?
- Should fallback be automatic or require user confirmation?
- How to cache failed provider attempts to avoid repeated failures?

**TODO-LLM-002: Response Caching Strategy**
- **Location**: `src/infrastructure/llm/cache.py` (to be created)
- **Description**: Implement efficient caching to reduce API costs by 60%
- **Priority**: HIGH
- **Research Required**: Yes
- **Task Master Action**: Research caching strategies and TTL optimization

**Research Questions**:
- What cache invalidation strategy is optimal?
- How to handle prompt variations (similar but not identical)?
- Should we use semantic similarity for cache hits?
- What's the optimal cache size and eviction policy?

**TODO-LLM-003: Prompt Template Versioning**
- **Location**: `src/infrastructure/llm/prompts/` (to be created)
- **Description**: Version control for prompt templates with A/B testing
- **Priority**: MEDIUM
- **Research Required**: Yes
- **Task Master Action**: Research prompt versioning best practices

---

#### 2. **Configuration Management TODOs**

**TODO-CONFIG-001: TOML Schema Validation**
- **Location**: `src/infrastructure/config/validator.py` (to be created)
- **Description**: Implement comprehensive TOML configuration validation
- **Priority**: HIGH
- **Research Required**: No
- **Task Master Action**: Create implementation task with schema definition

**Implementation Notes**:
- Use `pydantic` for schema validation
- Support multiple configuration versions
- Provide clear error messages for invalid configs
- Auto-migration for config version upgrades

**TODO-CONFIG-002: Environment Variable Substitution**
- **Location**: `src/infrastructure/config/resolver.py` (to be created)
- **Description**: Secure environment variable resolution with validation
- **Priority**: HIGH
- **Research Required**: Yes
- **Task Master Action**: Research secure env var handling patterns

**Research Questions**:
- How to handle missing environment variables?
- Should we support default values in TOML?
- How to validate API keys without exposing them?
- Should we support encrypted environment variables?

**TODO-CONFIG-003: Gemini CLI Compatibility Testing**
- **Location**: `tests/integration/test_gemini_compat.py` (to be created)
- **Description**: Ensure full compatibility with Gemini CLI config format
- **Priority**: MEDIUM
- **Research Required**: Yes
- **Task Master Action**: Research Gemini CLI config specification

---

#### 3. **Script Consolidation TODOs**

**TODO-CONSOLIDATE-001: Bash Script Migration**
- **Location**: Multiple bash scripts in `scripts/bash/`
- **Description**: Migrate 1,216+ lines of bash scripts to Python CLI
- **Priority**: HIGH
- **Research Required**: No
- **Task Master Action**: Create subtasks for each script migration

**Scripts to Migrate**:
1. `create-pr-resolution-spec.sh` (366 lines) → `eai create-specification`
2. `gh-pr-ci-integration.sh` (483 lines) → `eai github-integration`
3. `pr-test-executor.sh` → `eai execute-tests`

**TODO-CONSOLIDATE-002: PowerShell Script Migration**
- **Location**: `scripts/powershell/create-pr-resolution-spec.ps1`
- **Description**: Migrate 367 lines of PowerShell to cross-platform Python
- **Priority**: HIGH
- **Research Required**: No
- **Task Master Action**: Create migration task with compatibility testing

**TODO-CONSOLIDATE-003: Backward Compatibility Wrappers**
- **Location**: `scripts/wrappers/` (to be created)
- **Description**: Create wrapper scripts for backward compatibility
- **Priority**: MEDIUM
- **Research Required**: No
- **Task Master Action**: Create wrapper implementation tasks

---

#### 4. **Testing Framework TODOs**

**TODO-TEST-001: LLM Provider Mock System**
- **Location**: `tests/mocks/llm_providers.py` (to be created)
- **Description**: Create comprehensive mocks for all LLM providers
- **Priority**: HIGH
- **Research Required**: No
- **Task Master Action**: Create mock implementation tasks

**TODO-TEST-002: Integration Test Suite**
- **Location**: `tests/integration/` (to be created)
- **Description**: Comprehensive integration tests for all workflows
- **Priority**: HIGH
- **Research Required**: No
- **Task Master Action**: Create test suite implementation tasks

**TODO-TEST-003: Performance Benchmarks**
- **Location**: `tests/performance/` (to be created)
- **Description**: Establish performance benchmarks for all operations
- **Priority**: MEDIUM
- **Research Required**: Yes
- **Task Master Action**: Research performance testing best practices

**Research Questions**:
- What are acceptable performance targets for each operation?
- How to benchmark LLM provider response times?
- Should we include cost benchmarks (API usage)?
- How to test caching effectiveness?

---

#### 5. **Documentation TODOs**

**TODO-DOC-001: API Documentation**
- **Location**: `docs/api/` (to be created)
- **Description**: Complete API documentation for all modules
- **Priority**: MEDIUM
- **Research Required**: No
- **Task Master Action**: Create documentation tasks per module

**TODO-DOC-002: User Guide**
- **Location**: `docs/user-guide.md` (to be created)
- **Description**: Comprehensive user guide with examples
- **Priority**: MEDIUM
- **Research Required**: No
- **Task Master Action**: Create user guide writing tasks

**TODO-DOC-003: Migration Guide**
- **Location**: `docs/migration-guide.md` (to be created)
- **Description**: Guide for migrating from bash/PowerShell scripts
- **Priority**: HIGH
- **Research Required**: No
- **Task Master Action**: Create migration guide writing task

---

### Task Master Workflow for TODO Resolution

#### Phase 1: Discovery & Cataloging (Week 1)

```bash
# Use Task Master to catalog all TODOs
eai task-master-sync --discover-todos --create-tasks

# Expected output:
# - 15+ tasks created from TODOs
# - Tasks categorized by priority
# - Research tasks flagged
# - Dependencies mapped
```

#### Phase 2: Research & Planning (Week 2)

```bash
# Research high-priority TODOs with LLM assistance
eai research-todo --id TODO-LLM-001 --provider anthropic --save-results

# Generate implementation plans
eai generate-plan --todo-id TODO-LLM-001 --output plans/llm-fallback.md
```

#### Phase 3: Implementation (Weeks 3-4)

```bash
# Implement TODOs with Task Master tracking
eai implement-todo --id TODO-LLM-001 --track-progress

# Update Task Master status
eai task-master-sync --update-status --id TODO-LLM-001 --status in-progress
```

#### Phase 4: Validation & Completion (Week 5)

```bash
# Validate TODO resolution
eai validate-todo --id TODO-LLM-001 --run-tests

# Mark complete in Task Master
eai task-master-sync --complete --id TODO-LLM-001
```

---

### Research Priority Matrix

| TODO ID | Priority | Research Required | Complexity | Dependencies |
|---------|----------|-------------------|------------|--------------|
| TODO-LLM-001 | HIGH | Yes | High | None |
| TODO-LLM-002 | HIGH | Yes | Medium | TODO-LLM-001 |
| TODO-LLM-003 | MEDIUM | Yes | Medium | TODO-LLM-002 |
| TODO-CONFIG-001 | HIGH | No | Low | None |
| TODO-CONFIG-002 | HIGH | Yes | Medium | TODO-CONFIG-001 |
| TODO-CONFIG-003 | MEDIUM | Yes | Low | TODO-CONFIG-001 |
| TODO-CONSOLIDATE-001 | HIGH | No | High | None |
| TODO-CONSOLIDATE-002 | HIGH | No | Medium | TODO-CONSOLIDATE-001 |
| TODO-CONSOLIDATE-003 | MEDIUM | No | Low | TODO-CONSOLIDATE-002 |
| TODO-TEST-001 | HIGH | No | Medium | TODO-LLM-001 |
| TODO-TEST-002 | HIGH | No | High | TODO-CONSOLIDATE-001 |
| TODO-TEST-003 | MEDIUM | Yes | Medium | TODO-TEST-002 |
| TODO-DOC-001 | MEDIUM | No | Medium | All implementation TODOs |
| TODO-DOC-002 | MEDIUM | No | Low | TODO-DOC-001 |
| TODO-DOC-003 | HIGH | No | Low | TODO-CONSOLIDATE-001 |

---

### Automated TODO Tracking Integration

#### CLI Command for TODO Management

```bash
# Discover and catalog TODOs
eai discover-todos --scan-codebase --create-tasks

# Research specific TODO
eai research-todo --id TODO-LLM-001 --provider anthropic

# Generate implementation plan
eai plan-todo --id TODO-LLM-001 --output-format markdown

# Track implementation progress
eai track-todo --id TODO-LLM-001 --status in-progress

# Validate TODO resolution
eai validate-todo --id TODO-LLM-001 --run-tests

# Complete TODO
eai complete-todo --id TODO-LLM-001 --close-task
```

---

### Success Metrics for TODO Resolution

**Completion Targets**:
- Week 1: 100% TODOs cataloged and prioritized
- Week 2: 80% research-required TODOs researched
- Week 3-4: 70% high-priority TODOs implemented
- Week 5: 90% TODOs validated and completed

**Quality Metrics**:
- All high-priority TODOs resolved before release
- 100% research-required TODOs have documented research
- All TODOs have associated tests
- Zero unresolved TODOs in production code

---


```
src/
├── cli/                    # CLI Interface Layer
│   ├── commands/
│   │   ├── create_specification.py
│   │   ├── compare_strategies.py
│   │   └── github_integration.py
│   └── main.py
│
├── application/            # Application Service Layer
│   ├── specification_creator.py
│   ├── strategy_comparator.py
│   └── github_integrator.py
│
├── domain/                 # Domain Logic Layer
│   ├── strategies/
│   │   ├── base.py        # ResolutionStrategy ABC
│   │   ├── conservative.py
│   │   ├── balanced.py
│   │   └── aggressive.py
│   ├── constitutional/
│   │   ├── analyzer.py
│   │   └── validator.py
│   └── preservation/
│       └── validator.py
│
└── infrastructure/         # Infrastructure Layer
    ├── llm/
    │   ├── providers/
    │   │   ├── base.py    # LLMProvider ABC
    │   │   ├── openai.py
    │   │   ├── anthropic.py
    │   │   ├── google.py
    │   │   └── groq.py
    │   ├── orchestrator.py
    │   └── cache.py
    ├── config/
    │   ├── loader.py
    │   ├── validator.py
    │   └── resolver.py
    └── github/
        └── client.py
```

---

### Flexible Strategy Pattern Implementation

#### Strategy Registry

```python
class StrategyRegistry:
    """Registry for resolution strategies"""
    
    def __init__(self):
        self._strategies: Dict[str, Type[ResolutionStrategy]] = {}
    
    def register(self, name: str, strategy_class: Type[ResolutionStrategy]):
        """Register a new strategy"""
        self._strategies[name] = strategy_class
    
    def get(self, name: str) -> Type[ResolutionStrategy]:
        """Get strategy by name"""
        return self._strategies.get(name)
    
    def list_available(self) -> List[str]:
        """List all available strategies"""
        return list(self._strategies.keys())

# Global registry
registry = StrategyRegistry()

# Register built-in strategies
registry.register("conservative", ConservativeStrategy)
registry.register("balanced", BalancedStrategy)
registry.register("aggressive", AggressiveStrategy)

# Users can register custom strategies
registry.register("custom-ml", MachineLearningStrategy)
registry.register("custom-manual", ManualReviewStrategy)
```

#### Plugin System for Extensions

```python
class PluginInterface(ABC):
    """Base interface for plugins"""
    
    @abstractmethod
    def get_name(self) -> str:
        pass
    
    @abstractmethod
    def get_version(self) -> str:
        pass
    
    @abstractmethod
    def initialize(self, config: dict) -> None:
        pass

class StrategyPlugin(PluginInterface):
    """Plugin that provides custom strategies"""
    
    @abstractmethod
    def get_strategies(self) -> Dict[str, Type[ResolutionStrategy]]:
        pass

class ProviderPlugin(PluginInterface):
    """Plugin that provides custom LLM providers"""
    
    @abstractmethod
    def get_providers(self) -> Dict[str, Type[LLMProvider]]:
        pass

# Plugin loader
class PluginLoader:
    def load_plugins(self, plugin_dir: str) -> List[PluginInterface]:
        """Load plugins from directory"""
        pass
```

---

### Benefits of SOLID Implementation

#### Modularity
- ✅ Each component has clear, single responsibility
- ✅ Components can be developed and tested independently
- ✅ Easy to understand and maintain

#### Flexibility
- ✅ New providers can be added without modifying existing code
- ✅ New strategies can be registered dynamically
- ✅ Configuration sources can be swapped
- ✅ Testing frameworks can be changed

#### Testability
- ✅ Dependencies can be mocked easily
- ✅ Unit tests focus on single responsibilities
- ✅ Integration tests verify contracts
- ✅ Test doubles can replace real implementations

#### Extensibility
- ✅ Plugin system for custom extensions
- ✅ Strategy registry for custom strategies
- ✅ Provider factory for new LLM providers
- ✅ Open for extension, closed for modification

---

```

#### Strategy Recommendation Engine
```python
recommendation_prompt = PromptTemplate(
    input_variables=["strategies", "project_context"],
    template="""Recommend the best strategy:
    
    Available Strategies: {strategies}
    Project Context: {project_context}
    
    Consider:
    1. Time constraints
    2. Risk tolerance
    3. Team expertise
    4. Project deadlines
    
    Provide recommendation with reasoning..."""
)
```

---

track_progress = true
```

---

## Technical Specification

### New CLI Commands

#### 1. `create-specification`
```bash
eai create-specification --pr <number> [--interactive] [--template <name>]
```

**Purpose**: Interactive specification creation wizard  
**Output**: Generates `specs/<pr-number>-resolution/spec.md`  
**Features**:
- Interactive prompts for all specification sections
- Template-based initialization
- Real-time validation
- Auto-population from git metadata

**Workflow**:
1. Prompt for PR number and basic info
2. Analyze git branches for conflict details
3. Guide through specification sections
4. Validate completeness
5. Save to standardized location

---

#### 2. `compare-strategies`
```bash
eai compare-strategies --pr <number> [--strategies <count>] [--recommend]
```

**Purpose**: Generate and compare multiple resolution strategies  
**Output**: Strategy comparison table and recommendation  
**Features**:
- Generate 3-5 distinct strategies
- Compare across metrics (time, risk, complexity, preservation)
- AI-powered recommendation
- Interactive strategy selection

**Comparison Metrics**:
- Estimated resolution time
- Risk level (low/medium/high)
- Complexity score (1-10)
- Enhancement preservation rate
- Constitutional compliance score
- Team effort required

---

#### 3. `generate-tests`
```bash
eai generate-tests --pr <number> [--framework <pytest|unittest>] [--coverage-target <percent>]
```

**Purpose**: Automated test generation from specifications  
**Output**: Test files in `tests/` directory  
**Features**:
- Unit test generation
- Integration test creation
- Performance benchmark generation
- Enhancement preservation tests

**Test Categories**:
- Conflict resolution logic tests
- Constitutional compliance tests
- Enhancement preservation tests
- Integration workflow tests
- Performance regression tests

---

#### 4. `task-master-sync`
```bash
eai task-master-sync --pr <number> [--create-tasks] [--update-status]
```

**Purpose**: Synchronize resolution workflow with Task Master  
**Output**: Task creation/update confirmation  
**Features**:
- Automatic task creation from phases
- Task dependency mapping
- Progress tracking
- Status synchronization

**Task Structure**:
```json
{
  "task_id": "pr-123-phase-1",
  "title": "Phase 1: Content Analysis & Alignment",
  "description": "Analyze conflicts and determine alignment strategies",
  "dependencies": [],
  "status": "pending",
  "estimated_time": "30-45 minutes"
}
```

---

### Configuration Extensions

#### Constitutional Templates
Location: `.emailintelligence/constitutions/templates/`

**Template Categories**:
1. `security.yaml` - Security-focused rules
2. `performance.yaml` - Performance requirements
3. `code-quality.yaml` - Code quality standards
4. `architecture.yaml` - Architectural constraints
5. `testing.yaml` - Testing requirements

**Template Structure**:
```yaml
name: "Security Constitutional Rules"
version: "1.0.0"
category: "security"
requirements:
  - name: "Input Validation"
    type: "MUST"
    description: "All user inputs must be validated"
    severity: "critical"
  - name: "Authentication Required"
    type: "MUST"
    description: "Protected endpoints require authentication"
    severity: "critical"
```

---

#### Strategy Comparison Configuration
Location: `.emailintelligence/config.yaml`

**New Configuration Section**:
```yaml
strategy_comparison:
  enabled: true
  default_strategies: 3
  metrics:
    - time_estimate
    - risk_level
    - complexity_score
    - preservation_rate
    - compliance_score
  recommendation_weights:
    time: 0.2
    risk: 0.3
    complexity: 0.1
    preservation: 0.3
    compliance: 0.1
```

---

### Integration Points

#### 1. Task Master MCP Integration
**MCP Server**: `task-master-ai`  
**Tools Used**:
- `add_task` - Create resolution phase tasks
- `get_tasks` - Retrieve task status
- `set_task_status` - Update task completion
- `add_dependency` - Map phase dependencies

**Integration Flow**:
```
1. Parse resolution strategy phases
2. Create Task Master task for each phase
3. Map dependencies between phases
4. Track progress via task status
5. Trigger validation on phase completion
```

---

#### 2. Specification Schema Validation
**Schema Location**: `.emailintelligence/schemas/specification.json`

**Required Sections**:
- `metadata` - PR number, branches, dates
- `conflict_analysis` - Detailed conflict description
- `constitutional_requirements` - Applicable rules
- `resolution_strategy` - Planned approach
- `success_criteria` - Validation requirements
- `risk_assessment` - Identified risks and mitigations

---

### File Structure Extensions

```
.emailintelligence/
├── constitutions/
│   ├── templates/
│   │   ├── security.yaml
│   │   ├── performance.yaml
│   │   ├── code-quality.yaml
│   │   ├── architecture.yaml
│   │   └── testing.yaml
│   └── custom/
│       └── project-specific.yaml
├── schemas/
│   ├── specification.json
│   ├── strategy.json
│   └── constitution.json
├── strategies/
│   └── templates/
│       ├── conservative.json
│       ├── balanced.json
│       └── aggressive.json
└── config.yaml

specs/
└── <pr-number>-resolution/
    ├── spec.md
    ├── strategy-comparison.md
    ├── selected-strategy.json
    ├── risk-assessment.md
    └── test-plan.md

tests/
└── generated/
    └── pr-<number>/
        ├── test_conflict_resolution.py
        ├── test_constitutional_compliance.py
        ├── test_enhancement_preservation.py
        └── test_integration_workflow.py
```

---

## Non-Functional Requirements

### Performance
- Specification creation: < 5 minutes (70% faster than manual)
- Strategy comparison: < 2 minutes for 3 strategies
- Test generation: < 1 minute for standard test suite
- Task Master sync: < 10 seconds
- Constitutional validation: < 30 seconds

### Reliability
- Specification validation: 100% schema compliance
- Constitutional compliance: 95%+ violation detection
- Test generation: 80%+ code coverage
- Enhancement preservation: 95%+ feature retention
- Task Master integration: 99%+ uptime

### Usability
- Interactive wizard: Clear prompts with examples
- Strategy comparison: Visual table with color coding
- Test generation: Automatic framework detection
- Error messages: Actionable guidance
- Progress indicators: Real-time status updates

---

## Implementation Constraints

### Technical Constraints
- Must maintain backward compatibility with existing CLI
- Constitutional templates must be YAML/JSON format
- Test generation limited to Python frameworks
- Task Master integration requires MCP server availability
- Specification schema must be extensible

### Organizational Constraints
- Constitutional compliance is mandatory
- Enhancement preservation minimum 95%
- Human review required for critical decisions
- Test coverage minimum 80%
- Documentation must follow spec-kit standards

---

## Quality Standards

### Code Quality
- All new features follow spec-kit principles
- Test coverage > 90% for new code
- Performance benchmarks established
- Documentation complete and accurate
- Type hints for all public APIs

### Process Quality
- Specification → Plan → Tasks → Implement workflow
- Constitutional validation gates enforced
- Risk assessment required for all features
- Enhancement preservation validated
- Continuous integration testing

---

## Dependencies

### External Dependencies
- Task Master MCP server (optional but recommended)
- YAML parser (PyYAML)
- JSON schema validator
- Git command-line tools
- Python 3.9+

### Internal Dependencies
- Existing EmailIntelligence CLI (`emailintelligence_cli.py`)
- Constitutional analysis framework
- Worktree management system
- Validation framework
- Strategy generation system

---

## Migration Path

### Phase 1: Core Extensions (Week 1)
1. Implement `create-specification` command
2. Add constitutional template system
3. Extend configuration schema
4. Create specification validation

### Phase 2: Strategy Enhancement (Week 2)
1. Implement `compare-strategies` command
2. Add strategy comparison metrics
3. Build recommendation engine
4. Create strategy templates

### Phase 3: Automation (Week 3)
1. Implement `generate-tests` command
2. Add Task Master integration
3. Build enhancement preservation validation
4. Create automated workflows

### Phase 4: Integration & Polish (Week 4)
1. Integrate all new commands
2. Comprehensive testing
3. Documentation completion
4. Performance optimization

---

## Success Metrics

### Adoption Metrics
- 80%+ developers use interactive specification wizard
- 90%+ resolutions use constitutional templates
- 70%+ developers compare multiple strategies
- 60%+ projects integrate with Task Master

### Quality Metrics
- 95%+ constitutional compliance rate
- 95%+ enhancement preservation rate
- 80%+ test coverage from generation
- 90%+ specification completeness

### Efficiency Metrics
- 70% reduction in specification creation time
- 50% reduction in strategy development time
- 60% reduction in test writing time
- 40% reduction in overall resolution time

---

## Risk Assessment

### High-Risk Areas
1. **Task Master Integration**
   - Risk: External dependency availability
   - Mitigation: Graceful degradation when unavailable
   - Fallback: Manual task tracking

2. **Test Generation Quality**
   - Risk: Generated tests may be incomplete
   - Mitigation: Human review required
   - Fallback: Manual test supplementation

3. **Constitutional Template Accuracy**
   - Risk: Templates may not cover all scenarios
   - Mitigation: Extensible template system
   - Fallback: Custom rule creation

### Medium-Risk Areas
1. **Strategy Comparison Accuracy**
   - Risk: Recommendations may be suboptimal
   - Mitigation: Multiple metrics and human review
   
2. **Specification Validation**
   - Risk: Schema may be too rigid
   - Mitigation: Extensible schema design

---

## Future Enhancements

### Phase 5+ Considerations
- AI-powered conflict resolution suggestions
- Machine learning for strategy optimization
- Integration with CI/CD pipelines
- Real-time collaboration features
- Advanced analytics and reporting
- Custom plugin system

---

## Change Log
- **2025-11-12**: Initial specification created
- **Status**: Ready for `/speckit.clarify` or `/speckit.plan`

---

## Appendix

### A. Example Specification Template
```markdown
# PR Resolution Specification

## Metadata
- PR Number: 123
- Source Branch: feature/auth
- Target Branch: main
- Created: 2025-11-12

## Conflict Analysis
[Detailed conflict description]

## Constitutional Requirements
[Applicable constitutional rules]

## Resolution Strategy
[Planned resolution approach]

## Success Criteria
[Validation requirements]

## Risk Assessment
[Identified risks and mitigations]
```

### B. Example Strategy Comparison Output
```
Strategy Comparison for PR #123
================================

| Metric              | Conservative | Balanced | Aggressive |
|---------------------|--------------|----------|------------|
| Time Estimate       | 3-4 hours    | 2-3 hours| 1-2 hours  |
| Risk Level          | Low          | Medium   | High       |
| Complexity          | 3/10         | 5/10     | 8/10       |
| Preservation Rate   | 100%         | 98%      | 95%        |
| Compliance Score    | 98%          | 95%      | 90%        |

Recommendation: BALANCED
Reason: Optimal balance of time, risk, and quality
```

### C. Example Generated Test
```python
# tests/generated/pr-123/test_conflict_resolution.py
import pytest
from emailintelligence_cli import EmailIntelligenceCLI

def test_pr_123_setup_resolution():
    """Test resolution workspace setup for PR #123"""
    cli = EmailIntelligenceCLI()
    result = cli.setup_resolution(
        pr_number=123,
        source_branch="feature/auth",
        target_branch="main"
    )
    assert result['success'] is True
    assert 'metadata_file' in result

def test_pr_123_constitutional_compliance():
    """Test constitutional compliance for PR #123"""
    cli = EmailIntelligenceCLI()
    result = cli.analyze_constitutional(pr_number=123)
    assert result['compliance_score'] >= 0.95
```

---

*Specification complete. Ready for clarification and planning phases.*