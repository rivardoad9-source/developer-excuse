import os
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

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


class RefusesBadText(unittest.TestCase):
    def check_refused(self, bad):
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.object(main, "EXCUSE", bad):
                with self.assertRaises(ValueError):
                    main.main(tmp)
            self.assertFalse(os.path.exists(os.path.join(tmp, "entry.txt")))

    def test_refuses_empty_text(self):
        self.check_refused("")

    def test_refuses_text_over_200_chars(self):
        self.check_refused("x" * 201)

    def test_refuses_newline(self):
        self.check_refused("one\ntwo")

    def test_refuses_non_ascii(self):
        self.check_refused("café")

    def test_refuses_surrounding_whitespace(self):
        self.check_refused(" padded ")


class CommandLine(unittest.TestCase):
    def test_script_takes_output_dir_as_first_argument(self):
        with tempfile.TemporaryDirectory() as tmp:
            here = os.path.dirname(os.path.abspath(main.__file__))
            subprocess.run(
                [sys.executable, os.path.join(here, "main.py"), tmp], check=True
            )
            with open(os.path.join(tmp, "entry.txt"), "rb") as f:
                self.assertEqual(f.read().decode("utf-8"), EXPECTED)


if __name__ == "__main__":
    unittest.main()
