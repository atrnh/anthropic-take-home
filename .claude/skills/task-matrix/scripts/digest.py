#!/usr/bin/env python3
"""Print a compact digest of every corpus page: title, lede, headings, first paragraph.

Used once to seed taxonomy.yaml. Output is markdown on stdout.
"""
import argparse, json, pathlib, re

def digest(path: pathlib.Path, root: pathlib.Path) -> str:
    text = path.read_text()
    lines = text.splitlines()
    title = next((l[2:] for l in lines if l.startswith("# ")), path.name)
    lede = next((l[2:] for l in lines if l.startswith("> ") and "Documentation Index" not in l and "llms.txt" not in l and "Use this file" not in l), "")
    heads = [l for l in lines if re.match(r"^#{2,4} ", l)]
    # first non-empty, non-heading, non-blockquote paragraph after the H1
    body = [l for l in lines if l.strip() and not l.startswith(("#", ">", "<", "|", "```", "*", "-"))]
    first = body[0][:300] if body else ""
    out = [f"### {path.relative_to(root)}", f"title: {title}", f"lede: {lede}", f"words: {len(text.split())}"]
    if first: out.append(f"first: {first}")
    out += ["headings:"] + [f"  {h}" for h in heads]
    return "\n".join(out)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", default="corpus")
    a = ap.parse_args()
    root = pathlib.Path(a.corpus)
    m = json.load(open(root / "manifest.json"))
    for p in sorted(m["pages"], key=lambda p: p["path"]):
        print(digest(root / p["path"], root)); print()

if __name__ == "__main__":
    main()
