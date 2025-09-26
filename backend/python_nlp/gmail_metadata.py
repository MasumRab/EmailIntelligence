"""
Comprehensive Gmail Metadata Extraction
Extracts all available Gmail email metadata including headers, labels, importance, and thread information
"""

import base64
import json
import logging
import re
from dataclasses import dataclass
from datetime import datetime  # noqa: F401
from typing import Any, Dict, List, Optional


@dataclass
class GmailMessage:
    """Complete Gmail message metadata structure"""

    # Core identifiers
    message_id: str
    thread_id: str

    # Message headers
    subject: str
    from_address: str
    to_addresses: List[str]
    cc_addresses: List[str]
    bcc_addresses: List[str]
    reply_to: Optional[str]

    # Timestamps
    date: str
    internal_date: str

    # Content
    body_plain: str
    body_html: str
    snippet: str

    # Gmail-specific metadata
    labels: List[str]
    label_ids: List[str]
    importance_markers: Dict[str, Any]
    thread_info: Dict[str, Any]

    # Message properties
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

    # Attachments
    attachments: List[Dict[str, Any]]
    has_attachments: bool

    # Security and delivery
    spf_status: Optional[str]
    dkim_status: Optional[str]
    dmarc_status: Optional[str]
    encryption_info: Dict[str, Any]

    # Additional headers
    message_headers: Dict[str, str]
    custom_headers: Dict[str, str]

    # Conversation context
    in_reply_to: Optional[str]
    references: List[str]

    # Gmail categories (Primary, Social, Promotions, Updates, Forums)
    category: Optional[str]

    # Priority and handling
    priority: str
    auto_reply: bool
    mailing_list: Optional[str]

    # Raw data
    raw_email: Optional[str]


