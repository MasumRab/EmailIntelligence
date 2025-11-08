import asyncio
import json
import os
from datetime import datetime, timedelta

import gradio as gr
import requests

from src.core.database import DatabaseManager

SAVED_FILTERS_FILE = "saved_filters.json"


def get_saved_filters():
    if not os.path.exists(SAVED_FILTERS_FILE):
        return []
    with open(SAVED_FILTERS_FILE, "r", encoding="utf-8") as f:
        filters = [json.loads(line) for line in f]
    return filters


def get_saved_filter_names():
    filters = get_saved_filters()
    return [f["name"] for f in filters]


def load_filter(filter_name):
    filters = get_saved_filters()
    for f in filters:
        if f["name"] == filter_name:
            return (
                f["sender"],
                f["to"],
                f["subject"],
                f["keywords"],
                f["date_filter"],
                f["start_date"],
                f["end_date"],
                f["category"],
                f["has_attachment"],
            )
    return "", "", "", "", "Any time", "", "", "", False


def save_filter(
    name, sender, to, subject, keywords, date_filter, start_date, end_date, category, has_attachment
):
    if not name:
        return "Please enter a name for the filter."
    filter_data = {
        "name": name,
        "sender": sender,
        "to": to,
        "subject": subject,
        "keywords": keywords,
        "date_filter": date_filter,
        "start_date": start_date,
        "end_date": end_date,
        "category": category,
        "has_attachment": has_attachment,
    }
    with open(SAVED_FILTERS_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(filter_data) + "\n")
    return f"Filter '{name}' saved successfully!"


def get_categories():
    try:
        response = requests.get("http://127.0.0.1:8000/api/categories", timeout=10)
        if response.status_code == 200:
            return [c["name"] for c in response.json()]
        return []
    except (requests.RequestException, ValueError) as e:
        print(f"Error fetching categories: {e}")
        return ["uncategorized", "work", "personal"]


def build_query(
    sender, to, subject, keywords, date_filter, start_date, end_date, category, has_attachment
):
    query_parts = []
    if sender:
        query_parts.append(f"from:{sender}")
    if to:
        query_parts.append(f"to:{to}")
    if subject:
        query_parts.append(f"subject:{subject}")
    if keywords:
        query_parts.append(keywords)
    if category:
        query_parts.append(f"category:{category}")
    if has_attachment:
        query_parts.append("has:attachment")

    now = datetime.now()
    if date_filter == "Today":
        query_parts.append(f"after:{now.strftime('%Y/%m/%d')}")
    elif date_filter == "Yesterday":
        yesterday = now - timedelta(days=1)
        query_parts.append(f"after:{yesterday.strftime('%Y/%m/%d')}")
        query_parts.append(f"before:{now.strftime('%Y/%m/%d')}")
    elif date_filter == "Last 7 days":
        seven_days_ago = now - timedelta(days=7)
        query_parts.append(f"after:{seven_days_ago.strftime('%Y/%m/%d')}")
    elif date_filter == "Last 30 days":
        thirty_days_ago = now - timedelta(days=30)
        query_parts.append(f"after:{thirty_days_ago.strftime('%Y/%m/%d')}")
    elif date_filter == "Custom":
        if start_date:
            query_parts.append(f"after:{start_date}")
        if end_date:
            query_parts.append(f"before:{end_date}")

    return " ".join(query_parts)


def run_filter_workflow(
    sender, to, subject, keywords, date_filter, start_date, end_date, category, has_attachment, max_emails, download_format, test_only=False
):
    criteria = {
        "required_senders": [s.strip() for s in sender.split(",")] if sender else [],
        "required_recipients": [r.strip() for r in to.split(",")] if to else [],
        "required_keywords": [k.strip() for k in keywords.split(",")] if keywords else [],
        "required_categories": [category] if category else [],
        "has_attachment": has_attachment,
    }

    # Simplified date handling for this example
    if date_filter != "Any time" and date_filter != "Custom":
        # In a real scenario, you'd calculate the date range here
        pass

    workflow_payload = {
        "workflow": {
            "name": "Dynamic Filter Workflow",
            "nodes": [
                {"node_id": "source", "node_type": "EmailSourceNode", "config": {"max_emails": max_emails if not test_only else 0}},
                {"node_id": "filter", "node_type": "FilterNode", "config": {"criteria": criteria}},
            ],
            "connections": [
                {"source_node_id": "source", "source_port": "emails", "target_node_id": "filter", "target_port": "emails"}
            ]
        }
    }

    try:
        response = requests.post("http://127.0.0.1:8000/api/workflows/run_filter", json=workflow_payload, timeout=60)
        if response.status_code == 200:
            data = response.json()
            if test_only:
                filtered_count = data.get("results", {}).get("filter", {}).get("stats", {}).get("filtered_count", 0)
                return f"Estimated {filtered_count} matches for the current filter."

            filtered_emails = data.get("results", {}).get("filter", {}).get("filtered_emails", [])

            if download_format == "JSON":
                with open("retrieved_emails.json", "w", encoding="utf-8") as f:
                    json.dump(filtered_emails, f)
                return f"Successfully retrieved and saved {len(filtered_emails)} emails to retrieved_emails.json", filtered_emails
            else:  # CSV
                import pandas as pd
                df = pd.DataFrame(filtered_emails)
                df.to_csv("retrieved_emails.csv", index=False)
                return f"Successfully retrieved and saved {len(filtered_emails)} emails to retrieved_emails.csv", filtered_emails
        else:
            return f"Error: {response.text}", []
    except requests.RequestException as e:
        return f"Error connecting to the backend: {e}", []


