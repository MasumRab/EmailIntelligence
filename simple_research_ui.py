
#!/usr/bin/env python3
"""
Portable Gmail AI Research Interface
Simple scientist-level UI for email analysis research
Runs without root access, self-contained
"""

import os
import sys
import json
import asyncio
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

try:
    from fastapi import FastAPI, Request, Form, UploadFile, File, HTTPException
    from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
    from fastapi.staticfiles import StaticFiles
    from fastapi.templating import Jinja2Templates
    import uvicorn
except ImportError:
    print("Installing required packages...")
    os.system("pip install fastapi uvicorn python-multipart jinja2")
    from fastapi import FastAPI, Request, Form, UploadFile, File, HTTPException
    from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
    from fastapi.staticfiles import StaticFiles
    from fastapi.templating import Jinja2Templates
    import uvicorn

# Try to import NLP engine, fallback to basic analysis
try:
    from server.python_nlp.nlp_engine import NLPEngine
    HAS_NLP = True
except ImportError:
    HAS_NLP = False
    print("NLP engine not available, using basic analysis")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="Gmail AI Research Interface", version="1.0.0")

# Create templates directory if it doesn't exist
templates_dir = Path("templates")
templates_dir.mkdir(exist_ok=True)

# Simple in-memory storage for research data
research_data = {
    "emails": [],
    "analyses": [],
    "experiments": []
}

class SimpleAnalyzer:
    """Fallback analyzer when NLP engine is not available"""
    
    def analyze_text(self, text: str) -> Dict[str, Any]:
        """Basic text analysis"""
        words = text.split()
        sentences = text.split('.')
        
        # Simple sentiment scoring
        positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic']
        negative_words = ['bad', 'terrible', 'awful', 'horrible', 'poor', 'disappointing']
        
        pos_count = sum(1 for word in words if word.lower() in positive_words)
        neg_count = sum(1 for word in words if word.lower() in negative_words)
        
        sentiment_score = (pos_count - neg_count) / max(len(words), 1)
        
        return {
            "word_count": len(words),
            "sentence_count": len(sentences),
            "sentiment_score": sentiment_score,
            "sentiment": "positive" if sentiment_score > 0 else "negative" if sentiment_score < 0 else "neutral",
            "confidence": min(abs(sentiment_score) * 10, 1.0),
            "analysis_type": "basic"
        }

# Initialize analyzer
if HAS_NLP:
    analyzer = NLPEngine()
