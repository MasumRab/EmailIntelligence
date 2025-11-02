import gradio as gr
import pandas as pd
import asyncio
from src.core.factory import get_data_source
import logging

logger = logging.getLogger(__name__)

async def load_emails(limit=50, offset=0):
    """Load emails from the data source."""
    try:
        data_source = await get_data_source()
        if hasattr(data_source, 'get_all_emails'):
            emails = await data_source.get_all_emails(limit=limit, offset=offset)
            return emails
        elif hasattr(data_source, 'get_emails'):
            emails = await data_source.get_emails(limit=limit, offset=offset)
            return emails
        return []
    except Exception as e:
        logger.error(f"Error loading emails: {e}")
        return []

async def refresh_inbox():
    """Refresh the inbox display."""
    emails = await load_emails()
    if emails:
        # Convert to DataFrame for Gradio
        df = pd.DataFrame(emails)
        if not df.empty:
            # Select relevant columns for display
            columns_to_show = ["subject", "sender", "date"]
            # Only include columns that exist in the DataFrame
            available_columns = [col for col in columns_to_show if col in df.columns]
            if available_columns:
                display_df = df[available_columns].copy()
                # Rename columns for better display
                display_df.columns = [col.title() for col in available_columns]
                return display_df
    return pd.DataFrame(columns=["Subject", "From", "Date"])

def create_inbox_ui():
    """Creates the inbox UI components."""
    with gr.Blocks() as inbox_tab:
        gr.Markdown("# 📥 Inbox")
        gr.Markdown("## Browse and manage your emails")
        
        # Controls
        with gr.Row():
            refresh_btn = gr.Button("Refresh Inbox")
            search_box = gr.Textbox(label="Search", placeholder="Search emails...")
        
        # Email list
        email_list = gr.DataFrame(
            headers=["Subject", "From", "Date"],
            label="Emails",
            interactive=True
        )
        
        # Email content viewer
        with gr.Row():
            with gr.Column(scale=1):
                email_content = gr.Textbox(
                    label="Email Content",
                    lines=15,
                    interactive=False
                )
            with gr.Column(scale=1):
                email_metadata = gr.JSON(label="Email Metadata")
        
        async def on_email_select(evt: gr.SelectData, df: pd.DataFrame):
            """Handle email selection."""
            if evt.index is not None and not df.empty:
                try:
                    # Get the selected row
                    selected_row = df.iloc[evt.index[0]]
                    
                    # In a real implementation, we would fetch the full email content
                    # For now, we'll create a sample based on the selected email
                    subject = selected_row.get('Subject', 'No Subject')
                    sender = selected_row.get('From', 'Unknown Sender')
                    date = selected_row.get('Date', 'Unknown Date')
                    
                    content = f"Subject: {subject}\n\nFrom: {sender}\n\nDate: {date}\n\n"
                    content += "This is a sample email content for demonstration purposes. "
                    content += "In a full implementation, this would show the actual email content.\n\n"
                    content += "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
                    content += "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
                    
                    metadata = {
                        "subject": subject,
                        "sender": sender,
                        "date": date,
                        "size": "2.4 KB",
                        "tags": ["inbox", "unread"] if "Unread" in df.columns and selected_row.get('Unread', False) else ["inbox"]
                    }
                    return content, metadata
                except Exception as e:
                    logger.error(f"Error selecting email: {e}")
                    return "Error loading email content", {}
            return "", {}
        
        async def search_emails(search_term):
            """Search emails based on search term."""
            if not search_term:
                return await refresh_inbox()
            
            try:
                data_source = await get_data_source()
                if hasattr(data_source, 'search_emails'):
                    emails = await data_source.search_emails(search_term)
                    if emails:
                        df = pd.DataFrame(emails)
                        if not df.empty:
                            # Select relevant columns for display
                            columns_to_show = ["subject", "sender", "date"]
                            available_columns = [col for col in columns_to_show if col in df.columns]
                            if available_columns:
                                display_df = df[available_columns].copy()
                                display_df.columns = [col.title() for col in available_columns]
                                return display_df
                # Fallback to regular refresh
                return await refresh_inbox()
            except Exception as e:
                logger.error(f"Error searching emails: {e}")
                return await refresh_inbox()
        
        # Event handlers
        refresh_btn.click(
            fn=lambda: asyncio.run(refresh_inbox()),
            inputs=[],
            outputs=[email_list]
        )
        
        search_box.submit(
            fn=lambda term: asyncio.run(search_emails(term)),
            inputs=[search_box],
            outputs=[email_list]
        )
        
        email_list.select(
            fn=lambda evt, df: asyncio.run(on_email_select(evt, df)),
            inputs=[email_list],
            outputs=[email_content, email_metadata]
        )
        
        # Initialize on load
        inbox_tab.load(
            fn=lambda: asyncio.run(refresh_inbox()),
            inputs=[],
            outputs=[email_list]
        )
    
    return inbox_tab