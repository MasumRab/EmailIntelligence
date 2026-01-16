# IMAP Box Management Documentation

## Overview

The IMAP Box Management module provides intelligent email categorization and organization capabilities for the Email Intelligence Platform. It implements a smart inbox system that automatically sorts emails into different "boxes" based on content analysis, sender reputation, and user preferences.

## Architecture

### Key Components

#### 1. IMAP Box UI (`modules/imbox/imbox_ui.py`)
Gradio-based user interface for email categorization and sender labeling.

#### 2. Email Categorization System
Intelligent sorting of emails into different priority levels and categories.

#### 3. Sender Labeling System
User-driven classification system for email senders and their importance levels.

#### 4. Smart Filtering Engine
Automated email routing based on content analysis and user feedback.

### Data Flow
```
Incoming Emails → Content Analysis → Categorization Engine → IMAP Boxes
       ↓                    ↓                    ↓              ↓
   User Feedback     AI Classification     Sender Labels     UI Display
   (Learning)       (Auto-categorization) (Manual Labels)   (Organization)
```

### Integration Points
- **Email Data Sources:** Works with any email source (Gmail, IMAP, Notmuch)
- **AI Analysis Engine:** Uses ML models for content-based categorization
- **User Preferences:** Learns from user labeling decisions
- **Database Storage:** Persists categorization rules and sender labels
- **UI Integration:** Gradio tabs for different email categories

## Core Classes & Functions

### Email Categorization System

#### Email Category Types
```python
from enum import Enum

class EmailCategory(Enum):
    """Email categorization types for IMAP box organization."""

    IMPORTANT = "important"        # High-priority emails requiring attention
    FEED = "feed"                  # Regular communications and updates
    PAPER_TRAIL = "paper_trail"    # Transactional and administrative emails
    SPAM = "spam"                  # Unwanted or malicious emails
```

#### Smart Categorization Engine
```python
class EmailCategorizer:
    """Intelligent email categorization engine."""

    def __init__(self, ai_engine=None, database=None):
        self.ai_engine = ai_engine
        self.database = database
        self.sender_labels = self._load_sender_labels()
        self.categorization_rules = self._load_categorization_rules()

    async def categorize_email(self, email_data: Dict[str, Any]) -> EmailCategory:
        """Categorize an email using multiple signals.

        Args:
            email_data: Email metadata and content

        Returns:
            EmailCategory: Determined category for the email
        """
        # Check explicit sender labels first
        sender_category = self._check_sender_label(email_data['sender'])
        if sender_category:
            return sender_category

        # Use AI analysis for content-based categorization
        if self.ai_engine:
            ai_category = await self._analyze_content_category(email_data)
            if ai_category:
                return ai_category

        # Apply rule-based categorization
        rule_category = self._apply_categorization_rules(email_data)
        if rule_category:
            return rule_category

        # Default to feed for uncategorized emails
        return EmailCategory.FEED

    def _check_sender_label(self, sender: str) -> Optional[EmailCategory]:
        """Check if sender has an explicit label."""
        label = self.sender_labels.get(sender.lower())
        if label:
            return EmailCategory(label.lower())
        return None

    async def _analyze_content_category(self, email_data: Dict[str, Any]) -> Optional[EmailCategory]:
        """Use AI to analyze email content for categorization."""
        if not self.ai_engine:
            return None

        # Analyze subject and content for categorization signals
        analysis_prompt = f"""
        Analyze this email and determine its category:

        Subject: {email_data.get('subject', '')}
        From: {email_data.get('sender', '')}
        Content: {email_data.get('body', '')[:500]}...

        Categories:
        - IMPORTANT: Urgent, time-sensitive, requires action
        - FEED: Regular communications, updates, newsletters
        - PAPER_TRAIL: Receipts, confirmations, administrative
        - SPAM: Unwanted, promotional, potentially harmful

        Return only the category name.
        """

        try:
            response = await self.ai_engine.analyze_text(analysis_prompt)
            category_text = response.get('category', '').upper()

            # Map response to enum
            category_map = {
                'IMPORTANT': EmailCategory.IMPORTANT,
                'FEED': EmailCategory.FEED,
                'PAPER_TRAIL': EmailCategory.PAPER_TRAIL,
                'SPAM': EmailCategory.SPAM
            }

            return category_map.get(category_text)
        except Exception as e:
            logger.warning(f"AI categorization failed: {e}")
            return None

    def _apply_categorization_rules(self, email_data: Dict[str, Any]) -> Optional[EmailCategory]:
        """Apply rule-based categorization."""
        subject = email_data.get('subject', '').lower()
        sender = email_data.get('sender', '').lower()

        # High-priority keywords
        if any(keyword in subject for keyword in ['urgent', 'asap', 'important', 'deadline']):
            return EmailCategory.IMPORTANT

        # Transactional emails
        if any(keyword in subject for keyword in ['receipt', 'invoice', 'confirmation', 'order']):
            return EmailCategory.PAPER_TRAIL

        # Newsletter/unwanted content
        if any(domain in sender for domain in ['newsletter', 'promo', 'marketing']):
            return EmailCategory.SPAM

        return None
```

