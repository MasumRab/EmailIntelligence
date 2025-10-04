# EmailIntelligence Setup Guide

This guide will help you set up the EmailIntelligence application in a fresh environment.

## Prerequisites

Before starting, ensure you have the following installed:

- **Python 3.12+** - [Download Python](https://python.org/downloads/)
- **Node.js 18+** - [Download Node.js](https://nodejs.org/)
- **npm** (comes with Node.js)
- **Git** - [Download Git](https://git-scm.com/)

## Quick Setup (Automated)

1. Clone the repository and checkout the scientific branch:
```bash
git clone https://github.com/MasumRab/EmailIntelligence.git
cd EmailIntelligence
git checkout scientific
```

2. Run the automated setup script:
```bash
./setup.sh
```

The script will automatically:
- Create a Python virtual environment
- Install all Python dependencies using uv
- Install all Node.js dependencies
- Verify the setup

## Manual Setup

If you prefer to set up manually or the automated script fails:

### 1. Python Backend Setup

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install uv package manager (recommended)
pip install uv

# Install dependencies with uv (faster and more reliable)
uv sync

# Alternative: Install with pip
# pip install -e .
```

### 2. Node.js Frontend Setup

```bash
# Navigate to client directory
cd client

# Install dependencies
npm install

# Return to root directory
cd ..
```

## Running the Application

### Start Backend Server

```bash
# Activate virtual environment (if not already active)
source venv/bin/activate

# Start the FastAPI backend server
python3 backend/python_backend/main.py
```

The backend will be available at: http://localhost:8000

### Start Frontend Development Server

In a new terminal:

```bash
# Navigate to client directory
cd client

# Start Vite development server
npm run dev
```

The frontend will be available at: http://localhost:5173

## Alternative: Using the Launcher

The application includes a Python-based launcher that can start both backend and frontend:

```bash
# Activate virtual environment
source venv/bin/activate

# Use the launcher
python3 launch.py --help
```

## Verification

To verify your setup is working:

1. **Backend API**: Visit http://localhost:8000/docs to see the FastAPI documentation
2. **Frontend**: Visit http://localhost:5173 to see the React application
3. **API Connection**: The frontend should be able to connect to the backend API

## Troubleshooting

### Common Issues

1. **Python version error**: Ensure you have Python 3.12 or higher
   ```bash
   python3 --version
   ```

2. **Node.js version error**: Ensure you have Node.js 18 or higher
   ```bash
   node --version
   ```

3. **Permission denied on setup.sh**: Make the script executable
   ```bash
   chmod +x setup.sh
   ```

4. **Import errors**: Ensure virtual environment is activated
   ```bash
   source venv/bin/activate
   ```

5. **Frontend build errors**: Clear npm cache and reinstall
   ```bash
   cd client
   npm cache clean --force
   rm -rf node_modules package-lock.json
   npm install
   ```

6. **Port conflicts**: If ports 8000 or 5173 are in use, you can change them:
   - Backend: Set `PORT` environment variable
   - Frontend: Use `npm run dev -- --port 3000`

### Dependencies Issues

If you encounter dependency conflicts:

1. **Python dependencies**: Use uv for better dependency resolution
   ```bash
   uv sync --refresh
   ```

2. **Node.js dependencies**: Update to latest compatible versions
   ```bash
   cd client
   npm update
   ```

## Development Workflow

1. **Backend development**: 
   - Edit files in `backend/`
   - The server auto-reloads on changes
   - API docs at http://localhost:8000/docs

2. **Frontend development**:
   - Edit files in `client/src/`
   - Vite provides hot module replacement
   - Uses shadcn/ui components with Tailwind CSS

3. **Shared types**:
   - Edit files in `shared/`
   - Used by both backend and frontend

## Production Deployment

For production deployment:

1. **Build frontend**:
   ```bash
   cd client
   npm run build
   ```

2. **Configure backend** for production (set environment variables)

3. **Use a production WSGI server** like Gunicorn or Uvicorn

## Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Vite Documentation](https://vitejs.dev/)
- [shadcn/ui Documentation](https://ui.shadcn.com/)
- [Tailwind CSS Documentation](https://tailwindcss.com/)