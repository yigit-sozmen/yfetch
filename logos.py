from itertools import zip_longest

RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[31m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"

GENTOO_BANNER = r"""
 _____                        
|  ___)                       
| |  ___ _  _____ ___   ___   
| | / __) |/ (   ) _ \ / _ \  
| | > _)| / / | ( (_) | (_) ) 
|_| \___)__/   \_)___/ \___/  
"""

ARCH_BANNER = r"""
  ___                    
 / _ \                   
| |_| | _____   ___ __  
|  _  |/ _ \ \ / / '_ \ 
| | | | |_) ) v /| | | |
|_| |_|  __/ > < |_| | |
      | |   / ^ \    | | 
      |_|  /_/ \_\   |_| 
"""

ENDEAVOUR_BANNER = r"""
 _____       __                                         _________ 
|  ___)     / _)                                       / _ \  ___)
| |_   _  __\ \  ___ __  ___________  ___  _   _  ___ | | | \ \   
|  _) | |/ / _ \/ __)  \/ (  _____  )/ _ \| | | |/ _ \| | | |> >  
| |___| / ( (_) > _| ()  <| |_/ \_| ( (_) ) |_| | |_) ) |_| / /__ 
|_____)__/ \___/\___)__/\_\\___^___/ \___/ \___/|  __/ \___/_____)
                                                | |               
                                                |_|               
"""


YFETCH = r"""
                                     
            _                        
           | |                       
 _  _  _  _| |_  ___ _____   ___ __  
| || || |/     \/ __|   ) \ / / '_ \ 
| \| |/ ( (| |) > _) | | \ v /| | | |
 \_   _/ \_   _/\___) \_) > < |_| | |
   | |     | |           / ^ \    | |
   |_|     |_|          /_/ \_\   |_|
"""
LOGOS = {
    "gentoo": (GENTOO_BANNER, MAGENTA),
    "arch": (ARCH_BANNER, CYAN),
    "endeavour": (ENDEAVOUR_BANNER, MAGENTA),
}



def get_logo_and_color(distro_name: str) -> tuple[str, str]:
    normalized_name = distro_name.lower()

    for key, (logo, color) in LOGOS.items():
        if key in normalized_name:
            return logo, color

    return GENTOO_BANNER, MAGENTA





def render_fetch(logo_str: str, info_lines: list[str], logo_color: str):

    logo_lines = logo_str.strip("\n").splitlines()
    max_logo_width = max(len(line) for line in logo_lines) if logo_lines else 0

    for logo_line, info_line in zip_longest(logo_lines, info_lines, fillvalue=""):
        padded_logo = f"{logo_line:<{max_logo_width}}"
        print(f"{logo_color}{padded_logo}{RESET}  {info_line}")