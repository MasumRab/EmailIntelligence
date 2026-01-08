# 🛠️ Task Master AI MCP Configuration Guide

## 🎯 Overview

This guide provides comprehensive instructions for setting up Task Master AI MCP (Multi-Cursor Protocol) configurations for different agents and development environments.

## 📁 Configuration Files

### 1. **Cursor Editor Configuration**
**File**: `.cursor/mcp.json`

```json
{
	"mcpServers": {
		"task-master-ai": {
			"command": "npx",
			"args": ["-y", "task-master-ai"],
			"env": {
				"ANTHROPIC_API_KEY": "YOUR_ANTHROPIC_API_KEY_HERE",
				"PERPLEXITY_API_KEY": "YOUR_PERPLEXITY_API_KEY_HERE",
				"OPENAI_API_KEY": "YOUR_OPENAI_KEY_HERE",
				"GOOGLE_API_KEY": "YOUR_GOOGLE_KEY_HERE",
				"XAI_API_KEY": "YOUR_XAI_KEY_HERE",
				"OPENROUTER_API_KEY": "YOUR_OPENROUTER_KEY_HERE",
				"MISTRAL_API_KEY": "YOUR_MISTRAL_KEY_HERE",
				"AZURE_OPENAI_API_KEY": "YOUR_AZURE_KEY_HERE",
				"OLLAMA_API_KEY": "YOUR_OLLAMA_API_KEY_HERE"
			}
		}
	}
}
```

### 2. **VSCode Configuration**
**File**: `.vscode/mcp.json`

```json
{
  "mcpServers": {
    "task-master-ai": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "task-master-ai"],
      "env": {
        "ANTHROPIC_API_KEY": "YOUR_ANTHROPIC_API_KEY_HERE",
        "PERPLEXITY_API_KEY": "YOUR_PERPLEXITY_API_KEY_HERE",
        "OPENAI_API_KEY": "YOUR_OPENAI_KEY_HERE",
        "GOOGLE_API_KEY": "YOUR_GOOGLE_KEY_HERE",
        "XAI_API_KEY": "YOUR_XAI_KEY_HERE",
        "OPENROUTER_API_KEY": "YOUR_OPENROUTER_KEY_HERE",
        "MISTRAL_API_KEY": "YOUR_MISTRAL_KEY_HERE",
        "AZURE_OPENAI_API_KEY": "YOUR_AZURE_KEY_HERE",
        "OLLAMA_API_KEY": "YOUR_OLLAMA_API_KEY_HERE"
      }
    }
  }
}
```

## 🔧 Setup Instructions

### 1. **Prerequisites**

#### Required Tools
- Node.js (v18+ recommended)
- npm or yarn
- Git
- Task Master AI CLI (`task-master-ai`)

#### Install Task Master AI
```bash
npm install -g task-master-ai
# or
npx task-master-ai --version
```

### 2. **API Key Configuration**

#### Environment Variables
Create a `.env` file in your project root:

```bash
# .env
ANTHROPIC_API_KEY=your_anthropic_api_key_here
PERPLEXITY_API_KEY=your_perplexity_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
XAI_API_KEY=your_xai_api_key_here
OPENROUTER_API_KEY=your_openrouter_api_key_here
MISTRAL_API_KEY=your_mistral_api_key_here
AZURE_OPENAI_API_KEY=your_azure_api_key_here
OLLAMA_API_KEY=your_ollama_api_key_here
```

#### Minimum Required Keys
At least **one** API key is required:
- `ANTHROPIC_API_KEY` (Recommended for Claude models)
- `PERPLEXITY_API_KEY` (Recommended for research features)
- `OPENAI_API_KEY` (For GPT models)

### 3. **Agent-Specific Configurations**

