"""
validate.py
===========
Layer 2 + Layer 3 defence for the ODRL Axis Decomposition benchmark.

Layer 2 — pre-write assertion guards (called by the generator).
Layer 3 — post-write round-trip audit (run standalone or in CI).

Usage (standalone / CI):
    python validate.py --ax-dir Problems/ODRL/Axioms
    python validate.py --ax-dir Problems/ODRL/Axioms --problems-dir Problems/ODRL

Exit code 0 = all checks pass.  Non-zero = failures printed to stderr.
"""
import re
import sys
import argparse
from pathlib import Path

# ---------------------------------------------------------------------------
# Helpers shared by both layers
# ---------------------------------------------------------------------------

def count_fof(text: str) -> int:
    return len(re.findall(r"^fof\s*\(", text, re.MULTILINE))

def syntax_formulae(text: str) -> int | None:
    """Extract the formulae count from a rendered % Syntax block."""
    m = re.search(r"Number of formulae\s*:\s*(\d+)", text)
    return int(m.group(1)) if m else None

def comment_counts(text: str) -> list[int]:
    """Extract every integer that appears before the word 'axiom' or 'formulae'
    inside the % Comments block."""
    # Grab only the Comments field lines
    in_comments = False
    lines = []
    for line in text.splitlines():
        if re.match(r"^%\s*Comments\s*:", line):
            in_comments = True
        elif in_comments and re.match(r"^%\s+:", line):
            pass  # continuation
        elif in_comments:
            break  # end of Comments block
        if in_comments:
            lines.append(line)
    block = " ".join(lines)
    return [int(x) for x in re.findall(r"(\d+)\s+axioms?", block)]

# ---------------------------------------------------------------------------
# Layer 2 — pre-write guards (called inside the generator before file I/O)
# ---------------------------------------------------------------------------

class GeneratorGuard:
    """
    Accumulates assertion failures during generation so all errors are
    reported at once rather than stopping at the first failure.

    Usage inside generator:
        guard = GeneratorGuard()
        guard.check_count("PREC000-0.ax", PREC000_BODY, 19)
        guard.check_count("WF000-0.ax",   WF000_BODY,   26)
        guard.check_unique_names("PREC000-0.ax", PREC000_BODY)
        guard.raise_if_failed()   # crash before any file is written
    """

    def __init__(self):
        self._errors: list[str] = []

    def _fail(self, msg: str):
        self._errors.append(msg)

    def check_count(self, name: str, body: str, expected: int):
        """Assert body contains exactly `expected` fof() formulae."""
        actual = count_fof(body)
        if actual != expected:
            self._fail(
                f"{name}: expected {expected} fof() formulae, got {actual}. "
                f"Update the expected count or fix the body."
            )

    def check_unique_names(self, name: str, body: str):
        """Assert every fof() formula name is unique within the file."""
        names = re.findall(r"^fof\s*\(\s*([^,]+?)\s*,", body, re.MULTILINE)
        seen: set[str] = set()
        for n in names:
            if n in seen:
                self._fail(f"{name}: duplicate formula name '{n}'.")
            seen.add(n)

    def check_no_bare_include(self, name: str, body: str, forbidden: str):
        """Assert body does NOT contain a specific include() call."""
        """Assert body does NOT contain a specific include() call (ignores % lines)."""
        active = [l for l in body.splitlines() if not l.strip().startswith('%')]
        if any(f"include('{forbidden}')" in l for l in active):
            self._fail(
                f"{name}: redundant include('{forbidden}'). "
                f"Remove -- {forbidden} is loaded by the problem file."
            )

    def check_comment_count_matches(self, name: str, body: str, rendered: str):
        """
        Assert that every N in '% Comments : ... N axioms ...' equals the
        actual fof() count.  Catches the hand-written-count drift bug.
        """
        actual = count_fof(body)
        for n in comment_counts(rendered):
            if n != actual:
                self._fail(
                    f"{name}: % Comments says '{n} axioms' but body has "
                    f"{actual} fof() formulae."
                )

    def raise_if_failed(self):
        if self._errors:
            msg = "\n".join(f"  ✗ {e}" for e in self._errors)
            raise AssertionError(
                f"\n{len(self._errors)} generator guard(s) failed:\n{msg}"
            )

    @property
    def ok(self) -> bool:
        return not self._errors

# ---------------------------------------------------------------------------
# Layer 3 — post-write round-trip audit (standalone / CI)
# ---------------------------------------------------------------------------

