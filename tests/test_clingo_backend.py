"""
Test cases for main application functionality using pytest.
"""

import os
import tempfile
from unittest.mock import Mock

import pytest
from clingo import parse_term

from clinguin.server.backends import BackendArgs, ClingoBackend


def test_args_invalid_path():
    with pytest.raises(ValueError):
        BackendArgs(domain_files=["wrong/encoding.lp"])


def test_args_invalid_opt_mode():
    with pytest.raises(ValueError):
        BackendArgs(domain_files=["tests/data/encoding.lp"], default_opt_mode="invalid_mode")


def test_args_invalid_const_format():
    with pytest.raises(ValueError):
        BackendArgs(domain_files=["tests/data/encoding.lp"], const=["c,1"])


def test_args_defaults():
    args = BackendArgs(domain_files=["tests/data/encoding.lp"])
    assert args.domain_files == ["tests/data/encoding.lp"]
    assert args.ui_files == []
    assert args.const == []
    assert args.clingo_ctl_arg == []
    assert args.default_opt_mode == "ignore"
    assert args.opt_timeout is None

    args.const = None
    ClingoBackend(args)


def test_init():
    """Test initialization of the logging module."""
    args = BackendArgs(domain_files=["tests/data/encoding.lp"], ui_files=["tests/data/ui.lp"], const=["myconst=1"])
    backend = ClingoBackend(args)
    assert backend._ds_constructor.__class__.__name__ == "DomainState"
    assert backend._constants == {"myconst": "1"}
    assert backend._context == []
    assert backend._ctl.__class__.__name__ == "Control"
    assert backend._ui_state is None
    assert backend._atoms == set()
    assert backend._assumptions == set()
    assert backend._externals == {"true": set(), "false": set(), "released": set()}
    assert backend._handler is None
    assert backend._iterator is None
    assert backend._model is None
    assert backend._unsat_core is None
    assert backend._cost == []
    assert not backend._optimal
    assert not backend._optimizing
    assert backend._messages == []


def test_interaction_browse_select_download():
    """Test initialization of the logging module."""
    args = BackendArgs(domain_files=["tests/data/encoding.lp"], ui_files=["tests/data/ui.lp"])
    backend = ClingoBackend(args)
    backend.get()
    assert backend._model is not None
    assert len(backend._model) == 3
    assert backend._unsat_core is None
    assert backend._handler is None
    assert backend._iterator is None
    ds = backend._ds_constructor.get_domain_state_dict()
    assert "_clinguin_browsing" not in ds["_ds_browsing"]

    backend.next_solution()
    assert backend._model is not None
    assert backend._handler is not None
    assert backend._iterator is not None
    assert len(backend._assumptions) == 0
    ds = backend._ds_constructor.get_domain_state_dict()
    assert "_clinguin_browsing" in ds["_ds_browsing"]

    backend.download()
    assert backend._messages[0] == ("Download successful", "Information saved in file clinguin_download.lp.", "success")
    assert os.path.isfile("clinguin_download.lp")

    backend.download("", "my_file.lp")
    assert backend._messages[1] == ("Download successful", "Information saved in file my_file.lp.", "success")
    assert os.path.isfile("my_file.lp")

    backend.select()
    assert len(backend._assumptions) == 3
    assert backend._handler is None
    assert backend._iterator is None

    with pytest.raises(RuntimeError):
        backend.download()


