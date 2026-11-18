# data/raw_gz

Gzipped copies of the 9 Olist CSV files (about 42 MB in total), so the app can build `data/olist.db` where the
database itself is not available, for example on Streamlit Community Cloud. The database is not in git because it is
too large (about 169 MB).

- Written by `python src/load_db.py --pack` from `data/raw/`.
- `python src/load_db.py` uses `data/raw/` if it is there, otherwise these files. The Streamlit app runs it once on
  first start when `data/olist.db` is missing.
- A database built from these files has the same rows and the same schema text as one built from `data/raw/`, so the
  cached model replies in `logs/cache/` still match.

**Source and credit:** Brazilian E-Commerce Public Dataset by Olist, Kaggle (`olistbr/brazilian-ecommerce`).
Licence: to be confirmed on the Kaggle page (a secondary source lists CC BY-NC-SA 4.0, which requires credit and
non-commercial use). See `docs/responsible_ai.md`.
