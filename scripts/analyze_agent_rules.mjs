#!/usr/bin/env node
/**
 * Agent Rules Analyzer — Browser Automation (Node.js)
 * 
 * Automates submission of config files to agentrulegen.com/analyze
 * since no API exists.
 * 
 * Requirements: npx playwright (already installed)
 * 
 * Usage:
 *   node analyze_agent_rules.mjs .ruler/AGENTS.md
 *   node analyze_agent_rules.mjs .claude/hooks.yaml rulesync.jsonc
 */

import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';

const ANALYZE_URL = 'https://agentrulegen.com/analyze';
const MAX_CHARS = 10000;

async function analyzeRules(filePath) {
    const content = fs.readFileSync(filePath, 'utf-8');
    const truncatedContent = content.length > MAX_CHARS 
        ? content.slice(0, MAX_CHARS) 
        : content;
    
    console.log(`Analyzing: ${filePath} (${truncatedContent.length} chars)`);
    
    const browser = await chromium.launch({ headless: true });
    const page = await browser.newPage();
    
    try {
        // Navigate
        console.log('Navigating to agentrulegen.com/analyze...');
        await page.goto(ANALYZE_URL, { waitUntil: 'networkidle' });
        
        // Wait for textarea
        const textarea = await page.waitForSelector('textarea', { timeout: 10000 });
        
        // Fill content
        console.log('Submitting content...');
        await textarea.fill(truncatedContent);
        
        // Click analyze button
        const analyzeBtn = await page.waitForSelector('button:has-text("Analyze")', { timeout: 5000 });
        await analyzeBtn.click();
        
        // Wait for results
        console.log('Waiting for analysis results...');
        await page.waitForSelector(':text("results"), :text("redundant"), :text("essential")', { timeout: 60000 });
        
        // Scrape results
        console.log('Scraping results...');
        const bodyText = await page.innerHTML('body');
        
        // Try to extract structured data
        const results = {
            file: filePath,
            charCount: truncatedContent.length,
            rawResponse: bodyText,
            redundant: [],
            essential: [],
            improvable: [],
            missing: []
        };
        
        // Extract categories (look for common patterns)
        try {
            const redundantText = await page.textContent(':text-matches("redundant", "i") ~ ul, :text-matches("redundant", "i") + *');
            if (redundantText) results.redundant = redundantText.split('\n').filter(Boolean);
        } catch {}
        
        try {
            const essentialText = await page.textContent(':text-matches("essential", "i") ~ ul, :text-matches("essential", "i") + *');
            if (essentialText) results.essential = essentialText.split('\n').filter(Boolean);
        } catch {}
        
        try {
            const improvableText = await page.textContent(':text-matches("improvable", "i") ~ ul, :text-matches("improvable", "i") + *');
            if (improvableText) results.improvable = improvableText.split('\n').filter(Boolean);
        } catch {}
        
        return results;
        
    } catch (error) {
        return {
            file: filePath,
            error: error.message,
            success: false
        };
    } finally {
        await browser.close();
    }
}

async function batchAnalyze(files) {
    const results = [];
    for (const file of files) {
        const result = await analyzeRules(file);
        results.push(result);
        console.log(`Complete: ${file}`);
        // Delay between requests
        await new Promise(r => setTimeout(r, 2000));
    }
    return results;
}

// Main
const files = process.argv.slice(2);

if (files.length === 0) {
    console.log('Usage: node analyze_agent_rules.mjs <file> [file2] [file3]');
    console.log('Example: node analyze_agent_rules.mjs .ruler/AGENTS.md .claude/hooks.yaml');
    process.exit(1);
}

// Validate files exist
for (const f of files) {
    if (!fs.existsSync(f)) {
        console.log(`ERROR: File not found: ${f}`);
        process.exit(1);
    }
}

// Run
console.log('Starting analysis...\n');
batchAnalyze(files).then(results => {
    console.log('\n=== ANALYSIS RESULTS ===');
    console.log(JSON.stringify(results, null, 2));
    
    // Save to file
    const outputFile = 'agent_rules_analysis.json';
    fs.writeFileSync(outputFile, JSON.stringify(results, null, 2));
    console.log(`\nSaved to: ${outputFile}`);
});
