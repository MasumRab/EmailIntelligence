# EmailIntelligence Extensions

This directory contains extensions for the EmailIntelligence application. Extensions provide a way to add custom functionality to the application without modifying the core codebase.

## Available Extensions

- [Example Extension](../extensions/example/README.md) - Demonstrates the extension system by adding emojis and detailed metrics to sentiment analysis

## Extension Structure

Each extension should have the following structure:

- **Main Module**: Contains the extension code (e.g., `example.py`)
- **Metadata File**: Contains information about the extension (`metadata.json`)
- **README File**: Contains documentation for the extension (`README.md`)
- **Requirements File**: Contains dependencies for the extension (`requirements.txt`)

## Creating Extensions

You can create a new extension template using the launcher script:

```bash
python launch.py --create-extension my_extension
```

This will create a new extension template in the `extensions/my_extension` directory with the necessary files.

## Extension Lifecycle

Extensions go through the following lifecycle:

1. **Discovery**: Extensions are discovered in the extensions directory
2. **Loading**: Extension modules are loaded into memory
3. **Initialization**: Extensions are initialized with configuration
4. **Execution**: Extensions provide functionality during application execution
5. **Shutdown**: Extensions are properly shut down when the application exits

## Managing Extensions

You can manage extensions using the launcher script:

```bash
# List all installed extensions
python launch.py --list-extensions

# Install an extension from a Git repository
python launch.py --install-extension https://github.com/username/extension.git

# Update an extension
python launch.py --update-extension example

# Uninstall an extension
python launch.py --uninstall-extension example
```

## Extension API

The modern EmailIntelligence platform uses a modular architecture where extensions (called "modules") can seamlessly integrate with core application components. This section provides comprehensive documentation for accessing and extending the platform's core APIs.

### Module Registration

All modules must provide a `register()` function that takes the FastAPI app and Gradio app instances:

```python
def register(app: FastAPI, gradio_app: gr.Blocks):
    """Register module components with the main application."""
    # Add API routes
    app.include_router(your_router, prefix="/api/your-module", tags=["Your Module"])

    # Add Gradio UI components
    with gradio_app:
        # Add your UI components here
        pass
```

### 1. Accessing the AI Engine

Modules can access AI and NLP capabilities through the core AI engine and data sources.

#### Using the AI Engine Directly

```python
from src.core.factory import get_ai_engine

async def analyze_email_content(email_text: str):
    """Example: Analyze email content using the AI engine."""
    ai_engine = get_ai_engine()

    # Perform sentiment analysis
    sentiment_result = await ai_engine.analyze_sentiment(email_text)

    # Perform topic classification
    topic_result = await ai_engine.classify_topic(email_text)

    # Perform intent recognition
    intent_result = await ai_engine.recognize_intent(email_text)

    return {
        "sentiment": sentiment_result,
        "topic": topic_result,
        "intent": intent_result
    }
```

#### Using AI Engine in API Routes

```python
from fastapi import APIRouter, Depends
from src.core.factory import get_ai_engine
from src.core.auth import get_current_active_user

router = APIRouter()

@router.post("/analyze")
async def analyze_email(
    email_text: str,
    current_user: str = Depends(get_current_active_user),
    ai_engine = Depends(get_ai_engine)
):
    """API endpoint that uses AI engine for analysis."""
    sentiment = await ai_engine.analyze_sentiment(email_text)
    topics = await ai_engine.classify_topic(email_text)

    return {
        "sentiment": sentiment,
        "topics": topics,
        "analyzed_by": current_user
    }
```

#### Best Practices for AI Engine Usage
- Always use dependency injection (`Depends(get_ai_engine)`) in routes
- Handle AI processing errors gracefully
- Consider caching results for frequently analyzed content
- Respect rate limits and performance constraints

### 2. Interacting with the Data Store

Modules can read, write, and query application data through the data source abstraction layer.

#### Basic Data Operations

```python
from src.core.factory import get_data_source
from src.core.models import EmailCreate, EmailResponse

async def manage_emails():
    """Example: Basic CRUD operations with the data store."""
    db = get_data_source()

    # Create a new email
    email_data = EmailCreate(
        subject="Test Email",
        content="This is a test email",
        sender="test@example.com"
    )
    created_email = await db.create_email(email_data.model_dump())

    # Read emails
    all_emails = await db.get_all_emails()
    email_by_id = await db.get_email_by_id(created_email.id)

    # Search emails
    search_results = await db.search_emails("important project")

    # Filter by category
    category_emails = await db.get_emails_by_category("work")

    return {
        "created": created_email,
        "total_emails": len(all_emails),
        "search_results": len(search_results)
    }
```

#### Advanced Querying

