import add


def test_add():
    assert add.add(1, 2) == 3


def test_add_failure():
    assert add.add(1, 3) == 3