#### 🤖 Agent 1: Claude (Anthropic)
**Configuration**:
```json
{
  "mcpServers": {
    "task-master-claude": {
      "command": "npx",
      "args": ["-y", "task-master-ai"],
      "env": {
        "ANTHROPIC_API_KEY": "your_key_here",
        "TASK_MASTER_MAIN_MODEL": "claude-3-5-sonnet-20241022",
        "TASK_MASTER_RESEARCH_MODEL": "claude-3-haiku-20240307",
        "TASK_MASTER_FALLBACK_MODEL": "claude-3-opus-20240229"
      }
    }
  }
}
```

**Recommended Models**:
- Main: `claude-3-5-sonnet-20241022`
- Research: `claude-3-haiku-20240307` (faster, cheaper)
- Fallback: `claude-3-opus-20240229` (most capable)

#### 🔍 Agent 2: Perplexity (Research Focused)
**Configuration**:
```json
{
  "mcpServers": {
    "task-master-perplexity": {
      "command": "npx",
      "args": ["-y", "task-master-ai"],
      "env": {
        "PERPLEXITY_API_KEY": "your_key_here",
        "TASK_MASTER_MAIN_MODEL": "llama-3.1-sonar-large-128k-online",
        "TASK_MASTER_RESEARCH_MODEL": "llama-3.1-sonar-large-128k-online",
        "TASK_MASTER_FALLBACK_MODEL": "mistral-large-latest"
      }
    }
  }
}
```

**Recommended Models**:
- Main: `llama-3.1-sonar-large-128k-online` (best for research)
- Research: Same as main (Perplexity specializes in research)
- Fallback: `mistral-large-latest`

#### 🤖 Agent 3: OpenAI (GPT Models)
**Configuration**:
```json
{
  "mcpServers": {
    "task-master-gpt": {
      "command": "npx",
      "args": ["-y", "task-master-ai"],
      "env": {
        "OPENAI_API_KEY": "your_key_here",
        "TASK_MASTER_MAIN_MODEL": "gpt-4o-mini",
        "TASK_MASTER_RESEARCH_MODEL": "gpt-4o",
        "TASK_MASTER_FALLBACK_MODEL": "gpt-3.5-turbo"
      }
    }
  }
}
```

**Recommended Models**:
- Main: `gpt-4o-mini` (cost-effective)
- Research: `gpt-4o` (more capable)
- Fallback: `gpt-3.5-turbo` (fastest)

#### 🌐 Agent 4: Multi-Provider (Hybrid)
**Configuration**:
```json
{
  "mcpServers": {
    "task-master-hybrid": {
      "command": "npx",
      "args": ["-y", "task-master-ai"],
      "env": {
        "ANTHROPIC_API_KEY": "your_anthropic_key",
        "PERPLEXITY_API_KEY": "your_perplexity_key",
        "OPENAI_API_KEY": "your_openai_key",
        "TASK_MASTER_MAIN_MODEL": "claude-3-5-sonnet-20241022",
        "TASK_MASTER_RESEARCH_MODEL": "llama-3.1-sonar-large-128k-online",
        "TASK_MASTER_FALLBACK_MODEL": "gpt-4o-mini"
      }
    }
  }
}
```

**Strategy**: Best of each provider for different roles

### 4. **Environment-Specific Setups**

#### 🐧 Linux/WSL Configuration
```json
{
  "mcpServers": {
    "task-master-linux": {
      "command": "npx",
      "args": ["-y", "task-master-ai"],
      "env": {
        "ANTHROPIC_API_KEY": "${ANTHROPIC_API_KEY}",
        "PERPLEXITY_API_KEY": "${PERPLEXITY_API_KEY}",
        "TASK_MASTER_WORKSPACE": "/home/${USER}/taskmaster-workspace",
        "TASK_MASTER_CONFIG": "/home/${USER}/.taskmaster/config.json"
      }
    }
  }
}
```

#### 🍎 macOS Configuration
```json
{
  "mcpServers": {
    "task-master-macos": {
      "command": "npx",
      "args": ["-y", "task-master-ai"],
      "env": {
        "ANTHROPIC_API_KEY": "${ANTHROPIC_API_KEY}",
        "PERPLEXITY_API_KEY": "${PERPLEXITY_API_KEY}",
        "TASK_MASTER_WORKSPACE": "/Users/${USER}/taskmaster-workspace",
        "TASK_MASTER_CONFIG": "/Users/${USER}/.taskmaster/config.json"
      }
    }
  }
}
```

