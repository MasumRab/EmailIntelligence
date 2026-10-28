import unittest

from backend.python_nlp.ai_training import PromptEngineer


class TestPromptEngineer(unittest.TestCase):

    def test_fill(self):
        template = "Hello, {name}!"
        engineer = PromptEngineer(template)
        prompt = engineer.fill(name="World")
        self.assertEqual(prompt, "Hello, World!")

    def test_fill_multiple(self):
        template = "The {animal} says {sound}."
        engineer = PromptEngineer(template)
        prompt = engineer.fill(animal="cat", sound="meow")
        self.assertEqual(prompt, "The cat says meow.")

    def test_execute(self):
        template = "This is a {test}."
        engineer = PromptEngineer(template)
        result = engineer.execute(test="placeholder")
        self.assertEqual(result, "Executing prompt: This is a placeholder.")


if __name__ == "__main__":
    unittest.main()