else:
    analyzer = SimpleAnalyzer()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Main research interface"""
    return HTMLResponse(content="""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gmail AI Research Interface</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
            color: #333;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #2c3e50;
            text-align: center;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }
        .section {
            margin: 30px 0;
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 8px;
            background: #fafafa;
        }
        .section h2 {
            color: #34495e;
            margin-top: 0;
        }
        textarea, input[type="text"], input[type="file"] {
            width: 100%;
            padding: 12px;
            margin: 10px 0;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 14px;
        }
        textarea {
            height: 120px;
            resize: vertical;
        }
        button {
            background: #3498db;
            color: white;
            padding: 12px 25px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
            margin: 5px;
        }
        button:hover {
            background: #2980b9;
        }
        .results {
            margin-top: 20px;
            padding: 15px;
            background: #e8f4fd;
            border-radius: 5px;
            border-left: 4px solid #3498db;
        }
        .metric {
            display: inline-block;
            margin: 10px 15px 10px 0;
            padding: 8px 12px;
            background: #2c3e50;
            color: white;
            border-radius: 5px;
            font-size: 12px;
        }
        .email-item {
            margin: 10px 0;
            padding: 15px;
            background: white;
            border-radius: 5px;
            border: 1px solid #ddd;
        }
        .grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }
        @media (max-width: 768px) {
            .grid {
                grid-template-columns: 1fr;
            }
        }
        .status {
            padding: 5px 10px;
            border-radius: 3px;
            font-size: 12px;
            font-weight: bold;
        }
        .status.positive { background: #2ecc71; color: white; }
        .status.negative { background: #e74c3c; color: white; }
        .status.neutral { background: #95a5a6; color: white; }
    </style>
</head>
<body>
    <div class="container">
        <h1>📧 Gmail AI Research Interface</h1>
        <p style="text-align: center; color: #7f8c8d;">Simple, portable email analysis for research purposes</p>
        
        <div class="grid">
            <div class="section">
                <h2>🔬 Single Text Analysis</h2>
                <textarea id="singleText" placeholder="Paste email content or text to analyze..."></textarea>
                <button onclick="analyzeSingle()">Analyze Text</button>
                <div id="singleResults"></div>
            </div>
            
            <div class="section">
                <h2>📁 Batch Analysis</h2>
                <input type="file" id="fileUpload" accept=".txt,.csv,.json" multiple>
                <button onclick="uploadFiles()">Process Files</button>
                <div id="batchResults"></div>
            </div>
        </div>
        
        <div class="section">
            <h2>📊 Research Dashboard</h2>
            <button onclick="loadDashboard()">Refresh Data</button>
            <button onclick="exportResults()">Export Results</button>
            <button onclick="clearData()">Clear All Data</button>
            <div id="dashboard"></div>
        </div>
        
        <div class="section">
            <h2>📈 Recent Analyses</h2>
            <div id="recentAnalyses"></div>
        </div>
    </div>

    <script>
        async function analyzeSingle() {
            const text = document.getElementById('singleText').value;
            if (!text.trim()) return alert('Please enter some text to analyze');
            
            try {
                const response = await fetch('/analyze', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text: text })
                });
                const result = await response.json();
                
                document.getElementById('singleResults').innerHTML = `
                    <div class="results">
                        <h3>Analysis Results</h3>
                        <div class="metric">Words: ${result.word_count}</div>
                        <div class="metric">Sentences: ${result.sentence_count}</div>
                        <div class="metric">Sentiment: <span class="status ${result.sentiment}">${result.sentiment}</span></div>
                        <div class="metric">Score: ${result.sentiment_score.toFixed(3)}</div>
                        <div class="metric">Confidence: ${(result.confidence * 100).toFixed(1)}%</div>
                        <div class="metric">Type: ${result.analysis_type}</div>
                    </div>
                `;
                
                loadRecentAnalyses();
            } catch (error) {
                alert('Analysis failed: ' + error.message);
            }
        }
        
        async function uploadFiles() {
            const files = document.getElementById('fileUpload').files;
            if (files.length === 0) return alert('Please select files to upload');
            
            const formData = new FormData();
            for (let file of files) {
                formData.append('files', file);
            }
            
            try {
                const response = await fetch('/batch-analyze', {
                    method: 'POST',
                    body: formData
                });
                const result = await response.json();
                
                document.getElementById('batchResults').innerHTML = `
                    <div class="results">
                        <h3>Batch Analysis Complete</h3>
                        <div class="metric">Files Processed: ${result.files_processed}</div>
                        <div class="metric">Total Items: ${result.total_items}</div>
                        <div class="metric">Avg Sentiment: ${result.average_sentiment.toFixed(3)}</div>
                    </div>
                `;
                
                loadDashboard();
                loadRecentAnalyses();
            } catch (error) {
                alert('Batch analysis failed: ' + error.message);
            }
        }
        
        async function loadDashboard() {
            try {
                const response = await fetch('/dashboard');
                const data = await response.json();
                
                document.getElementById('dashboard').innerHTML = `
                    <div class="results">
                        <h3>Research Statistics</h3>
                        <div class="metric">Total Emails: ${data.total_emails}</div>
                        <div class="metric">Total Analyses: ${data.total_analyses}</div>
                        <div class="metric">Experiments: ${data.experiments}</div>
                        <div class="metric">Avg Sentiment: ${data.avg_sentiment.toFixed(3)}</div>
                        <div class="metric">Positive: ${data.sentiment_distribution.positive}%</div>
                        <div class="metric">Negative: ${data.sentiment_distribution.negative}%</div>
                        <div class="metric">Neutral: ${data.sentiment_distribution.neutral}%</div>
                    </div>
                `;
            } catch (error) {
                console.error('Dashboard load failed:', error);
            }
        }
        
        async function loadRecentAnalyses() {
            try {
                const response = await fetch('/recent');
                const analyses = await response.json();
                
                const html = analyses.map(analysis => `
                    <div class="email-item">
                        <strong>Text:</strong> ${analysis.text.substring(0, 100)}${analysis.text.length > 100 ? '...' : ''}<br>
                        <strong>Sentiment:</strong> <span class="status ${analysis.result.sentiment}">${analysis.result.sentiment}</span>
                        <strong>Score:</strong> ${analysis.result.sentiment_score.toFixed(3)}
                        <strong>Time:</strong> ${new Date(analysis.timestamp).toLocaleString()}
                    </div>
                `).join('');
                
                document.getElementById('recentAnalyses').innerHTML = html || '<p>No analyses yet</p>';
            } catch (error) {
                console.error('Recent analyses load failed:', error);
            }
        }
        
        async function exportResults() {
            try {
                const response = await fetch('/export');
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `research_data_${new Date().toISOString().split('T')[0]}.json`;
                a.click();
            } catch (error) {
                alert('Export failed: ' + error.message);
            }
        }
        
        async function clearData() {
            if (confirm('Are you sure you want to clear all research data?')) {
                try {
                    await fetch('/clear', { method: 'POST' });
                    alert('Data cleared successfully');
                    loadDashboard();
                    loadRecentAnalyses();
                } catch (error) {
                    alert('Clear failed: ' + error.message);
                }
            }
        }
        
        // Load initial data
        window.onload = function() {
            loadDashboard();
            loadRecentAnalyses();
        };
    </script>
