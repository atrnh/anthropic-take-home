#!/usr/bin/env python3
"""W/matrix/*.json -> W/out/inventory.md (product view), builder-inventory.md (builder view), appendix.md"""
import argparse, json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from validate import load_taxonomy

STAGES = ["build", "test", "package", "submit", "review", "distribute", "maintain", "remove"]
ARTIFACTS = ["skill", "plugin", "connector", "mcp-app"]

def cell_text(c):
    if not c or c.get("status") == "absent": return "—"
    v = ", ".join(c.get("variants", [])) or "?"
    d = ", ".join(x for x in c.get("diff", []) if x != "same")
    return f"**{v}**" + (f" · {d}" if d else "")

def short(s, n=25):
    w = s.split(); return " ".join(w[:n]) + (" …" if len(w) > n else "")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workdir", required=True)
    ap.add_argument("--taxonomy", default=str(pathlib.Path(__file__).parent.parent / "references/taxonomy.yaml"))
    a = ap.parse_args()
    W = pathlib.Path(a.workdir); out = W / "out"; out.mkdir(exist_ok=True)
    tasks, products = load_taxonomy(a.taxonomy)
    mats = [json.load(open(f)) for f in sorted((W / "matrix").glob("*.json"))]
    for m in mats:
        t = tasks.get(m["task_id"], {})
        m.setdefault("view", t.get("view", "product")); m["_artifact"] = t.get("artifact", ""); m["_stage"] = t.get("stage", "")
    scope = json.load(open(W / "merge.json"))["products_in_scope"]
    plabel = {p: products.get(p, {}).get("label", p) for p in scope}
    prod = [m for m in mats if m["view"] == "product"]; build = [m for m in mats if m["view"] == "builder"]

    # product view: tasks x products
    L = ["# Task–procedure inventory (product view)", "",
         "Rows are reader tasks; columns are products. A cell lists the procedure variant IDs that product documents for the task, then how they differ from the other products' variants. `—` = not documented. Variant IDs are per task; steps, actors, surfaces, and sources are in the appendix.", "",
         "| Task | " + " | ".join(plabel[p] for p in scope) + " | Summary |", "|---|" + "---|" * (len(scope) + 1)]
    for m in prod:
        L.append(f"| {m['task_id']} {m['task']} | " + " | ".join(cell_text(m["cells"].get(p)) for p in scope) + f" | {short(m.get('summary',''))} |")
    (out / "inventory.md").write_text("\n".join(L) + "\n")

    # builder view: stage x artifact
    B = ["# Development and publication inventory (builder view)", "",
         "Rows are lifecycle stages; columns are artifact types. A cell lists the tasks documented for that stage and artifact with their procedure variant IDs, so shared workflows line up across artifact types. `—` = nothing documented.", "",
         "| Stage | " + " | ".join(ARTIFACTS) + " |", "|---|" + "---|" * len(ARTIFACTS)]
    grid = {}
    for m in build:
        grid.setdefault(m["_stage"] or "other", {}).setdefault(m["_artifact"] or "other", []).append(m)
    for st in STAGES + [s for s in grid if s not in STAGES]:
        if st not in grid: continue
        cells = []
        for art in ARTIFACTS:
            ms = grid[st].get(art, [])
            cells.append("<br>".join(f"{m['task_id']} {m['task']}: " + ", ".join(v["variant_id"] for f in m["families"] for v in f["variants"]) for m in ms) or "—")
        B.append(f"| {st} | " + " | ".join(cells) + " |")
    B += ["", "## Per-task summaries", ""] + [f"- **{m['task_id']} {m['task']}** ({m['_artifact'] or '?'} / {m['_stage'] or '?'}): {short(m.get('summary',''))}" for m in build]
    (out / "builder-inventory.md").write_text("\n".join(B) + "\n")

    # appendix
    A = ["# Appendix: procedures by task", ""]
    for m in prod + build:
        A += [f"## {m['task_id']} {m['task']}  ({m['view']} view)", "", m.get("summary", ""), ""]
        for f in m["families"]:
            A.append(f"### {f['family_id']} · {f.get('surface','?')} / {f.get('mechanism','?')} · {f['label']}")
            for v in f["variants"]:
                A += ["", f"**{v['variant_id']}** {v['label']} — actor: {', '.join(v['actor']) if isinstance(v['actor'], list) else v['actor']}; products: {', '.join(plabel.get(p,p) for p in v['products'])}"]
                if v.get("preconditions"): A.append(f"Preconditions: {'; '.join(v['preconditions'])}")
                A += [f"{i+1}. {s}" for i, s in enumerate(v["steps"])]
                A.append("Sources: " + "; ".join(f"`{s['unit_id']}` {s['anchor']}" for s in v["sources"]))
            A.append("")
        if m["view"] == "product":
            A += ["Cells:", ""] + [f"- {plabel.get(p,p)}: {c['status']}; variants {', '.join(c['variants']) or '—'}; diff {', '.join(c['diff'])}. {c.get('note','')}" for p, c in m["cells"].items()]
        if m.get("misfiled"): A += ["", "Misfiled records (excluded):"] + [f"- `{x['unit_id']}` {x['anchor']}: {x['reason']} → {x.get('suggest','')}" for x in m["misfiled"]]
        if m.get("open_questions"): A += ["", "Open questions:"] + [f"- {q}" for q in m["open_questions"]]
        A.append("")
    (out / "appendix.md").write_text("\n".join(A) + "\n")
    print(f"rendered {len(prod)} product-view tasks x {len(scope)} products, {len(build)} builder-view tasks -> {out}")

if __name__ == "__main__":
    main()
