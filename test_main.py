import os
import tempfile
import unittest

import main

EXPECTED = "The incident is resolved. I deleted the dashboard that said there was one."


class WritesEntry(unittest.TestCase):
    def test_writes_the_excuse_to_entry_txt(self):
        with tempfile.TemporaryDirectory() as tmp:
            out_dir = os.path.join(tmp, "output")  # does not exist yet
            returned = main.main(out_dir)
            with open(os.path.join(out_dir, "entry.txt"), "rb") as f:
                raw = f.read()
            text = raw.decode("utf-8")
            self.assertEqual(text, EXPECTED)
            self.assertEqual(returned, EXPECTED)

    def test_entry_meets_the_gate(self):
        with tempfile.TemporaryDirectory() as tmp:
            main.main(tmp)
            with open(os.path.join(tmp, "entry.txt"), "rb") as f:
                text = f.read().decode("utf-8")
        self.assertEqual(len(text), 74)
        self.assertTrue(1 <= len(text) <= 200)
        self.assertEqual(text.strip(), text)
        self.assertNotIn("\n", text)
        self.assertTrue(text.isascii())


if __name__ == "__main__":
    unittest.main()
