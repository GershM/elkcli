MAJOR_VERSION = 0
MINOR_VERSION = 1
PATCH_VERSION = 0

__short_version__ = f"{MAJOR_VERSION}.{MINOR_VERSION}"
__version__ = f"{__short_version__}.{PATCH_VERSION}"


DESCRIPTION = "Elastic search CLI tool."
NAME = "GENA MIRSON"
BANNER_ART = r"""

 /$$$$$$$$ /$$                       /$$     /$$                  /$$$$$$                                          /$$              /$$$$$$  /$$       /$$$$$$
| $$_____/| $$                      | $$    |__/                 /$$__  $$                                        | $$             /$$__  $$| $$      |_  $$_/
| $$      | $$  /$$$$$$   /$$$$$$$ /$$$$$$   /$$  /$$$$$$$      | $$  \__/  /$$$$$$   /$$$$$$   /$$$$$$   /$$$$$$$| $$$$$$$       | $$  \__/| $$        | $$  
| $$$$$   | $$ |____  $$ /$$_____/|_  $$_/  | $$ /$$_____/      |  $$$$$$  /$$__  $$ |____  $$ /$$__  $$ /$$_____/| $$__  $$      | $$      | $$        | $$  
| $$__/   | $$  /$$$$$$$|  $$$$$$   | $$    | $$| $$             \____  $$| $$$$$$$$  /$$$$$$$| $$  \__/| $$      | $$  \ $$      | $$      | $$        | $$  
| $$      | $$ /$$__  $$ \____  $$  | $$ /$$| $$| $$             /$$  \ $$| $$_____/ /$$__  $$| $$      | $$      | $$  | $$      | $$    $$| $$        | $$  
| $$$$$$$$| $$|  $$$$$$$ /$$$$$$$/  |  $$$$/| $$|  $$$$$$$      |  $$$$$$/|  $$$$$$$|  $$$$$$$| $$      |  $$$$$$$| $$  | $$      |  $$$$$$/| $$$$$$$$ /$$$$$$
|________/|__/ \_______/|_______/    \___/  |__/ \_______/       \______/  \_______/ \_______/|__/       \_______/|__/  |__/       \______/ |________/|______/

"""

version = f"Version: {__version__}".center(80)

BANNER = f"{BANNER_ART.center(100)}\n{DESCRIPTION.center(80)}\n{version}\n"