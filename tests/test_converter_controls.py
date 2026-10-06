import importlib.util
import json
from pathlib import Path
import unittest

# Load the actual converter without importing the GUI and network entry points.
spec = importlib.util.spec_from_file_location("converter", Path(__file__).resolve().parents[1] / "source/expansion/converter.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
Converter = module.Converter


class ConverterControlTests(unittest.TestCase):
    def convert(self, data):
        return Converter._convert_object("window.__INITIAL_STATE__=" + json.dumps(data, ensure_ascii=False))

    def test_exact_u0083_reproduction(self):
        self.assertEqual(self.convert({"nickname": "test\u0083name"}), {"nickname": "testname"})

    def test_all_disallowed_c1_controls(self):
        for codepoint in [*range(0x7f, 0x85), *range(0x86, 0xa0)]:
            with self.subTest(codepoint=codepoint):
                self.assertEqual(self.convert({"nickname": "a" + chr(codepoint) + "b"}), {"nickname": "ab"})

    def test_allowed_whitespace_and_nel_are_not_removed(self):
        value = "\t\n\r\x85"
        self.assertEqual(Converter.YAML_ILLEGAL.sub("", value), value)

    def test_unicode_and_escaped_controls_keep_previous_behavior(self):
        data = {"nickname": "中文🌸", "desc": "line\nnext\tcolumn"}
        self.assertEqual(self.convert(data), data)
        self.assertEqual(self.convert({"nickname": r"test\u0083name"}), {"nickname": r"test\u0083name"})

    def test_pc_html_path_with_bad_nickname(self):
        state = {"note": {"noteDetailMap": {"id": {"note": {"nickname": "a\x83b"}}}}}
        html = "<html><script>window.__INITIAL_STATE__=" + json.dumps(state, ensure_ascii=False) + "</script></html>"
        self.assertEqual(Converter().run(html), {"nickname": "ab"})

    def test_phone_html_path_with_bad_description(self):
        state = {"noteData": {"data": {"noteData": {"desc": "a\x9fb"}}}}
        html = "<html><script>window.__INITIAL_STATE__=" + json.dumps(state, ensure_ascii=False) + "</script></html>"
        self.assertEqual(Converter().run(html), {"desc": "ab"})

    def test_javascript_sentinels_keep_previous_behavior(self):
        self.assertEqual(Converter._convert_object('window.__INITIAL_STATE__={"items":new Map([]),"value":undefined}'), {"items": [], "value": None})


if __name__ == "__main__":
    unittest.main()
