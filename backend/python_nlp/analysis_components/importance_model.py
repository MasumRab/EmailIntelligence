"""
A simple, placeholder model for identifying important emails.
"""

class ImportanceModel:
    """
    A placeholder model that uses keyword matching to determine if an email is important.
    """
    def __init__(self):
        self.important_keywords = ["urgent", "important", "action required", "asap"]

    def analyze(self, text: str) -> dict:
        """
        Analyzes the text for important keywords.
        """
        is_important = False
        for keyword in self.important_keywords:
            if keyword in text.lower():
                is_important = True
                break

        return {
            "is_important": is_important,
            "confidence": 0.9 if is_important else 0.5,
            "method_used": "keyword_matching"
        }
