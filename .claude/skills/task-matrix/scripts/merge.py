#!/usr/bin/env python3
"""Group accepted records by task into W/tasks/<task_id>.json; list NEW candidates."""
import argparse, json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from validate import load_taxonomy

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workdir", required=True)
    ap.add_argument("--taxonomy", default=str(pathlib.Path(__file__).parent.parent / "references/taxonomy.yaml"))
    a = ap.parse_args()
    W = pathlib.Path(a.workdir)
    tasks, products = load_taxonomy(a.taxonomy)
    by_task, new, seen_products = {}, [], set()
    for f in sorted((W / "accepted").glob("*.json")):
        for r in json.load(open(f))["records"]:
            seen_products.add(r["product"])
            if r["task_id"] == "NEW":
                new.append({"unit_id": r["_unit_id"], "label": r["new_task"]["label"], "why": r["new_task"]["why"], "product": r["product"]})
            else:
                by_task.setdefault(r["task_id"], []).append(r)
    scope = sorted(seen_products)
    out = W / "tasks"; out.mkdir(exist_ok=True)
    for tid, recs in by_task.items():
        json.dump({"task_id": tid, "task": tasks[tid].get("label", tid), "definition": tasks[tid].get("definition", ""),
                   "outcome": tasks[tid].get("outcome", ""), "view": tasks[tid].get("view", "product"),
                   "artifact": tasks[tid].get("artifact", ""), "stage": tasks[tid].get("stage", ""),
                   "products_in_scope": scope, "records": recs}, open(out / f"{tid}.json", "w"), indent=2, ensure_ascii=False)
    json.dump({"products_in_scope": scope, "new_candidates": new}, open(W / "merge.json", "w"), indent=2, ensure_ascii=False)
    print(f"{len(by_task)} tasks, {sum(map(len, by_task.values()))} records, {len(new)} NEW candidates; products: {scope}")
    for tid in sorted(by_task): print(f"  {tid} {tasks[tid].get('label','')!r}: {len(by_task[tid])} records over {sorted({r['product'] for r in by_task[tid]})}")
    for n in new: print(f"  NEW [{n['unit_id']}] {n['label']!r}: {n['why']}")

if __name__ == "__main__":
    main()
