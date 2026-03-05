# USMT TUI for Windows

This repository now contains a terminal-based USMT wrapper inspired by the
`UsmtGui10` workflow, but designed for Windows terminals.

## What it does

- Builds and runs `scanstate.exe` commands for capture.
- Builds and runs `loadstate.exe` commands for restore.
- Lets you manage common USMT options in an interactive TUI-style menu.
- Saves your settings to `usmt_tui_config.json` for reuse.

## Run

```powershell
python usmt_tui.py
```

## Notes

- This tool assumes USMT is already installed (for example through ADK).
- Default USMT path is `C:\Program Files\USMT` and can be changed in settings.
- User include/exclude syntax:
  - `*` = all users
  - `alice,bob` = include those users
  - `!tempuser` = exclude a user

## Example flow

1. Open tool.
2. Edit settings (paths, XML files, switches).
3. Preview generated commands.
4. Run ScanState on source machine.
5. Run LoadState on destination machine.