def test_interaction_assumptions():
    """Test initialization of the logging module."""
    args = BackendArgs(domain_files=["tests/data/encoding.lp"], ui_files=["tests/data/ui.lp"])
    backend = ClingoBackend(args)
    symbolc = parse_term("object(c)")

    backend.add_assumption("object(c)", "true")
    assert (symbolc, True) in backend._assumptions
    ds = backend._ds_constructor.get_domain_state_dict()
    assert "_all(object(c))" in ds["_ds_cautious"]
    assert "_all(object(d))" not in ds["_ds_cautious"]
    assert "_clinguin_assume(object(c),true)" in ds["_ds_assume"]

    backend.add_assumption("object(c)", "true")

    backend.add_assumption("wrong", "true")  # An invalid assumption
    symbolw = parse_term("wrong")
    assert (symbolw, True) in backend._assumptions
    assert (symbolc, True) in backend._assumptions
    ds = backend._ds_constructor.get_domain_state_dict()
    assert ds["_ds_unsat"] == ["_clinguin_unsat"]
    assert "_clinguin_assume(wrong,true)" in ds["_ds_assume"]
    assert "_clinguin_assume(object(c),true)" in ds["_ds_assume"]

    backend.remove_assumption_signature("object(any)")
    assert (symbolw, True) in backend._assumptions
    assert (symbolc, True) not in backend._assumptions

    backend.clear_assumptions()
    assert (symbolw, True) not in backend._assumptions
    ds = backend._ds_constructor.get_domain_state_dict()
    assert ds["_ds_unsat"] == []

    backend.add_assumption("object(c)", "false")
    assert (symbolc, False) in backend._assumptions
    ds = backend._ds_constructor.get_domain_state_dict()
    assert "_all(object(c))" not in ds["_ds_brave"]
    assert "_clinguin_assume(object(c),false)" in ds["_ds_assume"]

    backend.remove_assumption("object(c)")
    assert (symbolc, False) not in backend._assumptions


def test_interaction_atoms():
    """Test initialization of the logging module."""
    args = BackendArgs(domain_files=["tests/data/encoding.lp"], ui_files=["tests/data/ui.lp"])
    backend = ClingoBackend(args)
    id_control = id(backend._ctl)
    symbol = parse_term("new")

    backend.add_atom("new")
    assert symbol in backend._atoms
    ds = backend._ds_constructor.get_domain_state_dict()
    assert "_all(new)" in ds["_ds_cautious"]
    assert "_clinguin_atom(new)" in ds["_ds_atom"]
    assert id(backend._ctl) != id_control  # Ensure ctl is new

    backend._add_atom(symbol)
    backend.add_atom("new")

    backend.clear_atoms()
    assert symbol not in backend._atoms


def test_basic_interaction():
    """Test initialization of the logging module."""
    args = BackendArgs(domain_files=["tests/data/encoding.lp"], ui_files=["tests/data/ui.lp"])
    backend = ClingoBackend(args)
    backend.get()
    assert backend._model is not None
    assert len(backend._model) == 3
    assert backend._unsat_core is None
    assert backend._handler is None
    assert backend._iterator is None

    backend.next_solution()
    assert backend._model is not None
    assert backend._handler is not None
    assert backend._iterator is not None
    assert len(backend._assumptions) == 0

    backend.select()
    assert len(backend._assumptions) == 3
    assert backend._handler is None
    assert backend._iterator is None


def test_ds():
    """Test initialization of the logging module."""
    args = BackendArgs(domain_files=["tests/data/encoding.lp"], ui_files=["tests/data/ui.lp"])
    backend = ClingoBackend(args)
    ds = backend._ds_constructor.get_domain_state_dict()
    # Check all expected keys exist
    expected_keys = [
        "_ds_context",
        "_ds_constants",
        "_ds_browsing",
        "_ds_cautious_optimal",
        "_ds_brave_optimal",
        "_ds_cautious",
        "_ds_brave",
        "_ds_model",
        "_ds_opt",
        "_ds_unsat",
        "_ds_assume",
        "_ds_atom",
        "_ds_external",
    ]
    for key in expected_keys:
        assert key in ds

    # Check values for some keys (order may change)
    assert set(ds["_ds_cautious_optimal"]) == {"_all_opt(object(a))", "_all_opt(object(b))"}
    assert set(ds["_ds_brave_optimal"]) == {
        "_any_opt(object(a))",
        "_any_opt(object(b))",
        "_any_opt(object(c))",
        "_any_opt(object(d))",
    }
    assert set(ds["_ds_cautious"]) == {"_all(object(a))", "_all(object(b))"}
    assert set(ds["_ds_brave"]) == {
        "_any(object(a))",
        "_any(object(b))",
        "_any(object(c))",
        "_any(object(d))",
    }
    assert set(ds["_ds_model"]) == {"object(a)", "object(b)", "object(c)"}
    assert ds["_ds_opt"] == ["_clinguin_cost(())"]
    assert ds["_ds_unsat"] == []
    assert ds["_ds_assume"] == []
    assert ds["_ds_external"] == []


