#!/usr/bin/env bash
set -e

echo "Starting build process..."

# 1. Install Python Dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -e .

# 2. Build Frontend
if [ "$RENDER" = "true" ]; then
    echo "Detected Render environment. Building frontend..."

    if [ -d "client" ]; then
        cd client
        echo "Installing frontend dependencies..."
        npm install

        # Install missing dev dependencies if needed (e.g. drizzle-orm for shared schema)
        # Try to install them but don't fail if they are missing from registry?
        # Actually, npm install reads package.json.

        echo "Building frontend..."
        # Run build, but allow failure
        if npm run build; then
            if [ -d "dist" ]; then
                echo "Frontend build successful."
                cd ..
                mkdir -p static/dist
                echo "Copying frontend assets to static/dist..."
                cp -r client/dist/* static/dist/
                ls -F static/dist/
            else
                echo "Warning: npm run build succeeded but dist directory not found."
            fi
        else
            echo "Warning: Frontend build failed. Continuing with backend-only deployment."
        fi

        # Always return to root if we changed directory
        if [ "$(basename "$(pwd)")" = "client" ]; then
            cd ..
        fi
    else
        echo "Warning: client directory not found. Skipping frontend build."
    fi
else
    echo "Skipping frontend build (RENDER not set or false)."
fi

echo "Build process completed successfully."