```python
from datetime import datetime, timedelta

async def advanced_email_queries():
    """Example: Complex querying with filters."""
    db = get_data_source()

    # Get emails from last 7 days
    week_ago = datetime.now() - timedelta(days=7)
    recent_emails = await db.get_emails_after_date(week_ago)

    # Get unread emails
    unread_emails = await db.get_unread_emails()

    # Search with multiple criteria
    complex_results = await db.search_emails_with_filters(
        query="meeting",
        category="work",
        unread_only=True,
        limit=50
    )

    return complex_results
```

#### Using Data Sources in Routes

```python
from fastapi import APIRouter, Depends, Query
from typing import List
from src.core.data_source import DataSource
from src.core.factory import get_data_source

router = APIRouter()

@router.get("/", response_model=List[EmailResponse])
async def get_emails(
    db: DataSource = Depends(get_data_source),
    category: str = Query(None, description="Filter by category"),
    search: str = Query(None, description="Search query"),
    limit: int = Query(50, description="Maximum results")
):
    """Get emails with optional filtering."""
    if search:
        emails = await db.search_emails(search)
    elif category:
        emails = await db.get_emails_by_category(category)
    else:
        emails = await db.get_all_emails()

    return emails[:limit]
```

#### Best Practices for Data Store Usage
- Always use `Depends(get_data_source)` for dependency injection
- Handle database errors with appropriate HTTP status codes
- Use transactions for multi-step operations
- Implement proper pagination for large result sets
- Validate input data before database operations

### 3. Adding and Modifying UI Components

Modules can extend the Gradio interface by adding new tabs, components, and functionality.

#### Adding a New Tab

```python
import gradio as gr
from modules.your_module import analysis_functions

def register(app, gradio_app):
    # Add API routes
    # ... API registration code ...

    # Add UI components
    with gradio_app:
        with gr.TabItem("🤖 AI Analysis"):
            with gr.Row():
                with gr.Column():
                    input_text = gr.Textbox(
                        label="Email Content",
                        placeholder="Paste email content here...",
                        lines=5
                    )
                    analyze_btn = gr.Button("Analyze", variant="primary")

                with gr.Column():
                    sentiment_output = gr.Textbox(label="Sentiment")
                    topic_output = gr.Textbox(label="Topics")
                    intent_output = gr.Textbox(label="Intent")

            analyze_btn.click(
                fn=analysis_functions.analyze_email,
                inputs=[input_text],
                outputs=[sentiment_output, topic_output, intent_output]
            )
```

#### Integrating with Existing UI

```python
def enhance_existing_dashboard():
    """Example: Adding components to existing dashboard."""
    with gradio_app:
        # Find existing dashboard tab and add to it
        # Note: This requires knowledge of the existing UI structure

        # Add a custom metric card
        with gr.Row():
            custom_metric = gr.Number(
                label="Custom Metric",
                value=lambda: calculate_custom_metric(),
                every=30  # Update every 30 seconds
            )
```

#### Creating Reusable UI Components

```python
class EmailAnalyzerUI:
    """Reusable UI component for email analysis."""

    def __init__(self):
        self.input_text = None
        self.analyze_btn = None
        self.results = {}

    def create_component(self):
        """Create the UI component."""
        with gr.Column():
            self.input_text = gr.Textbox(
                label="Email Text",
                placeholder="Enter email content...",
                lines=4
            )

            with gr.Row():
                self.analyze_btn = gr.Button("🔍 Analyze", variant="primary")
                clear_btn = gr.Button("🗑️ Clear")

            # Results section
            with gr.Accordion("Analysis Results", open=True):
                self.results['sentiment'] = gr.Textbox(label="Sentiment")
                self.results['confidence'] = gr.Number(label="Confidence")
                self.results['topics'] = gr.Textbox(label="Topics")

            # Button actions
            self.analyze_btn.click(
                fn=self.analyze_email,
                inputs=[self.input_text],
                outputs=list(self.results.values())
            )

            clear_btn.click(
                fn=lambda: ("", 0.0, ""),
                outputs=list(self.results.values())
            )

    async def analyze_email(self, text):
        """Analysis function called by UI."""
        # Implementation here
        return sentiment, confidence, topics
```

#### Best Practices for UI Components
- Follow Gradio's design patterns and component conventions
- Use appropriate loading states for async operations
- Provide clear error messages and user feedback
- Make components responsive and accessible
- Test UI components across different screen sizes

### 4. Using the Event System

The platform provides an event system for loose coupling between modules.

#### Publishing Events

