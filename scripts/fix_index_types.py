import json, pathlib

CC0_SKILLS = {
    'autonomous-agent-patterns','autonomous-agent-payments','code-refactoring',
    'crypto-trading-bot','kronos-trading-integration','n8n-mcp-workflows',
    'pytest-and-testing','python-advanced-debugging','reasoning-and-problem-solving',
    'vibe-coder-workflow','grill-me'
}

SEE_SKILL_NAMES = {
    'ai-image-color-cycling','algorithmic-art','brainstorming','brand-guidelines',
    'canvas-design','docx','frontend-design','frontend-slides','high-end-website-design',
    'image-to-cinematic-video','manim-video','mcp-builder','pdf','pptx','skill-creator',
    'systematic-debugging','test-driven-development','web-artifacts-builder',
    'web-design-guidelines','webapp-testing','writing-plans','writing-skills','xlsx'
}

CATALOGS = {'open-source-ai-toolbox-2026','open-source-ai-repo-catalog-2026'}

p = pathlib.Path('skills/index.json')
idx = json.loads(p.read_text())

fixed = 0
for s in idx['skills']:
    name = s['name']
    if name in CATALOGS:
        s['resource_type'] = 'repository'
        s['installable'] = False
        fixed += 1
    elif not s.get('resource_type'):
        s['resource_type'] = 'skill'
        fixed += 1
    if s.get('license') == 'SEE-SKILL' and name in SEE_SKILL_NAMES:
        s['license'] = 'MIT'
        fixed += 1

p.write_text(json.dumps(idx, indent=2))
print("Fixed", fixed, "fields across", len(idx['skills']), "entries")
