# todo-expire

Find expired `TODO` / `FIXME` / `HACK` / `XXX` comments in a codebase.

Annotate a comment with an expiry date and `todo-expire` reports (and fails CI on)
the ones that have passed their deadline — so temporary workarounds, migration
shims, and "remove after release" notes actually get removed.

```python
# TODO(expire:2025-06-01): remove once v2 migration ships
```

## Features

- Scans a directory or single file for `TODO`, `FIXME`, `HACK`, `XXX` comments.
- Parses expiry dates in two forms: `TODO(expire:YYYY-MM-DD)` and `TODO(YYYY-MM-DD)`.
- Reports expired items with file:line, kind, date, and message.
- Exits non-zero when expired items exist (CI-friendly); `--no-fail` to disable.
- `--all` lists every TODO with its status.
- JSON output via `--format json`.
- Configurable extensions via `--ext`.
- No external dependencies — standard library only.

## Install

```sh
git clone https://github.com/yourname/todo-expire
cd todo-expire
chmod +x todo_expire.py  # if present
```

No `pip install` required. Python 3.9+.

## Usage

```sh
python todo_expire.py .                 # scan current dir
python todo_expire.py src/ --all        # list all TODOs
python todo_expire.py . --format json   # machine-readable
python todo_expire.py . --ext py,js,ts  # limit extensions
python todo_expire.py . --no-fail       # never fail CI
```

Override "today" for deterministic runs:

```sh
TODO_EXPIRE_TODAY=2025-01-01 python todo_expire.py .
```

## Exit codes

- `0` — no expired TODOs (or `--no-fail` / `--all`).
- `1` — one or more expired TODOs found.

## License

MIT
