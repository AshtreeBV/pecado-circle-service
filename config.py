import os.path
import pathlib

from internal import ConfigBase, UNSET


class Configuration(ConfigBase):

 #Circle configuration
    CIRCLE_API_KEY: str = "QVBJX0tFWTpkNzhmODQwYjEyNDI0YmI5NDNhODUzNDhlZmQzNzU2Njo1OWU1YmU1YWYxNmE1ZmVlZjE2MGU0MDJkYzYzOGYzNw=="
    CIRCLE_API_URL: str = "https://api-sandbox.circle.com/v1"

# --- Do not edit anything below this line, or do it, I'm not your mom ----
defaults = Configuration(autoload=False)
cfg = Configuration()
