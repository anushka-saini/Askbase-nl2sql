# re-runs every cached answer in the newest main-model results files through the pipeline and the scorer,
# offline, and checks that the stored pass / strict_pass verdicts come out the same.
# no api calls, nothing written to logs/calls.csv or to the results files. output: logs/recheck/offline_rescore_<time>.txt
# run: python eval/rescore_offline.py
# note: queries are stopped after 10 s, so on a busy machine some slow queries time out and their verdict differs

import json
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "eval")]
import config  # noqa: E402
import llm  # noqa: E402
llm.log_call = lambda row: None  # keep logs/calls.csv untouched
import pipeline  # noqa: E402
pipeline.ask = llm.ask
from score import score_item  # noqa: E402


def newest(files):
    # newest run per (version, split) for the main model
    best = {}
    for f in files:
        d = pd.read_csv(f, nrows=1)
        if d["model"].iloc[0] != config.MODEL:
            continue
        k = (d["version"].iloc[0], d["split"].iloc[0])
        if k not in best or d["run_id"].iloc[0] > best[k][1]:
            best[k] = (f, d["run_id"].iloc[0])
    return [best[k][0] for k in sorted(best)]


def main():
    items = {q["id"]: q for f in ["test_set.json", "test2_set.json"]
             for q in json.loads((ROOT / "eval" / f).read_text(encoding="utf-8"))}
    files = newest(list(config.LOGS.glob("results_v*_dev_2*.csv")) + list(config.LOGS.glob("results_v*_test_2*.csv"))
                   + list((config.LOGS / "test2").glob("results_*.csv")))
    lines, diffs, tot, same = [], [], 0, 0
    for f in files:
        d = pd.read_csv(f)
        ok_n = 0
        for _, r in d.iterrows():
            out = pipeline.run_question(r["question"], r["version"], qid=r["id"], repeat=int(r["repeat"]), offline=True)
            sc = score_item(items[r["id"]], out)
            ok = sc["pass"] == bool(r["pass"]) and sc["strict_pass"] == bool(r["strict_pass"])
            ok_n += ok
            if not ok:
                diffs.append(f"{r['version']} {r['split']} {r['id']} r{r['repeat']}: stored {r['status']}/{r['pass']} "
                             f"-> now {out['status']}/{sc['pass']} {out['error'][:60]}")
        tot += len(d)
        same += ok_n
        line = f"{d['version'].iloc[0]:3} {d['split'].iloc[0]:5} {f.name}: {ok_n}/{len(d)} verdicts reproduced"
        lines.append(line)
        print(line, flush=True)
    lines += [f"TOTAL {same}/{tot} reproduced"] + (diffs or ["no differences"])
    out = config.LOGS / "recheck" / f"offline_rescore_{datetime.now():%Y%m%d-%H%M%S}.txt"
    out.parent.mkdir(exist_ok=True)
    out.write_text(f"offline re-score run at {datetime.now():%Y-%m-%d %H:%M:%S} (cached answers only, no API calls)\n\n"
                   + "\n".join(lines) + "\n", encoding="utf-8")
    print(lines[-len(diffs or [0]) - 1])
    print("saved", out)


if __name__ == "__main__":
    main()
