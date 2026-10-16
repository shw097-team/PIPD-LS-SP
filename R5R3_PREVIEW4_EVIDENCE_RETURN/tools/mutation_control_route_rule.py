"""Mutation control for the corrected route-identity guard (per-paragraph rule).

Proves the rule is not vacuous: a README whose route paragraph names the SUPERSEDED digest must be
refused, and the unmutated text must be accepted. Prints the two verdicts; exits non-zero if the
detector fails to fire.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

README = Path("C:/Projects/wt-r5r3/README.md")
TAG = "v0.1.1-preview.4"
SERVED = "545e359a5ca6abc7bcbbaa2316f8e062244ad4a132ae1ae839bc9a8e17d95d75"
SUPERSEDED = "2f9ae010a6eba90787037a93a17e77f50bbc29dea5628f6fbe3e0f278fd2d199"
DISCLOSURE = ("superseded", "historical", "history", "do not install")


def paragraphs(text: str) -> list[str]:
    return [p for p in re.split(r"\n\s*\n", text) if p.strip()]


def rule1(text: str) -> list[int]:
    """Every paragraph naming the superseded digest must disclose it."""
    return [i for i, p in enumerate(paragraphs(text))
            if SUPERSEDED in p and not any(m in p.lower() for m in DISCLOSURE)]


def rule2(text: str) -> list[int]:
    """No download-route paragraph may name the superseded digest."""
    return [i for i, p in enumerate(paragraphs(text))
            if f"releases/download/{TAG}/pipd-ls-sp-public-skills.zip" in p and SUPERSEDED in p]


def main() -> int:
    live = README.read_text(encoding="utf-8")
    mutated = live.replace(SERVED, SUPERSEDED)          # swap the served digest in the route
    stripped = mutated
    for word in DISCLOSURE:                             # also remove every disclosure word
        stripped = re.sub(word, "xxx", stripped, flags=re.I)
    out = {
        "live_rule1_violations": rule1(live),
        "live_rule2_violations": rule2(live),
        "mutated_route_rule2_violations": rule2(mutated),
        "mutated_route_rule1_violations": rule1(stripped),
        "detector_fires_on_mutation": bool(rule2(mutated) and rule1(stripped)),
        "live_is_clean": not rule1(live) and not rule2(live),
    }
    print(out)
    return 0 if (out["detector_fires_on_mutation"] and out["live_is_clean"]) else 1


if __name__ == "__main__":
    sys.exit(main())
