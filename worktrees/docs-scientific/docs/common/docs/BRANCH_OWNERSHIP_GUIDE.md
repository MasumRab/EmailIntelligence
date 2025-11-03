# 📋 Branch Ownership & File Zone Guide

**Document Version:** 1.0
**Last Updated:** October 31, 2025
**Branches:** `scientific` (main) ↔ `feature-dashboard-stats-endpoint`

## 🎯 **Purpose**

This guide establishes clear **file ownership zones** and **branch responsibilities** to maintain maximal alignment between the `scientific` branch and `feature-dashboard-stats-endpoint` branch during dashboard consolidation development.

## 🗂️ **File Ownership Matrix**

### **🔴 Scientific Branch Exclusive Zones**

**Branch:** `scientific` (primary ownership)
**Purpose:** Core platform architecture and shared infrastructure

#### **Core Architecture (`src/`)**
```
src/
├── core/                    # 🔴 SCIENTIFIC EXCLUSIVE
│   ├── data/               # 🔴 Data access abstractions
│   ├── database.py         # 🔴 Database connections
│   ├── factory.py          # 🔴 Service factories
│   ├── ai_engine.py        # 🔴 AI processing core
│   └── auth.py             # 🔴 Authentication system
├── main.py                 # 🔴 Application entry point
└── **/*.py                 # 🔴 All other core files
```

#### **Backend Infrastructure (`backend/`)**
```
backend/
├── python_backend/         # 🔴 SCIENTIFIC EXCLUSIVE
│   ├── main.py            # 🔴 Legacy API (deprecated)
│   ├── database.py        # 🔴 Database operations
│   ├── models.py          # 🔴 Data models
│   └── services/          # 🔴 Business logic
└── **/*                    # 🔴 All backend files
```

#### **Shared Infrastructure**
```
├── pyproject.toml          # 🔴 Dependencies & build config
├── requirements*.txt       # 🔴 Python dependencies
├── launch.py              # 🔴 Application launcher
├── docker-compose*.yml     # 🔴 Container configuration
├── nginx/                  # 🔴 Web server config
├── monitoring/             # 🔴 Monitoring & logging
└── tests/                  # 🔴 Core test infrastructure
```

### **🟡 Feature Branch Exclusive Zones**

**Branch:** `feature-dashboard-stats-endpoint` (primary ownership)
**Purpose:** Dashboard consolidation and modular dashboard system

#### **Dashboard Module (`modules/dashboard/`)**
```
modules/dashboard/          # 🟡 FEATURE EXCLUSIVE
├── __init__.py            # 🟡 Module registration
├── routes.py              # 🟡 Dashboard API endpoints
├── models.py              # 🟡 Dashboard data models
└── **/*                   # 🟡 All dashboard files
```

#### **Dashboard Documentation (`docs/`)**
```
docs/
├── DASHBOARD_CONSOLIDATION_REPORT.md    # 🟡 Feature documentation
├── BRANCH_OWNERSHIP_GUIDE.md            # 🟡 This file
└── **dashboard*                         # 🟡 Dashboard-related docs
```

#### **Dashboard Tests (`tests/modules/dashboard/`)**
```
tests/modules/dashboard/    # 🟡 FEATURE EXCLUSIVE
├── test_dashboard.py      # 🟡 Dashboard unit tests
└── **/*                   # 🟡 Dashboard test files
```

### **🟢 Shared Zones (Collaborative Ownership)**

**Ownership:** Both branches (coordinated changes)
**Process:** Requires discussion and approval

#### **Module System (`modules/`)**
```
modules/
├── __init__.py            # 🟢 COORDINATED
├── auth/                  # 🟢 SCIENTIFIC (may affect dashboard)
├── categories/            # 🟢 SCIENTIFIC (may affect dashboard)
├── email/                 # 🟢 SCIENTIFIC (may affect dashboard)
└── **/*                   # 🟢 Discuss changes with feature team
```

#### **Client Interface (`client/`)**
```
client/
├── src/pages/dashboard.tsx    # 🟢 COORDINATED (dashboard UI)
└── **/*                       # 🟢 Frontend changes coordinated
```

#### **Configuration Files**
```
├── .gitignore              # 🟢 COORDINATED
├── package.json           # 🟢 COORDINATED
├── tsconfig.json          # 🟢 COORDINATED
└── **config files         # 🟢 Discuss breaking changes
```

## 🚦 **Conflict Resolution Protocol**

### **Zone 1: Exclusive Zones**
- **🔴 Scientific files:** Feature branch defers to scientific
- **🟡 Feature files:** Scientific branch should not modify
- **Action:** Accept the owning branch's version

### **Zone 2: Shared Zones**
- **Process:** Create issue/discussion before changes
- **Review:** Both branches review impact
- **Merge:** Coordinate through PR with both approvals

### **Zone 3: New Files**
- **Location:** Add to appropriate zone based on purpose
- **Documentation:** Update this guide when adding new zones

## 🔄 **Merge & Sync Protocol**

### **Weekly Sync Routine**
```bash
# On feature branch
git checkout feature-dashboard-stats-endpoint
git fetch origin
git merge origin/scientific --no-ff
# Test dashboard functionality
# Resolve any conflicts per ownership rules
git push origin feature-dashboard-stats-endpoint
```

### **Merge Readiness Checklist**
- [ ] All exclusive zone conflicts resolved per ownership
- [ ] Shared zone changes discussed and approved
- [ ] Dashboard functionality tested after merge
- [ ] No breaking changes to dependent systems

## 📊 **Monitoring & Metrics**

### **Alignment Health Indicators**
- ✅ **Zero conflicts** in exclusive zones
- ✅ **Coordinated changes** in shared zones
- ✅ **Weekly syncs** completed without issues
- ✅ **Dashboard tests** passing after merges

### **Ownership Drift Detection**
- **Monthly review** of file changes by zone
- **Automated checks** for cross-zone modifications
- **Documentation updates** when ownership changes

## 👥 **Team Responsibilities**

### **Scientific Branch Team**
- **Own:** Core architecture and shared infrastructure
- **Review:** Changes to shared zones
- **Support:** Feature branch integration
- **Communicate:** Breaking changes that affect dashboard

### **Feature Branch Team (Dashboard)**
- **Own:** Dashboard module and consolidation
- **Review:** Dashboard-related changes in shared zones
- **Test:** Dashboard functionality after scientific merges
- **Communicate:** Dashboard API changes and requirements

## 🚨 **Emergency Procedures**

### **Breaking Changes**
1. **Stop development** on affected branch
2. **Create issue** documenting the conflict
3. **Schedule meeting** between branch owners
4. **Implement solution** per ownership guidelines

### **Ownership Disputes**
1. **Document concerns** in issue tracker
2. **Escalate to** technical lead if needed
3. **Update this guide** with resolution
4. **Communicate changes** to all team members

## 📋 **Guide Maintenance**

### **Update Triggers**
- New files added to codebase
- Ownership changes between branches
- New shared zones identified
- Process improvements discovered

### **Update Process**
1. **Propose changes** via PR to this document
2. **Review** by both branch teams
3. **Approve** and merge changes
4. **Communicate** updates to team

---

**Document Owner:** Dashboard Consolidation Team
**Review Cycle:** Monthly
**Last Reviewed:** October 31, 2025

**Next Review:** November 30, 2025</content>
</xai:function_call">Create comprehensive branch ownership guide
