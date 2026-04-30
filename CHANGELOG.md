# Changelog

## [1.0.0] - 2026-04-30

### Added
- Task management (add, list, update, delete)
- Gregorian and Persian support
- Configuration system (`shapemind config`)
- Color-coded output with `rich` library
- Short unique IDs for tasks
- SQLite database for persistance

## [1.0.1] - 2026-04-30

### Fixed
- The parse_date function in shapemind/date_utils.py could now resolve date string in correct calendar.
