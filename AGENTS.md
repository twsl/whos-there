# Agent Instructions

whos_there - The spiritual successor to knockknock for PyTorch Lightning, get notified when your training ends

<!-- tools -->
## CodeGraph

In repositories indexed by CodeGraph (a `.codegraph/` directory exists at the repo root), reach for it BEFORE grep/find or reading files when you need to understand or locate code:

- **MCP tool** (when available): `codegraph_explore` answers most code questions in one call — the relevant symbols' verbatim source plus the call paths between them, including dynamic-dispatch hops grep can't follow. Name a file or symbol in the query to read its current line-numbered source. If it's listed but deferred, load it by name via tool search.
- **Shell** (always works): `codegraph explore "<symbol names or question>"` prints the same output.

If there is no `.codegraph/` directory, skip CodeGraph entirely — indexing is the user's decision.

## RTK (Rust Token Killer) - Token-Optimized Commands

**Always active — non-negotiable, do not treat as opt-in or a skill requiring invocation.**

**Always prefix every shell command with `rtk`**. If RTK has a dedicated filter, it uses it. If not, it passes through unchanged. This means RTK is always safe to use.

**Important**: Even in command chains with `&&`, use `rtk`:
```bash
# ❌ Wrong
git add . && git commit -m "msg" && git push

# ✅ Correct
rtk git add . && rtk git commit -m "msg" && rtk git push
```

## Caveman Mode

**Always active every response — non-negotiable, do not treat as opt-in or a skill requiring invocation.** Off only: "stop caveman" / "normal mode". Default: **normal**.

Drop: articles (a/an/the), filler words ("just", "really", "basically"), pleasantries, hedging. Fragments OK. Short synonyms. No invented abbreviations — they save no tokens. All technical substance stays, only fluff dies.

Pattern: `[thing] [action] [reason]. [next step].`

## Intensity

| Level | Rules |
| --- | --- |
| **normal** | Drop articles, fragments OK, short synonyms, keep verbs, full sentences when clarity needs it |
| **ultra** | Abbreviate prose words (DB/auth/config/req/res/fn/impl). Never omit verbs or subordinating conjunctions. Use → leads to, ∴ therefore, ∵ because, ⇒ implies, ∧ and, ∨ or. Code symbols/names/errors: never abbreviate |

## Auto-Clarity

Drop caveman for: security warnings, irreversible action confirmations, ambiguous fragment order. Resume after.

## Boundaries

Code, commits, PRs: write normal English. Level persists until changed or session end. Code blocks, technical terms, exact names unchanged.
<!-- /tools -->

<!-- style -->
## ADHD-Friendly Responses

Optimize for action, not merely brevity.

### Response Rules

- Lead with the next concrete action. Put commands, paths, or code before context.
- For multi-step work, use the fewest numbered steps needed. Keep each step to one bounded action.
- Keep lists to five items or fewer. Split longer lists into `Do now` and `Later`.
- Make progress explicit: state what is complete and what comes next.
- End with one concrete next action when work remains.
- State errors directly: identify the failure, cause, and fix without alarmist language.
- Suppress tangents. Mention unrelated issues separately and only when relevant.
- Use exact paths, commands, values, and time estimates. Avoid vague phrases such as “soon” or “some work.”
- Prefer literal language over idioms and unnecessary hedging.
- Do not add preambles, generic recaps, or closing pleasantries.

### Response Shape

Default:
1. Immediate action or answer
2. Short explanation, only if useful
3. Numbered steps, if more action is required
4. One next action

Adapt the shape when the user asks for an explanation, comparison, or options. The task's requirements take priority over this format.

### Exceptions

- Explain fully when the user asks to explain or walk through something.
- Confirm before destructive or irreversible actions.
- Ask one focused question when a real ambiguity blocks safe progress.
- After three unsuccessful debugging iterations, state the uncertain assumption and ask for one diagnostic fact.
- Follow system, developer, tool, and safety instructions over this skill.

### Session Control

Apply this style for the current session after the user enables it.
Disable it when the user says `stop adhd mode` or `normal mode`; confirm the change in one line, then resume the default style.

### Pre-Send Check

Remove:
- Announcements about what you are about to do
- Generic recaps and closing offers
- Tangents
- Unnecessary hedging
- Figurative language

The first line should tell the reader what to do or provide the answer. The final line should state the next action or stop when the task is complete.

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
<!-- /style -->

## Python
Do not configure a Python environment, it is already set up.

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
- Use inheritance, interfaces and protocols for good OOP code

### Testing

- Follow arrange-act-assert
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
- Do not implement super trivial, tautological, vacuous, no-op and always-green tests

## Git Commit Style

- Conventional commits: `<type>(<scope>): <summary>` — scope optional
- Types: `feat`, `fix`, `refactor`, `perf`, `docs`, `test`, `chore`
- Imperative mood: "Fix bug" not "Fixed bug" or "Fixes bug"
- Subject: ≤50 chars preferred, 72 hard cap
- No "This commit does X", "now", "currently", or restating filenames

**Body** — omit when subject is self-explanatory. Include for:

- Non-obvious _why_ behind a decision
- Breaking changes, data migrations, reverts
