"""
Test cases for main application functionality using pytest.
"""

import pytest

from clinguin.utils import logging
from clinguin.utils.logging import get_logger
from clinguin.server.backends import ClingoBackend, BackendArgs
from clingo import parse_term
import os
import json


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
