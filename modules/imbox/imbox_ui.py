import gradio as gr
import json
import os

SENDER_LABELS_FILE = "data/sender_labels.json"


def save_sender_label(sender_email, label):
    if not sender_email:
        return "Please enter a sender email."

    labels = {}
    if os.path.exists(SENDER_LABELS_FILE) and os.path.getsize(SENDER_LABELS_FILE) > 0:
        with open(SENDER_LABELS_FILE, "r") as f:
            labels = json.load(f)

    labels[sender_email] = label

    with open(SENDER_LABELS_FILE, "w") as f:
        json.dump(labels, f, indent=4)

    return f"Label for '{sender_email}' saved successfully!"


def get_sender_label(sender_email):
    if not os.path.exists(SENDER_LABELS_FILE):
        return "No labels saved yet."

    with open(SENDER_LABELS_FILE, "r") as f:
        labels = json.load(f)

    return labels.get(sender_email, "No label found for this sender.")


with gr.Blocks() as imbox_tab:
    with gr.Tabs():
        with gr.TabItem("Imbox"):
            gr.Markdown("## Imbox")
            gr.Markdown("Important emails will appear here.")
            # Placeholder for important emails
            gr.DataFrame(headers=["Date", "From", "Subject"], label="Important Emails")

        with gr.TabItem("The Feed"):
            gr.Markdown("## The Feed")
            gr.Markdown("Unimportant emails will appear here.")
            # Placeholder for unimportant emails
            gr.DataFrame(headers=["Date", "From", "Subject"], label="The Feed")

        with gr.TabItem("Paper Trail"):
            gr.Markdown("## Paper Trail")
            gr.Markdown("Transactional emails will appear here.")
            # Placeholder for transactional emails
            gr.DataFrame(headers=["Date", "From", "Subject"], label="Paper Trail")

        with gr.TabItem("Spam"):
            gr.Markdown("## Spam")
            gr.Markdown("Spam emails will appear here.")
            # Placeholder for spam emails
            gr.DataFrame(headers=["Date", "From", "Subject"], label="Spam")

    with gr.Row():
        with gr.Column():
            gr.Markdown("## Sender Labeling")
            sender_email = gr.Textbox(label="Sender Email")
            label = gr.Dropdown(label="Label", choices=["Important", "Not Important", "Spam"])
            save_label_button = gr.Button("Save Label")
            status = gr.Textbox(label="Status", interactive=False)

    save_label_button.click(fn=save_sender_label, inputs=[sender_email, label], outputs=[status])
