import os.path
import pathlib

from internal import ConfigBase, UNSET


class Configuration(ConfigBase):
    MY_CONFIGURATION: str = UNSET
    REMOTE_IP: str = UNSET


# --- Do not edit anything below this line, or do it, I'm not your mom ----
defaults = Configuration(autoload=False)
cfg = Configuration()