### Sender Labeling System

#### Sender Label Management
```python
class SenderLabelManager:
    """Manages sender labels and categorization preferences."""

    def __init__(self, labels_file: str = "data/sender_labels.json"):
        self.labels_file = labels_file
        self.labels = self._load_labels()

    def save_sender_label(self, sender_email: str, label: str) -> str:
        """Save a label for a specific sender.

        Args:
            sender_email: Email address of the sender
            label: Category label (Important, Not Important, Spam)

        Returns:
            Status message
        """
        if not sender_email:
            return "Please enter a sender email."

        # Normalize email to lowercase
        sender_email = sender_email.lower().strip()

        # Map user-friendly labels to internal categories
        label_mapping = {
            "Important": "important",
            "Not Important": "feed",
            "Spam": "spam"
        }

        internal_label = label_mapping.get(label)
        if not internal_label:
            return f"Invalid label: {label}"

        # Save label
        self.labels[sender_email] = internal_label
        self._save_labels()

        return f"Label for '{sender_email}' saved successfully!"

    def get_sender_label(self, sender_email: str) -> str:
        """Get the label for a specific sender."""
        if not os.path.exists(self.labels_file):
            return "No labels saved yet."

        sender_email = sender_email.lower().strip()
        label = self.labels.get(sender_email)

        if label:
            # Convert internal label back to user-friendly format
            user_labels = {
                "important": "Important",
                "feed": "Not Important",
                "spam": "Spam"
            }
            return user_labels.get(label, label)

        return "No label found for this sender."

    def _load_labels(self) -> Dict[str, str]:
        """Load sender labels from file."""
        if not os.path.exists(self.labels_file):
            return {}

        try:
            with open(self.labels_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            logger.warning(f"Failed to load sender labels: {e}")
            return {}

    def _save_labels(self):
        """Save sender labels to file."""
        try:
            with open(self.labels_file, "w", encoding="utf-8") as f:
                json.dump(self.labels, f, indent=4)
        except IOError as e:
            logger.error(f"Failed to save sender labels: {e}")
            raise
```

### UI Components

#### IMAP Box Interface
```python
def create_imbox_ui():
    """Create the IMAP Box Management UI."""

    with gr.Blocks() as imbox_tab:
        with gr.Tabs():
            # Important emails box
            with gr.TabItem("Imbox"):
                gr.Markdown("## Imbox - Important Emails")
                gr.Markdown("High-priority emails requiring attention.")

                important_emails_df = gr.DataFrame(
                    headers=["Date", "From", "Subject", "Priority"],
                    label="Important Emails"
                )

                # Load important emails
                load_important_btn = gr.Button("Load Important Emails")
                load_important_btn.click(
                    fn=load_emails_by_category,
                    inputs=[gr.State("important")],
                    outputs=[important_emails_df]
                )

            # Regular feed
            with gr.TabItem("The Feed"):
                gr.Markdown("## The Feed - Regular Communications")
                gr.Markdown("Newsletters, updates, and regular communications.")

                feed_emails_df = gr.DataFrame(
                    headers=["Date", "From", "Subject", "Category"],
                    label="Feed Emails"
                )

                load_feed_btn = gr.Button("Load Feed Emails")
                load_feed_btn.click(
                    fn=load_emails_by_category,
                    inputs=[gr.State("feed")],
                    outputs=[feed_emails_df]
                )

            # Transactional emails
            with gr.TabItem("Paper Trail"):
                gr.Markdown("## Paper Trail - Transactional Emails")
                gr.Markdown("Receipts, confirmations, and administrative communications.")

                paper_trail_df = gr.DataFrame(
                    headers=["Date", "From", "Subject", "Type"],
                    label="Transactional Emails"
                )

                load_paper_btn = gr.Button("Load Transactional Emails")
                load_paper_btn.click(
                    fn=load_emails_by_category,
                    inputs=[gr.State("paper_trail")],
                    outputs=[paper_trail_df]
                )

            # Spam emails
            with gr.TabItem("Spam"):
                gr.Markdown("## Spam - Unwanted Emails")
                gr.Markdown("Filtered spam and unwanted communications.")

                spam_emails_df = gr.DataFrame(
                    headers=["Date", "From", "Subject", "Reason"],
                    label="Spam Emails"
                )

                load_spam_btn = gr.Button("Load Spam Emails")
                load_spam_btn.click(
                    fn=load_emails_by_category,
                    inputs=[gr.State("spam")],
                    outputs=[spam_emails_df]
                )

        # Sender labeling system
        with gr.Row():
            with gr.Column():
                gr.Markdown("## Sender Labeling")
                gr.Markdown("Train the system by labeling email senders.")

                sender_email = gr.Textbox(
                    label="Sender Email",
                    placeholder="Enter sender email address"
                )

                label = gr.Dropdown(
                    label="Label",
                    choices=["Important", "Not Important", "Spam"],
                    value="Not Important"
                )

                save_label_button = gr.Button("Save Label")
                status = gr.Textbox(label="Status", interactive=False)

                # Save label functionality
                save_label_button.click(
                    fn=save_sender_label,
                    inputs=[sender_email, label],
                    outputs=[status]
                )

    return imbox_tab
```

