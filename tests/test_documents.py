"""Guard the shared lesson structure and the complete README equation reference."""
from pathlib import Path
import re
import unittest

ROOT=Path(__file__).resolve().parents[1]


class DocumentTests(unittest.TestCase):
    def test_lesson_structure(self):
        expected=["Learning goal","Model and assumptions","Inputs and free-body diagram","Equations",
                  "Symbols","Run","Expected behavior","Experiments","Project connections"]
        lessons=list(ROOT.glob("*/tier-*/README.md"))
        self.assertEqual(len(lessons),10)
        for path in lessons:
            self.assertEqual(re.findall(r"^## (.+)$",path.read_text(),re.M),expected,str(path))

    def test_main_readme_contains_all_lesson_equations(self):
        main=(ROOT/"README.md").read_text()
        for path in ROOT.glob("*/tier-*/README.md"):
            for block in re.findall(r"^\$\$\n.*?\n\$\$$",path.read_text(),re.M|re.S):
                self.assertIn(block,main,str(path))

    def test_equation_formatting(self):
        for path in ROOT.rglob("*.md"):
            if "results" in path.parts: continue
            text=re.sub(r"```.*?```","",path.read_text(),flags=re.S)
            inside=False
            depth=0
            for line in text.splitlines():
                if line.strip()=="$$":
                    if inside: self.assertEqual(depth,0,str(path))
                    inside=not inside
                elif inside:
                    self.assertTrue(line.strip(),str(path))
                    depth+=line.count("{")-line.count("}")
                    self.assertGreaterEqual(depth,0,str(path))
            self.assertFalse(inside,str(path))

    def test_relative_links(self):
        for path in ROOT.rglob("*.md"):
            if "results" in path.parts: continue
            for link in re.findall(r"\]\(([^)]+)\)",path.read_text()):
                if "://" in link or link.startswith("#"): continue
                self.assertTrue((path.parent/link.split("#")[0]).exists(),(str(path),link))


if __name__=="__main__": unittest.main()