class AuditResult:
    def __init__(self):
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.checked: int = 0

    def error(self, msg: str):   self.errors.append(msg)
    def warning(self, msg: str): self.warnings.append(msg)

    def summary(self) -> str:
        lines = [f"Checked {self.checked} file(s)."]
        if self.errors:
            lines.append(f"{len(self.errors)} error(s):")
            lines += [f"  ✗ {e}" for e in self.errors]
        if self.warnings:
            lines.append(f"{len(self.warnings)} warning(s):")
            lines += [f"  ⚠ {w}" for w in self.warnings]
        if not self.errors and not self.warnings:
            lines.append("All checks passed.")
        return "\n".join(lines)

    @property
    def ok(self) -> bool:
        return not self.errors


def audit_ax_file(path: Path, result: AuditResult):
    """Audit a single .ax file."""
    text = path.read_text(encoding="utf-8")
    result.checked += 1
    name = path.name

    # Check 1: % Syntax formulae matches actual fof() count
    syntax_n = syntax_formulae(text)
    actual_n = count_fof(text)
    if syntax_n is None:
        result.warning(f"{name}: no '% Syntax' block found.")
    elif syntax_n != actual_n:
        result.error(
            f"{name}: % Syntax says {syntax_n} formulae, "
            f"actual fof() count is {actual_n}."
        )

    # Check 2: % Comments counts match % Syntax count
    if syntax_n is not None:
        for n in comment_counts(text):
            if n != syntax_n:
                result.error(
                    f"{name}: % Comments mentions '{n} axioms' but "
                    f"% Syntax says {syntax_n}."
                )

    # Check 3: no duplicate formula names
    names = re.findall(r"^fof\s*\(\s*([^,]+?)\s*,", text, re.MULTILINE)
    seen: set[str] = set()
    for n in names:
        if n in seen:
            result.error(f"{name}: duplicate formula name '{n}'.")
        seen.add(n)

    # Check 4: flat include architecture — no axiom file self-includes ORD000-0.ax.
    # Scan only active (non-comment) lines; note strings in % Comments are fine.
    if name != "ORD000-0.ax":
        active = [l for l in text.splitlines() if not l.strip().startswith('%')]
        if any("include('Axioms/ORD000-0.ax')" in l for l in active):
            result.error(
                f"{name}: redundant include('Axioms/ORD000-0.ax'). "
                f"Remove -- ORD000-0.ax is loaded by the problem file."
            )
    # Check 5: file has a % File header matching its filename
    if f"% File     : {name}" not in text:
        result.warning(f"{name}: % File field does not match filename.")


def audit_p_file(path: Path, result: AuditResult):
    """Audit a single .p problem file."""
    text = path.read_text(encoding="utf-8")
    result.checked += 1
    name = path.name

    syntax_n = syntax_formulae(text)
    actual_n = count_fof(text)

    # Problem files have axioms + conjecture; just check Syntax is present
    if syntax_n is None:
        result.warning(f"{name}: no '% Syntax' block found.")
    elif syntax_n != actual_n:
        result.error(
            f"{name}: % Syntax says {syntax_n} formulae, "
            f"actual fof() count is {actual_n}."
        )

    # Must have exactly one conjecture
    conj = len(re.findall(r"^fof\s*\([^,]+,\s*conjecture\s*,",
                           text, re.MULTILINE))
    if conj == 0:
        result.warning(f"{name}: no conjecture formula found.")
    elif conj > 1:
        result.error(f"{name}: {conj} conjecture formulae (expected 1).")

    # Status field must be present
    if not re.search(r"^% Status\s*:", text, re.MULTILINE):
        result.warning(f"{name}: no % Status field.")


def run_audit(ax_dir: Path | None, problems_dir: Path | None) -> AuditResult:
    result = AuditResult()

    if ax_dir and ax_dir.exists():
        for p in sorted(ax_dir.glob("*.ax")):
            audit_ax_file(p, result)
    elif ax_dir:
        result.error(f"Axiom directory not found: {ax_dir}")

    if problems_dir and problems_dir.exists():
        for p in sorted(problems_dir.glob("*.p")):
            audit_p_file(p, result)

    return result


# ---------------------------------------------------------------------------
# CLI entry point (Layer 3 standalone)
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Round-trip audit for ODRL Axis Decomposition benchmark files."
    )
    parser.add_argument("--ax-dir",
                        default="Problems/ODRL/Axioms",
                        help="Directory containing .ax axiom files.")
    parser.add_argument("--problems-dir",
                        default=None,
                        help="Directory containing .p problem files (optional).")
    args = parser.parse_args()

    result = run_audit(
        ax_dir       = Path(args.ax_dir),
        problems_dir = Path(args.problems_dir) if args.problems_dir else None,
    )
    print(result.summary())
    sys.exit(0 if result.ok else 1)


if __name__ == "__main__":
    main()
