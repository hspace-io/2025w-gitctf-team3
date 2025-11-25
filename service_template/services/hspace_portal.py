from __future__ import annotations
import dataclasses


users: dict[str, "PortalUser"] = {}


@dataclasses.dataclass
class PortalConfig:
    mode: str = "light"


@dataclasses.dataclass
class PortalUser:
    username: str
    config: PortalConfig

    @staticmethod
    def merge_info(src, dest, *, depth=0):
        if depth > 3:
            raise Exception("Reached maximum depth")
        for k, v in src.items():
            if hasattr(dest, "__getitem__"):
                if dest.get(k) and isinstance(v, dict):
                    PortalUser.merge_info(v, dest.get(k), depth=depth + 1)
                else:
                    dest[k] = v
            elif hasattr(dest, k) and isinstance(v, dict):
                PortalUser.merge_info(v, getattr(dest, k), depth=depth + 1)
            else:
                setattr(dest, k, v)

    @staticmethod
    def get(username: str):
        if username not in users:
            raise Exception("The user doesn't exist")
        return users[username]

    @staticmethod
    def get_or_create(username: str):
        if username not in users:
            users[username] = PortalUser(username, PortalConfig())
        return users[username]
