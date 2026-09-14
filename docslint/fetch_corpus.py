import hashlib, json, pathlib, re, subprocess, sys, datetime

SCRATCH = pathlib.Path(__file__).parent
OUT = pathlib.Path("/Users/ashley/personal/anthropic-take-home/corpus")

urls = sorted(set(
    u for u in (SCRATCH / "all-urls.txt").read_text().split()
    if re.search(r"/docs/(skills|plugins|connectors)/", u)
    or re.search(r"(skill|plugin|connector)", u.rsplit("/", 1)[-1], re.I)
))

fetched_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
entries = []
for url in urls:
    rel = url.removeprefix("https://claude.com/docs/")
    dest = OUT / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    r = subprocess.run(["curl", "-sS", "--max-time", "30", "-w", "%{http_code}",
                        "-o", str(dest), url], capture_output=True, text=True)
    code = r.stdout.strip()
    if code != "200":
        print(f"FAIL {code} {url}", file=sys.stderr)
        dest.unlink(missing_ok=True)
        continue
    body = dest.read_bytes()
    entries.append({
        "url": url,
        "path": str(dest.relative_to(OUT)),
        "sha256": hashlib.sha256(body).hexdigest(),
        "bytes": len(body),
        "words": len(body.decode("utf-8", "replace").split()),
    })
    print(f"ok {rel}")

manifest = {
    "source_index": "https://claude.com/docs/llms.txt",
    "slice": "Skills, Plugins, and Connectors",
    "fetched_at": fetched_at,
    "page_count": len(entries),
    "pages": entries,
}
(OUT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
print(f"\n{len(entries)}/{len(urls)} pages -> {OUT}")