#### ⚙️ Windows Configuration
```json
{
  "mcpServers": {
    "task-master-windows": {
      "command": "npx",
      "args": ["-y", "task-master-ai"],
      "env": {
        "ANTHROPIC_API_KEY": "%ANTHROPIC_API_KEY%",
        "PERPLEXITY_API_KEY": "%PERPLEXITY_API_KEY%",
        "TASK_MASTER_WORKSPACE": "C:\\Users\\%USERNAME%\\taskmaster-workspace",
        "TASK_MASTER_CONFIG": "C:\\Users\\%USERNAME%\\.taskmaster\\config.json"
      }
    }
  }
}
```

## 🎛️ Advanced Configuration

### 1. **Model Role Configuration**

Configure specific models for different Task Master roles:

```json
{
  "mcpServers": {
    "task-master-advanced": {
      "command": "npx",
      "args": ["-y", "task-master-ai"],
      "env": {
        "ANTHROPIC_API_KEY": "your_key_here",
        "TASK_MASTER_MAIN_MODEL": "claude-3-5-sonnet-20241022",
        "TASK_MASTER_RESEARCH_MODEL": "claude-3-haiku-20240307",
        "TASK_MASTER_FALLBACK_MODEL": "claude-3-opus-20240229",
        "TASK_MASTER_PLANNING_MODEL": "claude-3-opus-20240229",
        "TASK_MASTER_ANALYSIS_MODEL": "claude-3-sonnet-20240229",
        "TASK_MASTER_IMPLEMENTATION_MODEL": "claude-3-haiku-20240307"
      }
    }
  }
}
```

### 2. **Task Master Configuration File**

Create `.taskmaster/config.json`:

```json
{
  "models": {
    "main": "claude-3-5-sonnet-20241022",
    "research": "llama-3.1-sonar-large-128k-online",
    "fallback": "gpt-4o-mini",
    "planning": "claude-3-opus-20240229",
    "analysis": "claude-3-sonnet-20240229",
    "implementation": "claude-3-haiku-20240307"
  },
  "workspace": ".taskmaster",
  "defaultProject": "current",
  "api": {
    "timeout": 120000,
    "maxRetries": 3,
    "concurrency": 5
  }
}
```

### 3. **Multi-Agent Workflow**

For team environments with multiple agents:

```json
{
  "mcpServers": {
    "task-master-lead": {
      "command": "npx",
      "args": ["-y", "task-master-ai", "--role", "lead"],
      "env": {
        "ANTHROPIC_API_KEY": "${ANTHROPIC_API_KEY}",
        "TASK_MASTER_ROLE": "lead",
        "TASK_MASTER_MODEL": "claude-3-opus-20240229"
      }
    },
    "task-master-dev": {
      "command": "npx",
      "args": ["-y", "task-master-ai", "--role", "developer"],
      "env": {
        "ANTHROPIC_API_KEY": "${ANTHROPIC_API_KEY}",
        "TASK_MASTER_ROLE": "developer",
        "TASK_MASTER_MODEL": "claude-3-sonnet-20240229"
      }
    },
    "task-master-review": {
      "command": "npx",
      "args": ["-y", "task-master-ai", "--role", "reviewer"],
      "env": {
        "ANTHROPIC_API_KEY": "${ANTHROPIC_API_KEY}",
        "TASK_MASTER_ROLE": "reviewer",
        "TASK_MASTER_MODEL": "claude-3-haiku-20240307"
      }
    }
  }
}
```

## 🚀 Quick Start

### 1. **Basic Setup**
```bash
# Install Task Master AI
npm install -g task-master-ai

# Initialize in your project
npx task-master-ai init

# Configure MCP
cp .cursor/mcp.json.example .cursor/mcp.json
# Edit with your API keys

# Start using
npx task-master-ai list
```

