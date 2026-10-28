# DEPRECATED: Example Extension

**This extension is part of the deprecated `backend` package and will be removed in a future release.**

This extension demonstrates the extension system by adding a simple sentiment analysis enhancement to the EmailIntelligence application.

## Features

- Adds emojis to sentiment analysis results (😊 for positive, 😞 for negative, 😐 for neutral)
- Adds detailed metrics to sentiment analysis results:
  - Word count
  - Character count
  - Exclamation count
  - Question count

## Installation

This extension is included with EmailIntelligence by default. If you need to install it manually:

1. Clone this repository into the `extensions` directory of your EmailIntelligence installation:
   ```
   cd /path/to/EmailIntelligence/extensions
   git clone https://github.com/emailintelligence/example-extension.git example
   ```

2. Restart the EmailIntelligence application.

## Usage

The extension automatically enhances the sentiment analysis functionality of EmailIntelligence. No additional configuration is required.

### API

The extension also provides utility functions that can be used directly:

```python
from extensions.example.example import get_sentiment_emoji, analyze_text_with_emojis

# Get an emoji for a sentiment
emoji = get_sentiment_emoji("positive")  # Returns "😊"

# Analyze text with emojis
result = analyze_text_with_emojis("I love this application!")
# Returns:
# {
#     "text": "I love this application!",
#     "word_count": 4,
#     "character_count": 24,
#     "exclamation_count": 1,
#     "question_count": 0,
#     "sentiment": "positive",
#     "emoji": "😊"
# }
```

## Configuration

You can configure the extension by editing the `metadata.json` file:

```json
{
    "settings": {
        "add_emojis": true,
        "add_detailed_metrics": true
    }
}
```

## License

This extension is licensed under the MIT License. See the LICENSE file for details.