import csv
import pytest

from charade import Charade, Email, EmailAttachment, File, Image


@pytest.fixture
def instance():
    return Charade(prefix="TEST", fill=5, size=5000)


def test_charade():
    c = Charade(prefix="TEST", fill=5, size=50)
    assert "Charade(" in repr(c)
    assert len(c.people) >= 15  # minimum of 15 people, even for small sets
    c = Charade(prefix="TEST", fill=5, size=5000)
    count = 0
    for d in c:
        count += 1 + len(d)
    assert count >= 5000  # returns at least number specified in size


def test_charade_delimited(instance):
    d = instance.delimited()
    reader = csv.reader(d, delimiter="\x14", quotechar="\xfe")
    row = next(reader)
    assert row[0] == "TEST00001"


def test_email(instance):
    e = Email(instance)
    assert "Email(" in repr(e)
    assert "From:" in str(e)
    for a in e:
        assert isinstance(a, EmailAttachment)
    assert "EmailAttachment(" in repr(a)
    assert len(a) == 1


def test_file(instance):
    f = File(instance)
    for a in f:
        assert isinstance(a, File)
    assert "File(" in repr(f)

def test_image(instance):
    i = Image(instance)