with gr.Blocks() as email_retrieval_tab:
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("## Email Account")
            email_address = gr.Textbox(label="Email Address")
            password = gr.Textbox(label="Password", type="password")
            server = gr.Dropdown(
                label="Email Server",
                choices=["imap.gmail.com", "imap.mail.yahoo.com", "outlook.office365.com"],
            )

            gr.Markdown("## Saved Filters")
            with gr.Row():
                saved_filters_dropdown = gr.Dropdown(
                    label="Load Filter", choices=get_saved_filter_names()
                )
                load_filter_button = gr.Button("Load")
                refresh_filters_button = gr.Button("Refresh")

            gr.Markdown("## Filter Criteria")
            sender = gr.Textbox(label="From")
            to = gr.Textbox(label="To")
            subject = gr.Textbox(label="Subject")
            keywords = gr.Textbox(label="Keywords (comma-separated)")
            category = gr.Dropdown(label="Topic", choices=get_categories())
            has_attachment = gr.Checkbox(label="Has Attachment")

            with gr.Row():
                date_filter = gr.Dropdown(
                    label="Date",
                    choices=[
                        "Any time",
                        "Today",
                        "Yesterday",
                        "Last 7 days",
                        "Last 30 days",
                        "Custom",
                    ],
                    value="Any time",
                )
                start_date = gr.Textbox(label="Start Date (YYYY/MM/DD)", visible=False)
                end_date = gr.Textbox(label="End Date (YYYY/MM/DD)", visible=False)

            def toggle_date_fields(date_filter_value):
                return gr.update(visible=date_filter_value == "Custom"), gr.update(
                    visible=date_filter_value == "Custom"
                )

            date_filter.change(
                toggle_date_fields, inputs=date_filter, outputs=[start_date, end_date]
            )

            gr.Markdown("## Save Filter")
            with gr.Row():
                new_filter_name = gr.Textbox(label="Filter Name")
                save_button = gr.Button("Save Filter")

            test_button = gr.Button("Test Filter", variant="secondary")
            estimation_output = gr.Textbox(label="Filter Estimation", interactive=False)

        with gr.Column(scale=2):
            gr.Markdown("## Email Retrieval")
            with gr.Row():
                max_emails_slider = gr.Slider(
                    minimum=10, maximum=1000, step=10, label="Max Emails to Download", value=100
                )
                download_format_dropdown = gr.Dropdown(
                    label="Download Format", choices=["JSON", "CSV"], value="JSON"
                )
            download_button = gr.Button("Download Emails", variant="primary")
            retrieval_status = gr.Textbox(label="Status", interactive=False)
            email_table = gr.DataFrame(
                headers=["Date", "From", "Subject"], label="Retrieved Emails"
            )

    load_filter_button.click(
        fn=load_filter,
        inputs=[saved_filters_dropdown],
        outputs=[
            sender,
            to,
            subject,
            keywords,
            date_filter,
            start_date,
            end_date,
            category,
            has_attachment,
        ],
    )

    def refresh_filters():
        return gr.update(choices=get_saved_filter_names())

    refresh_filters_button.click(fn=refresh_filters, inputs=[], outputs=[saved_filters_dropdown])

    save_button.click(
        fn=save_filter,
        inputs=[
            new_filter_name,
            sender,
            to,
            subject,
            keywords,
            date_filter,
            start_date,
            end_date,
            category,
            has_attachment,
        ],
        outputs=[retrieval_status],
    ).then(fn=refresh_filters, inputs=[], outputs=[saved_filters_dropdown])

    test_button.click(
        fn=lambda sender, to, subject, keywords, date_filter, start_date, end_date, category, has_attachment: run_filter_workflow(
            sender, to, subject, keywords, date_filter, start_date, end_date, category, has_attachment, 0, "JSON", test_only=True
        ),
        inputs=[
            sender,
            to,
            subject,
            keywords,
            date_filter,
            start_date,
            end_date,
            category,
            has_attachment,
        ],
        outputs=estimation_output,
    )

    download_button.click(
        fn=lambda sender, to, subject, keywords, date_filter, start_date, end_date, category, has_attachment, max_emails, download_format: run_filter_workflow(
            sender, to, subject, keywords, date_filter, start_date, end_date, category, has_attachment, max_emails, download_format, test_only=False
        ),
        inputs=[
            sender,
            to,
            subject,
            keywords,
            date_filter,
            start_date,
            end_date,
            category,
            has_attachment,
            max_emails_slider,
            download_format_dropdown,
        ],
        outputs=[retrieval_status, email_table],
    )