```python
from src.core.events import EventBus, Event

async def publish_analysis_complete():
    """Example: Publishing an event when analysis is complete."""
    event_bus = EventBus.get_instance()

    analysis_event = Event(
        type="analysis.completed",
        data={
            "email_id": "123",
            "results": {
                "sentiment": "positive",
                "confidence": 0.95
            }
        },
        source="ai_module"
    )

    await event_bus.publish(analysis_event)
```

#### Subscribing to Events

```python
from src.core.events import EventBus, EventHandler

class AnalysisEventHandler(EventHandler):
    """Handle analysis completion events."""

    async def handle(self, event: Event):
        """Process analysis completion events."""
        if event.type == "analysis.completed":
            analysis_data = event.data

            # Store results in database
            await store_analysis_results(analysis_data)

            # Trigger follow-up actions
            await trigger_follow_up_actions(analysis_data)

# Register the event handler
def register_event_handlers():
    """Register event handlers during module initialization."""
    event_bus = EventBus.get_instance()
    handler = AnalysisEventHandler()

    event_bus.subscribe("analysis.completed", handler)
    event_bus.subscribe("analysis.failed", handler)
```

#### Event Types and Patterns

Common event types in the platform:
- `email.received` - New email received
- `email.analyzed` - Email analysis completed
- `user.action` - User performed an action
- `system.error` - System error occurred
- `workflow.started` - Workflow execution started
- `workflow.completed` - Workflow execution completed

#### Best Practices for Event System
- Use descriptive event types with dot notation
- Include relevant data in event payloads
- Handle events asynchronously to avoid blocking
- Implement error handling in event handlers
- Document custom events your module publishes

### 5. Practical Use Cases and Examples

#### Use Case 1: Custom Email Filter Module

```python
# modules/custom_filter/__init__.py
from .routes import router as filter_router
from .ui import create_filter_ui

def register(app: FastAPI, gradio_app: gr.Blocks):
    """Register custom email filter module."""
    # API routes
    app.include_router(filter_router, prefix="/api/filters", tags=["Filters"])

    # UI components
    with gradio_app:
        create_filter_ui()
```

```python
# modules/custom_filter/routes.py
from fastapi import APIRouter, Depends
from src.core.factory import get_data_source
from .filter_logic import apply_custom_filters

router = APIRouter()

@router.post("/apply")
async def apply_filters(
    filter_criteria: dict,
    db = Depends(get_data_source)
):
    """Apply custom filters to emails."""
    emails = await db.get_all_emails()
    filtered_emails = await apply_custom_filters(emails, filter_criteria)

    return {"filtered_count": len(filtered_emails)}
```

#### Use Case 2: AI Enhancement Module

```python
# modules/ai_enhancer/__init__.py
from .enhancer import AIEnhancer

enhancer = AIEnhancer()

def register(app: FastAPI, gradio_app: gr.Blocks):
    """Register AI enhancement module."""
    # Initialize enhancer
    enhancer.initialize()

    # Add enhancement UI
    with gradio_app:
        enhancer.create_ui()
```

```python
# modules/ai_enhancer/enhancer.py
from src.core.factory import get_ai_engine

class AIEnhancer:
    def initialize(self):
        """Initialize the enhancer by hooking into AI engine."""
        # This would typically monkey-patch or extend AI engine methods
        pass

    def create_ui(self):
        """Create enhancement UI components."""
        with gr.TabItem("🚀 AI Enhancer"):
            gr.Markdown("Enhanced AI capabilities")
            # Add UI components here
```

### Module Development Best Practices

1. **Separation of Concerns**: Keep API routes, UI components, and business logic separate
2. **Error Handling**: Implement comprehensive error handling with appropriate logging
3. **Testing**: Write unit tests for module components and integration tests
4. **Documentation**: Document all public APIs and configuration options
5. **Configuration**: Use environment variables for configurable settings
6. **Performance**: Optimize for performance and memory usage
7. **Security**: Validate inputs and implement proper authentication/authorization
8. **Compatibility**: Test with different Python versions and environments

### Migration from Legacy Extensions

If you're migrating from the old extension system to the new modular system:

1. **Replace extension hooks** with module registration functions
2. **Use dependency injection** instead of direct imports
3. **Implement proper error handling** with FastAPI's exception system
4. **Add authentication** using the core auth system
5. **Test thoroughly** with the new modular architecture

For more examples, see the existing modules in the `modules/` directory.

## Best Practices

When creating extensions, follow these best practices:

1. **Isolation**: Keep your extension isolated from other extensions
2. **Error Handling**: Handle errors gracefully to avoid affecting the core application
3. **Documentation**: Document your extension thoroughly
4. **Testing**: Test your extension thoroughly before distributing it
5. **Dependencies**: Minimize dependencies and specify them in `requirements.txt`