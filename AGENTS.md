# Agent Instructions

whos_there - The spiritual successor to knockknock for PyTorch Lightning, get notified when your training ends

## Core Decision Ladder

Before writing anything, climb these rungs in order:

1. Already in the codebase? → **Reuse it**
2. Standard library covers it? → **Use it**
3. Native platform feature? → **Use it**
4. Installed dependency works? → **Use it**
5. Can it be one line? → **Do it**
6. Is it really needed at all? → **YAGNI but carefully**
7. Only then write the minimum that works

## Key Principles

- "Boring over clever" — predictability beats ingenuity
- "Prefer deletion over addition" — less code, fewer problems
- "Shortest working diff wins once you understand the problem"
- Bug fixes target root cause, not symptoms — one fix where all callers converge
- Abstractions when the same concept appears in 2+ places — name the concept, not the callers

## What You Never Skip

Validation, error handling, security, accessibility, and data-loss protection are **non-negotiable**. Neither is actually understanding the problem first.

## Delivery Pattern

Ship the lean version, then flag what was omitted: _"Did X. Y covers it. Need full X? Say so."_ If the user confirms they want more — build it, no debate.

---

## Caveman Mode

Speak like caveman. Drop articles, filler words ("just", "really", "basically"), and redundant phrasing. Use fragments. No invented abbreviations — they don't save tokens.

Pattern: `[thing] [action] [reason]. [next step].`

- Code blocks, technical terms, and exact names stay unchanged
- Auto-suspend for: security warnings, irreversible action confirmations — resume after

---

## Python Style

### Toolchain

- Package/run: `uv` — no venv activation, use `uv run <cmd>` and `uv add <pkg>`
- Lint/format: `ruff` — run `ruff check` and `ruff format`
- Type-check: `ty` — run `ty check`

### File & Folder Layout

- One class per file; filename matches class name in snake_case
- Group related classes in a folder with an `__init__.py` that re-exports them
- Flat is fine until 3+ related classes exist — then make a folder

### Code Conventions

- Only write comments when they add value beyond the code itself like justifying a design choice or explaining a non-obvious implementation detail
- Type-annotate all function signatures
- Prefer `pathlib.Path` over `os.path`
- Prefer dataclasses or `typing.NamedTuple` over plain dicts for structured data
- No `# type: ignore` without a comment explaining why

### Testing

- Use `pytest`; name test files `test_<module>.py`
- Use `pytest.mark.parametrize` for multiple input cases
- Use `pytest-mock` only at true external boundaries (filesystem, network, subprocesses) — never mock internal code
- **Don't test the obvious** — no tests for getters, constructors, or trivial assignments; test behavior, invariants, and error paths
- Prefer `conftest.py` fixtures over helper modules imported across test files — shared setup belongs in fixtures, not `test_utils.py`
- Layer tests by scope:
  - **Unit**: pure functions, edge cases, error paths — fast, no I/O
  - **Integration**: component interactions with real data (e.g., actual COCO annotation dicts, real RLE masks)
  - **E2E**: full pipeline from raw JSON → evaluation result; run against a known small COCO subset
- Tests against real domain data are preferred over hand-crafted stubs when the logic is non-trivial

---

## Git Commit Style

- Conventional commits: `<type>(<scope>): <summary>` — scope optional
- Types: `feat`, `fix`, `refactor`, `perf`, `docs`, `test`, `chore`
- Imperative mood: "Fix bug" not "Fixed bug" or "Fixes bug"
- Subject: ≤50 chars preferred, 72 hard cap
- No "This commit does X", "now", "currently", or restating filenames

**Body** — omit when subject is self-explanatory. Include for:

- Non-obvious _why_ behind a decision
- Breaking changes, data migrations, reverts

---

<!-- CODEGRAPH_START -->

## CodeGraph

In repositories indexed by CodeGraph (a `.codegraph/` directory exists at the repo root), reach for it BEFORE grep/find or reading files when you need to understand or locate code:

- **MCP tool** (when available): `codegraph_explore` answers most code questions in one call — the relevant symbols' verbatim source plus the call paths between them, including dynamic-dispatch hops grep can't follow. Name a file or symbol in the query to read its current line-numbered source. If it's listed but deferred, load it by name via tool search.
- **Shell** (always works): `codegraph explore "<symbol names or question>"` prints the same output.

If there is no `.codegraph/` directory, skip CodeGraph entirely — indexing is the user's decision.

<!-- CODEGRAPH_END -->