## Configuration

### Environment Variables
```bash
# Email categorization settings
EMAIL_CATEGORIZATION_ENABLED=true
AI_CATEGORIZATION_ENABLED=true
SENDER_LABELS_FILE=data/sender_labels.json

# Categorization rules
IMPORTANT_KEYWORDS=urgent,asap,deadline,important
TRANSACTIONAL_KEYWORDS=receipt,invoice,confirmation,order
SPAM_DOMAINS=promo,marketing,newsletter

# UI settings
DEFAULT_EMAIL_LIMIT=50
AUTO_REFRESH_INTERVAL=300
CATEGORY_FILTERING_ENABLED=true
```

### Runtime Configuration
```python
from modules.imbox.categorizer import EmailCategorizer
from modules.imbox.sender_labels import SenderLabelManager

# Initialize categorization system
categorizer = EmailCategorizer(
    ai_engine=ai_engine,
    database=database_manager
)

# Configure categorization rules
categorizer.add_rule("important", {
    "keywords": ["urgent", "asap", "deadline"],
    "senders": ["boss@company.com", "urgent@system.com"],
    "priority": "high"
})

categorizer.add_rule("spam", {
    "domains": ["promo.com", "marketing.net"],
    "keywords": ["unsubscribe", "free offer"],
    "priority": "low"
})

# Initialize sender label manager
label_manager = SenderLabelManager()
```

### Sender Labels File Structure
```json
{
  "important@company.com": "important",
  "newsletter@promo.com": "spam",
  "team@internal.com": "feed",
  "receipts@store.com": "paper_trail",
  "updates@service.com": "feed"
}
```

## Usage Examples

### Basic Email Categorization

```python
from modules.imbox.categorizer import EmailCategorizer, EmailCategory

# Initialize categorizer
categorizer = EmailCategorizer()

# Categorize an email
email_data = {
    "subject": "Urgent: Project Deadline Extended",
    "sender": "boss@company.com",
    "body": "The deadline for the quarterly project has been extended to next Friday."
}

category = await categorizer.categorize_email(email_data)
print(f"Email categorized as: {category.value}")  # Output: important
```

### Sender Labeling

```python
from modules.imbox.sender_labels import SenderLabelManager

# Initialize label manager
label_manager = SenderLabelManager()

# Save sender labels
label_manager.save_sender_label("boss@company.com", "Important")
label_manager.save_sender_label("newsletter@promo.com", "Spam")
label_manager.save_sender_label("receipts@store.com", "Not Important")

# Get sender label
label = label_manager.get_sender_label("boss@company.com")
print(f"Sender label: {label}")  # Output: Important
```

### Loading Emails by Category

