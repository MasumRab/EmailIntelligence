import unittest
from modules.new_ui.utils import sanitize_html

class TestSanitizer(unittest.TestCase):
    def test_unclosed_script(self):
        html = "<div>hi<script>alert(1)</div>"
        self.assertEqual(sanitize_html(html), "<div>hi</div>")

    def test_script_whitespace(self):
        html = "<script >alert(1)</script >"
        self.assertEqual(sanitize_html(html), "")
        
    def test_unquoted_handler(self):
        html = "<img src=x onerror=alert(1)>"
        self.assertEqual(sanitize_html(html), "")

    def test_javascript_href(self):
        html = "<a href=\"javascript:alert(1)\">click</a>"
        self.assertEqual(sanitize_html(html), "<a>click</a>")

    def test_nested_uppercase(self):
        html = "<ScRiPt><script>alert(1)</script></sCrIpT>"
        self.assertEqual(sanitize_html(html), "")

    def test_regression_img_bypass(self):
        html = "<img src=\"x&quot; onerror=alert(1)\">"
        self.assertEqual(sanitize_html(html), "")

    def test_regression_meta_refresh(self):
        html = "<meta http-equiv=\"refresh\" content=\"0;url=javascript:alert(1)\">"
        self.assertEqual(sanitize_html(html), "")

    def test_regression_iframe_src(self):
        html = "<iframe src=\"javascript:alert(1)\"></iframe>"
        self.assertEqual(sanitize_html(html), "")

    def test_regression_form_action(self):
        html = "<form action=\"javascript:alert(1)\"><input></form>"
        self.assertEqual(sanitize_html(html), "")

    def test_regression_object_data(self):
        html = "<object data=\"javascript:alert(1)\"></object>"
        self.assertEqual(sanitize_html(html), "")

    def test_regression_svg_xlink(self):
        html = "<svg><a xlink:href=\"javascript:alert(1)\"><text>c</text></a></svg>"
        self.assertEqual(sanitize_html(html), "<a>c</a>")

    def test_regression_style_background(self):
        html = "<div style=\"background:url(javascript:alert(1))\">x</div>"
        self.assertEqual(sanitize_html(html), "<div>x</div>")

    def test_unterminated_entity(self):
        self.assertEqual(sanitize_html("a &am"), "a &amp;am")
        self.assertEqual(sanitize_html("<p>ok</p> &am"), "<p>ok</p> &amp;am")
        self.assertEqual(sanitize_html("x <b>y</b> z &am"), "x <b>y</b> z &amp;am")

    def test_benign_markup(self):
        html = "<div><p>Hello <b>World</b></p></div>"
        self.assertEqual(sanitize_html(html), html)

    def test_benign_attributes(self):
        html = "<div class=\"foo\" id=\"bar\">baz</div>"
        self.assertEqual(sanitize_html(html), html)

if __name__ == '__main__':
    unittest.main()
