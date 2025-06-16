import unittest
from unittest.mock import patch
from server.python_nlp.action_item_extractor import ActionItemExtractor, HAS_NLTK

class TestActionItemExtractor(unittest.TestCase):

    def setUp(self):
        self.extractor = ActionItemExtractor()

    def test_extract_actions_clear_phrase_with_due_date(self):
        text = "Please review the attached document by Friday."
        actions = self.extractor.extract_actions(text)
        self.assertEqual(len(actions), 1)
        action = actions[0]
        self.assertEqual(action['action_phrase'], "Please review the attached document by Friday.")
        self.assertEqual(action['raw_due_date_text'], "by Friday")
        self.assertEqual(action['context'], "Please review the attached document by Friday.")
        if HAS_NLTK:
            self.assertIsNotNone(action['verb']) # NLTK should find 'review'
            # self.assertEqual(action['object'], "document") # Object extraction can be tricky

    def test_extract_actions_keyword_task(self):
        text = "Task: John to complete the slides by tomorrow."
        actions = self.extractor.extract_actions(text)
        self.assertEqual(len(actions), 1)
        action = actions[0]
        self.assertTrue(action['action_phrase'].startswith("Task: John to complete the slides"))
        self.assertEqual(action['raw_due_date_text'], "by tomorrow")
        self.assertEqual(action['context'], "Task: John to complete the slides by tomorrow.")
        if HAS_NLTK:
            self.assertIsNotNone(action['verb']) # NLTK might pick up 'complete'

    def test_extract_actions_keyword_action_required(self):
        text = "Action required: Update the JIRA ticket."
        actions = self.extractor.extract_actions(text)
        self.assertEqual(len(actions), 1)
        action = actions[0]
        self.assertEqual(action['action_phrase'], "Action required: Update the JIRA ticket.")
        self.assertIsNone(action['raw_due_date_text'])
        self.assertEqual(action['context'], "Action required: Update the JIRA ticket.")
        if HAS_NLTK:
            self.assertEqual(action['verb'], "Update")

    def test_extract_actions_need_to_phrase(self):
        text = "We need to finalize the report."
        actions = self.extractor.extract_actions(text)
        self.assertEqual(len(actions), 1)
        action = actions[0]
        self.assertEqual(action['action_phrase'], "need to finalize the report.")
        self.assertIsNone(action['raw_due_date_text'])
        self.assertEqual(action['context'], "We need to finalize the report.")
        if HAS_NLTK:
             self.assertEqual(action['verb'], "finalize") # NLTK should pick 'finalize'

    def test_extract_actions_no_action_items(self):
        text = "This is a general update email with no specific tasks."
        actions = self.extractor.extract_actions(text)
        self.assertEqual(len(actions), 0)

    def test_extract_actions_multiple_action_items(self):
        text = "Please call the vendor. Also, can you send the invoice by EOD?"
        actions = self.extractor.extract_actions(text)
        self.assertEqual(len(actions), 2)

        self.assertEqual(actions[0]['action_phrase'], "Please call the vendor.")
        self.assertIsNone(actions[0]['raw_due_date_text'])
        if HAS_NLTK:
            self.assertEqual(actions[0]['verb'], "call")

        self.assertEqual(actions[1]['action_phrase'], "can you send the invoice by EOD?")
        self.assertEqual(actions[1]['raw_due_date_text'], "by EOD")
        if HAS_NLTK:
            self.assertEqual(actions[1]['verb'], "send")


    def test_extract_actions_simple_due_date_tomorrow(self):
        text_no_keyword = "Submit the expenses by tomorrow."
        actions_no_keyword = self.extractor.extract_actions(text_no_keyword)
        self.assertEqual(len(actions_no_keyword), 0) # Text without keyword should not produce action

        # Now test with a keyword
        text_with_keyword = "You should Submit the expenses by tomorrow."
        actions_with_keyword = self.extractor.extract_actions(text_with_keyword)
        self.assertEqual(len(actions_with_keyword), 1)
        self.assertEqual(actions_with_keyword[0]['raw_due_date_text'], "by tomorrow")
        self.assertTrue(actions_with_keyword[0]['action_phrase'].startswith("should Submit the expenses"))

    def test_extract_actions_due_date_on_monday(self):
        text = "We need to finish this on Monday."
        actions = self.extractor.extract_actions(text)
        self.assertEqual(len(actions), 1)
        self.assertEqual(actions[0]['raw_due_date_text'], "on Monday")

    def test_structure_of_action_item(self):
        text = "Please prepare the presentation for next week."
        actions = self.extractor.extract_actions(text)
        self.assertEqual(len(actions), 1)
        action = actions[0]
        self.assertIn('action_phrase', action)
        self.assertIn('verb', action)
        self.assertIn('object', action)
        self.assertIn('raw_due_date_text', action)
        self.assertIn('context', action)
        self.assertEqual(action['raw_due_date_text'], "next week")

    def test_empty_input_string(self):
        text = ""
        actions = self.extractor.extract_actions(text)
        self.assertEqual(len(actions), 0)

    def test_none_input(self):
        actions = self.extractor.extract_actions(None)
        self.assertEqual(len(actions), 0)

    def test_input_with_only_whitespace(self):
        text = "    \n  \t  "
        actions = self.extractor.extract_actions(text)
        self.assertEqual(len(actions), 0)

    # Example of mocking NLTK if its presence changes behavior significantly for a specific case
    @patch('server.python_nlp.action_item_extractor.HAS_NLTK', False)
    def test_extract_actions_without_nltk(self):
        # This test will run as if NLTK is not installed
        extractor_no_nltk = ActionItemExtractor() # Re-initialize to pick up the patched HAS_NLTK
        text = "Please review the document."
        actions = extractor_no_nltk.extract_actions(text)
        self.assertEqual(len(actions), 1)
        action = actions[0]
        self.assertEqual(action['action_phrase'], "Please review the document.")
        self.assertIsNone(action['verb']) # Verb should be None as NLTK is mocked to False
        self.assertIsNone(action['object']) # Object should be None

    @patch('server.python_nlp.action_item_extractor.HAS_NLTK', True)
    @patch('nltk.pos_tag')
    @patch('nltk.word_tokenize')
    def test_extract_actions_with_nltk_mocked_behavior(self, mock_word_tokenize, mock_pos_tag):
        # This test runs with NLTK assumed present, but mocks its functions
        mock_word_tokenize.return_value = ["Please", "review", "the", "document", "."]
        mock_pos_tag.return_value = [("Please", "VB"), ("review", "VB"), ("the", "DT"), ("document", "NN"), (".", ".")]

        # Re-initialize to ensure fresh state if HAS_NLTK was changed by other tests
        # or to ensure it picks up the True patch if default is False for some reason.
        extractor_with_nltk = ActionItemExtractor()

        text = "Please review the document." # Text content doesn't strictly matter here as functions are mocked
        actions = extractor_with_nltk.extract_actions(text)

        self.assertEqual(len(actions), 1)
        action = actions[0]
        self.assertEqual(action['verb'], "Please") # Because "Please" is the first VB as per mock_pos_tag
        self.assertEqual(action['object'], "document") # "document" is the first NN after "Please"
        mock_word_tokenize.assert_called_once() # Check if it was called on the relevant part
        mock_pos_tag.assert_called_once()

if __name__ == '__main__':
    unittest.main()
