# Branch Switching Guide for EmailIntelligence

This guide provides instructions for switching between the `scientific` branch (JSON backend) and `sqlite` branch (SQLite backend) in the EmailIntelligence project.

## Understanding the Branches

### Scientific Branch (JSON Backend)
- Uses JSON file storage with gzip compression
- Data stored in `./data/` directory
- No database services required
- Lightweight and suitable for development/testing
- Environment variable: `DATA_DIR` for data directory path

### SQLite Branch (SQLite Backend)
- Uses SQLite database for storage
- Data stored in `sqlite.db` file
- Uses Drizzle ORM for database operations
- Requires database migration scripts
- Environment variable: `DATABASE_URL` for database file path

## Prerequisites

Before switching branches, ensure you have:

1. Git installed and configured
2. Python 3.12+ installed
3. Node.js LTS installed
4. All project dependencies installed for both branches
5. A clean working directory (commit or stash changes)

## Switching from Scientific to SQLite Branch

### 1. Prepare Current Branch
```bash
# Commit or stash any changes
git add .
git commit -m "Save changes before switching branches"  # or git stash

# Ensure data is backed up if needed
cp -r ./data ./data_backup_scientific
```

### 2. Switch to SQLite Branch
```bash
git checkout sqlite
```

### 3. Install Dependencies
```bash
<<<<<<< HEAD
# Install/update all dependencies using launch.py
python launch.py --update-deps
=======
# Install/update Python dependencies
pip install -r requirements.txt

# Install/update Node.js dependencies
npm install
>>>>>>> scientific
```

### 4. Set Up Environment
```bash
# Copy .env.example to .env if it doesn't exist
cp .env.example .env  # if .env.example exists

# Ensure DATABASE_URL is set correctly in .env
echo "DATABASE_URL=sqlite.db" >> .env
```

### 5. Migrate Data (Optional)
If you want to preserve data from the scientific branch:

```bash
# Use the data migration utility to convert JSON data to SQLite
<<<<<<< HEAD
python old_workflow_docs/data_migration.py json-to-sqlite --data-dir ./data --db-path sqlite.db
=======
python deployment/data_migration.py json-to-sqlite --data-dir ./data --db-path sqlite.db
>>>>>>> scientific
```

### 6. Initialize Database
```bash
# Run database migrations
python deployment/migrate.py apply
```

### 7. Run Tests
```bash
# Run tests to ensure everything works correctly
python -m pytest
```

## Switching from SQLite to Scientific Branch

### 1. Prepare Current Branch
```bash
# Commit or stash any changes
git add .
git commit -m "Save changes before switching branches"  # or git stash

# Backup SQLite database if needed
cp sqlite.db sqlite_backup.db
```

### 2. Switch to Scientific Branch
```bash
git checkout scientific
```

### 3. Install Dependencies
```bash
<<<<<<< HEAD
# Install/update all dependencies using launch.py
python launch.py --update-deps
=======
# Install/update Python dependencies
pip install -r requirements.txt

# Install/update Node.js dependencies
npm install
>>>>>>> scientific
```

### 4. Set Up Environment
```bash
# Copy .env.example to .env if it doesn't exist
cp .env.example .env  # if .env.example exists

# Ensure DATA_DIR is set correctly in .env (or use defaults)
echo "DATA_DIR=./data" >> .env
```

### 5. Migrate Data (Optional)
If you want to preserve data from the SQLite branch:

```bash
# Use the data migration utility to export SQLite data to JSON
<<<<<<< HEAD
python old_workflow_docs/data_migration.py sqlite-to-json --db-path sqlite.db --data-dir ./data
=======
python deployment/data_migration.py sqlite-to-json --db-path sqlite.db --data-dir ./data
>>>>>>> scientific
```

### 6. Run Tests
```bash
# Run tests to ensure everything works correctly
python -m pytest
```

## Data Migration Utilities

The project includes a data migration utility to help convert data between formats:

### JSON to SQLite Migration
```bash
# Convert JSON data to SQLite database
<<<<<<< HEAD
python old_workflow_docs/data_migration.py json-to-sqlite --data-dir ./data --db-path sqlite.db
=======
python deployment/data_migration.py json-to-sqlite --data-dir ./data --db-path sqlite.db
>>>>>>> scientific
```

### SQLite to JSON Export
```bash
# Export SQLite data to JSON files
<<<<<<< HEAD
python old_workflow_docs/data_migration.py sqlite-to-json --db-path sqlite.db --data-dir ./data
=======
python deployment/data_migration.py sqlite-to-json --db-path sqlite.db --data-dir ./data
>>>>>>> scientific
```

### Data Validation
```bash
# Validate JSON data files
<<<<<<< HEAD
python old_workflow_docs/data_migration.py validate-json --data-dir ./data

# Validate SQLite database
python old_workflow_docs/data_migration.py validate-sqlite --db-path sqlite.db
=======
python deployment/data_migration.py validate-json --data-dir ./data

# Validate SQLite database
python deployment/data_migration.py validate-sqlite --db-path sqlite.db
>>>>>>> scientific
```

## Common Issues and Solutions

### Merge Conflicts
If you encounter merge conflicts when switching branches:

1. **Backup your work**:
   ```bash
   git stash
   ```

2. **Force checkout**:
   ```bash
   git checkout -f <branch_name>
   ```

3. **Restore your work**:
   ```bash
   git stash pop
   ```

### Dependency Issues
If you encounter dependency issues after switching branches:

1. **Clean install**:
   ```bash
   # For Python
   pip uninstall -r requirements.txt -y
   pip install -r requirements.txt
   
   # For Node.js
   rm -rf node_modules package-lock.json
   npm install
   ```

### Database Connection Errors
If you encounter database connection errors:

1. **Check .env file**:
   Ensure `DATABASE_URL` is set correctly

2. **Check database file permissions**:
   ```bash
   ls -la sqlite.db
   chmod 644 sqlite.db  # if needed
   ```

3. **Reinitialize database**:
   ```bash
   rm sqlite.db
   python deployment/migrate.py apply
   ```

## Best Practices

### Before Switching Branches
1. Always commit or stash your changes
2. Backup important data
3. Note your current working directory state
4. Document any local configuration changes

### After Switching Branches
1. Install/update dependencies
2. Run tests to verify functionality
3. Update environment variables as needed
4. Migrate data if required
5. Test core functionality

### Maintaining Compatibility
1. Keep both branches updated with latest changes
2. Document any breaking changes
3. Test migration procedures regularly
4. Maintain clean, well-documented code in both branches

## Troubleshooting

### Environment Variables
Different branches may expect different environment variables:

- **Scientific branch**: Uses `DATA_DIR` for JSON data directory
- **SQLite branch**: Uses `DATABASE_URL` for SQLite database path

Always check the `.env` file after switching branches.

### File Structure Differences
The branches have different file structures:

- **Scientific branch**: No database-related files (`server/db.ts`, `drizzle.config.ts`)
- **SQLite branch**: Includes database-related files and configuration

Be aware that some files may not exist when switching between branches.

### Performance Considerations
- **Scientific branch**: JSON file storage may be slower for large datasets
- **SQLite branch**: Database queries are generally faster for complex operations

Choose the appropriate branch based on your needs and dataset size.