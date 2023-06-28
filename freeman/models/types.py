import typing

Pk: typing.TypeAlias = int | str
JSONableType: typing.TypeAlias = int | str | bool | None | dict[str, "JSONableType"]


class PartialUpdateType(typing.TypedDict):
    pk: Pk
    _set: dict[str, typing.Any]
