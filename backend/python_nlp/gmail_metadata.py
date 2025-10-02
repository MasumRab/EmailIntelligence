"""
Provides comprehensive extraction of metadata from Gmail API message objects.

This module defines a detailed data structure for holding all relevant
metadata from a Gmail message and includes a class to perform the extraction
from the raw API response.
"""

import base64
import json
import logging
import re
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class GmailMessage:
    """
    A comprehensive data structure for holding extracted Gmail message metadata.

    Attributes:
        message_id: The unique ID of the message.
        thread_id: The ID of the conversation thread the message belongs to.
        subject: The subject line of the email.
        from_address: The sender's email address.
        to_addresses: A list of recipient email addresses.
        cc_addresses: A list of CC recipient email addresses.
        bcc_addresses: A list of BCC recipient email addresses.
        reply_to: The reply-to address, if specified.
        date: The timestamp from the 'Date' header.
        internal_date: The internal timestamp of the message.
        body_plain: The plain text body of the email.
        body_html: The HTML body of the email.
        snippet: A short snippet of the message content.
        labels: A list of human-readable labels applied to the message.
        label_ids: A list of raw label IDs from the Gmail API.
        importance_markers: A dictionary of importance-related markers.
        thread_info: A dictionary containing conversation thread details.
        size_estimate: An estimate of the message size in bytes.
        history_id: The history ID of the message.
        is_unread: True if the message is marked as unread.
        is_starred: True if the message is starred.
        is_important: True if the message is marked as important.
        is_draft: True if the message is a draft.
        is_sent: True if the message is in the sent folder.
        is_spam: True if the message is marked as spam.
        is_trash: True if the message is in the trash.
        is_chat: True if the message is a chat message.
        attachments: A list of dictionaries, each describing an attachment.
        has_attachments: True if the message has attachments.
        spf_status: The SPF authentication status (e.g., 'pass', 'fail').
        dkim_status: The DKIM authentication status.
        dmarc_status: The DMARC authentication status.
        encryption_info: A dictionary containing details about message encryption.
        message_headers: A dictionary of all message headers.
        custom_headers: A dictionary of custom (X-) headers.
        in_reply_to: The Message-ID of the message this is a reply to.
        references: A list of Message-IDs in the conversation thread.
        category: The Gmail category (e.g., 'primary', 'social').
        priority: The priority level of the message (e.g., 'high', 'normal').
        auto_reply: True if the message is detected as an auto-reply.
        mailing_list: The identifier of the mailing list, if any.
        raw_email: The raw, unparsed email content.
    """
    message_id: str
    thread_id: str
    subject: str
    from_address: str
    to_addresses: List[str]
    cc_addresses: List[str]
    bcc_addresses: List[str]
    reply_to: Optional[str]
    date: str
    internal_date: str
    body_plain: str
    body_html: str
    snippet: str
    labels: List[str]
    label_ids: List[str]
    importance_markers: Dict[str, Any]
    thread_info: Dict[str, Any]
    size_estimate: int
    history_id: str
    is_unread: bool
    is_starred: bool
    is_important: bool
    is_draft: bool
    is_sent: bool
    is_spam: bool
    is_trash: bool
    is_chat: bool
    attachments: List[Dict[str, Any]]
    has_attachments: bool
    spf_status: Optional[str]
    dkim_status: Optional[str]
    dmarc_status: Optional[str]
    encryption_info: Dict[str, Any]
    message_headers: Dict[str, str]
    custom_headers: Dict[str, str]
    in_reply_to: Optional[str]
    references: List[str]
    category: Optional[str]
    priority: str
    auto_reply: bool
    mailing_list: Optional[str]
    raw_email: Optional[str]


