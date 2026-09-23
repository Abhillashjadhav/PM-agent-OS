import sys, re, yaml
path = sys.argv[1]
text = open(path).read()
checks = {key: False for key in (
    "frontmatter_parses", "has_name", "name_kebab_case", "has_description",
    "desc_under_1024_chars", "desc_has_trigger_phrases", "desc_has_negative_trigger",
)}
fm = re.match(r'^---\n(.*?)\n---', text, re.S)
checks["frontmatter_parses"] = False
if fm:
    try:
        meta = yaml.safe_load(fm.group(1))
        checks["frontmatter_parses"] = isinstance(meta, dict)
        if isinstance(meta, dict):
            name = meta.get("name", "")
            desc = meta.get("description", "")
            checks["has_name"] = isinstance(name, str) and bool(name.strip())
            checks["name_kebab_case"] = isinstance(name, str) and bool(re.fullmatch(r'[a-z0-9]+(-[a-z0-9]+)*', name))
            checks["has_description"] = isinstance(desc, str) and bool(desc.strip())
            checks["desc_under_1024_chars"] = isinstance(desc, str) and len(desc) <= 1024
            checks["desc_has_trigger_phrases"] = isinstance(desc, str) and ("Use this skill" in desc or "Use when" in desc)
            checks["desc_has_negative_trigger"] = isinstance(desc, str) and ("Do NOT" in desc or "Do not" in desc)
    except Exception as e:
        pass
checks["body_under_500_lines"] = len(text.splitlines()) <= 500
checks["has_limitations_section"] = "Limitations" in text
for k, v in checks.items():
    print(f"{'PASS' if v else 'FAIL'}  {k}")
sys.exit(0 if all(checks.values()) else 1)
