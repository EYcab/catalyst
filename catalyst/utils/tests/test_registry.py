import pytest

from catalyst.utils.registry import RegistryException
from ..registry import *
from .registery_foo import foo, bar
from . import registery_foo as module


def test_add_function():
    r = Registry()

    r.add(foo)

    assert "foo" in r._factories


def test_add_function_name_override():
    r = Registry()

    r.add(foo, name="bar")

    assert "bar" in r._factories


def test_add_lambda_fail():
    r = Registry()

    with pytest.raises(RegistryException):
        r.add(lambda x: x)


def test_add_lambda_override():
    r = Registry()

    r.add(lambda x: x, name="bar")

    assert "bar" in r._factories


def test_fail_multiple_with_name():
    r = Registry()

    with pytest.raises(RegistryException):
        r.add(foo, foo, name="bar")


def test_fail_double_add():
    r = Registry()
    r.add(foo)

    with pytest.raises(RegistryException):
        r.add(foo)


def test_instantiations():
    r = Registry()

    r.add(foo)

    res = r.get_instance("foo", 1, 2)
    assert res == {"a": 1, "b": 2}

    res = r.get_instance("foo", 1, b=2)
    assert res == {"a": 1, "b": 2}

    res = r.get_instance("foo", a=1, b=2)
    assert res == {"a": 1, "b": 2}


def test_fail_instantiation():
    r = Registry()

    r.add(foo)

    with pytest.raises(RegistryException) as e_ifo:
        r.get_instance("foo", c=1)

    assert hasattr(e_ifo.value, "__cause__")


def test_decorator():
    r = Registry()

    @r.add
    def bar():
        pass

    r.get("bar")


def test_kwargs():
    r = Registry()

    r.add(bar=foo)

    r.get("bar")

def test_add_module():
    r = Registry()

    r.add_from_module(module)

    r.get("foo")

    with pytest.raises(RegistryException):
        r.get_instance("bar")








