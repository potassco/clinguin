"""Test domain_state.py functionality."""

from types import SimpleNamespace
from unittest.mock import patch

import pytest
from clingo import Symbol

from clinguin.server.backends import BackendArgs, ClingoBackend
from clinguin.server.domain_state import DomainState


def test_ds_context_with_context_items():
    """Test _ds_context when backend has context items."""
    # Create backend with test files
    args = BackendArgs(domain_files=["tests/data/encoding.lp"], ui_files=["tests/data/ui.lp"])
    backend = ClingoBackend(args)

    # Create mock context items
    context_item1 = SimpleNamespace(key="test_key", value="test_value")
    context_item2 = SimpleNamespace(key="num_key", value="42")
    context_item3 = SimpleNamespace(key="invalid_key", value="invalid(term")

    backend._context = [context_item1, context_item2, context_item3]

    # Test the domain state constructor
    ds = DomainState(backend)
    result = ds._ds_context

    # Verify the output
    assert "#defined _clinguin_context/2." in result
    assert "_clinguin_context(test_key,test_value)." in result
    assert "_clinguin_context(num_key,42)." in result
    assert '_clinguin_context(invalid_key,"invalid(term").' in result


def test_ds_context_empty():
    """Test _ds_context when backend has no context."""
    args = BackendArgs(domain_files=["tests/data/encoding.lp"], ui_files=["tests/data/ui.lp"])
    backend = ClingoBackend(args)

    # Empty context (default)
    assert backend._context == []

    ds = DomainState(backend)
    result = ds._ds_context

    # Should only contain the definition
    assert result == "#defined _clinguin_context/2. \n"


def test_ds_opt_with_optimization_info():
    """Test _ds_opt when backend has optimization information."""
    args = BackendArgs(domain_files=["tests/data/encoding.lp"], ui_files=["tests/data/ui.lp"])
    backend = ClingoBackend(args)

    # Set optimization information
    backend._cost = [10, 20, 5]
    backend._optimal = True
    backend._optimizing = True

    ds = DomainState(backend)
    result = ds._ds_opt

    # Verify the output
    assert "#defined _clinguin_cost/2. #defined _clinguin_cost/1. #defined _clinguin_optimal/1." in result
    assert "_clinguin_cost(0,10)." in result
    assert "_clinguin_cost(1,20)." in result
    assert "_clinguin_cost(2,5)." in result
    assert "_clinguin_optimal." in result
    assert "_clinguin_optimizing." in result
    assert "_clinguin_cost((10, 20, 5))." in result


def test_ds_opt_default_values():
    """Test _ds_opt with default values (no optimization)."""
    args = BackendArgs(domain_files=["tests/data/encoding.lp"], ui_files=["tests/data/ui.lp"])
    backend = ClingoBackend(args)

    # Default values
    assert backend._cost == []
    assert backend._optimal == False
    assert backend._optimizing == False

    ds = DomainState(backend)
    result = ds._ds_opt

    # Should only contain definitions and empty cost tuple
    expected = (
        "#defined _clinguin_cost/2. #defined _clinguin_cost/1. #defined _clinguin_optimal/1. _clinguin_cost(()).\n"
    )
    assert result == expected


def test_ds_brave_not_used():
    """Test _ds_brave when _any/1 predicate is not used in UI files."""
    args = BackendArgs(domain_files=["tests/data/encoding.lp"], ui_files=["tests/data/ui.lp"])
    backend = ClingoBackend(args)
    ds = DomainState(backend)

    with patch.object(ds, "_ui_uses_predicate", return_value=False) as mock_ui_uses:
        result = ds._ds_brave
        mock_ui_uses.assert_called_with("_any", 1)
        assert result == "% NOT USED\n"


def test_ds_cautious_not_used():
    """Test _ds_cautious when _all/1 predicate is not used in UI files."""
    args = BackendArgs(domain_files=["tests/data/encoding.lp"], ui_files=["tests/data/ui.lp"])
    backend = ClingoBackend(args)
    ds = DomainState(backend)

    with patch.object(ds, "_ui_uses_predicate", return_value=False) as mock_ui_uses:
        result = ds._ds_cautious
        mock_ui_uses.assert_called_with("_all", 1)
        assert result == "% NOT USED\n"


