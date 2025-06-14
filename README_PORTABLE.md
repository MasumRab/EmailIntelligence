
# Gmail AI Research Interface - Portable Version

A simple, scientist-friendly email analysis interface that runs anywhere without root access.

## 🚀 Quick Start

### Option 1: Direct Run
```bash
python3 simple_research_ui.py
```

### Option 2: Portable Runner
```bash
python3 run_portable.py
```

## 📋 Features

- **Single Text Analysis**: Analyze individual emails or text snippets
- **Batch Processing**: Upload and analyze multiple files at once
- **Research Dashboard**: View statistics and trends
- **Data Export**: Export results as JSON for further analysis
- **No Dependencies**: Automatically installs minimal requirements
- **No Root Access**: Runs with user permissions only
- **Memory-Based**: No database setup required

## 💾 Portable Deployment

### USB Drive Setup
1. Copy these files to your USB drive:
   - `simple_research_ui.py`
   - `run_portable.py`
   - `README_PORTABLE.md`

2. On any computer with Python 3.7+:
   ```bash
   cd /path/to/usb/drive
   python3 run_portable.py
   ```

3. Access via browser: `http://localhost:8080`

### Supported File Types
- `.txt` - Plain text files
- `.csv` - CSV files (text will be extracted)
- `.json` - JSON files (text fields will be analyzed)

### Analysis Capabilities
- **Basic Analysis**: Word count, sentence count
- **Sentiment Analysis**: Positive/negative/neutral classification
- **Confidence Scoring**: Reliability of sentiment prediction
- **Batch Statistics**: Aggregate metrics across multiple texts

## 🔧 Configuration

### Change Port
```bash
PORT=9000 python3 simple_research_ui.py
```

### Environment Variables
- `PORT`: Server port (default: 8080)
- `NODE_ENV`: Set to 'development' for debug mode

## 📊 Research Workflow

1. **Individual Analysis**: Paste email content for immediate analysis
2. **Batch Processing**: Upload text files for bulk analysis
3. **Review Results**: Check dashboard for aggregate statistics
4. **Export Data**: Download results for external analysis tools

## 🔒 Privacy & Security

- **Local Processing**: All analysis happens locally
- **No External Calls**: No data sent to external services
- **Memory Storage**: Data cleared when application stops
- **No Persistence**: No permanent data storage by default

## 🛠️ Customization

### Adding Custom Analysis
Edit `simple_research_ui.py` and modify the `SimpleAnalyzer` class:

```python
def analyze_text(self, text: str) -> Dict[str, Any]:
    # Add your custom analysis logic here
    result = {
        "custom_metric": your_analysis_function(text),
        # ... other metrics
    }
    return result
```

### Styling
Modify the CSS in the HTML template within `simple_research_ui.py`.

## 📁 File Structure
```
portable_research_ui/
├── simple_research_ui.py    # Main application
├── run_portable.py          # Portable runner
└── README_PORTABLE.md       # This file
```

## 🐛 Troubleshooting

### Common Issues

**"ModuleNotFoundError: fastapi"**
- Run `python3 run_portable.py` instead
- Or manually install: `pip install --user fastapi uvicorn`

**"Permission denied"**
- Don't use sudo/admin privileges
- Make sure you have write access to the directory

**"Port already in use"**
- Change port: `PORT=9001 python3 simple_research_ui.py`
- Kill existing processes: `pkill -f simple_research_ui`

### System Requirements
- Python 3.7 or higher
- 50MB free space for dependencies
- Internet connection for initial setup only

## 📈 Performance Notes

- **Memory Usage**: ~50-100MB depending on data size
- **Processing Speed**: ~1000 texts per minute (basic analysis)
- **File Limits**: No hard limits, but large files may be slow
- **Browser Compatibility**: Works in any modern browser

This interface is designed for research purposes and prioritizes simplicity and portability over enterprise features.