```python
async def load_emails_by_category(category: str, limit: int = 50):
    """Load emails filtered by category."""
    data_source = await get_data_source()

    # Build query based on category
    if category == "important":
        # Load emails marked as important or from important senders
        important_senders = get_important_senders()
        query = f"({' OR '.join(f'from:{sender}' for sender in important_senders)})"

    elif category == "spam":
        # Load emails from known spam domains or marked as spam
        spam_domains = get_spam_domains()
        query = f"({' OR '.join(f'from:*@{domain}' for domain in spam_domains)})"

    elif category == "paper_trail":
        # Load transactional emails
        transactional_keywords = ["receipt", "invoice", "confirmation", "order"]
        query = f"({' OR '.join(f'subject:{keyword}' for keyword in transactional_keywords)})"

    else:  # feed
        # Load regular emails (not in other categories)
        query = "NOT (important OR spam OR paper_trail)"

    # Execute search
    emails = await data_source.search_emails(query, limit=limit)

    # Format for display
    formatted_emails = []
    for email in emails:
        formatted_emails.append({
            "Date": email.get("date", ""),
            "From": email.get("sender", ""),
            "Subject": email.get("subject", ""),
            "Category": category.title()
        })

    return formatted_emails
```

### Training the Categorization System

```python
async def train_categorization_system():
    """Train the email categorization system with user feedback."""

    categorizer = EmailCategorizer()
    label_manager = SenderLabelManager()

    # Get historical email data
    historical_emails = await get_historical_emails(limit=1000)

    training_data = []
    for email in historical_emails:
        # Get user-provided category (from labels or manual categorization)
        user_category = determine_user_category(email, label_manager)

        if user_category:
            training_data.append({
                "email": email,
                "category": user_category
            })

    # Train AI model if available
    if categorizer.ai_engine:
        await categorizer.train_ai_model(training_data)

    # Update rule-based categorization
    await categorizer.update_rules_from_feedback(training_data)

    print(f"Trained on {len(training_data)} email categorizations")

def determine_user_category(email: Dict, label_manager: SenderLabelManager) -> Optional[str]:
    """Determine user-assigned category for training."""
    sender = email.get("sender", "")

    # Check sender labels
    label = label_manager.get_sender_label(sender)
    if label and label != "No label found":
        return label.lower()

    # Check for manual categorizations in database
    # (implementation would depend on how categorizations are stored)
    return None
```

## API Reference

### Email Categorization

#### `categorize_email(email_data) -> EmailCategory`
Categorizes an email using multiple signals.

**Parameters:**
- `email_data` (dict): Email metadata and content

**Returns:**
- `EmailCategory`: Determined category

#### `add_categorization_rule(category, criteria)`
Adds a custom categorization rule.

**Parameters:**
- `category` (str): Category name
- `criteria` (dict): Rule criteria (keywords, senders, domains)

#### `update_rules_from_feedback(training_data)`
Updates categorization rules based on user feedback.

### Sender Label Management

#### `save_sender_label(sender_email, label) -> str`
Saves a label for a sender.

**Parameters:**
- `sender_email` (str): Sender email address
- `label` (str): Category label

**Returns:**
- `str`: Status message

#### `get_sender_label(sender_email) -> str`
Retrieves label for a sender.

**Parameters:**
- `sender_email` (str): Sender email address

**Returns:**
- `str`: Category label or status message

#### `remove_sender_label(sender_email) -> bool`
Removes label for a sender.

#### `list_labeled_senders() -> Dict[str, str]`
Returns all labeled senders.

### UI Functions

#### `load_emails_by_category(category, limit) -> List[Dict]`
Loads emails filtered by category.

**Parameters:**
- `category` (str): Email category
- `limit` (int): Maximum emails to load

**Returns:**
- `List[Dict]`: Formatted email data

#### `save_sender_label(sender_email, label) -> str`
UI wrapper for saving sender labels.

#### `get_sender_label(sender_email) -> str`
UI wrapper for retrieving sender labels.

## Performance Considerations

### Categorization Performance
- **Rule-Based:** < 1ms per email (fastest)
- **AI-Based:** 50-200ms per email (variable)
- **Hybrid Approach:** Best of both worlds

### Memory Usage
- **Sender Labels:** < 1MB for typical usage
- **Categorization Rules:** < 100KB
- **AI Models:** 50-500MB depending on model size

### Scalability
```python
# Performance optimization settings
performance_config = {
    "batch_categorization": True,
    "batch_size": 50,
    "cache_enabled": True,
    "cache_ttl": 3600,  # 1 hour
    "parallel_processing": True,
    "max_workers": 4
}

# Large-scale deployment
large_scale_config = {
    "distributed_categorization": True,
    "redis_cache": "redis://cache-server:6379",
    "message_queue": "rabbitmq://queue-server:5672",
    "load_balancing": "kubernetes"
}
```

