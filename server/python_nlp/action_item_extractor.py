import re
import logging
from typing import List, Dict, Any, Optional

# Attempt to import NLTK for POS tagging
try:
    import nltk
    # Ensure necessary NLTK data is available, if not, download it.
    # This is more for a local setup; in a container, it should be pre-installed.
    try:
        nltk.data.find('taggers/averaged_perceptron_tagger')
    except nltk.downloader.ErrorMessage:
        nltk.download('averaged_perceptron_tagger', quiet=True)
    try:
        nltk.data.find('tokenizers/punkt')
    except nltk.downloader.ErrorMessage:
        nltk.download('punkt', quiet=True)
    HAS_NLTK = True
except ImportError:
    HAS_NLTK = False

logger = logging.getLogger(__name__)

class ActionItemExtractor:
    """
    Extracts potential action items from text using rule-based logic
    and optional NLTK POS tagging.
    """

    def __init__(self):
        # Regex for keywords indicating action items
        self.action_keywords_regex = re.compile(
            r'\b(please|task:|action:|need to|required to|must|should|can you|could you|will you)\b',
            re.IGNORECASE
        )
        # Regex for simple due date patterns
        # This is a basic version and can be expanded significantly
        self.due_date_regex = re.compile(
            r'\b(by (next )?(monday|tuesday|wednesday|thursday|friday|saturday|sunday|tomorrow|end of day|eod)|'
            r'on \d{1,2}(st|nd|rd|th)? (jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)(\w*)?(\s\d{4})?|'
            r'in \d+ (days?|weeks?|months?)|'
            r'next (week|month|year))\b',
            re.IGNORECASE
        )
        self.sentence_splitter_regex = re.compile(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s')

        if HAS_NLTK:
            logger.info("NLTK found. POS tagging will be available for action item extraction.")
        else:
            logger.warning("NLTK not found. Action item extraction will rely solely on regex and keyword spotting.")

    def _extract_verb_object_with_nltk(self, text: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Extracts verb and object from a phrase using NLTK POS tagging.
        This is a simplified approach.
        """
        if not HAS_NLTK:
            return None, None
        try:
            tokens = nltk.word_tokenize(text)
            tagged_tokens = nltk.pos_tag(tokens)

            verb = None
            obj = None

            # Find first verb
            for token, tag in tagged_tokens:
                if tag.startswith('VB'): # VB, VBP, VBZ, VBG, VBD, VBN
                    verb = token
                    break

            # Find first noun or pronoun after the verb as a simple object
            if verb:
                verb_index = tokens.index(verb)
                for i in range(verb_index + 1, len(tagged_tokens)):
                    token, tag = tagged_tokens[i]
                    if tag.startswith('NN') or tag.startswith('PRP'): # Noun or Pronoun
                        obj = token
                        break
            return verb, obj
        except Exception as e:
            logger.error(f"Error during NLTK POS tagging or verb/object extraction: {e}")
            return None, None

    def extract_actions(self, text: str) -> List[Dict[str, Any]]:
        """
        Extracts action items from the given text.
        """
        action_items: List[Dict[str, Any]] = []
        if not text or not isinstance(text, str):
            return action_items

        # Split text into sentences to provide context
        # Using a simple regex for sentence splitting, can be improved with NLTK's sent_tokenize
        sentences = self.sentence_splitter_regex.split(text)

        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue

            match = self.action_keywords_regex.search(sentence)
            if match:
                action_phrase = sentence[match.start():] # Capture from keyword onwards as a starting point

                # Refine action_phrase to be more specific if possible
                # For example, stop at the end of the clause or sentence.
                # This is a simplification; more advanced parsing would be better.

                verb, obj = None, None
                if HAS_NLTK:
                    # Try to get a more specific part of the sentence for verb/object extraction
                    # This could be the text following the keyword.
                    potential_action_segment = sentence[match.end():].strip()
                    verb, obj = self._extract_verb_object_with_nltk(potential_action_segment)

                due_date_match = self.due_date_regex.search(action_phrase)
                raw_due_date_text = None
                if due_date_match:
                    raw_due_date_text = due_date_match.group(0).strip()
                    # Optionally, remove due date from action phrase to avoid redundancy
                    # action_phrase = action_phrase.replace(raw_due_date_text, "").strip()


                action_item: Dict[str, Any] = {
                    'action_phrase': action_phrase.strip(),
                    'verb': verb,
                    'object': obj,
                    'raw_due_date_text': raw_due_date_text,
                    'context': sentence.strip() # The full sentence as context
                }
                action_items.append(action_item)
                logger.debug(f"Extracted action item: {action_item}")

        logger.info(f"Extracted {len(action_items)} potential action items.")
        return action_items

if __name__ == '__main__':
    # Example Usage
    logging.basicConfig(level=logging.DEBUG)
    extractor = ActionItemExtractor()

    test_text_1 = "Please submit the report by Friday. We also need to review the budget. Can you schedule a meeting?"
    test_text_2 = "Action: John to complete the slides. Task: Maria to send out invites by tomorrow. Required to update the JIRA ticket."
    test_text_3 = "No actions here, just a general update."
    test_text_4 = "Could you please finalize the presentation by next Monday? Also, will you call the vendor?"

    print("\n--- Test Text 1 ---")
    actions1 = extractor.extract_actions(test_text_1)
    for action in actions1:
        print(action)

    print("\n--- Test Text 2 ---")
    actions2 = extractor.extract_actions(test_text_2)
    for action in actions2:
        print(action)

    print("\n--- Test Text 3 ---")
    actions3 = extractor.extract_actions(test_text_3)
    for action in actions3:
        print(action)

    print("\n--- Test Text 4 ---")
    actions4 = extractor.extract_actions(test_text_4)
    for action in actions4:
        print(action)

    if HAS_NLTK:
        print("\nNLTK was used.")
    else:
        print("\nNLTK was NOT used.")
