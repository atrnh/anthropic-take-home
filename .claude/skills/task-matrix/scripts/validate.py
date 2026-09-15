#!/usr/bin/env python3
"""Validate extraction JSON against schema + taxonomy + evidence grep.

Writes W/validation.json and W/accepted/<unit_id>.json (records that passed).
Exit 1 if any unit failed to parse.
"""
import argparse, json, pathlib, re, sys

MECH = {"click-through", "command", "edit-file", "api-call", "prompt-claude", "request-person", "other"}
SURF = {"app-settings", "admin-settings", "chat", "terminal", "filesystem", "web-portal", "third-party-admin", "other"}
ACTOR = {"end-user", "admin", "developer"}

def load_taxonomy(path):
    """Tiny YAML reader for the flat structure taxonomy.yaml uses."""
    tasks, products, section, cur = {}, {}, None, None
    for line in pathlib.Path(path).read_text().splitlines():
        if not line.strip() or line.lstrip().startswith("#"): continue
        if not line.startswith(" "):
            section = line.rstrip(":"); cur = None; continue
        m = re.match(r"^  - id: (\S+)", line)
        if m:
            cur = m.group(1)
            (tasks if section == "tasks" else products if section == "products" else {})[cur] = {}
            continue
        m = re.match(r"^    (\w+): (.*)$", line)
        if m and cur:
            d = tasks if section == "tasks" else products
            if cur in d: d[cur][m.group(1)] = m.group(2).strip().strip('"')
    return tasks, products

def norm(s: str) -> str:
    s = s.replace("`", "").replace("*", "").replace("’", "'").replace("“", '"').replace("”", '"')
    s = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", s)   # [text](url) -> text
    return re.sub(r"\s+", " ", s).strip().lower()

def check_record(r, unit_text, unit_norm, tasks, products, default_product):
    errs = []
    tid = r.get("task_id")
    if tid == "NEW":
        nt = r.get("new_task") or {}
        if not nt.get("label") or not nt.get("why") or not nt.get("outcome"): errs.append("NEW without label/outcome/why")
    elif tid not in tasks: errs.append(f"unknown task_id {tid}")
    if r.get("product") not in products: errs.append(f"unknown product {r.get('product')}")
    elif r["product"] != default_product:
        ev = (r.get("product_evidence") or "").lower()
        names = [n.strip() for n in products[r["product"]].get("names", "").lower().split(";") if n.strip()]
        names.append(r["product"].replace("-", " "))
        if not ev: errs.append("product override without product_evidence")
        elif not any(n in ev for n in names): errs.append(f"product_evidence does not name the product ({r['product']})")
    if r.get("mechanism") not in MECH: errs.append(f"bad mechanism {r.get('mechanism')}")
    if r.get("surface") not in SURF: errs.append(f"bad surface {r.get('surface')}")
    if not (r.get("outcome") or "").strip(): errs.append("no outcome")
    if r.get("partial") and r.get("stage_of") not in tasks: errs.append("partial without valid stage_of")
    actors = r.get("actor")
    if isinstance(actors, str): actors = [a.strip() for a in actors.split(",")]
    if not actors or any(a not in ACTOR for a in actors): errs.append(f"bad actor {r.get('actor')}")
    steps = r.get("steps") or []
    if not steps: errs.append("no steps")
    if len(steps) > 12: errs.append("more than 12 steps")
    ev = r.get("evidence") or {}
    q, anchor = ev.get("quote", ""), ev.get("anchor", "")
    if not q: errs.append("no quote")
    else:
        if len(q.split()) > 30: errs.append("quote over 30 words")
        if norm(q) not in unit_norm: errs.append("quote not found in unit")
    if anchor and anchor.strip() not in {l.strip() for l in unit_text.splitlines() if l.startswith("#")}:
        errs.append("anchor not a heading in unit")
    return errs

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workdir", required=True)
    ap.add_argument("--taxonomy", default=str(pathlib.Path(__file__).parent.parent / "references/taxonomy.yaml"))
    a = ap.parse_args()
    W = pathlib.Path(a.workdir)
    tasks, products = load_taxonomy(a.taxonomy)
    acc = W / "accepted"; acc.mkdir(exist_ok=True)
    report, bad_parse = {}, 0
    for uf in sorted((W / "units").glob("*.json")):
        unit = json.load(open(uf)); uid = unit["unit_id"]
        ef = W / "extractions" / f"{uid}.json"
        if not ef.exists():
            report[uid] = {"status": "missing"}; continue
        try:
            ex = json.load(open(ef))
        except Exception as e:
            report[uid] = {"status": "unparseable", "error": str(e)}; bad_parse += 1; continue
        unorm = norm(unit["text"])
        kept, rejected = [], []
        for i, r in enumerate(ex.get("records", [])):
            errs = check_record(r, unit["text"], unorm, tasks, products, unit["product_default"])
            (rejected if errs else kept).append({"index": i, "task_id": r.get("task_id"), "errors": errs} if errs else r)
        for r in kept: r["_unit_id"] = uid; r["_page"] = unit["page"]
        json.dump({"unit_id": uid, "page": unit["page"], "records": kept}, open(acc / f"{uid}.json", "w"), indent=2, ensure_ascii=False)
        report[uid] = {"status": "ok", "accepted": len(kept), "rejected": rejected,
                       "no_procedures": ex.get("no_procedures", False)}
    json.dump(report, open(W / "validation.json", "w"), indent=2)
    tot_a = sum(v.get("accepted", 0) for v in report.values())
    tot_r = sum(len(v.get("rejected", [])) for v in report.values())
    print(f"accepted {tot_a}  rejected {tot_r}  units {len(report)}")
    for uid, v in report.items():
        if v["status"] != "ok": print(f"  !! {uid}: {v['status']}")
        for rj in v.get("rejected", []): print(f"  - {uid}#{rj['index']} ({rj['task_id']}): {'; '.join(rj['errors'])}")
    sys.exit(1 if bad_parse else 0)

if __name__ == "__main__":
    main()