## Security Considerations

### Data Protection
- **Email Content:** Sanitize sensitive information before categorization
- **Sender Privacy:** Hash sender emails for analysis while preserving categorization
- **Access Control:** Restrict categorization rule modifications to authorized users

### Safe Categorization
```python
class SecureEmailCategorizer:
    """Security-focused email categorization."""

    def __init__(self):
        self.sensitive_patterns = [
            r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b',  # Credit cards
            r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',            # SSN
            r'password|token|key|secret',                # Sensitive keywords
        ]

    def sanitize_email_for_categorization(self, email_data: Dict) -> Dict:
        """Remove sensitive information before categorization."""
        sanitized = email_data.copy()

        # Sanitize subject and body
        for field in ['subject', 'body']:
            if field in sanitized:
                sanitized[field] = self._remove_sensitive_data(
                    sanitized[field]
                )

        return sanitized

    def _remove_sensitive_data(self, text: str) -> str:
        """Remove sensitive patterns from text."""
        for pattern in self.sensitive_patterns:
            text = re.sub(pattern, '[REDACTED]', text, flags=re.IGNORECASE)
        return text

    async def secure_categorize(self, email_data: Dict) -> EmailCategory:
        """Categorize email with security measures."""
        # Sanitize first
        safe_email = self.sanitize_email_for_categorization(email_data)

        # Categorize sanitized version
        category = await self.categorizer.categorize_email(safe_email)

        # Log categorization (without sensitive data)
        logger.info(f"Email from {email_data['sender']} categorized as {category.value}")

        return category
```

## Troubleshooting

### Common Issues

#### Incorrect Categorization
```
Symptom: Emails appearing in wrong categories
```

**Diagnosis:**
```python
# Check sender labels
label_manager = SenderLabelManager()
label = label_manager.get_sender_label("sender@example.com")
print(f"Sender label: {label}")

# Check categorization rules
categorizer = EmailCategorizer()
rules = categorizer.get_rules()
print(f"Active rules: {len(rules)}")

# Test categorization manually
test_email = {
    "subject": "Urgent meeting tomorrow",
    "sender": "boss@company.com",
    "body": "We need to discuss the project."
}
category = await categorizer.categorize_email(test_email)
print(f"Categorized as: {category.value}")
```

**Solutions:**
```python
# Update sender labels
label_manager.save_sender_label("boss@company.com", "Important")

# Add categorization rules
categorizer.add_rule("important", {
    "keywords": ["urgent", "meeting", "deadline"],
    "senders": ["boss@company.com"]
})

# Retrain AI model
await categorizer.retrain_ai_model()
```

#### Missing Emails in Categories
```
Symptom: Expected emails not appearing in category views
```

**Diagnosis:**
```bash
# Check email data source
python -c "
import asyncio
from src.core.factory import get_data_source

async def check_emails():
    ds = await get_data_source()
    emails = await ds.search_emails('', limit=10)
    print(f'Found {len(emails)} emails in data source')
    for email in emails[:3]:
        print(f'- {email[\"subject\"]} from {email[\"sender\"]}')

asyncio.run(check_emails())
"
```

**Solutions:**
```python
# Refresh data source
await data_source.refresh_index()

# Update category filters
await categorizer.update_category_filters()

# Clear and rebuild caches
await categorizer.clear_caches()
```

#### Sender Label Not Saving
```
Symptom: Sender labels not persisting
```

**Diagnosis:**
```bash
# Check file permissions
ls -la data/sender_labels.json

# Check file content
cat data/sender_labels.json

# Test label saving
python -c "
from modules.imbox.sender_labels import SenderLabelManager
manager = SenderLabelManager()
result = manager.save_sender_label('test@example.com', 'Important')
print(f'Save result: {result}')
"
```

**Solutions:**
```bash
# Fix file permissions
chmod 644 data/sender_labels.json

# Create directory if missing
mkdir -p data

# Reset labels file
echo '{}' > data/sender_labels.json
```

### Debug Mode

