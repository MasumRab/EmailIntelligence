# EmailIntelligence Documentation

This directory contains comprehensive documentation for the EmailIntelligence project.

## 📁 Directory Structure

### 📖 [guides/](guides/)
User guides, tutorials, and feature documentation
- Getting started guides
- Feature documentation  
- Module documentation
- Workflow guides

### 🏗️ [architecture/](architecture/)
Architecture and system design documentation
- System architecture overview
- Workflow system design
- Component architecture

### 💻 [development/](development/)
Development and contribution documentation
- Developer guides
- Coding standards
- Environment setup
- Extension development

### 🚀 [deployment/](deployment/)
Deployment and operations documentation
- Deployment guides
- Launch configuration
- Environment hardening

### 🔌 [api/](api/)
API documentation and references
- API reference
- Dashboard APIs
- Integration guides

### 📋 [project-management/](project-management/)
Project management and planning documentation
- Branch management
- Documentation workflow
- Task tracking
- Project reports

### 📝 [adr/](adr/)
Architecture Decision Records
- System design decisions
- Technology choices
- Implementation decisions

### 📋 [changelog/](changelog/)
Change logs and release notes

### 📝 [templates/](templates/)
Documentation templates and examples

## 🚀 Quick Start

1. **New to the project?** Start with [guides/getting_started.md](guides/getting_started.md)
2. **Want to contribute?** Read [development/DEVELOPER_GUIDE.md](development/DEVELOPER_GUIDE.md)
3. **Need API info?** Check [api/API_REFERENCE.md](api/API_REFERENCE.md)
4. **Planning features?** See [project-management/](project-management/)

## 📊 Documentation Health

This documentation is maintained across multiple Git worktrees with automatic synchronization.

- **Inheritance Base**: `docs/clean-inheritance-base` branch
- **Worktrees**: `docs-main` (main), `docs-scientific` (scientific)
- **Sync Status**: Automatically synchronized
- **Health Checks**: Run `python scripts/maintenance_docs.py --health`

## 🤝 Contributing

When adding documentation:
1. Place files in the appropriate subdirectory
2. Follow the established naming conventions
3. Update this README if adding new sections
4. Commit to the appropriate worktree branch

The documentation system will automatically sync changes across all worktrees.
