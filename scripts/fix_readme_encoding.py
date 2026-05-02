"""Fix the known mojibake sequences in README.md using exact Unicode codepoints."""
import pathlib

p = pathlib.Path('README.md')
t = p.read_text(encoding='utf-8')

# Bad sequences are the cp1252-misread UTF-8 bytes, re-encoded as UTF-8 characters.
# Format: (bad_sequence, correct_unicode_replacement)
fixes = [
    ('\u00e2\u20ac\u201d', '\u2014'),   # â€" -> em dash
    ('\u00e2\u2020\u2019', '\u2192'),   # â†' -> right arrow
    ('\u00e2\u2020\x90',   '\u2192'),   # â†<ctrl-90> -> right arrow (corrupted path)
    # Box-drawing: ├── each char is 3 bytes encoded as 3 garbled chars
    ('\u00e2\u201d\u0153\u00e2\u201d\u20ac\u00e2\u201d\u20ac', '\u251c\u2500\u2500'),  # ├──
    ('\u00e2\u201d\u2014\u00e2\u201d\u20ac\u00e2\u201d\u20ac', '\u2514\u2500\u2500'),  # └──
    ('\u00e2\u0161\u00a1', '\u26a1'),   # âš¡ -> lightning bolt
]

for bad, good in fixes:
    count = t.count(bad)
    print(f'Found {count}x -> {good}')
    t = t.replace(bad, good)

p.write_text(t, encoding='utf-8')

ok_chars = set('\u2014\u2013\u2018\u2019\u2192\u2190\u26a1\u251c\u2514\u2500')
remaining = [c for c in t if ord(c) > 127 and c not in ok_chars]
print(f'Remaining non-ASCII: {len(remaining)}')
if remaining:
    print('Unique:', list(set(remaining))[:10])
else:
    print('All clean!')
print()
print(t[:400])