```python
import logging

# Enable detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Enable categorizer debug
categorizer = EmailCategorizer()
categorizer.debug_mode = True

# Enable label manager debug
label_manager = SenderLabelManager()
label_manager.debug_mode = True

# Debug categorization process
async def debug_categorization(email_data):
    print("=== Categorization Debug ===")

    # Check sender label
    sender_label = label_manager.get_sender_label(email_data['sender'])
    print(f"Sender label: {sender_label}")

    # Check rule-based categorization
    rule_result = categorizer._apply_categorization_rules(email_data)
    print(f"Rule result: {rule_result}")

    # Check AI categorization
    ai_result = await categorizer._analyze_content_category(email_data)
    print(f"AI result: {ai_result}")

    # Final categorization
    final_result = await categorizer.categorize_email(email_data)
    print(f"Final result: {final_result}")

    return final_result
```

## Development Notes

### Testing

```bash
# Run IMAP box tests
pytest tests/modules/imbox/ -v

# Test categorization
pytest tests/modules/imbox/test_categorization.py -v

# Test sender labels
pytest tests/modules/imbox/test_sender_labels.py -v

# Integration tests
pytest tests/integration/test_email_categorization.py -v

# UI tests
pytest tests/modules/imbox/test_ui.py -v
```

### Code Style

```python
# IMAP box best practices
class EmailBoxManager:
    """Manages email categorization and box organization."""

    def __init__(self, categorizer: EmailCategorizer, label_manager: SenderLabelManager):
        self.categorizer = categorizer
        self.label_manager = label_manager
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self._stats = {
            "categorized_emails": 0,
            "important_count": 0,
            "spam_count": 0,
            "paper_trail_count": 0,
            "feed_count": 0
        }

    async def process_and_categorize_email(self, email_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process and categorize a single email with comprehensive tracking."""
        try:
            # Categorize email
            category = await self.categorizer.categorize_email(email_data)

            # Update statistics
            self._stats["categorized_emails"] += 1
            self._stats[f"{category.value}_count"] += 1

            # Add category to email data
            email_data["category"] = category.value
            email_data["categorized_at"] = time.time()
            email_data["categorization_method"] = self._determine_method(email_data)

            # Log categorization
            self.logger.info(
                f"Email '{email_data['subject'][:50]}...' categorized as {category.value}"
            )

            return email_data

        except Exception as e:
            self.logger.error(f"Email categorization failed: {e}")
            # Default to feed category on error
            email_data["category"] = EmailCategory.FEED.value
            email_data["categorization_error"] = str(e)
            return email_data

    def _determine_method(self, email_data: Dict[str, Any]) -> str:
        """Determine which categorization method was used."""
        sender = email_data.get("sender", "")

        # Check if sender label was used
        if self.label_manager.get_sender_label(sender) != "No label found":
            return "sender_label"

        # Check for rule matches
        subject = email_data.get("subject", "").lower()
        rule_keywords = ["urgent", "receipt", "invoice", "spam"]

        if any(keyword in subject for keyword in rule_keywords):
            return "rule_based"

        # Default to AI or manual
        return "ai_categorization"

    def get_categorization_stats(self) -> Dict[str, int]:
        """Get categorization statistics."""
        return self._stats.copy()

    async def retrain_categorization_model(self):
        """Retrain the categorization model based on user feedback."""
        # Implementation would analyze user corrections
        # and update categorization rules/AI model
        pass
```

### Contributing

1. **Categorization Rules:** Add new rules for better email classification
2. **AI Integration:** Improve AI-based categorization accuracy
3. **UI Enhancement:** Add more advanced filtering and search capabilities
4. **Performance:** Optimize categorization for large email volumes
5. **Feedback Loop:** Implement user feedback for continuous improvement

## Changelog

### Version 2.0.0
- **Added:** Intelligent email categorization system
- **Added:** Sender labeling and user preference learning
- **Added:** Gradio UI for email box management
- **Added:** Multi-signal categorization (rules + AI + user feedback)
- **Added:** Performance monitoring and statistics tracking

### Version 1.5.0
- **Added:** Rule-based email categorization
- **Added:** Basic sender labeling system
- **Added:** Email box UI components
- **Improved:** Categorization accuracy with user feedback

### Version 1.0.0
- **Added:** Basic IMAP box management
- **Added:** Simple email categorization
- **Added:** Sender preference storage

---

*Module Version: 2.0.0*
*Last Updated: 2025-10-31*
*Email Categories: IMPORTANT, FEED, PAPER_TRAIL, SPAM*
*Data Storage: JSON-based sender labels*
*UI Framework: Gradio tabs*