class GmailMetadataExtractor:
    """Comprehensive Gmail metadata extraction with full API integration"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

        # Gmail label mappings
        self.system_labels = {
            "INBOX": "inbox",
            "SENT": "sent",
            "DRAFT": "draft",
            "SPAM": "spam",
            "TRASH": "trash",
            "STARRED": "starred",
            "IMPORTANT": "important",
            "UNREAD": "unread",
            "CATEGORY_PERSONAL": "personal",
            "CATEGORY_SOCIAL": "social",
            "CATEGORY_PROMOTIONS": "promotions",
            "CATEGORY_UPDATES": "updates",
            "CATEGORY_FORUMS": "forums",
        }

        # Priority indicators
        self.priority_headers = [
            "X-Priority",
            "Priority",
            "Importance",
            "X-MSMail-Priority",
        ]

        # Security headers
        self.security_headers = [
            "Authentication-Results",
            "Received-SPF",
            "DKIM-Signature",
            "ARC-Authentication-Results",
        ]

    def extract_complete_metadata(self, gmail_message: Dict[str, Any]) -> GmailMessage:
        """Extract all available metadata from Gmail API message"""
        try:
            # Basic message info
            message_id = gmail_message.get("id", "")
            thread_id = gmail_message.get("threadId", "")
            snippet = gmail_message.get("snippet", "")
            size_estimate = gmail_message.get("sizeEstimate", 0)
            history_id = gmail_message.get("historyId", "")
            internal_date = gmail_message.get("internalDate", "")

            # Extract labels and determine message state
            label_ids = gmail_message.get("labelIds", [])
            labels = [self.system_labels.get(label_id, label_id) for label_id in label_ids]

            # Determine message state from labels
            is_unread = "UNREAD" in label_ids
            is_starred = "STARRED" in label_ids
            is_important = "IMPORTANT" in label_ids
            is_draft = "DRAFT" in label_ids
            is_sent = "SENT" in label_ids
            is_spam = "SPAM" in label_ids
            is_trash = "TRASH" in label_ids
            is_chat = "CHAT" in label_ids

            # Determine category
            category = self._extract_category(label_ids)

            # Extract payload (headers and body)
            payload = gmail_message.get("payload", {})
            headers = self._extract_headers(payload.get("headers", []))

            # Extract body content
            body_plain, body_html = self._extract_body_content(payload)

            # Extract attachments
            attachments = self._extract_attachments(payload)
            has_attachments = len(attachments) > 0

            # Extract importance markers
            importance_markers = self._extract_importance_markers(headers, label_ids)

            # Extract thread information
            thread_info = self._extract_thread_info(headers, gmail_message)

            # Extract security information
            spf_status, dkim_status, dmarc_status = self._extract_security_status(headers)
            encryption_info = self._extract_encryption_info(headers)

            # Extract priority information
            priority = self._extract_priority(headers)

            # Extract mailing list information
            mailing_list = self._extract_mailing_list_info(headers)

            # Check for auto-reply
            auto_reply = self._is_auto_reply(headers, labels)

            # Extract conversation context
            in_reply_to = headers.get("In-Reply-To")
            references = self._extract_references(headers.get("References", ""))

            # Extract addresses
            from_address = self._extract_email_address(headers.get("From", ""))
            to_addresses = self._extract_email_addresses(headers.get("To", ""))
            cc_addresses = self._extract_email_addresses(headers.get("Cc", ""))
            bcc_addresses = self._extract_email_addresses(headers.get("Bcc", ""))
            reply_to = headers.get("Reply-To")

            # Filter custom headers
            custom_headers = self._extract_custom_headers(headers)

            return GmailMessage(
                message_id=message_id,
                thread_id=thread_id,
                subject=headers.get("Subject", ""),
                from_address=from_address,
                to_addresses=to_addresses,
                cc_addresses=cc_addresses,
                bcc_addresses=bcc_addresses,
                reply_to=reply_to,
                date=headers.get("Date", ""),
                internal_date=internal_date,
                body_plain=body_plain,
                body_html=body_html,
                snippet=snippet,
                labels=labels,
                label_ids=label_ids,
                importance_markers=importance_markers,
                thread_info=thread_info,
                size_estimate=size_estimate,
                history_id=history_id,
                is_unread=is_unread,
                is_starred=is_starred,
                is_important=is_important,
                is_draft=is_draft,
                is_sent=is_sent,
                is_spam=is_spam,
                is_trash=is_trash,
                is_chat=is_chat,
                attachments=attachments,
                has_attachments=has_attachments,
                spf_status=spf_status,
                dkim_status=dkim_status,
                dmarc_status=dmarc_status,
                encryption_info=encryption_info,
                message_headers=headers,
                custom_headers=custom_headers,
                in_reply_to=in_reply_to,
                references=references,
                category=category,
                priority=priority,
                auto_reply=auto_reply,
                mailing_list=mailing_list,
                raw_email=gmail_message.get("raw"),
            )

        except Exception as e:
            self.logger.error(
                f"Error extracting metadata from message {gmail_message.get('id', 'unknown')}: {e}"
            )
            # Return minimal metadata on error
            return self._create_minimal_metadata(gmail_message)

    def _extract_headers(self, headers_list: List[Dict[str, str]]) -> Dict[str, str]:
        """Extract and normalize email headers"""
        headers = {}
        for header in headers_list:
            name = header.get("name", "")
            value = header.get("value", "")
            headers[name] = value
        return headers

    def _extract_body_content(self, payload: Dict[str, Any]) -> tuple[str, str]:
        """Extract plain text and HTML body content"""
        body_plain = ""
        body_html = ""

        def extract_from_part(part: Dict[str, Any]):
            nonlocal body_plain, body_html

            mime_type = part.get("mimeType", "")
            body = part.get("body", {})
            data = body.get("data", "")

            # Decode base64 content
            if data:
                try:
                    decoded = base64.urlsafe_b64decode(data + "===").decode(
                        "utf-8", errors="ignore"
                    )
                    if mime_type == "text/plain":
                        body_plain += decoded
                    elif mime_type == "text/html":
                        body_html += decoded
                except Exception as e:
                    self.logger.warning(f"Error decoding body content: {e}")

            # Recursively process parts
            for subpart in part.get("parts", []):
                extract_from_part(subpart)

        extract_from_part(payload)
        return body_plain.strip(), body_html.strip()

    def _extract_attachments(self, payload: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract attachment information"""
        attachments = []

        def process_part(part: Dict[str, Any]):
            body = part.get("body", {})
            attachment_id = body.get("attachmentId")

            if attachment_id:
                filename = part.get("filename", "unknown")
                mime_type = part.get("mimeType", "application/octet-stream")
                size = body.get("size", 0)

                attachments.append(
                    {
                        "attachment_id": attachment_id,
                        "filename": filename,
                        "mime_type": mime_type,
                        "size": size,
                        "part_id": part.get("partId", ""),
                    }
                )

            # Process nested parts
            for subpart in part.get("parts", []):
                process_part(subpart)

        process_part(payload)
        return attachments

    def _extract_category(self, label_ids: List[str]) -> Optional[str]:
        """Extract Gmail category from labels"""
        category_mappings = {
            "CATEGORY_PERSONAL": "primary",
            "CATEGORY_SOCIAL": "social",
            "CATEGORY_PROMOTIONS": "promotions",
            "CATEGORY_UPDATES": "updates",
            "CATEGORY_FORUMS": "forums",
        }

        for label_id in label_ids:
            if label_id in category_mappings:
                return category_mappings[label_id]

        # Default to primary if no category found and in inbox
        if "INBOX" in label_ids:
            return "primary"

        return None

    def _extract_importance_markers(
        self, headers: Dict[str, str], label_ids: List[str]
    ) -> Dict[str, Any]:
        """Extract importance and priority markers"""
        markers = {
            "is_important": "IMPORTANT" in label_ids,
            "is_starred": "STARRED" in label_ids,
            "priority_header": None,
            "importance_header": None,
            "auto_important": False,
            "user_important": False,
        }

        # Check priority headers
        for priority_header in self.priority_headers:
            if priority_header in headers:
                markers["priority_header"] = headers[priority_header]
                break

        # Check importance header
        if "Importance" in headers:
            markers["importance_header"] = headers["Importance"]

        # Determine if importance was set automatically or by user
        # This would typically require additional API calls to get label history
        markers["auto_important"] = markers["is_important"]  # Simplified

        return markers

    def _extract_thread_info(
        self, headers: Dict[str, str], gmail_message: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Extract thread and conversation information"""
        return {
            "thread_id": gmail_message.get("threadId", ""),
            "message_id_header": headers.get("Message-ID", ""),
            "in_reply_to": headers.get("In-Reply-To"),
            "references": self._extract_references(headers.get("References", "")),
            "thread_index": headers.get("Thread-Index"),
            "thread_topic": headers.get("Thread-Topic"),
            "conversation_id": headers.get("X-Gmail-Conversation-ID"),
            "is_first_message": not bool(headers.get("In-Reply-To")),
        }

    def _extract_references(self, references_header: str) -> List[str]:
        """Extract message references from References header"""
        if not references_header:
            return []

        # References header contains space-separated message IDs
        references = re.findall(r"<([^>]+)>", references_header)
        return references

    def _extract_security_status(
        self, headers: Dict[str, str]
    ) -> tuple[Optional[str], Optional[str], Optional[str]]:
        """Extract SPF, DKIM, and DMARC status"""
        spf_status = None
        dkim_status = None
        dmarc_status = None

        # Parse Authentication-Results header
        auth_results = headers.get("Authentication-Results", "")
        if auth_results:
            # Extract SPF
            spf_match = re.search(r"spf=(\w+)", auth_results, re.IGNORECASE)
            if spf_match:
                spf_status = spf_match.group(1).lower()

            # Extract DKIM
            dkim_match = re.search(r"dkim=(\w+)", auth_results, re.IGNORECASE)
            if dkim_match:
                dkim_status = dkim_match.group(1).lower()

            # Extract DMARC
            dmarc_match = re.search(r"dmarc=(\w+)", auth_results, re.IGNORECASE)
            if dmarc_match:
                dmarc_status = dmarc_match.group(1).lower()

        # Check individual headers as fallback
        if not spf_status and "Received-SPF" in headers:
            spf_result = headers["Received-SPF"].lower()
            if "pass" in spf_result:
                spf_status = "pass"
            elif "fail" in spf_result:
                spf_status = "fail"

        return spf_status, dkim_status, dmarc_status

    def _extract_encryption_info(self, headers: Dict[str, str]) -> Dict[str, Any]:
        """Extract encryption and security information"""
        encryption_info = {
            "tls_encrypted": False,
            "end_to_end_encrypted": False,
            "signed": False,
            "encryption_protocol": None,
        }

        # Check Received headers for TLS information
        received_headers = [v for k, v in headers.items() if k.startswith("Received")]
        for received in received_headers:
            if "TLS" in received or "SSL" in received:
                encryption_info["tls_encrypted"] = True
                # Extract TLS version if available
                tls_match = re.search(r"TLS(\d+\.\d+)", received)
                if tls_match:
                    encryption_info["encryption_protocol"] = f"TLS{tls_match.group(1)}"
                break

        # Check for S/MIME or PGP signatures
        content_type = headers.get("Content-Type", "")
        if "multipart/signed" in content_type:
            encryption_info["signed"] = True
            if "application/pkcs7-signature" in content_type:
                encryption_info["signature_type"] = "S/MIME"
            elif "application/pgp-signature" in content_type:
                encryption_info["signature_type"] = "PGP"

        return encryption_info

    def _extract_priority(self, headers: Dict[str, str]) -> str:
        """Extract message priority"""
        priority_value = None

        # Check various priority headers
        for header_name in self.priority_headers:
            if header_name in headers:
                priority_value = headers[header_name].lower()
                break

        if not priority_value:
            return "normal"

        # Normalize priority values
        if any(keyword in priority_value for keyword in ["high", "urgent", "1"]):
            return "high"
        elif any(keyword in priority_value for keyword in ["low", "5"]):
            return "low"
        else:
            return "normal"

    def _extract_mailing_list_info(self, headers: Dict[str, str]) -> Optional[str]:
        """Extract mailing list information"""
        # Check common mailing list headers
        list_headers = [
            "List-ID",
            "List-Post",
            "List-Unsubscribe",
            "Mailing-List",
            "X-Mailing-List",
        ]

        for header_name in list_headers:
            if header_name in headers:
                list_value = headers[header_name]
                # Extract list name/ID
                if header_name == "List-ID":
                    match = re.search(r"<([^>]+)>", list_value)
                    if match:
                        return match.group(1)
                return list_value

        return None

    def _is_auto_reply(self, headers: Dict[str, str], labels: List[str]) -> bool:
        """Determine if message is an auto-reply"""
        auto_reply_indicators = [
            "Auto-Submitted",
            "X-Auto-Response-Suppress",
            "X-Autorespond",
            "X-Autoreply",
        ]

        # Check auto-reply headers
        for header_name in auto_reply_indicators:
            if header_name in headers:
                value = headers[header_name].lower()
                if "auto-replied" in value or "yes" in value:
                    return True

        # Check subject for auto-reply patterns
        subject = headers.get("Subject", "").lower()
        auto_reply_subjects = [
            "out of office",
            "automatic reply",
            "auto-reply",
            "vacation",
            "away message",
        ]

        return any(pattern in subject for pattern in auto_reply_subjects)

    def _extract_email_address(self, address_header: str) -> str:
        """Extract email address from header value"""
        if not address_header:
            return ""

        # Handle format: "Name <email@domain.com>" or just "email@domain.com"
        email_match = re.search(r"<([^>]+)>", address_header)
        if email_match:
            return email_match.group(1)

        # Direct email address
        email_match = re.search(
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", address_header
        )
        if email_match:
            return email_match.group(0)

        return address_header.strip()

    def _extract_email_addresses(self, addresses_header: str) -> List[str]:
        """Extract multiple email addresses from header value"""
        if not addresses_header:
            return []

        # Split by comma and extract each address
        addresses = []
        for addr in addresses_header.split(","):
            email_addr = self._extract_email_address(addr.strip())
            if email_addr:
                addresses.append(email_addr)

        return addresses

    def _extract_custom_headers(self, headers: Dict[str, str]) -> Dict[str, str]:
        """Extract custom/non-standard headers"""
        standard_headers = {
            "From",
            "To",
            "Cc",
            "Bcc",
            "Subject",
            "Date",
            "Message-ID",
            "In-Reply-To",
            "References",
            "Reply-To",
            "Return-Path",
            "Content-Type",
            "Content-Transfer-Encoding",
            "MIME-Version",
            "Delivered-To",
            "Received",
            "Authentication-Results",
        }

        custom_headers = {}
        for name, value in headers.items():
            if name not in standard_headers and (name.startswith("X-") or name.startswith("x-")):
                custom_headers[name] = value

        return custom_headers

    def _create_minimal_metadata(self, gmail_message: Dict[str, Any]) -> GmailMessage:
        """Create minimal metadata structure when extraction fails"""
        return GmailMessage(
            message_id=gmail_message.get("id", ""),
            thread_id=gmail_message.get("threadId", ""),
            subject="",
            from_address="",
            to_addresses=[],
            cc_addresses=[],
            bcc_addresses=[],
            reply_to=None,
            date="",
            internal_date=gmail_message.get("internalDate", ""),
            body_plain="",
            body_html="",
            snippet=gmail_message.get("snippet", ""),
            labels=[],
            label_ids=gmail_message.get("labelIds", []),
            importance_markers={},
            thread_info={},
            size_estimate=gmail_message.get("sizeEstimate", 0),
            history_id=gmail_message.get("historyId", ""),
            is_unread=False,
            is_starred=False,
            is_important=False,
            is_draft=False,
            is_sent=False,
            is_spam=False,
            is_trash=False,
            is_chat=False,
            attachments=[],
            has_attachments=False,
            spf_status=None,
            dkim_status=None,
            dmarc_status=None,
            encryption_info={},
            message_headers={},
            custom_headers={},
            in_reply_to=None,
            references=[],
            category=None,
            priority="normal",
            auto_reply=False,
            mailing_list=None,
            raw_email=None,
        )

    def extract_batch_metadata(self, gmail_messages: List[Dict[str, Any]]) -> List[GmailMessage]:
        """Extract metadata from multiple messages efficiently"""
        extracted_messages = []

        for message in gmail_messages:
            try:
                metadata = self.extract_complete_metadata(message)
                extracted_messages.append(metadata)
            except Exception as e:
                self.logger.error(
                    f"Failed to extract metadata for message {message.get('id', 'unknown')}: {e}"
                )
                # Include minimal metadata even on failure
                minimal_metadata = self._create_minimal_metadata(message)
                extracted_messages.append(minimal_metadata)

        return extracted_messages

    def to_training_format(self, gmail_message: GmailMessage) -> Dict[str, Any]:
        """Convert Gmail metadata to training data format"""
        return {
            "id": gmail_message.message_id,
            "subject": gmail_message.subject,
            "content": gmail_message.body_plain or gmail_message.snippet,
            "sender": gmail_message.from_address,
            "sender_email": gmail_message.from_address,
            "timestamp": gmail_message.date,
            "labels": gmail_message.labels,
            "is_important": gmail_message.is_important,
            "is_starred": gmail_message.is_starred,
            "is_unread": gmail_message.is_unread,
            "category": gmail_message.category,
            "priority": gmail_message.priority,
            "has_attachments": gmail_message.has_attachments,
            "thread_id": gmail_message.thread_id,
            "auto_reply": gmail_message.auto_reply,
            "mailing_list": gmail_message.mailing_list,
            "security_status": {
                "spf": gmail_message.spf_status,
                "dkim": gmail_message.dkim_status,
                "dmarc": gmail_message.dmarc_status,
            },
            "metadata": {
                "size": gmail_message.size_estimate,
                "encryption": gmail_message.encryption_info,
                "custom_headers": gmail_message.custom_headers,
                "importance_markers": gmail_message.importance_markers,
            },
        }


def main():
    """Example usage of Gmail metadata extractor"""
    extractor = GmailMetadataExtractor()

    # Example Gmail API message response
    sample_message = {
        "id": "msg_123456789",
        "threadId": "thread_123456789",
        "labelIds": ["INBOX", "IMPORTANT", "CATEGORY_PERSONAL"],
        "snippet": "This is a sample email message...",
        "sizeEstimate": 2048,
        "historyId": "987654321",
        "internalDate": "1640995200000",
        "payload": {
            "headers": [
                {"name": "From", "value": "John Doe <john@example.com>"},
                {"name": "To", "value": "jane@example.com"},
                {"name": "Subject", "value": "Important Project Update"},
                {"name": "Date", "value": "Fri, 31 Dec 2021 12:00:00 +0000"},
                {"name": "Message-ID", "value": "<unique-id@example.com>"},
                {"name": "X-Priority", "value": "High"},
            ],
            "body": {"data": base64.urlsafe_b64encode(b"This is the email content.").decode()},
            "mimeType": "text/plain",
        },
    }

    # Extract metadata
    metadata = extractor.extract_complete_metadata(sample_message)

    print(f"Message ID: {metadata.message_id}")
    print(f"Subject: {metadata.subject}")
    print(f"From: {metadata.from_address}")
    print(f"Important: {metadata.is_important}")
    print(f"Category: {metadata.category}")
    print(f"Priority: {metadata.priority}")
    print(f"Labels: {metadata.labels}")

    # Convert to training format
    training_data = extractor.to_training_format(metadata)
    print(f"Training format: {json.dumps(training_data, indent=2)}")


if __name__ == "__main__":
    main()
