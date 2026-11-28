import unittest
import os
from backend.node_engine.security_manager import InputSanitizer

class TestInputSanitizerEnhanced(unittest.TestCase):
    def test_sanitize_markdown(self):
        # Test basic markdown
        markdown = "# Header\n\n* List item 1\n* List item 2"
        self.assertEqual(InputSanitizer.sanitize_markdown(markdown), markdown)

        # Test embedded HTML script
        unsafe = "# Header <script>alert(1)</script>"
        sanitized = InputSanitizer.sanitize_markdown(unsafe)
        self.assertNotIn("<script>", sanitized)
        # bleach with strip=True removes the tag but keeps content for many tags,
        # but for script/style it usually removes content too if configured?
        # In this environment, it seems to keep content 'alert(1)'.
        # The key is that the script TAG is gone.

        # Test dangerous link
        unsafe_link = "[Click me](javascript:alert(1))"
        sanitized_link = InputSanitizer.sanitize_markdown(unsafe_link)
        self.assertIn("unsafe-link:javascript", sanitized_link)

        # Test dangerous link with data URI
        unsafe_data = "[Download](data:text/html;base64,...)"
        sanitized_data = InputSanitizer.sanitize_markdown(unsafe_data)
        self.assertIn("unsafe-link:data", sanitized_data)

    def test_sanitize_csv(self):
        # Test normal
        self.assertEqual(InputSanitizer.sanitize_csv("hello"), "hello")
        self.assertEqual(InputSanitizer.sanitize_csv("123"), "123")

        # Test injections
        self.assertEqual(InputSanitizer.sanitize_csv("=1+1"), "'=1+1")
        self.assertEqual(InputSanitizer.sanitize_csv("+1+1"), "'+1+1")
        self.assertEqual(InputSanitizer.sanitize_csv("-1+1"), "'-1+1")
        self.assertEqual(InputSanitizer.sanitize_csv("@SUM(1,2)"), "'@SUM(1,2)")

    def test_sanitize_xml(self):
        # Test basic XML
        xml = "<root><child>value</child></root>"
        sanitized = InputSanitizer.sanitize_xml(xml)
        self.assertTrue("<root" in sanitized)
        self.assertTrue("child" in sanitized)

        # Test malformed XML
        with self.assertRaises(ValueError):
            InputSanitizer.sanitize_xml("<root><unclosed>")

        # Test XXE attempt
        xxe = """<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]><root>&xxe;</root>"""
        # Should raise ValueError (or subclass EntitiesForbidden/DTDForbidden)
        with self.assertRaises(ValueError):
             InputSanitizer.sanitize_xml(xxe)

    def test_sanitize_xml_schema(self):
        # Create a temporary schema
        schema_content = """<?xml version="1.0"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
<xs:element name="note">
  <xs:complexType>
    <xs:sequence>
      <xs:element name="to" type="xs:string"/>
      <xs:element name="from" type="xs:string"/>
    </xs:sequence>
  </xs:complexType>
</xs:element>
</xs:schema>"""

        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write(schema_content)
            schema_path = f.name

        try:
            valid_xml = "<note><to>Tove</to><from>Jani</from></note>"
            sanitized = InputSanitizer.sanitize_xml(valid_xml, schema_path=schema_path)
            self.assertTrue("note" in sanitized)

            invalid_xml = "<note><to>Tove</to></note>" # Missing 'from'
            with self.assertRaises(ValueError) as cm:
                InputSanitizer.sanitize_xml(invalid_xml, schema_path=schema_path)
            self.assertIn("XML validation failed", str(cm.exception))

        finally:
            os.unlink(schema_path)

if __name__ == '__main__':
    unittest.main()
