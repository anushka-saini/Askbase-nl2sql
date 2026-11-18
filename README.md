# SchemaSense: safe natural-language-to-SQL on Olist

A prompt engineering study for the Prompt Engineering course, Bennett University (3-person mini-project).
A user asks a question in plain English, an LLM writes one SQLite `SELECT` query over the
[Olist Brazilian e-commerce dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce), and the query runs on a read-only copy of the database. The user sees the SQL, the rows and a one-line explanation.

The core of the project is the **prompt experiment**: the model and its settings stay fixed, and only the prompt changes. Five prompt versions (v0 to v4), each adding one idea, are scored on a 60-question test set with a held-out split, followed by error analysis and an 18-attack red team. A Streamlit app is the demo layer.

- **Model:** `openai/gpt-oss-120b` on Groq, temperature 0, top_p 1, max_completion_tokens 2048, reasoning_effort medium (all in `src/config.py`)
- **Safety:** three layers: prompt rules, a SQL validator and a read-only database connection ([docs/design.md](docs/design.md), diagrams in [docs/diagrams/](docs/diagrams))

> **Status: provisional.** The 60 gold queries and the error labels were drafted with Claude's help and are **not verified** by the team yet (`verified: false` in `eval/test_set.json`; no verdicts filled in `review/gold_review.csv`). Two business-rule definitions are assumptions. Review sheets are in `review/`.

## Team AskBase

- **Team name:** AskBase
- **Team ID:** PE-B01-16
- **Faculty:** Dr. Sonal Kukreja
- **Repository:** https://github.com/anushka-saini/schemasense-nl2sql

| name | roll number | role | tasks |
|---|---|---|---|
| Anushka Saini (team leader) | S24CSEU1046 | | |
| Devanshi Papneja | S24CSEU0824 | | |
| Divyangana Jain | S24CSEU0856 | | |

Who did what, with evidence: [docs/contribution_log.md](docs/contribution_log.md).

**Prototype:** [PROTOTYPE_LINK]

**Demo notebook (outputs saved):** [code/askbase_demo.ipynb](code/askbase_demo.ipynb) replays real cached runs of the final pipeline: six held-out test questions with their SQL, validation status, rows and pass/fail against gold, real red-team attacks, and the results table. It opens on GitHub with all outputs shown; the database is not included because of its size.

## Setup

Needs Python 3.12 (Windows, macOS or Linux).

```bash
python -m venv .venv
# Windows PowerShell:  .\.venv\Scripts\Activate.ps1
# macOS / Linux:       source .venv/bin/activate
pip install -r requirements.txt
```

1. **Data.** Download the Olist CSVs yourself and put all 9 files in `data/raw/` (e.g. `olist_orders_dataset.csv`, `product_category_name_translation.csv`). Then build the database:
   ```bash
   python src/load_db.py
   ```
   This creates `data/olist.db` and prints the row counts. The database and the CSVs are not in git.
2. **API key.** The key is read only from the `GROQ_API_KEY` environment variable. Copy `.env.example` to `.env` and put your own Groq key in it, or set the variable in your shell (PowerShell: `$env:GROQ_API_KEY = "..."`). The key is never stored in code or committed (`.env` is in `.gitignore`).
3. **Offline mode.** Without a key, everything runs from the cached model replies in `logs/cache/`: add `--offline` to any evaluation command, or tick *Offline demo mode* in the app's sidebar.

## How to run

```bash
# tests (no API key)
python tests/test_validate.py    # validator + read-only connection
python tests/test_pipeline.py    # reply parsing, prompts, v3 examples, repair loop (fake LLM)
python tests/test_score.py       # result comparison and metrics
python eval/check_gold.py        # every gold query runs and returns rows

# one question end to end, from the cache
python src/pipeline.py v4 "How many orders were delivered?" --offline

# evaluation (--offline uses only the cache; the held-out test split needs --allow-test)
python eval/run_eval.py --version v4 --split dev --offline
python eval/run_eval.py --version v4 --split test --repeats 3 --allow-test --offline

# analysis (no API)
python eval/stats.py --split test
python eval/significance.py --split test
python eval/run_redteam.py --set all --payload-only
python eval/make_report_assets.py
python eval/export_assets.py

# app
streamlit run app/app.py
```

Note: `run_eval.py` writes a new results file on every run, and the reports use the newest file per version. Every command, in order, is in [docs/report/reproducibility.md](docs/report/reproducibility.md).

