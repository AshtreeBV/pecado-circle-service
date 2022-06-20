from __future__ import annotations
from typing import Callable, Optional
from fastapi import FastAPI, APIRouter, Body
from app.__internal import Function

from config import cfg


def error(message, info):
    return {
        "success": False,
        "error": f"{message}",
        "info": info
    }


class CreateGameParam():
    registrationStartTimestamp: int = 0
    registrationEndTimestamp:   int = 0
    tournamentStartTimestamp:   int = 0
    tournamentEndTimestamp:     int = 0
    minRoosters:                int = 0
    maxRoosters:                int = 0
    fee:                        int = 0
    distributions:              list[int]

class Scholarship(Function):

    def __init__(self, error: Callable):
        self.log.info("This is where the initialization code go")

    def Bootstrap(self, app: FastAPI):

        router = APIRouter(prefix="/api/sample")

        @router.get("/")
        def index():
            self.log.debug("Hello debug!")
            self.log.verbose("Hello verbose!")
            return {"hello": "world"}


        @router.get("/foo")
        def foo():
            self.log.info("Somoeone called the foo endpoint!")
            return {
                "mnemonic": cfg.MY_CONFIGURATION,
                "remote": cfg.REMOTE_ID
            }

        app.include_router(router)

