"""End-to-end integrity and completeness test suite for The Maritime AIS Handbook."""

import pathlib
import re
import unittest

ROOT_DIR = pathlib.Path(__file__).resolve().parent.parent


class TestBookIntegrity(unittest.TestCase):
    """Verifies that all TASKS.md items, chapters, appendices, and links are complete."""

    def test_all_tasks_checked_off_in_tasks_md(self) -> None:
        tasks_path = ROOT_DIR / "TASKS.md"
        self.assertTrue(tasks_path.exists(), "TASKS.md must exist")
        text = tasks_path.read_text(encoding="utf-8")
        unchecked = re.findall(r"^- \[ \].*$", text, re.M)
        checked = re.findall(r"^- \[x\].*$", text, re.M)
        self.assertEqual(
            len(unchecked),
            0,
            f"Found unchecked tasks in TASKS.md: {unchecked}",
        )
        self.assertEqual(len(checked), 80, "Expected all 80 tasks in TASKS.md to be checked")

    def test_all_book_readme_links_resolve(self) -> None:
        readme_path = ROOT_DIR / "book" / "README.md"
        self.assertTrue(readme_path.exists(), "book/README.md must exist")
        text = readme_path.read_text(encoding="utf-8")
        links = re.findall(r"\[[^\]]+\]\(([^)#]+)(?:#[^)]*)?\)", text)
        self.assertGreaterEqual(len(links), 54)
        for link in links:
            if link.startswith(("http://", "https://", "file://")):
                continue
            target = (readme_path.parent / link).resolve()
            self.assertTrue(target.exists(), f"Broken link in book/README.md: {link} -> {target}")
            self.assertGreater(target.stat().st_size, 1000, f"File too small: {target}")

    def test_all_40_chapters_and_8_appendices_exist_and_substantial(self) -> None:
        chapters = sorted((ROOT_DIR / "book").glob("part*/ch*.md"))
        self.assertEqual(len(chapters), 40, f"Expected 40 chapters, found {len(chapters)}")
        for ch in chapters:
            content = ch.read_text(encoding="utf-8")
            lines = content.splitlines()
            self.assertGreaterEqual(
                len(lines),
                450,
                f"Chapter {ch.name} has {len(lines)} lines, expected >= 450",
            )
            self.assertIn("```", content, f"Chapter {ch.name} must contain code/diagram blocks")

        appendices = sorted((ROOT_DIR / "book" / "appendices").glob("appendix-*.md"))
        self.assertEqual(len(appendices), 8, f"Expected 8 appendices, found {len(appendices)}")
        for app in appendices:
            content = app.read_text(encoding="utf-8")
            self.assertGreater(len(content), 10000, f"Appendix {app.name} is too short")

    def test_master_bibliography_bibtex_and_appendix_h_parity(self) -> None:
        bib_path = ROOT_DIR / "MASTER_BIBLIOGRAPHY.bib"
        app_h_path = ROOT_DIR / "book" / "appendices" / "appendix-h-master-bibliography.md"
        self.assertTrue(bib_path.exists(), "MASTER_BIBLIOGRAPHY.bib must exist")
        self.assertTrue(app_h_path.exists(), "appendix-h-master-bibliography.md must exist")

        bib_text = bib_path.read_text(encoding="utf-8")
        app_h_text = app_h_path.read_text(encoding="utf-8")

        bib_keys = set(re.findall(r"^@\w+\{([^,\s]+),", bib_text, re.M))
        self.assertGreaterEqual(len(bib_keys), 80, "Expected at least 80 BibTeX entries")
        for key in bib_keys:
            self.assertIn(
                f"`{key}`",
                app_h_text,
                f"BibTeX key {key} missing from Appendix H markdown",
            )


if __name__ == "__main__":
    unittest.main()