### 2. **Verify Configuration**
```bash
# Check Task Master AI is working
npx task-master-ai --version

# Test MCP connection
# In your editor, check MCP server status

# Verify models are configured
npx task-master-ai models
```

## 🔍 Troubleshooting

### Common Issues

#### 1. **MCP Connection Failed**
**Symptoms**: Editor shows "MCP server not responding"

**Solutions**:
- Verify `npx task-master-ai` works in terminal
- Check API keys are correctly set in environment
- Ensure Node.js is installed and in PATH
- Restart your editor

#### 2. **API Key Errors**
**Symptoms**: "Invalid API key" or "Authentication failed"

**Solutions**:
- Verify keys in `.env` file
- Check keys are correctly referenced in MCP config
- Test keys with provider's API directly
- Ensure no typos in key names

#### 3. **Model Not Found**
**Symptoms**: "Model XYZ not available"

**Solutions**:
- Check model names are correct
- Verify your API key has access to the model
- Use `task-master-ai models --list` to see available models
- Fall back to a different model

### Debug Commands

```bash
# Check Task Master AI installation
npx task-master-ai --version

# List available models
npx task-master-ai models --list

# Test configuration
npx task-master-ai doctor

# Verbose mode
DEBUG=task-master-* npx task-master-ai list
```

## 📚 Best Practices

### 1. **API Key Management**
- Use environment variables, not hardcoded keys
- Rotate keys regularly
- Use different keys for different environments
- Set spending limits on API accounts

### 2. **Model Selection**
- **Main Model**: Balance of capability and cost
- **Research Model**: Optimized for information retrieval
- **Fallback Model**: Fast and reliable
- **Planning Model**: Most capable for complex tasks

### 3. **Configuration Organization**
- Keep `.mcp.json` files in version control (without keys)
- Use `.env` for sensitive data (add to `.gitignore`)
- Document your configuration choices
- Create different configs for different workflows

### 4. **Team Collaboration**
- Standardize on model configurations
- Share configuration templates
- Document workflow patterns
- Use consistent naming conventions

## 🎯 Recommended Model Configurations

### For Different Workflows

| Workflow Type | Main Model | Research Model | Fallback Model |
|---------------|------------|----------------|----------------|
| **General Development** | claude-3-5-sonnet | llama-3.1-sonar-large | gpt-4o-mini |
| **Research Heavy** | llama-3.1-sonar-large | llama-3.1-sonar-large | claude-3-haiku |
| **Code Implementation** | claude-3-haiku | gpt-4o | gpt-3.5-turbo |
| **Planning & Architecture** | claude-3-opus | claude-3-sonnet | claude-3-haiku |
| **Cost Optimized** | gpt-4o-mini | gpt-4o-mini | gpt-3.5-turbo |

### For Different Team Roles

| Team Role | Recommended Configuration |
|-----------|--------------------------|
| **Tech Lead** | Main: Opus, Research: Sonar, Fallback: Sonnet |
| **Developer** | Main: Sonnet, Research: Haiku, Fallback: GPT-4o-mini |
| **Researcher** | Main: Sonar, Research: Sonar, Fallback: Sonar |
| **Reviewer** | Main: Haiku, Research: Sonnet, Fallback: GPT-4o |
| **Documentation** | Main: Sonnet, Research: Sonar, Fallback: Haiku |

## 🔄 Update & Maintenance

### Updating Configurations
```bash
# Update Task Master AI
npm update -g task-master-ai

# Check for new models
npx task-master-ai models --update

# Migrate configurations
npx task-master-ai config migrate
```

### Configuration Versioning
```bash
# Create configuration backup
cp .cursor/mcp.json .cursor/mcp.json.backup-$(date +%Y%m%d)

# Restore from backup
cp .cursor/mcp.json.backup-20241220 .cursor/mcp.json
```

---

*Last Updated: 2025-12-20* | *Task Master AI Version: 2.0+*