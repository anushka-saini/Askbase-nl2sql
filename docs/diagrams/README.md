# Diagrams

Mermaid sources (`.mmd`) for four views of the system. Each one follows the code it names, so check the code
first if you change a diagram. The `.svg` and `.png` files next to them are renders of the same sources.

| file | shows | follows |
|---|---|---|
| `prompt_workflow.mmd` | the final pipeline's two prompts: generate (P1) and repair (P2), and when the repair loop runs | `src/build_prompt.py`, `src/pipeline.py` (`run_question`, `MAX_REPAIRS = 2`), `prompts/final/` |
| `task_decomposition.mmd` | which sub-tasks the model does and which are plain code | `src/schema.py`, `src/validate.py`, `src/run_sql.py`, `app/app.py`, `eval/score.py` |
| `input_output_flow.mmd` | inputs (question, prompt version, database, API key) and every output file | `src/pipeline.py`, `src/llm.py`, `eval/run_eval.py`, `eval/export_assets.py` |
| `system_architecture.mmd` | the three safety layers (prompt rules, validator, read-only connection) and the v4 repair loop | `src/validate.py`, `src/run_sql.py`, `src/llm.py`, `src/pipeline.py` |

The older hand-drawn overview is `docs/architecture.svg` (described in `docs/architecture.md` and `docs/design.md`).

## Rendering

Any Mermaid renderer works, for example the Mermaid Live Editor or GitHub's Markdown preview (paste the source into a
```` ```mermaid ```` block). The renders here were made offline with the Mermaid build that ships inside the installed
`streamlit` package, run in a headless browser.
