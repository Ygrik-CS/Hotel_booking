"""Tests for Lab 2: Recursion and closures."""
import pytest
from core.recursion import (
    split_date_range,
    flatten_tuple,
    filter_tree,
    max_depth,
    count_leaves,
    sum_recursive,
    reverse_recursive
)


def test_split_date_range():
    """Test recursive date range splitting."""
    dates = split_date_range("2024-01-01", "2024-01-03")
    assert len(dates) == 2
    assert dates[0] == "2024-01-01"
    assert dates[1] == "2024-01-02"


def test_flatten_tuple():
    """Test recursive tuple flattening."""
    nested = (1, (2, 3), (4, (5, 6)), 7)
    flat = flatten_tuple(nested)
    assert flat == (1, 2, 3, 4, 5, 6, 7)


def test_filter_tree():
    """Test recursive tree filtering."""
    tree = (1, (2, 3), (4, (5, 6)))
    filtered = filter_tree(lambda x: x > 3, tree)
    # Should keep only elements > 3
    assert 1 not in flatten_tuple(filtered)
    assert 5 in flatten_tuple(filtered)


def test_max_depth():
    """Test calculating tree depth."""
    tree = (1, (2, (3, (4,))))
    depth = max_depth(tree)
    assert depth == 4


def test_count_leaves():
    """Test counting leaf nodes."""
    tree = (1, (2, 3), (4, (5, 6)))
    leaves = count_leaves(tree)
    assert leaves == 6


def test_sum_recursive():
    """Test recursive sum."""
    numbers = (1, 2, 3, 4, 5)
    total = sum_recursive(numbers)
    assert total == 15


def test_reverse_recursive():
    """Test recursive reverse."""
    items = (1, 2, 3, 4, 5)
    reversed_items = reverse_recursive(items)
    assert reversed_items == (5, 4, 3, 2, 1)
