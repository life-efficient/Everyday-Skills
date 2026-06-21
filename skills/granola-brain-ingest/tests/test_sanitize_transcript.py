import pathlib
import sys
import unittest


SCRIPT_DIR = pathlib.Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

import sanitize_transcript  # noqa: E402


class SanitizeTranscriptTests(unittest.TestCase):
    def test_redacts_banned_sentences(self):
        text = "We agreed on the launch plan. That is bullshit. The next step is a demo."
        sanitized, counts = sanitize_transcript.sanitize(text)

        self.assertIn("We agreed on the launch plan.", sanitized)
        self.assertIn("[redacted: profanity]", sanitized)
        self.assertIn("The next step is a demo.", sanitized)
        self.assertNotIn("bullshit", sanitized.lower())
        self.assertEqual(counts["profanity"], 1)

    def test_collapses_adjacent_identical_redactions(self):
        text = "This is stupid. What an idiot. Continue with procurement."
        sanitized, counts = sanitize_transcript.sanitize(text)

        self.assertEqual(sanitized.count("[redacted: insult]"), 1)
        self.assertIn("Continue with procurement.", sanitized)
        self.assertEqual(counts["insult"], 2)


if __name__ == "__main__":
    unittest.main()