def test_ds_brave_optimal_not_used():
    """Test _ds_brave_optimal when _any_opt/1 predicate is not used in UI files."""
    args = BackendArgs(domain_files=["tests/data/encoding.lp"], ui_files=["tests/data/ui.lp"])
    backend = ClingoBackend(args)
    ds = DomainState(backend)

    with patch.object(ds, "_ui_uses_predicate", return_value=False) as mock_ui_uses:
        result = ds._ds_brave_optimal
        mock_ui_uses.assert_called_with("_any_opt", 1)
        assert result == "% NOT USED\n"


def test_ds_cautious_optimal_not_used():
    """Test _ds_cautious_optimal when _all_opt/1 predicate is not used in UI files."""
    args = BackendArgs(domain_files=["tests/data/encoding.lp"], ui_files=["tests/data/ui.lp"])
    backend = ClingoBackend(args)
    ds = DomainState(backend)

    with patch.object(ds, "_ui_uses_predicate", return_value=False) as mock_ui_uses:
        result = ds._ds_cautious_optimal
        mock_ui_uses.assert_called_with("_all_opt", 1)
        assert result == "% NOT USED\n"


def test_ds_constants_with_constants():
    """Test _ds_constants when backend has constants."""
    args = BackendArgs(
        domain_files=["tests/data/encoding.lp"], ui_files=["tests/data/ui.lp"], const=["n=5", "name=test"]
    )
    backend = ClingoBackend(args)

    # Verify constants were set
    assert backend._constants == {"n": "5", "name": "test"}

    ds = DomainState(backend)
    result = ds._ds_constants

    # Verify the output
    assert "#defined _clinguin_const/2." in result
    assert "_clinguin_const(n,5)." in result
    assert "_clinguin_const(name,test)." in result


def test_ds_constants_empty():
    """Test _ds_constants when backend has no constants."""
    args = BackendArgs(domain_files=["tests/data/encoding.lp"], ui_files=["tests/data/ui.lp"])
    backend = ClingoBackend(args)

    # No constants (default)
    assert backend._constants == {}

    ds = DomainState(backend)
    result = ds._ds_constants

    # Should only contain the definition
    assert result == "#defined _clinguin_const/2. \n"


def test_tag_with_none():
    """Test tag method when tag_name is None."""
    from clingo import parse_term

    symbols = [parse_term("a"), parse_term("b(1)"), parse_term("c(x,y)")]

    result = DomainState.tag(symbols, None)

    assert result == symbols
    assert result is symbols


def test_call_solver_with_cache_while_browsing():
    """Test _call_solver_with_cache when backend is browsing."""
    args = BackendArgs(domain_files=["tests/data/encoding.lp"], ui_files=["tests/data/ui.lp"])
    backend = ClingoBackend(args)
    ds = DomainState(backend)

    backend.next_solution()
    assert backend._is_browsing == True

    # Test with cache entry
    ds._backup_cache["test_id"] = "cached_result"
    result = ds._call_solver_with_cache("test_id", "_tag", 0, "ignore", "brave")
    assert result == "cached_result"

    # Test without cache entry
    result = ds._call_solver_with_cache("missing_id", "_tag", 0, "ignore", "brave")
    assert result == ""


def test_ds_external_with_released():
    """Test _ds_external when there are released external atoms."""
    from clingo import parse_term

    args = BackendArgs(domain_files=["tests/data/encoding.lp"], ui_files=["tests/data/ui.lp"])
    backend = ClingoBackend(args)

    # Add some external atoms in different states
    symbol_true = parse_term("ext_true")
    symbol_false = parse_term("ext_false")
    symbol_released = parse_term("ext_released")

    backend._externals["true"].add(symbol_true)
    backend._externals["false"].add(symbol_false)
    backend._externals["released"].add(symbol_released)

    ds = DomainState(backend)
    result = ds._ds_external

    assert "#defined _clinguin_external/2." in result
    assert "_clinguin_external(ext_true,true)." in result
    assert "_clinguin_external(ext_false,false)." in result
    assert "_clinguin_external(ext_released,release)." in result
