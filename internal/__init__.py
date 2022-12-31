from typing import List, get_type_hints
import azure.functions as func
import os
import json

UNSET = "CONFIG-NULL"

def coerce(type, value):
    if value == UNSET:
        return UNSET

    return type(value)

class ConfigBase:
    def __init__(self, autoload=True):
        if autoload:
            self.Load()

    def Load(self):
        type_of = get_type_hints(self)
        for x in self.__dir__():
            if x.startswith("__"): continue
            if callable(getattr(self, x)): continue
            if method := getattr(self, f"resolve_{x}", None):
                self.__dict__[x] = method()
            else:
                self.__dict__[x] = coerce(type_of[x], os.getenv(x, getattr(self, x)))
        try:
            with open(".env") as f:
                lines = f.readlines()

            for i, line in enumerate(lines):
                x = line.strip().split("=")
                if len(x) >= 2:
                    self.__dict__[x[0]] = coerce(type_of[x[0]], "=".join(x[1:]))
                else:
                    print(f"Warning: .env produced an invalid entry in line {i + 1}")

        except FileNotFoundError:
            ...

        try:
            with open("config.apply.json") as f:
                cfgs = json.loads(f.read())
                print("Applying config.apply.json...")
                for cfg in cfgs:
                    if type_of.get(cfg["name"], None) is None:
                        continue
                    print(f" -> {cfg['name']} = {cfg['value']}")
                    self.__dict__[cfg["name"]] = coerce(type_of[cfg["name"]], cfg["value"])
        except FileNotFoundError:
            ...

        return self

    def has_unset(self) -> List[str]:
        r = []
        for k, v in self.__dict__.items():
            if v == UNSET:
                r.append(k)

        return r

def json_response(data, status_code=200) -> func.HttpResponse:
    return func.HttpResponse(
        json.dumps(data), status_code=status_code, mimetype="application/json"
    )
