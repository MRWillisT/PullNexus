#!/usr/bin/env python3
"""
Validate that a spec response contains the required sections.

Usage:
    echo "Goals: ... Constraints: ... Success Metrics: ... Edge cases: ..." | python tools/validate_spec.py
    # or
    python tools/validate_spec.py < my_spec.txt
"""
import sys


REQUIRED_SECTIONS = ["Goals", "Constraints", "Success Metrics", "Edge cases"]


def validate_spec(text: str) -> bool:
    missing = [s for s in REQUIRED_SECTIONS if s.lower() not in text.lower()]
    if missing:
        print(f"WARNING  Missing sections: {missing}")
        return False
    print("OK  Spec contains all required sections.")
    return True


if __name__ == "__main__":
    text = sys.stdin.read()
    ok = validate_spec(text)
    sys.exit(0 if ok else 1)
