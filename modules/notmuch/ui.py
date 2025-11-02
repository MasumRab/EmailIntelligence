import gradio as gr
import asyncio
from src.core.factory import get_data_source
import pandas as pd

async def search_notmuch(query):
    """Callback function to search emails in notmuch."""
    data_source = await get_data_source()
    if hasattr(data_source, 'search_emails'):
        emails = await data_source.search_emails(query)
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

        email_data_df = gr.DataFrame(visible=False)

        results_list = gr.DataFrame(
            headers=["Subject", "From", "Date", "Tags"],
            label="Search Results",
            interactive=True
        )

        email_viewer = gr.Textbox(label="Email Content", lines=20, interactive=False)

        with gr.Row():
            tag_input = gr.Textbox(label="Tags", placeholder="Enter comma-separated tags...")
            update_button = gr.Button("Update Tags")

        selected_message_id = gr.Textbox(visible=False)

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
                tags = selected_row['tags']

                content = asyncio.run(get_email_content(message_id))
                tag_str = ', '.join(tags) if isinstance(tags, list) else ''

                return content, message_id, tag_str
            return "Select an email to view its content.", "", ""

        async def update_tags_callback(message_id: str, tags_str: str, current_query: str):
            if not message_id:
                gr.Warning("No message selected!")
                return pd.DataFrame()

            tags = [tag.strip() for tag in tags_str.split(',') if tag.strip()]

            data_source = await get_data_source()
            if hasattr(data_source, 'update_tags_for_message'):
                success = await data_source.update_tags_for_message(message_id, tags)
                if success:
                    gr.Info("Tags updated successfully! Refreshing search...")
                    refreshed_df = await search_notmuch(current_query)
                    return refreshed_df
                else:
                    gr.Error("Failed to update tags.")

            return pd.DataFrame()

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
            outputs=[email_viewer, selected_message_id, tag_input]
        )

        update_button.click(
            fn=lambda msg_id, tags, query: asyncio.run(update_tags_callback(msg_id, tags, query)),
            inputs=[selected_message_id, tag_input, search_bar],
            outputs=email_data_df
        ).then(
            fn=display_search_results,
            inputs=email_data_df,
            outputs=[email_data_df, results_list]
        )

    return notmuch_tab