**Reproducibility.** The cached results reproduce: every model reply is saved in `logs/cache/`, so `--offline` gives the same SQL for every question without calling the API, and the stored results files are what every reported number is computed from. Re-executing that SQL offline can still give a different verdict on a busy machine, because each query is stopped after 10 seconds and a few correct queries take several seconds. In the last offline re-score (`python eval/rescore_offline.py`, output in `logs/recheck/offline_rescore_20261118.txt`), 731 of 760 stored verdicts matched; the other 29 timed out under load, or needed a repair call that a timeout triggers and that is not in the cache. Queries spot-checked on their own finished in 1.7–6.8 s.

The app opens at http://localhost:8501. Tabs: **Ask** (step-by-step pipeline view, edit and re-run the SQL), **Compare versions**, **Results dashboard** (reads `logs/results_*.csv`, with 95% intervals), **Safety** (newest file in `logs/redteam/`), **Schema and data**, **About**. The demo script is in [docs/demo_script.md](docs/demo_script.md).

## Repository layout

```
README.md            this file
CHANGELOG.md         dated changes, grouped by theme
prompts/             working prompt files v0.txt ... v5.txt, repair.txt, CHANGELOG.md (why each change was made)
  v1/ v2/ v3/        copies of each version's generate prompt (P1_generate.txt)
  final/             copies of the prompts the final pipeline (v4) uses: P1_generate.txt, P2_repair.txt
code/                README pointing to the code folders below (code is not duplicated), askbase_demo.ipynb (demo with saved outputs)
src/                 the pipeline: config, data load, schema, prompt builder, LLM call + cache, validator, read-only runner
eval/                test sets, scorer, evaluation runner, statistics, red team, review and report scripts
app/                 Streamlit demo (app.py + helpers), theme in .streamlit/
tests/               validator, pipeline and scorer tests (no API key needed)
test-data/           CSV copies of the test questions, saved outputs and red-team results (eval/make_test_data.py)
docs/                design, data notes, error taxonomy, limitations, responsible AI (draft), report assets
  diagrams/          Mermaid sources: prompt workflow, task decomposition, input-output flow, architecture
  report/            results.json, figures, abstract, prompt diff, reproducibility
review/              sheets for the team: gold_review(_test2).csv, labels_review(_test).csv, usability_sheet.csv
logs/                the evidence: call log, LLM cache, results, red-team runs, test outputs
data/raw/            Olist CSVs (you add these, not in git)
data/olist.db        SQLite database built by src/load_db.py (not in git)
```

What each code file does: [code/README.md](code/README.md). What each prompt folder holds: [prompts/README.md](prompts/README.md). Where each test-data file comes from: [test-data/README.md](test-data/README.md).

## Prompt versions

Full text: `prompts/` and [docs/report/prompts_appendix.md](docs/report/prompts_appendix.md). Why each change was made: [prompts/CHANGELOG.md](prompts/CHANGELOG.md). Diff with accuracy: [docs/report/prompt_diff.md](docs/report/prompt_diff.md).

| version | adds | schema given | examples | repair loop |
|---|---|---|---|---|
| v0 | control: question only | none | none | no |
| v1 | SELECT-only + CANNOT_ANSWER + answer format | table and column names | none | no |
| v2 | join keys + business rules | real CREATE TABLE | none | no |
| v3 | worked examples | real CREATE TABLE | 5 | no |
| v4 | repair with the exact error | real CREATE TABLE | 5 | yes, max 2 |
| v5 | *post-hoc, exploratory:* v3 + "do not approximate missing data" (test2 only) | real CREATE TABLE | 5 | no |

The final pipeline (v4) uses two prompts: the generate prompt (`prompts/v4.txt`, same text as v3) and the repair prompt (`prompts/repair.txt`), sent at most twice when the SQL is invalid, errors or returns no rows.

## Test data

`eval/test_set.json` has 60 questions in 6 tiers of 10: simple, join, aggregation, multi-step/fan-out, ambiguous, unanswerable/unsafe. 20 are the **dev** split (used to check the prompts) and 40 are the **held-out test** split, which needs `--allow-test` and was run only after the prompts were frozen. There was no training; "dev" plays the role of a validation set. The 5 v3 examples are separate questions, and `eval/check_gold.py` checks that they do not overlap with the test set.

`eval/test2_set.json` is a third, separate split of 20 new questions (`test2`). It exists only for the post-hoc v5 check: v5 was written after the test results were seen, so it is never run on the test split.

## Results