class GmailMetadataExtractor:
    """
    Extracts comprehensive metadata from raw Gmail API message objects.

    This class provides methods to parse the complex structure of a Gmail API
    response and populate a structured `GmailMessage` object.
    """

    def __init__(self):
        """Initializes the GmailMetadataExtractor."""
        self.logger = logging.getLogger(__name__)
        self.system_labels = {
            "INBOX": "inbox", "SENT": "sent", "DRAFT": "draft", "SPAM": "spam",
            "TRASH": "trash", "STARRED": "starred", "IMPORTANT": "important",
            "UNREAD": "unread", "CATEGORY_PERSONAL": "personal", "CATEGORY_SOCIAL": "social",
            "CATEGORY_PROMOTIONS": "promotions", "CATEGORY_UPDATES": "updates", "CATEGORY_FORUMS": "forums",
        }
        self.priority_headers = ["X-Priority", "Priority", "Importance", "X-MSMail-Priority"]
        self.security_headers = ["Authentication-Results", "Received-SPF", "DKIM-Signature", "ARC-Authentication-Results"]

    def extract_complete_metadata(self, gmail_message: Dict[str, Any]) -> GmailMessage:
        """
        Extracts all available metadata from a raw Gmail API message dictionary.

        Args:
            gmail_message: A dictionary representing the raw message object
                           from the Gmail API.

        Returns:
            A `GmailMessage` object populated with the extracted metadata.
            Returns a minimally populated object on failure.
        """
        try:
            message_id = gmail_message.get("id", "")
            thread_id = gmail_message.get("threadId", "")
            snippet = gmail_message.get("snippet", "")
            size_estimate = gmail_message.get("sizeEstimate", 0)
            history_id = gmail_message.get("historyId", "")
            internal_date = gmail_message.get("internalDate", "")
            label_ids = gmail_message.get("labelIds", [])
            labels = [self.system_labels.get(label_id, label_id) for label_id in label_ids]
            is_unread = "UNREAD" in label_ids
            is_starred = "STARRED" in label_ids
            is_important = "IMPORTANT" in label_ids
            is_draft = "DRAFT" in label_ids
            is_sent = "SENT" in label_ids
            is_spam = "SPAM" in label_ids
            is_trash = "TRASH" in label_ids
            is_chat = "CHAT" in label_ids
            category = self._extract_category(label_ids)
            payload = gmail_message.get("payload", {})
            headers = self._extract_headers(payload.get("headers", []))
            body_plain, body_html = self._extract_body_content(payload)
            attachments = self._extract_attachments(payload)
            has_attachments = len(attachments) > 0
            importance_markers = self._extract_importance_markers(headers, label_ids)
            thread_info = self._extract_thread_info(headers, gmail_message)
            spf_status, dkim_status, dmarc_status = self._extract_security_status(headers)
            encryption_info = self._extract_encryption_info(headers)
            priority = self._extract_priority(headers)
            mailing_list = self._extract_mailing_list_info(headers)
            auto_reply = self._is_auto_reply(headers, labels)
            in_reply_to = headers.get("In-Reply-To")
            references = self._extract_references(headers.get("References", ""))
            from_address = self._extract_email_address(headers.get("From", ""))
            to_addresses = self._extract_email_addresses(headers.get("To", ""))
            cc_addresses = self._extract_email_addresses(headers.get("Cc", ""))
            bcc_addresses = self._extract_email_addresses(headers.get("Bcc", ""))
            reply_to = headers.get("Reply-To")
            custom_headers = self._extract_custom_headers(headers)

            return GmailMessage(
                message_id=message_id, thread_id=thread_id, subject=headers.get("Subject", ""),
                from_address=from_address, to_addresses=to_addresses, cc_addresses=cc_addresses,
                bcc_addresses=bcc_addresses, reply_to=reply_to, date=headers.get("Date", ""),
                internal_date=internal_date, body_plain=body_plain, body_html=body_html,
                snippet=snippet, labels=labels, label_ids=label_ids,
                importance_markers=importance_markers, thread_info=thread_info,
                size_estimate=size_estimate, history_id=history_id, is_unread=is_unread,
                is_starred=is_starred, is_important=is_important, is_draft=is_draft,
                is_sent=is_sent, is_spam=is_spam, is_trash=is_trash, is_chat=is_chat,
                attachments=attachments, has_attachments=has_attachments,
                spf_status=spf_status, dkim_status=dkim_status, dmarc_status=dmarc_status,
                encryption_info=encryption_info, message_headers=headers,
                custom_headers=custom_headers, in_reply_to=in_reply_to, references=references,
                category=category, priority=priority, auto_reply=auto_reply,
                mailing_list=mailing_list, raw_email=gmail_message.get("raw"),
            )
        except Exception as e:
            self.logger.error(f"Error extracting metadata from message {gmail_message.get('id', 'unknown')}: {e}")
            return self._create_minimal_metadata(gmail_message)

    def _extract_headers(self, headers_list: List[Dict[str, str]]) -> Dict[str, str]:
        """Extracts and normalizes email headers into a dictionary."""
        return {h.get("name"): h.get("value") for h in headers_list}

    def _extract_body_content(self, payload: Dict[str, Any]) -> tuple[str, str]:
        """Recursively extracts plain text and HTML body content from the payload."""
        body_plain = []
        body_html = []

        def extract_from_part(part: Dict[str, Any]):
            mime_type = part.get("mimeType", "")
            if "data" in (body := part.get("body", {})):
                try:
                    decoded = base64.urlsafe_b64decode(body["data"] + "===").decode("utf-8", errors="ignore")
                    if mime_type == "text/plain":
                        body_plain.append(decoded)
                    elif mime_type == "text/html":
                        body_html.append(decoded)
                except Exception as e:
                    self.logger.warning(f"Error decoding body content: {e}")
            for subpart in part.get("parts", []):
                extract_from_part(subpart)

        extract_from_part(payload)
        return "".join(body_plain).strip(), "".join(body_html).strip()

    def _extract_attachments(self, payload: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Recursively extracts attachment information from the payload."""
        attachments = []

        def process_part(part: Dict[str, Any]):
            if "attachmentId" in (body := part.get("body", {})):
                attachments.append({
                    "attachment_id": body["attachmentId"],
                    "filename": part.get("filename", "unknown"),
                    "mime_type": part.get("mimeType", "application/octet-stream"),
                    "size": body.get("size", 0),
                    "part_id": part.get("partId", ""),
                })
            for subpart in part.get("parts", []):
                process_part(subpart)

        process_part(payload)
        return attachments

    def _extract_category(self, label_ids: List[str]) -> Optional[str]:
        """Extracts the primary Gmail category from a list of label IDs."""
        category_mappings = {
            "CATEGORY_PERSONAL": "primary", "CATEGORY_SOCIAL": "social",
            "CATEGORY_PROMOTIONS": "promotions", "CATEGORY_UPDATES": "updates", "CATEGORY_FORUMS": "forums",
        }
        for label_id in label_ids:
            if label_id in category_mappings:
                return category_mappings[label_id]
        return "primary" if "INBOX" in label_ids else None

    def _extract_importance_markers(self, headers: Dict[str, str], label_ids: List[str]) -> Dict[str, Any]:
        """Extracts various importance and priority markers."""
        markers = {"is_important": "IMPORTANT" in label_ids, "is_starred": "STARRED" in label_ids}
        for header in self.priority_headers:
            if header in headers:
                markers["priority_header"] = headers[header]
                break
        return markers

    def _extract_thread_info(self, headers: Dict[str, str], gmail_message: Dict[str, Any]) -> Dict[str, Any]:
        """Extracts conversation thread-related information."""
        return {
            "thread_id": gmail_message.get("threadId", ""),
            "message_id_header": headers.get("Message-ID", ""),
            "in_reply_to": headers.get("In-Reply-To"),
            "references": self._extract_references(headers.get("References", "")),
        }

    def _extract_references(self, references_header: str) -> List[str]:
        """Extracts a list of Message-IDs from the 'References' header."""
        return re.findall(r"<([^>]+)>", references_header) if references_header else []

    def _extract_security_status(self, headers: Dict[str, str]) -> tuple[Optional[str], Optional[str], Optional[str]]:
        """Extracts SPF, DKIM, and DMARC status from authentication headers."""
        auth_results = headers.get("Authentication-Results", "")
        spf = re.search(r"spf=(\w+)", auth_results, re.IGNORECASE)
        dkim = re.search(r"dkim=(\w+)", auth_results, re.IGNORECASE)
        dmarc = re.search(r"dmarc=(\w+)", auth_results, re.IGNORECASE)
        return (spf.group(1).lower() if spf else None,
                dkim.group(1).lower() if dkim else None,
                dmarc.group(1).lower() if dmarc else None)

    def _extract_encryption_info(self, headers: Dict[str, str]) -> Dict[str, Any]:
        """Extracts information about message encryption (TLS, S/MIME, etc.)."""
        info = {"tls_encrypted": False, "signed": False}
        for received in [v for k, v in headers.items() if k.lower() == "received"]:
            if "TLS" in received or "SSL" in received:
                info["tls_encrypted"] = True
                break
        if "multipart/signed" in headers.get("Content-Type", ""):
            info["signed"] = True
        return info

    def _extract_priority(self, headers: Dict[str, str]) -> str:
        """Extracts and normalizes the message priority."""
        for header in self.priority_headers:
            if value := headers.get(header, "").lower():
                if any(k in value for k in ["high", "urgent", "1"]):
                    return "high"
                if any(k in value for k in ["low", "5"]):
                    return "low"
        return "normal"

    def _extract_mailing_list_info(self, headers: Dict[str, str]) -> Optional[str]:
        """Extracts mailing list information from headers."""
        for header in ["List-ID", "List-Post", "Mailing-List"]:
            if value := headers.get(header):
                return value
        return None

    def _is_auto_reply(self, headers: Dict[str, str], labels: List[str]) -> bool:
        """Determines if a message is likely an auto-reply."""
        for header in ["Auto-Submitted", "X-Auto-Response-Suppress"]:
            if value := headers.get(header, "").lower():
                if "auto-replied" in value or "yes" in value:
                    return True
        subject = headers.get("Subject", "").lower()
        return any(p in subject for p in ["out of office", "automatic reply"])

    def _extract_email_address(self, address_header: str) -> str:
        """Extracts a single email address from a header string."""
        if match := re.search(r"<([^>]+)>", address_header):
            return match.group(1)
        return address_header.strip()

    def _extract_email_addresses(self, addresses_header: str) -> List[str]:
        """Extracts multiple email addresses from a header string."""
        return [self._extract_email_address(addr.strip()) for addr in (addresses_header or "").split(",") if addr]

    def _extract_custom_headers(self, headers: Dict[str, str]) -> Dict[str, str]:
        """Extracts custom headers (those starting with 'X-')."""
        standard = {"From", "To", "Cc", "Bcc", "Subject", "Date", "Message-ID"}
        return {k: v for k, v in headers.items() if k not in standard and k.startswith("X-")}

    def _create_minimal_metadata(self, gmail_message: Dict[str, Any]) -> GmailMessage:
        """Creates a minimally populated GmailMessage object for error cases."""
        return GmailMessage(
            message_id=gmail_message.get("id", ""), thread_id=gmail_message.get("threadId", ""),
            subject="", from_address="", to_addresses=[], cc_addresses=[], bcc_addresses=[],
            reply_to=None, date="", internal_date=gmail_message.get("internalDate", ""),
            body_plain="", body_html="", snippet=gmail_message.get("snippet", ""),
            labels=[], label_ids=gmail_message.get("labelIds", []), importance_markers={},
            thread_info={}, size_estimate=gmail_message.get("sizeEstimate", 0),
            history_id=gmail_message.get("historyId", ""), is_unread=False, is_starred=False,
            is_important=False, is_draft=False, is_sent=False, is_spam=False,
            is_trash=False, is_chat=False, attachments=[], has_attachments=False,
            spf_status=None, dkim_status=None, dmarc_status=None, encryption_info={},
            message_headers={}, custom_headers={}, in_reply_to=None, references=[],
            category=None, priority="normal", auto_reply=False, mailing_list=None,
            raw_email=None,
        )

    def extract_batch_metadata(self, gmail_messages: List[Dict[str, Any]]) -> List[GmailMessage]:
        """
        Extracts metadata from a batch of Gmail message objects.

        Args:
            gmail_messages: A list of raw Gmail API message dictionaries.

        Returns:
            A list of `GmailMessage` objects.
        """
        return [self.extract_complete_metadata(msg) for msg in gmail_messages]

    def to_training_format(self, gmail_message: GmailMessage) -> Dict[str, Any]:
        """
        Converts a `GmailMessage` object into a dictionary suitable for training data.

        Args:
            gmail_message: The `GmailMessage` object to convert.

        Returns:
            A dictionary formatted for use in a training dataset.
        """
        return {
            "id": gmail_message.message_id, "subject": gmail_message.subject,
            "content": gmail_message.body_plain or gmail_message.snippet,
            "sender": gmail_message.from_address, "timestamp": gmail_message.date,
            "labels": gmail_message.labels, "category": gmail_message.category,
            "metadata": {"size": gmail_message.size_estimate, "has_attachments": gmail_message.has_attachments},
        }


def main():
    """Demonstrates the usage of the GmailMetadataExtractor."""
    extractor = GmailMetadataExtractor()
    sample_message = {
        "id": "msg_123456789", "threadId": "thread_123456789",
        "labelIds": ["INBOX", "IMPORTANT", "CATEGORY_PERSONAL"],
        "snippet": "This is a sample email message...", "payload": {
            "headers": [
                {"name": "From", "value": "John Doe <john@example.com>"},
                {"name": "Subject", "value": "Important Project Update"},
            ],
            "body": {"data": base64.urlsafe_b64encode(b"This is the email content.").decode()},
        },
    }
    metadata = extractor.extract_complete_metadata(sample_message)
    print(f"Subject: {metadata.subject}")
    print(f"From: {metadata.from_address}")
    training_data = extractor.to_training_format(metadata)
    print(f"Training format: {json.dumps(training_data, indent=2)}")


if __name__ == "__main__":
    main()
