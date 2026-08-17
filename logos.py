import re
from itertools import zip_longest

RESET = "\033[0m"
BOLD = "\033[1m"


RED = "\033[31m"      # Color 1
GREEN = "\033[32m"    # Color 2
YELLOW = "\033[33m"   # Color 3
BLUE = "\033[34m"     # Color 4
MAGENTA = "\033[35m"  # Color 5
CYAN = "\033[36m"     # Color 6
WHITE = "\033[37m"    # Color 7


GENTOO_BANNER = r"""
{c1} _____                        
|  ___)                       
| |  ___ _  _____ ___   ___   
| | / __) |/ (   ) _ \ / _ \  
| | > _)| / / | ( (_) | (_) ) 
|_| \___)__/   \_)___/ \___/  {reset}
"""

ARCH_BANNER = r"""
{c1} ___                    
/ _ \                   
| |_| | _____   ___ __  
|  _  |/ _ \ \ / / '_ \ 
| | | | |_) ) v /| | | |
|_| |_|  __/ > < |_| | |
      | |   / ^ \   | | 
      |_|  /_/ \_\  |_| {reset}
"""

ENDEAVOUR_BANNER = r"""
{c1} _____       __                                         _________ 
|  ___)     / _)                                       / _ \  ___)
| |_   _  __\ \  ___ __  ___________  ___  _   _  ___ | | | \ \   
|  _) | |/ / _ \/ __)  \/ (  _____  )/ _ \| | | |/ _ \| | | |> >  
| |___| / ( (_) > _| ()  <| |_/ \_| ( (_) ) |_| | |_) ) |_| / /__ 
|_____)__/ \___/\___)__/\_\\___^___/ \___/ \___/|  __/ \___/_____)
                                                | |               
                                                |_|               {reset}
"""

LOGOS = {
    "gentoo": (GENTOO_BANNER, MAGENTA, WHITE),
    "arch": (ARCH_BANNER, CYAN, WHITE),
    "endeavour": (ENDEAVOUR_BANNER, MAGENTA, RED),
}


def get_logo_and_color(distro_name: str) -> tuple[str, str, str]:
    normalized_name = distro_name.lower()

    for key, (logo_template, c1, c2) in LOGOS.items():
        if key in normalized_name:
            rendered_logo = logo_template.format(c1=c1, c2=c2, reset=RESET)
            return rendered_logo, c1, c2

    # Fallback to Gentoo
    rendered_logo = GENTOO_BANNER.format(c1=MAGENTA, c2=WHITE, reset=RESET)
    return rendered_logo, MAGENTA, WHITE