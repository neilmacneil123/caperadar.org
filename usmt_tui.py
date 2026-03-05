#!/usr/bin/env python3
"""USMT TUI for Windows.

A terminal user interface inspired by GUI wrappers around Microsoft's
User State Migration Tool (USMT) `scanstate.exe` and `loadstate.exe`.
"""

from __future__ import annotations

import json
import os
import shlex
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import List

APP_NAME = "USMT TUI"
CONFIG_FILE = Path("usmt_tui_config.json")


@dataclass
class UsmtProfile:
    usmt_bin: str = r"C:\Program Files\USMT"
    migration_store: str = r"C:\USMT\Store"
    include_xml: List[str] = field(
        default_factory=lambda: ["MigDocs.xml", "MigApp.xml", "MigUser.xml"]
    )
    extra_switches: List[str] = field(default_factory=list)
    log_path: str = r"C:\USMT\Logs\usmt.log"
    progress_log_path: str = r"C:\USMT\Logs\progress.log"
    temp_store: str = r"C:\USMT\Temp"
    hardlink: bool = False
    continue_on_non_fatal: bool = True
    copy_raw: bool = False
    target_windows: str = r"C:\Windows"
    users: str = "*"
    domain: str = ""
    local_only: bool = False
    offline_scan: bool = False


def clear() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def pause(msg: str = "Press Enter to continue...") -> None:
    input(msg)


def load_profile() -> UsmtProfile:
    if CONFIG_FILE.exists():
        try:
            data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
            return UsmtProfile(**data)
        except Exception:
            return UsmtProfile()
    return UsmtProfile()


def save_profile(profile: UsmtProfile) -> None:
    CONFIG_FILE.write_text(json.dumps(asdict(profile), indent=2), encoding="utf-8")


def quote_args(args: List[str]) -> str:
    return " ".join(shlex.quote(arg) for arg in args)


def tool_path(profile: UsmtProfile, tool_name: str) -> str:
    return str(Path(profile.usmt_bin) / tool_name)


def build_common_args(profile: UsmtProfile) -> List[str]:
    args = []
    for xml in profile.include_xml:
        args.append(f"/i:{xml}")

    args.append(f"/l:{profile.log_path}")
    args.append(f"/progress:{profile.progress_log_path}")

    if profile.continue_on_non_fatal:
        args.append("/c")
    if profile.copy_raw:
        args.append("/copyraw")
    if profile.hardlink:
        args.extend(["/hardlink", "/nocompress"])

    args.extend(profile.extra_switches)
    return args


def build_scanstate_command(profile: UsmtProfile) -> List[str]:
    args = [tool_path(profile, "scanstate.exe"), profile.migration_store]
    args.extend(build_common_args(profile))

    if profile.users:
        for user in [u.strip() for u in profile.users.split(",") if u.strip()]:
            args.append(f"/ue:{user}") if user.startswith("!") else args.append(f"/ui:{user}")

    if profile.domain:
        args.append(f"/md:{profile.domain}")

    if profile.local_only:
        args.append("/localonly")

    if profile.offline_scan:
        args.append(f"/offlineWinDir:{profile.target_windows}")

    return args


def build_loadstate_command(profile: UsmtProfile) -> List[str]:
    args = [tool_path(profile, "loadstate.exe"), profile.migration_store]
    args.extend(build_common_args(profile))

    if profile.domain:
        args.append(f"/mu:{profile.domain}:{profile.domain}")

    return args


def run_command(command: List[str]) -> int:
    clear()
    print("Executing:\n")
    print(quote_args(command))
    print("\n--- output ---\n")
    try:
        proc = subprocess.run(command, check=False)
        print("\n--------------")
        print(f"Exit code: {proc.returncode}")
        pause()
        return proc.returncode
    except FileNotFoundError:
        print("Executable not found. Verify the USMT path in settings.")
        pause()
        return 127


