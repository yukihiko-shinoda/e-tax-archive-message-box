from pathlib import Path
from typing import Any

from yaml import safe_load


class Config:
    def __init__(self) -> None:
        config: dict[str, Any] = safe_load(
            Path("config.yml").read_text(encoding="utf-8")
        )
        self.login = config["login"]
