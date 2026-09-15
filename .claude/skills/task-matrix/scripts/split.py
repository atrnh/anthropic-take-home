#!/usr/bin/env python3
"""manifest.json -> work units. Chunks pages over --max-words at H2 boundaries."""
import argparse, json, pathlib, re

DEFAULT_PRODUCT = [
    ("claude-science/", "claude-science"),
    ("claude-tag/", "claude-tag"),
    ("cowork/", "claude"),
    ("government/", "claude-gov"),
    ("office-agents/", "office-agents"),
    ("third-party/claude-desktop/", "claude-desktop-3p"),
    ("connectors/building/", "claude"),
    ("connectors/mcp-tunnels/", "claude"),
    ("", "claude"),
]

def product_for(path: str) -> str:
    for prefix, prod in DEFAULT_PRODUCT:
        if path.startswith(prefix):
            return prod
    return "claude"

def unit_id(path: str, suffix: str = "") -> str:
    base = path.removesuffix(".md").replace("/", "--")
    return base + suffix

def chunk(text: str, max_words: int):
    """Yield (heading_chain, chunk_text). Splits at H2 when the page is long."""
    if len(text.split()) <= max_words:
        yield [], text
        return
    lines = text.splitlines()
    h1 = next((l for l in lines if l.startswith("# ")), "")
    pre, cur, cur_head, parts = [], [], None, []
    for l in lines:
        if l.startswith("## "):
            if cur_head is None:
                pre = cur
            else:
                parts.append((cur_head, cur))
            cur, cur_head = [l], l
        else:
            cur.append(l)
    if cur_head is None:
        yield [], text; return
    parts.append((cur_head, cur))
    # an H2 that alone exceeds max_words is split again at H3
    split_parts = []
    for head, body in parts:
        if len(" ".join(body).split()) <= max_words:
            split_parts.append((head, body)); continue
        sub, sub_head = [], head
        for l in body:
            if l.startswith("### ") and sub:
                split_parts.append((sub_head, sub)); sub, sub_head = [], f"{head} > {l}"
            sub.append(l)
        split_parts.append((sub_head, sub))
    parts = split_parts
    preamble = "\n".join(pre).strip()
    yield [h1], preamble
    # greedy pack H2 sections up to max_words
    bucket, bucket_heads, n = [], [], 0
    for head, body in parts:
        w = len(" ".join(body).split())
        if bucket and n + w > max_words:
            yield [h1] + bucket_heads, "\n".join(bucket)
            bucket, bucket_heads, n = [], [], 0
        bucket += body; bucket_heads.append(head); n += w
    if bucket:
        yield [h1] + bucket_heads, "\n".join(bucket)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", default="corpus")
    ap.add_argument("--workdir", required=True)
    ap.add_argument("--max-words", type=int, default=2500)
    ap.add_argument("--pages", nargs="*", help="restrict to these corpus-relative paths")
    a = ap.parse_args()
    root = pathlib.Path(a.corpus)
    out = pathlib.Path(a.workdir) / "units"; out.mkdir(parents=True, exist_ok=True)
    m = json.load(open(root / "manifest.json"))
    pages = [p for p in m["pages"] if not a.pages or p["path"] in a.pages]
    index = []
    for p in sorted(pages, key=lambda p: p["path"]):
        text = (root / p["path"]).read_text()
        chunks = list(chunk(text, a.max_words))
        uids = [unit_id(p["path"], f"--part{i+1:02d}" if len(chunks) > 1 else "") for i in range(len(chunks))]
        for i, (chain, body) in enumerate(chunks):
            uid = uids[i]
            unit = {"unit_id": uid, "page": p["path"], "url": p["url"],
                    "product_default": product_for(p["path"]),
                    "part": i + 1, "parts": len(chunks),
                    "sibling_units": [u for u in uids if u != uid],
                    "heading_chain": chain, "words": len(body.split()), "text": body}
            (out / f"{uid}.json").write_text(json.dumps(unit, indent=2, ensure_ascii=False))
            index.append({k: unit[k] for k in ("unit_id", "page", "product_default", "part", "parts", "words")})
    (pathlib.Path(a.workdir) / "units.json").write_text(json.dumps(index, indent=2))
    print(f"{len(index)} units from {len(pages)} pages -> {out}")
    for u in index: print(f"  {u['words']:5d}  {u['unit_id']}  [{u['product_default']}]")

if __name__ == "__main__":
    main()
