import typing

from data import _singleton

database: _singleton.Singleton[dict[str, typing.Any]] = _singleton.Singleton(dict())
