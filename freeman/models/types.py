import typing

Pk: typing.TypeAlias = int | str

class PartialUpdateType(typing.TypedDict):
    pk: Pk
    _set: dict[str, typing.Any]
