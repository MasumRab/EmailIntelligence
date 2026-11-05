"""Laziness of ``_EmailContext`` in ``src.core.smart_filter_manager``.

``_EmailContext`` exists so the filter-application loop does not recompute the
lowercased subject, body and sender for every filter. Subject and body were
made lazy earlier; the sender was not, so both construction sites still
lowercased it eagerly and handed it in — an email whose active filters never
look at the sender paid for ``.lower()`` on every application anyway.

That last step is easy to lose silently: an eager sender passes every existing
test in this module, because those tests assert on the *values* the context
exposes, never on how many of them were produced. These tests assert on reads.
Before the change they fail on the constructor signature itself — a caller was
not allowed to leave the sender uncomputed.
"""

from __future__ import annotations

from typing import Any

import pytest

from src.core.smart_filter_manager import _EmailContext


class RecordingEmail(dict):
    """A dict that records which keys were read through ``.get()``."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.reads: list[str] = []

    def get(self, key: str, default: Any = None) -> Any:
        self.reads.append(key)
        return super().get(key, default)


@pytest.fixture
def email() -> RecordingEmail:
    return RecordingEmail(
        {
            "subject": "Quarterly Report",
            "content": "The body text everyone would rather not lowercase.",
            "sender_email": "Alice@Example.COM",
        }
    )


def test_reading_the_subject_does_not_touch_the_body(email: RecordingEmail) -> None:
    context = _EmailContext(email=email, sender_domain="example.com")

    assert context.subject_lower == "quarterly report"
    assert "content" not in email.reads
    assert "body" not in email.reads


def test_reading_the_sender_does_not_touch_the_subject_or_body(email: RecordingEmail) -> None:
    context = _EmailContext(email=email, sender_domain="example.com")

    assert context.sender_lower == "alice@example.com"
    assert "subject" not in email.reads
    assert "content" not in email.reads
    assert "body" not in email.reads


def test_each_field_is_computed_at_most_once(email: RecordingEmail) -> None:
    context = _EmailContext(email=email, sender_domain="example.com")

    assert context.content_lower == context.content_lower
    assert email.reads.count("content") == 1


def test_the_body_falls_back_to_the_legacy_key(email: RecordingEmail) -> None:
    legacy = RecordingEmail({"body": "Legacy Field", "sender": "bob@example.com"})
    context = _EmailContext(email=legacy, sender_domain="example.com")

    assert context.content_lower == "legacy field"
    assert context.sender_lower == "bob@example.com"


def test_the_sender_domain_is_the_one_it_was_given(email: RecordingEmail) -> None:
    """The manager computes the domain once; the context must not recompute it."""
    context = _EmailContext(email=email, sender_domain="example.com")

    assert context.sender_domain == "example.com"
