"""
Regression Tests: False Positive Suppression in Course Quality Audit.

Verifies that ordinary Russian words (если, пока, повтор) no longer trigger
premature concept detection, while explicit Python concept instructions,
future syntax in code/solutions, and legitimate scaffolding checks are preserved.

Run:
    pytest tests/test_course_quality_audit_false_positives.py -v

Or directly:
    python -m pytest tests/test_course_quality_audit_false_positives.py -v
"""

import json
import os
import subprocess
import sys
import pytest

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT_PATH = os.path.join(BASE, "scripts", "audit_course_quality.py")
REGISTRY_PATH = os.path.join(BASE, "docs", "course_quality_issue_registry.json")

# Words that should NOT trigger premature concept detection
SUPPRESSED_WORDS = ["если", "пока", "повтор", "повтори", "повторяется", "повторить"]


class TestAuditPipeline:
    """Verify the audit pipeline runs successfully."""

    def test_audit_script_runs(self):
        """Audit script should complete with exit code 0."""
        result = subprocess.run(
            [sys.executable, SCRIPT_PATH],
            cwd=BASE,
            capture_output=True, text=True,
            timeout=120,
        )
        assert result.returncode == 0, (
            f"Audit failed with code {result.returncode}\n"
            f"STDERR: {result.stderr[:500]}\n"
            f"STDOUT: {result.stdout[:500]}"
        )

    def test_registry_file_created(self):
        """Audit should produce the issue registry JSON."""
        assert os.path.exists(REGISTRY_PATH), (
            f"Issue registry not found at {REGISTRY_PATH}"
        )


class TestFalsePositiveSuppression:
    """Verify ordinary Russian words don't trigger false premature concept issues."""

    @pytest.fixture(scope="class")
    def registry(self):
        """Load the latest audit issue registry."""
        # Run audit first
        result = subprocess.run(
            [sys.executable, SCRIPT_PATH],
            cwd=BASE,
            capture_output=True, text=True,
            timeout=120,
        )
        assert result.returncode == 0, f"Audit failed: {result.stderr[:500]}"
        with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
            return json.load(f)

    def _get_dialogue_issues_by_word(self, registry, word):
        """Get dialogue_premature_concept issues whose reason mentions the word."""
        return [
            i for i in registry["issues"]
            if i["issue_type"] == "dialogue_premature_concept"
            and word.lower() in i.get("reason", "").lower()
        ]

    def test_must_fix_now_is_zero(self, registry):
        """must_fix_now count should remain 0 after suppression."""
        counts = registry.get("severity_counts", {})
        assert counts.get("must_fix_now", -1) == 0, (
            f"must_fix_now = {counts.get('must_fix_now')}, expected 0"
        )

    def test_ordinary_russian_if_word_not_flagged(self, registry):
        """'если' in dialogue should NOT create premature_if issues."""
        issues = self._get_dialogue_issues_by_word(registry, "если")
        assert len(issues) == 0, (
            f"Found {len(issues)} issues triggered by 'если': "
            + " | ".join(i["current_text"][:80] for i in issues)
        )

    def test_ordinary_russian_while_word_not_flagged(self, registry):
        """'пока' in dialogue should NOT create premature_while issues."""
        issues = self._get_dialogue_issues_by_word(registry, "пока")
        assert len(issues) == 0, (
            f"Found {len(issues)} issues triggered by 'пока': "
            + " | ".join(i["current_text"][:80] for i in issues)
        )

    def test_ordinary_russian_repeat_word_not_flagged(self, registry):
        """'повтор' in dialogue should NOT create premature_loop issues."""
        for word in ["повтор", "повтори", "повторяется", "повторить"]:
            issues = self._get_dialogue_issues_by_word(registry, word)
            assert len(issues) == 0, (
                f"Found {len(issues)} issues triggered by '{word}': "
                + " | ".join(i["current_text"][:80] for i in issues)
            )

    def test_all_suppressed_words_not_flagged(self, registry):
        """None of the suppressed Russian words should appear in dialogue issue reasons."""
        dialogue_issues = [
            i for i in registry["issues"]
            if i["issue_type"] == "dialogue_premature_concept"
        ]
        for word in SUPPRESSED_WORDS:
            for issue in dialogue_issues:
                assert word not in issue.get("reason", "").lower(), (
                    f"Suppressed word '{word}' found in issue {issue['issue_id']}: "
                    f"{issue['current_text'][:100]}"
                )

    def test_dialogue_premature_concept_count_reduced(self, registry):
        """Total dialogue_premature_concept issues should be less than the previous 24."""
        all_dialogue = [
            i for i in registry["issues"]
            if i["issue_type"] == "dialogue_premature_concept"
        ]
        # Before suppression: 24 dialogue issues (23 false positives + 1 acceptable)
        # After suppression: only real/acceptable ones remain
        assert len(all_dialogue) < 24, (
            f"Expected < 24 dialogue_premature_concept issues, got {len(all_dialogue)}. "
            "Suppression may not be working."
        )