From `docs/report/results.json` (generated 2026-11-18 19:53 by `python eval/export_assets.py`). Execution accuracy with a 95% bootstrap interval over questions. Provisional until the gold set is verified.

<!-- results:start -->
| version | dev exec. (n=20, 1 run) | dev strict | test exec. (n=40, 3 repeats) | test strict | test exec., gpt-oss-20b (1 run) | test strict, gpt-oss-20b |
|---|---|---|---|---|---|---|
| v0 | 15.0% [0.0–30.0] | 15.0% [0.0–30.0] | 7.5% [0.0–17.5] | 7.5% [0.0–17.5] | not run | not run |
| v1 | 55.0% [35.0–75.0] | 50.0% [30.0–70.0] | 81.7% [69.2–92.5] | 66.7% [52.5–80.8] | 57.5% [42.5–72.5] | 45.0% [30.0–60.0] |
| v2 | 90.0% [75.0–100.0] | 80.0% [60.0–95.0] | 80.8% [69.2–90.8] | 61.7% [47.5–75.8] | 82.5% [70.0–92.5] | 62.5% [47.5–77.5] |
| v3 | 90.0% [75.0–100.0] | 75.0% [55.0–90.0] | 88.3% [78.3–96.7] | 62.5% [47.5–76.7] | 92.5% [82.5–100.0] | 67.5% [52.5–82.5] |
| v4 | 90.0% [75.0–100.0] | 75.0% [55.0–90.0] | 88.3% [78.3–96.7] | 62.5% [47.5–76.7] | 95.0% [87.5–100.0] | 70.0% [55.0–82.5] |
| v0 lenient extractor | 15.0% [0.0–30.0] | 15.0% [0.0–30.0] | 10.0% [2.5–20.0] | 10.0% [2.5–20.0] | – | – |

Strict accuracy also requires exactly the gold number of columns; the gap to execution accuracy is answers with the right rows plus extra columns (for example a count next to the name asked for).

Post-hoc check on 20 new questions (test2), v5 = v3 + "do not approximate missing data". Written after the test results were seen, so it is exploratory and not part of the main comparison:

| version | test2 exec. (n=20) | test2 strict |
|---|---|---|
| v2 (post-hoc, exploratory) | 90.0% [75.0–100.0] | 75.0% [55.0–95.0] |
| v3 (post-hoc, exploratory) | 85.0% [70.0–100.0] | 70.0% [50.0–90.0] |
| v5 (post-hoc, exploratory) | 90.0% [75.0–100.0] | 75.0% [55.0–90.0] |
<!-- results:end -->

- **Significance** (paired exact McNemar, Holm-corrected, test split): v0 against each of v1–v4 is significant (p_holm = 0.0); every comparison among v1–v4 has p_holm = 1.0, so 40 questions cannot separate them. v3 and v4 have identical scores: the repair loop fired once on the test split (M03) and did not change the outcome.
- **Refusals (test):** refusal recall v1 100.0%, v2 83.3%, v3 100.0%, v4 100.0%; over-refusal 0.0% for all of them.
- **Red team (18 attacks):** through the full v4 pipeline all 18 were stopped (16 by the model's own reply, 1 by the validator, 1 by the 200-row limit), prompt text leaked in 0 replies, and no table row count changed. Sent directly, skipping the model, the validator alone blocked 15 of 18 and the read-only connection alone 15 of 18.
- 762 live API calls (914,124 tokens) were made in total; every reply is cached in `logs/cache/`.

Figures: `docs/report/figures/` (SVG + PNG). Every number: `docs/report/results.json`.

More: [abstract](docs/report/abstract.md), [dev vs test reversal](docs/report/dev_test_reversal.md), [limitations](docs/limitations.md), [failure examples](docs/report/failure_examples.md), [v0 strict vs lenient](docs/report/v0_baseline.md), [responsible AI (draft)](docs/responsible_ai.md).

## Notes

- Gold SQL in `eval/test_set.json` is a first draft. Every item has `verified: false` until a team member checks it (`review/gold_review.csv`, then `python eval/read_review.py`).
- Error labels in `logs/error_labels_*.csv` are drafts ("claude draft - team to confirm"); none is confirmed yet.
- Two business-rule definitions (which orders count as sales, and what "revenue" means) are assumptions, listed in `prompts/CHANGELOG.md`.
- Facts about the data, each checked by a query, are in `docs/data_notes.md`.
- Changes to the validator after a red-team run go in `docs/validator_changelog.md` as v-next.
