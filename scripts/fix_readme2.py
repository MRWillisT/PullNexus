import pathlib
t = pathlib.Path('README.md').read_text(encoding='utf-8')

# en dash (E2 80 93) -> cp1252: â (E2), euro (80), left-dquote (93)
bad_endash = '\u00e2\u20ac\u201c'
# bottom-left box (E2 94 94) -> cp1252: â (E2), right-dquote (94), right-dquote (94)
bad_bottomleft = '\u00e2\u201d\u201d\u00e2\u201d\u20ac\u00e2\u201d\u20ac'

print('en dash matches:', t.count(bad_endash))
print('bottom-left matches:', t.count(bad_bottomleft))

t = t.replace(bad_endash, '\u2013')
t = t.replace(bad_bottomleft, '\u2514\u2500\u2500')

pathlib.Path('README.md').write_text(t, encoding='utf-8')

ok = set('\u2014\u2013\u2018\u2019\u2192\u2190\u26a1\u251c\u2514\u2500')
remaining = [c for c in t if ord(c) > 127 and c not in ok]
print('Remaining bad chars:', len(remaining))
print(t[:500])
