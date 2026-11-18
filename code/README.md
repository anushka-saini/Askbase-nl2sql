# Code

The code is not copied here. It lives in four folders at the repo root, so every script keeps its
current paths. Run everything from the repo root with the virtual environment active.

| folder | what is in it | how to run |
|---|---|---|
| [`src/`](../src) | the pipeline: settings (`config.py`), database load (`load_db.py`), schema reader (`schema.py`), prompt builder (`build_prompt.py`), Groq call + cache + call log (`llm.py`), SQL validator (`validate.py`), read-only runner (`run_sql.py`), one question end to end incl. the repair loop (`pipeline.py`), data checks (`data_checks.py`) | `python src/load_db.py` (build `data/olist.db` once)<br>`python src/pipeline.py v4 "How many orders were delivered?" --offline` |
| [`eval/`](../eval) | test sets (`test_set.json`, `test2_set.json`), scorer (`score.py`), evaluation runner (`run_eval.py`), statistics (`stats.py`, `significance.py`), error sheets (`error_report.py`), red team (`run_redteam.py`), review and report scripts | `python eval/run_eval.py --version v4 --split dev --offline`<br>`python eval/stats.py --split test` |
| [`app/`](../app) | Streamlit demo: `app.py` (tabs), `data.py` (reads logs and test set), `ui.py` (layout helpers) | `streamlit run app/app.py` (tick *Offline demo mode* to use only cached answers) |
| [`tests/`](../tests) | validator, pipeline and scorer tests; no API key needed | `python tests/test_validate.py`<br>`python tests/test_pipeline.py`<br>`python tests/test_score.py` |

## Demo notebook

[`askbase_demo.ipynb`](askbase_demo.ipynb) shows the final pipeline (v4) on real cached runs, with every output saved
in the file, so it can be read on GitHub or in Colab without running anything: the architecture, the two final prompts
(`prompts/final/`), six held-out test questions (two Normal, two Edge, two Invalid, one of them a real failure) with
their SQL, validation status, rows and pass/fail against gold, real red-team attacks and the layer that stopped each,
and the results table from `docs/report/results.json`. It replays cached answers only (no API calls, nothing written
to `logs/calls.csv`). Re-running it needs `data/olist.db`, which is not in the repo because of its size.

## Notes

- The API key is read only from the `GROQ_API_KEY` environment variable (or a local `.env`, see `.env.example`).
  Without a key, add `--offline` and every answer comes from `logs/cache/`.
- The held-out test split needs `--allow-test`. The full ordered list of commands is in
  [docs/report/reproducibility.md](../docs/report/reproducibility.md).
- The tests write their output to `logs/test_*.txt`.