def test_set_constants():
    """Test _set_constant method"""
    args = BackendArgs(domain_files=["tests/data/encoding.lp"], ui_files=["tests/data/ui.lp"])
    backend = ClingoBackend(args)

    # Test with quoted strings
    backend._set_constant('"myconst"', '"myvalue"')
    assert backend._constants["myconst"] == "myvalue"

    # Test with unquoted
    backend._set_constant("const2", 42)
    assert backend._constants["const2"] == "42"


def test_set_external():
    """Test _set_external method with all state transitions"""
    args = BackendArgs(domain_files=["tests/data/encoding.lp"], ui_files=["tests/data/ui.lp"])
    backend = ClingoBackend(args)

    symbol = parse_term("external_atom")

    # Set external to true
    backend._set_external(symbol, "true")
    assert symbol in backend._externals["true"]
    assert symbol not in backend._externals["false"]
    assert symbol not in backend._externals["released"]

    # Transition from true to release
    backend._set_external(symbol, "release")
    assert symbol not in backend._externals["true"]
    assert symbol not in backend._externals["false"]
    assert symbol in backend._externals["released"]

    symbol2 = parse_term("external_atom2")

    # Set external to false
    backend._set_external(symbol2, "false")
    assert symbol2 not in backend._externals["true"]
    assert symbol2 in backend._externals["false"]
    assert symbol2 not in backend._externals["released"]

    # Transition from false to release
    backend._set_external(symbol2, "release")
    assert symbol2 not in backend._externals["true"]
    assert symbol2 not in backend._externals["false"]
    assert symbol2 in backend._externals["released"]

    symbol3 = parse_term("external_atom3")

    # Test false to true transition
    backend._set_external(symbol3, "false")
    backend._set_external(symbol3, "true")
    assert symbol3 in backend._externals["true"]
    assert symbol3 not in backend._externals["false"]
    assert symbol3 not in backend._externals["released"]

    # Test true to false transition
    backend._set_external(symbol3, "false")
    assert symbol3 not in backend._externals["true"]
    assert symbol3 in backend._externals["false"]
    assert symbol3 not in backend._externals["released"]

    # Test invalid value raises error
    with pytest.raises(ValueError, match="Invalid external value invalid. Must be true, false or relase"):
        backend._set_external(symbol, "invalid")


def test_next_solution_basic():
    """Test basic next_solution functionality"""
    args = BackendArgs(domain_files=["tests/data/encoding.lp"], ui_files=["tests/data/ui.lp"])
    backend = ClingoBackend(args)

    # First call should initialize iterator
    assert backend._iterator is None
    assert backend._handler is None

    backend.next_solution()

    # Should have iterator and handler now
    assert backend._iterator is not None
    assert backend._handler is not None
    assert backend._model is not None


def test_next_solution_opt_mode_change():
    """Test next_solution when opt_mode changes"""
    args = BackendArgs(domain_files=["tests/data/encoding.lp"], ui_files=["tests/data/ui.lp"])
    backend = ClingoBackend(args)

    # Start browsing with default mode
    backend.next_solution("ignore")
    assert backend._iterator is not None

    # Change opt_mode should trigger _outdate()
    backend.next_solution("optN")
    # Should still have iterator but configuration should change
    assert backend._iterator is not None


def test_select_no_model():
    """Test select when no model exists"""
    args = BackendArgs(domain_files=["tests/data/encoding.lp"], ui_files=["tests/data/ui.lp"])
    backend = ClingoBackend(args)
    backend._model = None

    backend.select()

    # Should have error message about no solution
    messages = [msg for msg in backend._messages if "No solution" in msg[0]]
    assert len(messages) > 0
    assert "There is no solution to be selected" in messages[0][1]
    assert messages[0][2] == "danger"


def test_select_with_show_program():
    """Test select with valid show program"""
    args = BackendArgs(domain_files=["tests/data/encoding.lp"], ui_files=["tests/data/ui.lp"])
    backend = ClingoBackend(args)
    backend.get()

    backend.select("#show object/1.")

    assert len(backend._assumptions) > 0
    assert backend._handler is None
    assert backend._iterator is None


