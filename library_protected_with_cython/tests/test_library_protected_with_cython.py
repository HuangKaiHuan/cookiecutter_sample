#!/usr/bin/env python

"""Tests for `library_protected_with_cython` package."""

from library_protected_with_cython.library_protected_with_cython import sample


def test_sample():
    assert sample(True)
    assert not sample(False)