</body>
</html>
    """)

@app.post("/analyze")
async def analyze_text(request: Request):
    """Analyze a single text"""
    data = await request.json()
    text = data.get("text", "")
    
    if not text.strip():
        raise HTTPException(status_code=400, detail="Text is required")
    
    try:
        if HAS_NLP:
            result = analyzer.analyze_text(text)
        else:
            result = analyzer.analyze_text(text)
        
        # Store analysis
        analysis = {
            "text": text,
            "result": result,
            "timestamp": datetime.now().isoformat()
        }
        research_data["analyses"].append(analysis)
        
        return result
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/batch-analyze")
async def batch_analyze(files: List[UploadFile] = File(...)):
    """Analyze multiple files"""
    results = []
    total_items = 0
    
    for file in files:
        try:
            content = await file.read()
            text = content.decode('utf-8')
            
            # Split by lines for batch processing
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            
            for line in lines:
                if len(line) > 10:  # Skip very short lines
                    if HAS_NLP:
                        result = analyzer.analyze_text(line)
                    else:
                        result = analyzer.analyze_text(line)
                    
                    analysis = {
                        "text": line,
                        "result": result,
                        "source_file": file.filename,
                        "timestamp": datetime.now().isoformat()
                    }
                    research_data["analyses"].append(analysis)
                    results.append(result)
                    total_items += 1
        
        except Exception as e:
            logger.error(f"Failed to process file {file.filename}: {e}")
    
    # Calculate summary statistics
    if results:
        avg_sentiment = sum(r.get("sentiment_score", 0) for r in results) / len(results)
    else:
        avg_sentiment = 0
    
    return {
        "files_processed": len(files),
        "total_items": total_items,
        "average_sentiment": avg_sentiment,
        "status": "complete"
    }

@app.get("/dashboard")
async def get_dashboard():
    """Get research dashboard data"""
    analyses = research_data["analyses"]
    
    if not analyses:
        return {
            "total_emails": 0,
            "total_analyses": 0,
            "experiments": len(research_data["experiments"]),
            "avg_sentiment": 0,
            "sentiment_distribution": {"positive": 0, "negative": 0, "neutral": 0}
        }
    
    sentiments = [a["result"].get("sentiment", "neutral") for a in analyses]
    sentiment_counts = {
        "positive": sentiments.count("positive"),
        "negative": sentiments.count("negative"),
        "neutral": sentiments.count("neutral")
    }
    
    total = len(sentiments)
    sentiment_distribution = {
        k: round((v / total) * 100, 1) if total > 0 else 0 
        for k, v in sentiment_counts.items()
    }
    
    avg_sentiment = sum(
        a["result"].get("sentiment_score", 0) for a in analyses
    ) / len(analyses) if analyses else 0
    
    return {
        "total_emails": len(research_data["emails"]),
        "total_analyses": len(analyses),
        "experiments": len(research_data["experiments"]),
        "avg_sentiment": avg_sentiment,
        "sentiment_distribution": sentiment_distribution
    }

@app.get("/recent")
async def get_recent_analyses():
    """Get recent analyses"""
    recent = research_data["analyses"][-10:]  # Last 10 analyses
    return list(reversed(recent))

@app.get("/export")
async def export_data():
    """Export all research data"""
    export_data = {
        "export_date": datetime.now().isoformat(),
        "total_analyses": len(research_data["analyses"]),
        "data": research_data
    }
    
    # Create temporary file
    import tempfile
    import json
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(export_data, f, indent=2)
        temp_path = f.name
    
    return FileResponse(
        temp_path,
        media_type='application/json',
        filename=f"research_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    )

@app.post("/clear")
async def clear_data():
    """Clear all research data"""
    research_data["emails"].clear()
    research_data["analyses"].clear()
    research_data["experiments"].clear()
    return {"status": "cleared"}

if __name__ == "__main__":
    print("🔬 Starting Gmail AI Research Interface...")
    print("📍 This is a portable, research-focused interface")
    print("💾 No database required - runs entirely in memory")
    print("🚀 No root access needed")
    
    # Get port from environment or use default
    port = int(os.getenv("PORT", 8080))
    
    print(f"🌐 Access your research interface at: http://0.0.0.0:{port}")
    print("📋 Features:")
    print("   - Single text analysis")
    print("   - Batch file processing") 
    print("   - Research dashboard")
    print("   - Data export")
    print("   - No external dependencies")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
