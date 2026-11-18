# Prompts

The working prompt files are the flat files in this folder: `v0.txt` ... `v5.txt` and `repair.txt`.
The code loads them by name (`src/build_prompt.py`), so they are the ones to edit.
The full history and the reason for every change is in [CHANGELOG.md](CHANGELOG.md).

The subfolders hold **copies**, so each version can be read on its own:

| folder | file | copy of | used for |
|---|---|---|---|
| `v1/` | `P1_generate.txt` | `v1.txt` | names-only schema + basic rules |
| `v2/` | `P1_generate.txt` | `v2.txt` | real `CREATE TABLE` text + join keys + business rules |
| `v3/` | `P1_generate.txt` | `v3.txt` | v2 + 5 worked examples |
| `final/` | `P1_generate.txt` | `v4.txt` (same text as `v3.txt`) | first SQL answer in the final pipeline |
| `final/` | `P2_repair.txt` | `repair.txt` | sent only when the SQL is invalid, errors or returns no rows (max 2 times) |

The final pipeline is version **v4**: one generate prompt, plus the repair prompt in a loop
(`src/pipeline.py`, `MAX_REPAIRS = 2`). Blocked (unsafe) SQL and refusals are never sent for repair.

`v0.txt` (question only, the control) and `v5.txt` (v3 + one rule, post-hoc, only run on `eval/test2_set.json`)
have no subfolder.

If you change a working file, copy it again here so the two stay the same.
