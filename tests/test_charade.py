import pytest

from charade import Charade


@pytest.fixture
def config():
    return {}


def test_charade_init():
    c = Charade(prefix="TEST", fill=5, start=11, size=50)
    assert "Charade(" in repr(c)
    assert len(c.people) >= 15  # minimum of 15 people, even for small sets
    c = Charade(prefix="TEST", fill=5, start=11, size=5000)
    count = 0
    for d in c:
        count += 1 + len(d)
    assert count >= 5000  # returns at least number specified in size