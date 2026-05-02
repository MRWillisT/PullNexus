import re
content = open('README.md', encoding='utf-8').read()
bad = [c for c in content if ord(c) > 127 and ord(c) < 256 and c not in '\u2014\u2192\u251c\u2500\u2514\u26a1\u2019\u201c\u201d']
print(f'Suspicious chars: {len(bad)}')
for c in set(bad):
    print(f'  U+{ord(c):04X} {repr(c)}')
print()
# Show lines with issues
for i, line in enumerate(content.splitlines(), 1):
    if any(ord(c) > 127 and ord(c) < 256 for c in line):
        print(f'Line {i}: {line[:80]}')
