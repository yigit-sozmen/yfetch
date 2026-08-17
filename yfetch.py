import argparse
from datetime import datetime
from itertools import zip_longest
import os
import platform
import re
import shutil
import subprocess

import psutil
from logos import BOLD, RESET, get_logo_and_color


def parse_args():
    parser = argparse.ArgumentParser(description="yfetch - A custom system fetch tool")
    parser.add_argument(
        "-d",
        "--distro",
        type=str,
        help="Override auto-detected OS logo (e.g. yfetch -d gentoo)",
    )
    return parser.parse_args()


def strip_ansi(text: str) -> str:
    return re.sub(r"\033\[[0-9;]*m", "", text)


def os_name() -> str:
    try:
        return platform.freedesktop_os_release().get("NAME", platform.system())
    except (AttributeError, OSError):
        return platform.system()


def shell_name():
    shell_path = os.environ.get("SHELL", "UNKNOWN")
    return os.path.basename(shell_path)


def cpu_info():
    try:
        with open("/proc/cpuinfo", "r") as f:
            for line in f:
                if "model name" in line:
                    return line.split(":", 1)[1].strip()
    except Exception:
        pass
    return "N/A"


def gpu_info():
    try:
        output = subprocess.run(
            ["lspci"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        gpu_lines = re.findall(
            r"(VGA compatible controller|3D controller): (.+)",
            output.stdout,
            re.IGNORECASE,
        )
        gpu_names = [gpu[1] for gpu in gpu_lines]
        return ", ".join(gpu_names) if gpu_names else "N/A"
    except Exception:
        return "N/A"


def uptime():
    boot_time = psutil.boot_time()
    now = datetime.now().timestamp()
    uptime_s = int(now - boot_time)
    days, remainder = divmod(uptime_s, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, _ = divmod(remainder, 60)

    if days > 0:
        return f"{days}d {hours}h {minutes}m"
    elif hours > 0:
        return f"{hours}h {minutes}m"
    return f"{minutes}m"


def de_wm():
    raw_de = (
        os.environ.get("XDG_CURRENT_DESKTOP")
        or os.environ.get("DESKTOP_SESSION")
        or ""
    )
    de_map = {
        "KDE": "KDE Plasma",
        "plasma": "KDE Plasma",
        "GNOME": "GNOME",
        "XFCE": "XFCE",
        "X-Cinnamon": "Cinnamon",
        "MATE": "MATE",
        "LXQt": "LXQt",
    }
    for item in raw_de.split(":"):
        if item in de_map:
            return de_map[item]
    return raw_de.title() if raw_de else "N/A"


def packages():
    pkg_managers = {
        "pacman": (["pacman", "-Q"], False),
        "dpkg-query": (["dpkg-query", "-f", ".\n", "-W"], False),
        "rpm": (["rpm", "-qa"], False),
        "emerge": (["qlist", "-I"], False),
        "xbps-query": (["xbps-query", "-l"], False),
        "flatpak": (["flatpak", "list"], False),
        "snap": (["snap", "list"], True),
    }

    results = []

    for binary, (cmd, has_header) in pkg_managers.items():
        if shutil.which(binary):
            try:
                output = subprocess.run(
                    cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
                )
                if output.returncode == 0:
                    lines = [
                        line for line in output.stdout.strip().splitlines() if line
                    ]
                    count = (
                        len(lines) - 1
                        if has_header and len(lines) > 0
                        else len(lines)
                    )
                    display_name = (
                        "pacman" if binary == "pacman" else binary.replace("-query", "")
                    )
                    results.append(f"{count} ({display_name})")
            except Exception:
                pass

    return ", ".join(results) if results else "N/A"


def print_fetch(distro: str, raw_stats: list[tuple[str, str]]):
    logo_ascii, c1, _ = get_logo_and_color(distro)

    logo_lines = [
        f"{c1}{line}{RESET}" for line in logo_ascii.strip("\n").splitlines()
    ]

    header_text = f"{platform.node()}@yfetch"
    separator = "-" * len(header_text)

    info_lines = [
        f"{BOLD}{c1}{header_text}{RESET}",
        f"{c1}{separator}{RESET}",
    ] + [f"{BOLD}{c1}{label}:{RESET} {value}" for label, value in raw_stats]

    
    color_blocks = [
        "",
        "".join(f"\033[4{i}m   " for i in range(8)) + RESET,
        "".join(f"\033[10{i}m   " for i in range(8)) + RESET,
    ]
    info_lines.extend(color_blocks)

    max_logo_width = (
        max(len(strip_ansi(line)) for line in logo_lines) if logo_lines else 0
    )

    for logo_line, info in zip_longest(logo_lines, info_lines, fillvalue=""):
        logo_line = logo_line or ""
        info = info or ""

        visible_len = len(strip_ansi(logo_line))
        padding = " " * (max_logo_width - visible_len)

        print(f"{logo_line}{padding}  {info}")


def main():
    args = parse_args()

    actual_os = os_name()
    logo_distro = args.distro if args.distro else actual_os

    raw_stats = [
        ("OS", actual_os),
        ("Kernel", platform.release()),
        ("Uptime", uptime()),
        ("Packages", packages()),
        ("Shell", shell_name()),
        ("DE/WM", de_wm()),
        ("CPU", cpu_info()),
        ("GPU", gpu_info()),
    ]

    print_fetch(logo_distro, raw_stats)

if __name__ == "__main__":
    main()
