import tempfile
import unittest
from pathlib import Path

from core.forensics import evaluate_forensic_threat_matrix
from core.parser import parse_email_evidence
from core.rule_gen import export_threat_rules


class RuleExportRegressionTests(unittest.TestCase):
    def test_export_paths_match_gui_consumers(self):
        evidence = parse_email_evidence(
            b"From: sender@example.test\nSubject: Test\n\nBody\n",
            filename="test.eml",
        )
        threat = evaluate_forensic_threat_matrix(evidence)
        with tempfile.TemporaryDirectory() as tmp:
            result = export_threat_rules(evidence, threat, tmp)
            self.assertEqual(set(result), {"yara", "snort", "stix"})
            for path in result.values():
                self.assertTrue(Path(path).is_file())


if __name__ == "__main__":
    unittest.main()
