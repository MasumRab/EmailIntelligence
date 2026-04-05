# EmailIntelligence CLI Framework

This framework provides a modular approach to integrating CLI features into other branches without interfering with existing non-CLI files.

## Overview

The EmailIntelligence CLI Framework enables safe integration of advanced conflict resolution and analysis features into any branch of the EmailIntelligence project. The framework follows a non-interference policy to preserve existing functionality while adding new capabilities.

## Features

- **Modular Installation**: Install only the components you need
- **Safe Integration**: Backups are created before modifying any files
- **Non-Interference Policy**: Existing functionality is preserved
- **Rollback Capability**: Easy restoration to previous state
- **Multiple Installation Modes**: Full, minimal, or custom installations

## Installation Modes

### 1. Minimal Mode (Default)
Installs only the core CLI functionality:
- `emailintelligence_cli.py` - Main CLI entry point
- Core conflict detection and analysis modules
- Basic constitutional engine

### 2. Full Mode
Installs all CLI features with dependencies:
- Complete constitutional analysis engine
- Advanced conflict resolution capabilities
- Semantic merging functionality
- Strategy generation and risk assessment
- All supporting modules

## Usage

### Prerequisites
- `jq` installed on your system

### Installation Commands

```bash
# Install in minimal mode (default)
./.cli_framework/install.sh

# Install in full mode
./.cli_framework/install.sh full

# Check for potential conflicts before installing
./.cli_framework/install.sh minimal
```

## Framework Components

### Core Components
- `emailintelligence_cli.py`: Main CLI application
- `src/resolution/`: Constitutional engine and resolution modules
- `src/git/`: Git operations and conflict detection
- `src/analysis/`: Conflict analysis and constitutional analysis
- `src/core/`: Core models and interfaces

### Optional Components (Full Mode)
- `src/strategy/`: Strategy generation and risk assessment
- `src/validation/`: Validation modules
- `src/utils/`: Utility functions and logging

## Safety Features

1. **Automatic Backups**: All modified files are backed up before changes
2. **Non-Destructive**: Existing functionality is preserved
3. **Modular Design**: Components can be installed independently
4. **Logging**: All installation steps are logged for troubleshooting

## Directory Structure

```
.cli_framework/
├── config.json          # Framework configuration
├── install.sh           # Installation script
├── README.md            # This file
└── install.log          # Installation log (created during installation)
```

## Rollback Procedure

If you need to rollback changes:
1. Locate backup files in `.cli_backups/` directory
2. Restore the files you wish to revert

## Integration Points

The framework integrates with:
- Main application entry points (`src/main.py`)
- API endpoints
- Configuration files
- Existing project structure

## Best Practices

1. Always run installation in a clean git state
2. Review changes before committing
3. Test functionality after installation
4. Keep backups until you're satisfied with the changes

## Support

For issues or questions about the CLI Framework, please contact the development team.