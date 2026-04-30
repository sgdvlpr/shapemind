**Declutter your mind. Master your tasks.**

A CLI task manager with Persian calendar support. Add, edit, delete, and review tasks — all from your terminal. No accounts. No setup fuss. Just your tasks, your way.

## Why Shapemind?

Unlike generic task managers, Shapemind is built for **developers and terminal lovers** who need:

- ✅ **Persian (Jalali) calendar** support — because not everyone lives on the Gregorian calendar
- ✅ **Lightning fast** — no waiting for web apps to load
- ✅ **Local-first** — your data stays in a local SQLite database. Private by default
- ✅ **Simple CLI** — intuitive commands that just work
- ✅ **Beautiful output** — color-coded tables with the `rich` library

## Installation

### From source (recommended)

```bash
git clone https://github.com/sgdvlpr/shapemind.git
cd shapemind
pip install -e .

```

## Dependencies (installed automatically)
`typer` — CLI framework

`rich` — beautiful terminal formatting

`jdatetime` — Persian calendar support

`tabulate` — Clean table layouts for task lists

## Quick Start

**Add your first task:**
```bash
shapemind task add "Review pull requests" --due tomorrow
```

**See what's waiting:**
```bash
shapemind task ls
```

**Add a task with Persian date**
```bash
shapemind task add "تکمیل پروژه" --due 1404-10-15
```

**Show only urgent tasks**
```bash
shapemind task ls --status todo --before tomorrow
```

## Command Reference

| Command | Description |
|---------|-------------|
| `shapemind task add "Title" --due tomorrow` | Add a new task |
| `shapemind task ls` | Show all tasks |
| `shapemind task ls --status todo` | Show only todo tasks |
| `shapemind task ls --status done` | Show completed tasks |
| `shapemind task ls --on 2026-10-10` | Show tasks due on a specific date |
| `shapemind task update a3b5 --status done` | Mark a task complete |
| `shapemind task update a3b5 --title "New Title"` | Change task title |
| `shapemind task delete a3b5` | Delete a single task |
| `shapemind task delete --all` | Delete ALL tasks |
| `shapemind config` | Show current calendar |
| `shapemind config persian` | Switch to Persian calendar |
| `shapemind config gregorian` | Switch to Gregorian calendar |

## Data Storage
Shapemind uses SQLite for persistence. Your tasks are stored in shapemind.db in the directory you run the command from.

- No cloud dependency
- No sign-up required
- Your data, your machine

## Development
Run without installing
```bash
python -m shapemind.cli task ls
```

Install in editable mode (changes reflect immediately)
```bash
pip install -e .
```

## Configuration

| Command | Description |
|---------|-------------|
| `shapemind config` | Show current calendar setting |
| `shapemind config persian` | Switch to Persian (Jalali) calendar |
| `shapemind config gregorian` | Switch to Gregorian calendar |

## Date Formats

| Input | Meaning | Example |
|-------|---------|---------|
| `today` | Current day | `--due today` |
| `tomorrow` | Next day | `--due tomorrow` |
| `YYYY-MM-DD` (Persian) | Persian calendar date | `--due 1404-10-15` |
| `YYYY-MM-DD` (Gregorian) | Gregorian date | `--due 2026-06-05` |

> **Smart parsing:** Shapemind automatically detects which calendar you're using. Mix them freely.

## Example Output

Run `shapemind task ls --status todo`:

| ID | Title | Due | Status |
|----|-------|-----|--------|
| a | Review PRs | 2026-05-09 | todo |
| f | Deploy to production | 2026-05-15 | todo |
| k | Write documentation | 2026-05-23 | todo |

## Roadmap
- Tagging and grouping tasks
- Export/import (JSON, CSV)
- Sharing tasks via encrypted links (could expire within a certain time)
- Recurring tasks
- Notifications (Windows toast)

## 📄 License

MIT License — free for personal and commercial use.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


