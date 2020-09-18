#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for the ligands_database module.
"""
import pytest

from ligands_database import ligands_database


def test_something():
    assert True


def test_with_error():
    with pytest.raises(ValueError):
        # Do something that raises a ValueError
        raise(ValueError)


# Fixture example
@pytest.fixture
def an_object():
    return {}


def test_ligands_database(an_object):
    assert an_object == {}