def test_select_with_invalid_show_program():
    """Test select with invalid show program syntax"""
    args = BackendArgs(domain_files=["tests/data/encoding.lp"], ui_files=["tests/data/ui.lp"])
    backend = ClingoBackend(args)
    backend.get()

    with pytest.raises(Exception, match="Show program can't be parsed"):
        backend.select("invalid syntax :-.")


def test_select_with_empty_show_program():
    """Test select with empty show program"""
    args = BackendArgs(domain_files=["tests/data/encoding.lp"], ui_files=["tests/data/ui.lp"])
    backend = ClingoBackend(args)
    backend.get()

    backend.select("")

    assert len(backend._assumptions) > 0


def test_select_excludes_externals():
    """Test that select excludes external atoms from assumptions"""
    args = BackendArgs(domain_files=["tests/data/encoding.lp"], ui_files=["tests/data/ui.lp"])
    backend = ClingoBackend(args)

    # Add some external atoms
    ext_symbol = parse_term("external_atom")
    backend._externals["true"].add(ext_symbol)
    backend._externals["false"].add(parse_term("external_atom2"))

    backend.get()
    backend._model = list(backend._model) + [ext_symbol]
    backend.select()

    # External atoms should not be in assumptions
    assumption_symbols = [a[0] for a in backend._assumptions]
    assert ext_symbol not in assumption_symbols


def test_set_constant_public():
    """Test public set_constant method"""
    args = BackendArgs(domain_files=["tests/data/encoding.lp"], ui_files=["tests/data/ui.lp"])
    backend = ClingoBackend(args)

    # Set a constant using the public method
    backend.set_constant("myconst", "myvalue")

    # Verify constant was set
    assert backend._constants["myconst"] == "myvalue"


def test_set_external_public():
    """Test public set_external method"""
    args = BackendArgs(domain_files=["tests/data/encoding.lp"], ui_files=["tests/data/ui.lp"])
    backend = ClingoBackend(args)

    # Set external using public method
    backend.set_external("external_atom", "true")

    # Verify it was set
    symbol = parse_term("external_atom")
    assert symbol in backend._externals["true"]


def test_remove_atom():
    """Test remove_atom method for both existing and non-existing atoms"""
    args = BackendArgs(domain_files=["tests/data/encoding.lp"], ui_files=["tests/data/ui.lp"])
    backend = ClingoBackend(args)
    symbol = parse_term("new_atom")

    backend.add_atom("new_atom")
    assert symbol in backend._atoms
    id_control_before = id(backend._ctl)

    backend.remove_atom("new_atom")
    assert symbol not in backend._atoms
    assert id(backend._ctl) != id_control_before

    initial_atoms_count = len(backend._atoms)
    backend.remove_atom("non_existing_atom")
    assert len(backend._atoms) == initial_atoms_count


def test_load_and_add_file_not_found():
    """Test _load_and_add when domain file doesn't exist"""
    args = BackendArgs(domain_files=["tests/data/encoding.lp"], ui_files=["tests/data/ui.lp"])
    backend = ClingoBackend(args)

    backend._args.domain_files = ["nonexistent_file.lp"]

    with pytest.raises(FileNotFoundError, match="File nonexistent_file.lp does not exist"):
        backend.restart()


