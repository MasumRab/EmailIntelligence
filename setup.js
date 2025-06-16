#!/usr/bin/env node

import { execSync } from 'child_process';
import fs from 'fs';
import path from 'path';

const LOG_PREFIX = '[EmailIntelligence Setup]';

function log(message) {
  console.log(`${LOG_PREFIX} ${message}`);
}

function error(message) {
  console.error(`${LOG_PREFIX} ERROR: ${message}`);
}

function runCommand(command, description) {
  try {
    log(`${description}...`);
    execSync(command, { stdio: 'inherit' });
    log(`✓ ${description} completed`);
  } catch (err) {
    error(`Failed to ${description.toLowerCase()}: ${err.message}`);
    process.exit(1);
  }
}

function checkFile(filePath, description) {
  if (fs.existsSync(filePath)) {
    log(`✓ ${description} already exists`);
    return true;
  }
  return false;
}

function createEnvFile() {
  const envPath = path.join(process.cwd(), '.env');
  const envExamplePath = path.join(process.cwd(), '.env.example');
  
  if (checkFile(envPath, '.env file')) {
    return;
  }
  
  if (fs.existsSync(envExamplePath)) {
    try {
      fs.copyFileSync(envExamplePath, envPath);
      log('✓ Created .env file from .env.example');
    } catch (err) {
      error(`Failed to create .env file: ${err.message}`);
    }
  } else {
    error('.env.example file not found');
  }
}

async function main() {
  log('Starting EmailIntelligence setup...');
  
  // Check if we're in the right directory
  if (!fs.existsSync('package.json')) {
    error('Please run this script from the project root directory');
    process.exit(1);
  }
  
  // Create .env file if it doesn't exist
  createEnvFile();
  
  // Install Node.js dependencies
  runCommand('npm install', 'Installing Node.js dependencies');
  
  // Check if Docker is available
  try {
    execSync('docker --version', { stdio: 'ignore' });
    log('Docker is available');
    
    // Ask if user wants to start database
    log('');
    log('To start the local PostgreSQL database, run:');
    log('  docker-compose up -d');
    log('');
    log('Then push the database schema:');
    log('  npm run db:push');
    log('');
  } catch (err) {
    log('Docker not available, you will need to set up PostgreSQL manually');
    log('Update the DATABASE_URL in your .env file to point to your PostgreSQL instance');
    log('');
  }
  
  log('Setup completed! Next steps:');
  log('1. Update .env file with your database credentials if needed');
  log('2. Start the database: docker-compose up -d (if using Docker)');
  log('3. Push database schema: npm run db:push');
  log('4. Start the application: npm run dev');
  log('');
  log('For Gmail integration, see the README.md for Gmail API setup instructions.');
}

main().catch(err => {
  error(`Setup failed: ${err.message}`);
  process.exit(1);
});