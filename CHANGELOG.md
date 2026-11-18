# Changelog

Dates are derived from evidence in the repo only: file modification times, the timestamps in `logs/calls.csv`
(one row per model call), the run times written inside log files (for example `logs/data_checks.txt`), the
timestamp in each results file name, and the dated entries already in `prompts/CHANGELOG.md`. A modification time
shows when a file was last changed, so some work may have started earlier than the date shown. No evidence in
the repo is older than 2026-10-30, so nothing is listed before that date.

Prompt-level detail is in [prompts/CHANGELOG.md](prompts/CHANGELOG.md); validator changes after a red-team run go in
[docs/validator_changelog.md](docs/validator_changelog.md).

## Data

- **2026-10-30**: Olist CSVs loaded into SQLite (`src/load_db.py`, `data/olist.db`). 36 data checks written
  (`src/data_checks.py`) and run; output in `logs/data_checks.txt` (run 2026-10-30 23:57:42). Facts written up in
  `docs/data_notes.md`, each citing its check (customer_id is one per order, items × payments fan-out, Portuguese
  category names, zip-prefix fan-out in geolocation).
- **2026-10-31**: settings in one place (`src/config.py`) and a schema reader (`src/schema.py`) that builds the
  `CREATE TABLE` and names-only schema text from the database.

- **2026-11-18**: gzipped copies of the 9 CSVs in `data/raw_gz/` (`python src/load_db.py --pack`). `load_db.py`
  builds from them when `data/raw/` is missing, into a temporary file first. A database built this way has the same
  schema text and the same rows in 8 of 9 tables; `geolocation` latitude/longitude differ only in the last binary
  digit (at most 1.4e-14) from the existing local file, and no gold query uses that table.

## Safety

- **2026-10-31**: SQL validator (`src/validate.py`): one statement, SELECT or WITH first, no comments, no write or
  admin keywords, no `sqlite_*` / `pragma_*` objects, only existing tables. Read-only runner (`src/run_sql.py`):
  `mode=ro`, `PRAGMA query_only`, an authorizer that allows only reads, row and time limits. Tests in
  `tests/test_validate.py`.
- **2026-11-08**: validator hardened and locked-file retries added to the runner (`src/run_sql.py`, last changed
  2026-11-08).
- No validator change has been made after a red-team run (`docs/validator_changelog.md`, v-next is empty).

## Prompts

- **2026-11-08**: prompt versions v0–v4 and `repair.txt` written; v4 has the same text as v3 and adds the repair loop
  (max 2). Prompts frozen before the held-out test runs (`prompts/CHANGELOG.md`).
- **2026-11-09**: `prompts/v5.txt` written after the test results were seen (v3 + "do not approximate missing data").
  Post-hoc and exploratory; only run on the separate `test2` questions. v0–v4 unchanged.
- **2026-11-18**: copies of the prompts in `prompts/v1/`, `prompts/v2/`, `prompts/v3/` and `prompts/final/`
  (`P1_generate.txt`, `P2_repair.txt`), with `prompts/README.md`. The working files are unchanged.

## Evaluation

- **2026-11-08**: 60-question test set in 6 tiers, 20 dev / 40 held-out test (`eval/test_set.json`); gold check run
  (`logs/gold_check.txt`, 2026-11-08 13:26:44). Scorer (`eval/score.py`, execution and strict accuracy), evaluation
  runner, significance test and error report. First live model call 2026-11-08 14:13:31 (`logs/calls.csv`). Dev runs
  of v0–v4 (`logs/results_v*_dev_20261108-*.csv`); held-out test runs of v0, v1, v2 (3 repeats) and the gpt-oss-20b
  check of v1–v4 (`logs/results_*_test_*20261108-*.csv`).
- **2026-11-09**: lenient extractor for the v0 baseline analysis only (`logs/lenient/`, files from 2026-11-09).
  95% confidence intervals (`eval/stats.py`), generated limitations (`docs/limitations.md`). Review sheets for gold
  queries and draft error labels (`review/`). 20 `test2` questions (`eval/test2_set.json`, written by
  `eval/make_test2.py`), dev-vs-test reversal analysis (`eval/reversal.py`), usability sheet scripts.
- **2026-11-09 to 2026-11-10**: held-out test runs of v3 (`results_v3_test_20261109-233548.csv`) and v4
  (`results_v4_test_20261109-233843.csv`), significance tests, draft test error labels (`logs/error_labels_test.csv`).
  test2 runs of v2, v3 and v5 (`logs/test2/`); last live call 2026-11-10 05:10:10 (`logs/calls.csv`).
- **2026-11-10**: report exports (`eval/export_assets.py`): `docs/report/results.json`, figures,
  `logs/per_question_test.csv`. Fix: test2 intervals were not picked up in the export.
- **2026-11-18**: `test-data/` with plain CSV copies of the questions, saved outputs and red-team results
  (`eval/make_test_data.py`).

## Red team

- **2026-11-08**: red-team runner (`eval/run_redteam.py`) and the first 10 attacks (`docs/redteam.json`).
- **2026-11-09**: 8 more attacks (RT11–RT18; `docs/validator_changelog.md`). Payload-only run of all 18 against each
  layer (`logs/redteam/redteam_all_payload-only_20261109-001402.csv`), then all 18 through the full v4 pipeline
  (`logs/redteam/redteam_all_v4_20261109-234439.csv`).

## App

- **2026-11-08**: Streamlit demo (`app/`, theme in `.streamlit/config.toml`) with Ask, Compare versions, Results
  dashboard, Safety, Schema and data, and About tabs; offline demo mode uses only cached answers.
- **2026-11-18**: the app builds `data/olist.db` from `data/raw_gz/` on first start when the database is missing
  (for Streamlit Community Cloud), and shows team AskBase in the header.
- **2026-11-09**: app updated (`app/app.py`, `app/data.py`, `app/ui.py` last changed 2026-11-09), including v5 in the
  version colours.

## Docs

- **2026-11-08**: architecture notes and error taxonomy (`docs/architecture.md`, `docs/error_taxonomy.md`).
- **2026-11-09**: design doc (`docs/design.md`), responsible-AI draft (`docs/responsible_ai.md`), contribution log
  template (`docs/contribution_log.md`).
- **2026-11-10**: report assets regenerated after the last runs (`docs/report/*.md`, `docs/demo_script.md`) and the
  README results block.
- **2026-11-18**: `code/README.md`, this changelog, Mermaid diagrams in `docs/diagrams/`, README restructured.
