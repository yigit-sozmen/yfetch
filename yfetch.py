import os
import platform
import re
import subprocess
from datetime import datetime
import psutil
import shutil


def os_name() -> str:

    try:
        return platform.freedesktop_os_release().get("NAME", platform.system())
    except (AttributeError, OSError):
        return platform.system()


def shell_name():
    shell_path = os.environ.get("SHELL","UNKNOWN")
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

# def gpu_info():
#     try:
#         output = subprocess.run(['lspci'] , stdout=subprocess.PIPE,stderr=subprocess , text=True)
#         gpu_lines = re.findall(r'(VGA compatible controller|3D Controller): (.+)', output.stdout , re.IGNORECASE)
#         gpu_name = [gpu[1] for gpu in gpu_lines]
#         return ','. join(gpu_name)  if gpu_name else 'N/A'
#     except Exception:
#         return("N/A")

def gpu_info():
    try:
        output = subprocess.run(['lspci'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        gpu_lines = re.findall(r'(VGA compatible controller|3D controller): (.+)', output.stdout, re.IGNORECASE)
        gpu_names = [gpu[1] for gpu in gpu_lines]
        return ', '.join(gpu_names) if gpu_names else 'N/A'
    except Exception:
        return "N/A"

def uptime():
    boot_time = psutil.boot_time()
    now = datetime.now().timestamp()
    uptime_s = int(now - boot_time)
    days, remainder = divmod(uptime_s, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)

    uptime_final = f"{days}d {hours}h {minutes}m"
    return uptime_final


def de_wm():
    raw_de = os.environ.get("XDG_CURRENT_DESKTOP") or os.environ.get("DESKTOP_SESSION") or ""
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
                output = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                if output.returncode == 0:
                    lines = [line for line in output.stdout.strip().splitlines() if line]
                    count = len(lines) - 1 if has_header and len(lines) > 0 else len(lines)
                    display_name = "pacman" if binary == "pacman" else binary.replace("-query", "")
                    results.append(f"{count} ({display_name})")
            except Exception:
                pass

    return ", ".join(results) if results else "N/A"


def main():
    print("yfetch...")
    print("Operating System : " + str(os_name()))
    print("Kernel : " + platform.release())
    print("Hostname : " + platform.node())
    print("CPU : " + cpu_info())
    print("GPU : " + gpu_info())
    print("Shell : " + str(shell_name()))
    print("DE/WM : " + de_wm())
    print("Packages : " + packages())
    print("Uptime : " + uptime())




if __name__ == "__main__":
    main()


