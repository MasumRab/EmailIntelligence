import gradio as gr
import asyncio
from src.core.factory import get_data_source
import pandas as pd

async def search_notmuch(query):
    """Callback function to search emails in notmuch."""
    data_source = await get_data_source()
    if hasattr(data_source, 'search_emails'):
        emails = await data_source.search_emails(query)
        # Store message_id in a DataFrame
        df = pd.DataFrame(emails)
        return df
    return pd.DataFrame()

async def get_email_content(message_id: str):
    """Callback function to get email content."""
    data_source = await get_data_source()
    if hasattr(data_source, 'get_email_by_message_id'):
        email = await data_source.get_email_by_message_id(message_id)
        if email:
            return email.get("body", "No content found.")
    return "Email not found."

def create_notmuch_ui():
    """Creates the Gradio UI for notmuch."""
    with gr.Blocks() as notmuch_tab:
        gr.Markdown("## Notmuch Email Search")

        with gr.Row():
            search_bar = gr.Textbox(label="Search Query", placeholder="Enter notmuch query...")
            search_button = gr.Button("Search")

        # Hidden DataFrame to store full email data
        email_data_df = gr.DataFrame(visible=False)

        results_list = gr.DataFrame(
            headers=["Subject", "From", "Date", "Tags"],
            label="Search Results",
            interactive=True
        )

        email_viewer = gr.Textbox(label="Email Content", lines=20, interactive=False)

        def display_search_results(df):
            if not df.empty:
                display_df = df[["subject", "sender", "date", "tags"]]
                display_df['tags'] = display_df['tags'].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)
                return df, display_df
            return pd.DataFrame(), pd.DataFrame(columns=["Subject", "From", "Date", "Tags"])

        def on_select(evt: gr.SelectData, df: pd.DataFrame):
            if evt.index is not None and not df.empty:
                selected_row = df.iloc[evt.index[0]]
                message_id = selected_row['message_id']
                # Run async function to get content
                content = asyncio.run(get_email_content(message_id))
                return content
            return "Select an email to view its content."

        search_button.click(
            fn=lambda q: asyncio.run(search_notmuch(q)),
            inputs=search_bar,
            outputs=email_data_df
        ).then(
            fn=display_search_results,
            inputs=email_data_df,
            outputs=[email_data_df, results_list]
        )

        results_list.select(
            fn=on_select,
            inputs=[email_data_df],
            outputs=email_viewer
        )

    return notmuch_tab

if __name__ == '__main__':
    # To run this file for testing, you need to set the DATA_SOURCE_TYPE environment variable
    # Example: DATA_SOURCE_TYPE=notmuch python modules/notmuch/ui.py
    import os
    os.environ["DATA_SOURCE_TYPE"] = "notmuch"

    ui = create_notmuch_ui()
    ui.launch()
