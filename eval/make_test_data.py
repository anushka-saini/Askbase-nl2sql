# copies the test questions, the saved model outputs and the red-team results into test-data/ as plain csv files
# reads only eval/*.json and logs/, writes only test-data/. no api calls.
# run: python eval/make_test_data.py

import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
import config  # noqa: E402

ROOT = config.ROOT
OUT = ROOT / "test-data"
LOGS = config.LOGS

# tier -> input type
TYPE = {"simple": "Normal", "join": "Normal", "aggregation": "Normal",
        "fanout": "Edge", "ambiguous": "Edge", "refuse": "Invalid"}


def inputs():
    rows = []
    for f, fixed_split in [("test_set.json", None), ("test2_set.json", "test2")]:
        for q in json.loads((ROOT / "eval" / f).read_text(encoding="utf-8")):
            rows.append({"id": q["id"], "tier": q["tier"], "type": TYPE[q["tier"]], "question": q["question"],
                         "split": fixed_split or q["split"], "expected": q["expected"] if q["expected"] == "REFUSE" else "ANSWER",
                         "refuse_ok": bool(q.get("refuse_ok")), "verified": bool(q.get("verified"))})
    return pd.DataFrame(rows)


def latest_runs(folder):
    # newest run per (version, split, model); files are logs/results_<version>_<split>[_<model>]_<time>.csv
    best = {}
    for f in sorted(folder.glob("results_*.csv")):
        d = pd.read_csv(f, nrows=1)
        key = (d["version"].iloc[0], d["split"].iloc[0], d["model"].iloc[0])
        if key not in best or d["run_id"].iloc[0] > best[key][1]:
            best[key] = (f, d["run_id"].iloc[0])
    return [f for f, _ in best.values()]


def outputs():
    cols = ["split", "version", "model", "run_id", "id", "tier", "repeat", "question", "generated_sql", "status",
            "error", "retries", "pass", "strict_pass", "matched"]
    parts = []
    for f in latest_runs(LOGS) + latest_runs(LOGS / "test2"):
        d = pd.read_csv(f)
        d["source_file"] = f.relative_to(ROOT).as_posix()
        parts.append(d[[c for c in cols if c in d.columns] + ["source_file"]])
    out = pd.concat(parts, ignore_index=True)
    out["type"] = out["tier"].map(TYPE)
    # per-question majority over the 3 repeats (test split) from logs/per_question_test.csv
    pq = pd.read_csv(LOGS / "per_question_test.csv")[["id", "version", "model", "run_id", "pass_rate", "majority_pass"]]
    out = out.merge(pq, on=["id", "version", "model", "run_id"], how="left")
    out["pass"] = out["pass"].map({True: "pass", False: "fail"})
    out["strict_pass"] = out["strict_pass"].map({True: "pass", False: "fail"})
    return out.sort_values(["split", "model", "version", "id", "repeat"])


def redteam():
    fs = sorted((LOGS / "redteam").glob("redteam_all_v4_*.csv"))
    d = pd.read_csv(fs[-1])
    d["stopped_by"] = d.apply(lambda r: "model refused (CANNOT_ANSWER)" if r["pipeline_status"] == "refused"
                              else "model wrote only a read query" if r["pipeline_layer"] == "prompt"
                              else r["pipeline_layer"], axis=1)
    keep = ["id", "type", "attack", "version", "pipeline_status", "stopped_by", "pipeline_detail", "retries",
            "prompt_leak", "payload_sql", "validator_blocks", "validator_reason", "readonly_blocks", "readonly_error",
            "tables_unchanged", "model", "time"]
    d = d[keep].rename(columns={"type": "attack_type"})
    d["source_file"] = fs[-1].relative_to(ROOT).as_posix()
    return d


def main():
    OUT.mkdir(exist_ok=True)
    a, b, c = inputs(), outputs(), redteam()
    a.to_csv(OUT / "test_inputs.csv", index=False)
    b.to_csv(OUT / "saved_outputs.csv", index=False)
    c.to_csv(OUT / "redteam_summary.csv", index=False)
    print(f"test_inputs.csv: {len(a)} questions ({a['type'].value_counts().to_dict()})")
    print(f"saved_outputs.csv: {len(b)} rows from {b['source_file'].nunique()} results files")
    print(f"redteam_summary.csv: {len(c)} attacks from {c['source_file'].iloc[0]}")


if __name__ == "__main__":
    main()
