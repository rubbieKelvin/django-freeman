import pytest
from freeman.utils.dsa import *


def test_dotdict():
    # Create a new DotDict instance
    d = DotDict()

    # Add some keys and values
    d.name = "Alice"
    d.age = 25
    d.address = {"street": "123 Main St", "city": "New York", "state": "NY"}

    # Check that the keys and values are accessible using the dot notation
    assert d.name == "Alice"
    assert d.age == 25
    assert d.address.street == "123 Main St"  # type: ignore
    assert d.address.city == "New York"  # type: ignore
    assert d.address.state == "NY"  # type: ignore

    # Check that setting values works using the dot notation
    d.name = "Bob"
    assert d.name == "Bob"

    # Check that trying to access a non-existent key raises an AttributeError
    with pytest.raises(AttributeError):
        d.nonexistent_key

    # Check that trying to set a new key using attribute assignment works
    d.new_key = "new_value"
    assert d.new_key == "new_value"
    assert d["new_key"] == "new_value"