def edit_profile(profile: UsmtProfile) -> None:
    while True:
        clear()
        print(f"{APP_NAME} - Settings\n")
        print(f"1) USMT bin directory      : {profile.usmt_bin}")
        print(f"2) Migration store         : {profile.migration_store}")
        print(f"3) Include XML (comma list): {', '.join(profile.include_xml)}")
        print(f"4) Extra switches          : {' '.join(profile.extra_switches) or '(none)'}")
        print(f"5) Log file                : {profile.log_path}")
        print(f"6) Progress log file       : {profile.progress_log_path}")
        print(f"7) Target Windows path     : {profile.target_windows}")
        print(f"8) Users list              : {profile.users}")
        print(f"9) Domain                  : {profile.domain or '(none)'}")
        print(f"a) Toggle hardlink         : {profile.hardlink}")
        print(f"b) Toggle /c               : {profile.continue_on_non_fatal}")
        print(f"c) Toggle /copyraw         : {profile.copy_raw}")
        print(f"d) Toggle /localonly       : {profile.local_only}")
        print(f"e) Toggle offline scan     : {profile.offline_scan}")
        print("s) Save profile")
        print("q) Back")

        choice = input("\nSelect option: ").strip().lower()
        if choice == "1":
            profile.usmt_bin = input("USMT bin directory: ").strip() or profile.usmt_bin
        elif choice == "2":
            profile.migration_store = input("Migration store path: ").strip() or profile.migration_store
        elif choice == "3":
            value = input("XML list (comma separated): ").strip()
            if value:
                profile.include_xml = [x.strip() for x in value.split(",") if x.strip()]
        elif choice == "4":
            value = input("Extra switches (space separated): ").strip()
            profile.extra_switches = value.split() if value else []
        elif choice == "5":
            profile.log_path = input("Log path: ").strip() or profile.log_path
        elif choice == "6":
            profile.progress_log_path = input("Progress log path: ").strip() or profile.progress_log_path
        elif choice == "7":
            profile.target_windows = input("Target Windows directory: ").strip() or profile.target_windows
        elif choice == "8":
            profile.users = input("Users list (*, user1, !excludeUser): ").strip() or profile.users
        elif choice == "9":
            profile.domain = input("Domain: ").strip()
        elif choice == "a":
            profile.hardlink = not profile.hardlink
        elif choice == "b":
            profile.continue_on_non_fatal = not profile.continue_on_non_fatal
        elif choice == "c":
            profile.copy_raw = not profile.copy_raw
        elif choice == "d":
            profile.local_only = not profile.local_only
        elif choice == "e":
            profile.offline_scan = not profile.offline_scan
        elif choice == "s":
            save_profile(profile)
            print("Profile saved.")
            pause()
        elif choice == "q":
            return


def show_preview(profile: UsmtProfile) -> None:
    clear()
    print(f"{APP_NAME} - Command Preview\n")
    print("ScanState command:\n")
    print(quote_args(build_scanstate_command(profile)))
    print("\nLoadState command:\n")
    print(quote_args(build_loadstate_command(profile)))
    print()
    pause()


def main() -> int:
    profile = load_profile()

    while True:
        clear()
        print(f"{APP_NAME}\n")
        print("1) Run ScanState (capture user state)")
        print("2) Run LoadState (restore user state)")
        print("3) Command preview")
        print("4) Edit settings")
        print("5) Save settings")
        print("q) Quit")

        choice = input("\nSelect option: ").strip().lower()

        if choice == "1":
            run_command(build_scanstate_command(profile))
        elif choice == "2":
            run_command(build_loadstate_command(profile))
        elif choice == "3":
            show_preview(profile)
        elif choice == "4":
            edit_profile(profile)
        elif choice == "5":
            save_profile(profile)
            print("Saved.")
            pause()
        elif choice == "q":
            return 0


if __name__ == "__main__":
    sys.exit(main())