def test_load_and_add_syntax_error():
    """Test _load_and_add when domain file has syntax errors"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".lp", delete=False) as temp_file:
        temp_file.write("invalid syntax :-. this is not valid ASP syntax at all \\invalid")
        temp_file_path = temp_file.name

    args = BackendArgs(domain_files=["tests/data/encoding.lp"], ui_files=["tests/data/ui.lp"])
    backend = ClingoBackend(args)

    backend._args.domain_files = [temp_file_path]

    with pytest.raises(Exception):
        backend.restart()


def test_stop_browsing():
    """Test stop_browsing method"""
    args = BackendArgs(domain_files=["tests/data/encoding.lp"], ui_files=["tests/data/ui.lp"])
    backend = ClingoBackend(args)

    # Start browsing to set up handler and iterator
    backend.next_solution()
    assert backend._handler is not None
    assert backend._iterator is not None
    assert backend._model is not None

    # Stop browsing
    backend.stop_browsing()

    # Verify browsing state is cleared
    assert backend._handler is None
    assert backend._iterator is None
    assert backend._model is None


def test_on_model():
    """Test _on_model when model has optimization cost"""
    backend = ClingoBackend(BackendArgs(domain_files=["tests/data/encoding.lp"]))
    mock_model = Mock()
    mock_model.cost = [1]
    mock_model.optimality_proven = False
    backend._on_model(mock_model)


def test_update_ui_state_with_messages():
    """Test _update_ui_state processes messages"""
    backend = ClingoBackend(BackendArgs(domain_files=["tests/data/encoding.lp"], ui_files=["tests/data/ui.lp"]))
    backend._messages = [("Test", "Test message", "info")]
    backend.get()


def test_set_context():
    """Test _set_context method"""
    backend = ClingoBackend(BackendArgs(domain_files=["tests/data/encoding.lp"]))
    context = {"key": "value", "user": "test"}
    backend._set_context(context)
    assert backend._context == context


def test_ground():
    """Test ground method"""
    backend = ClingoBackend(BackendArgs(domain_files=["tests/data/encoding.lp"]))
    backend.ground("base")


def test_update():
    """Test update method"""
    backend = ClingoBackend(BackendArgs(domain_files=["tests/data/encoding.lp"]))
    backend.update()


def test_download_invalid_show_program():
    """Test download with invalid show program"""
    backend = ClingoBackend(BackendArgs(domain_files=["tests/data/encoding.lp"]))
    backend.get()

    with pytest.raises(Exception, match="Show program can't be parsed"):
        backend.download("invalid syntax :-.")


def test_next_solution_stop_iteration_optimizing():
    """Test next_solution StopIteration handling with optimization"""
    from unittest.mock import Mock

    backend = ClingoBackend(BackendArgs(domain_files=["tests/data/encoding.lp"]))

    backend.next_solution("optN")

    mock_iterator = Mock()
    mock_iterator.__next__ = Mock(side_effect=StopIteration)
    backend._iterator = mock_iterator

    backend.next_solution("optN")

    assert any("No more optimal solutions" in msg[1] for msg in backend._messages)


def test_next_solution_skip_non_optimal():
    """Test next_solution skipping non-optimal models"""
    from unittest.mock import Mock

    backend = ClingoBackend(BackendArgs(domain_files=["tests/data/encoding.lp"]))
    backend.next_solution("optN")

    non_optimal = Mock(cost=[5], optimality_proven=False, symbols=Mock(return_value=[]))
    optimal = Mock(cost=[3], optimality_proven=True, symbols=Mock(return_value=[]))
    backend._iterator = Mock(__next__=Mock(side_effect=[non_optimal, optimal]))

    backend.next_solution("optN")
    assert backend._iterator.__next__.call_count == 2


def test_next_solution_no_more_solutions():
    """Test next_solution 'No more solutions' message"""
    backend = ClingoBackend(BackendArgs(domain_files=["tests/data/encoding.lp"]))
    backend.next_solution()
    backend._iterator = iter([])
    backend.next_solution()

    assert any("No more solutions" in msg[1] for msg in backend._messages)


def test_next_solution_timeout():
    """Test next_solution timeout handling"""
    from unittest.mock import Mock, patch

    backend = ClingoBackend(BackendArgs(domain_files=["tests/data/encoding.lp"], opt_timeout=1))
    backend.next_solution("optN")

    with patch("clinguin.server.backends.clingo_backend.time") as mock_time:
        mock_time.time.side_effect = [0, 2]
        backend._iterator = Mock(
            __next__=Mock(return_value=Mock(cost=[5], optimality_proven=False, symbols=Mock(return_value=[])))
        )
        backend.next_solution("optN")

    assert backend._model is not None


def test_remove_assumption_signature_no_match():
    """Test remove_assumption_signature when arguments don't match"""
    backend = ClingoBackend(BackendArgs(domain_files=["tests/data/encoding.lp"]))
    backend.add_assumption("person(anna,25)")

    backend.remove_assumption_signature("person(anna,30)")

    assert len(backend._assumptions) == 1


def test_remove_assumption_not_found():
    """Test remove_assumption when assumption doesn't exist"""
    backend = ClingoBackend(BackendArgs(domain_files=["tests/data/encoding.lp"]))
    backend.add_assumption("object(a)")
    backend.remove_assumption("object(z)")

    assert len(backend._assumptions) == 1
