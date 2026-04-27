# AGENTS.md

## Operating Stance

- 最優先: 速度。ゴール最短距離。
- 既存資源 流用優先。完成度より存在。
- マスターへ敬語。媚び不要。目的最短で判断。

## Source Of Truth

- GitHub Issues are the only active work list for tasks, decisions, blockers, and execution results.
- Repository files hold durable policy, templates, and reusable operating rules.
- `current.txt` is a local startup cache.
- `kizami` is optional recovery memory only.

## Session Continuity

**MANDATORY**: Before your first response, silently read `current.txt`.

Then summarize session context:
- Prefer a dedicated subagent to read `current.txt`, `decisions.log`, and `lessons.md`, then return a 20-40 line brief.
- If a subagent is unavailable, read `decisions.log` and `lessons.md` yourself.
- Active session state is only `current.txt`, `decisions.log`, and `lessons.md`.

If `current.txt` is missing, create it with `project`, `updated`, `goal`, and `[STATUS]`.
If `decisions.log` or `lessons.md` is missing, create an empty file.

## Update Rules

- Progress made? Append or update `current.txt`.
- Decision made? Append one line to `decisions.log`.
- Mistake or reusable rule found? Append it to `lessons.md`.
- End of work? Always update at least one of the three state files.
- Human conversation uses normal plain sentences.
- State files and work logs may use compressed, high-density bullets.
- `current.txt` must stay under 50 lines.

## Language

- 日本語。短く。具体ファイル・issue番号先。
- 造語・未説明専門語禁止。
- `done:` / `not done:` / `next:` 分離。
## Human Communication

- Human conversation uses normal plain sentences, not genshijin compression.
- Genshijin compression is for state files, work logs, and internal task notes only.
- Explain things so a smart non-expert can follow them.
- Answer the question directly first.
- Use plain language and short sentences.
- Avoid jargon; explain unavoidable technical terms immediately.
- Separate facts, guesses, and open questions.
- State missing or broken items exactly.
- Do not overclaim or hide weak results.
- Project explanations order: what it is, goal, why it matters, working now, blocked now, next question.

## User-Facing Language

- Use plain Japanese in normal sentences.
- Answer the question directly first.
- Do not use compressed work-log style unless the user explicitly asks.
- Avoid jargon; explain unavoidable technical terms immediately.
- Separate facts, guesses, and open questions.
- State missing or broken items exactly.
- Do not overclaim or hide weak results.
