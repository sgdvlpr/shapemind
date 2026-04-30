**Declutter your mind. Master your tasks.**

A Windows-native CLI task manager with Persian calendar support. Add, edit, delete, and review tasks — all from your terminal. No accounts. No setup fuss. Just your tasks, your way.

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

# Add your first task
shapemind task add "Review pull requests" --due tomorrow

# See what's waiting
shapemind task list

# Mark it done
shapemind task update a3b5 --status done

# Add a task with Persian date
shapemind task add "تکمیل پروژه" --due 1404-10-15

# Show only urgent tasks
shapemind task list --status todo --before tomorrow