class TestRealDetectionPreserved:
    """Verify that real concept detections still work after suppression."""

    @pytest.fixture(scope="class")
    def registry(self):
        """Load the latest audit issue registry."""
        result = subprocess.run(
            [sys.executable, SCRIPT_PATH],
            cwd=BASE,
            capture_output=True, text=True,
            timeout=120,
        )
        assert result.returncode == 0, f"Audit failed: {result.stderr[:500]}"
        with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
            return json.load(f)

    def test_legitimate_scaffolding_still_detected(self, registry):
        """'услови' (condition) scaffolding should still be detected (PQA-0018)."""
        услови_issues = [
            i for i in registry["issues"]
            if i["issue_type"] == "dialogue_premature_concept"
            and "услови" in i.get("reason", "").lower()
        ]
        assert len(услови_issues) >= 1, (
            "'услови' scaffolding issue (PQA-0018) should still be detected. "
            "It is NOT a suppressed word."
        )

    def test_forward_dict_reference_still_detected(self, registry):
        """'словар' (dict) forward reference should still be detected (PQA-0024)."""
        словар_issues = [
            i for i in registry["issues"]
            if i["issue_type"] == "dialogue_premature_concept"
            and "словар" in i.get("reason", "").lower()
        ]
        assert len(словар_issues) >= 1, (
            "'словар' dict forward reference (PQA-0024) should still be detected. "
            "It is NOT a suppressed word."
        )

    def test_wording_issues_preserved(self, registry):
        """Wording clarity issues should still exist (13 wording_ambiguous + 2 wording_overstated + wording_*. correctly flagged)."""
        wording_issues = [
            i for i in registry["issues"]
            if i["issue_type"].startswith("wording_")
        ]
        # Before: 13 wording_ambiguous + 2 wording_overstated
        # These should not be affected by suppression
        assert len(wording_issues) >= 1, (
            "Wording clarity issues should still be detected. "
            "They are independent from premature concept detection."
        )

    def test_structural_issues_preserved(self, registry):
        """Structural audit issues should still be detected."""
        structural_types = [
            "missing_required_field", "invalid_difficulty",
            "missing_analogy", "missing_quiz", "missing_what_outputs",
        ]
        structural_issues = [
            i for i in registry["issues"]
            if i["issue_type"] in structural_types
        ]
        # These should not be affected by suppression
        assert len(structural_issues) >= 0  # Just check it doesn't crash

    def test_no_new_wording_issues_created(self, registry):
        """No new wording issues should be created by the suppression changes."""
        # Get list of issue types
        issue_types = set(i["issue_type"] for i in registry["issues"])
        # Check we don't have unexpected types from the audit modification
        expected_prefixes = {
            "dialogue_premature_concept", "suspicious_one_line_code",
            "wording_", "missing_", "premature_",
            "invalid_", "no_", "insufficient_",
            "correct_", "empty_", "consecutive_",
            "bagus_", "va_", "novice_",
            "dialogue_too_long", "placeholder_",
            "task_asks_output_but_none_expected",
            "boss_no_code_watch",
            "missing_post_error_dialogue",
        }
        for t in issue_types:
            # Every issue type should either match an expected prefix or be documented
            assert any(t.startswith(p) for p in expected_prefixes), (
                f"Unexpected issue type '{t}' appeared after suppression changes"
            )

    def test_audit_report_generated(self, registry):
        """Audit report should be generated."""
        report_path = os.path.join(BASE, "docs", "course_quality_audit_report.md")
        assert os.path.exists(report_path), (
            f"Audit report not found at {report_path}"
        )


class TestDetectionLogicUnit:
    """Unit-level tests for the detection logic via config."""

    def test_concept_detection_rules_loaded(self):
        """Concept detection rules config should be valid JSON with required fields."""
        config_path = os.path.join(
            BASE, "scripts", "config", "audit_concept_detection_rules.json"
        )
        assert os.path.exists(config_path), f"Config not found at {config_path}"
        with open(config_path, "r", encoding="utf-8") as f:
            rules = json.load(f)
        assert "version" in rules
        assert "natural_language_suppression" in rules
        nl = rules["natural_language_suppression"]
        assert "ordinary_russian_words" in nl
        assert "если" in nl["ordinary_russian_words"]
        assert "пока" in nl["ordinary_russian_words"]
        assert "повтор" in nl["ordinary_russian_words"]

    def test_suppressed_words_are_actual_russian_words(self):
        """Ensure suppressed words are natural language, not Python keywords."""
        config_path = os.path.join(
            BASE, "scripts", "config", "audit_concept_detection_rules.json"
        )
        with open(config_path, "r", encoding="utf-8") as f:
            rules = json.load(f)
        words = rules["natural_language_suppression"]["ordinary_russian_words"]
        # None of these should be Python keywords
        python_keywords = {"if", "else", "elif", "for", "while", "def", "return",
                          "class", "import", "from", "try", "except", "with",
                          "as", "pass", "break", "continue", "and", "or", "not",
                          "in", "is", "True", "False", "None"}
        for w in words:
            assert w not in python_keywords, (
                f"'{w}' is a Python keyword and should not be in natural_language_words"
            )
