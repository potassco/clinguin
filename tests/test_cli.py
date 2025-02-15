"""
Test the CLI commands and ensure they run without crashing.
"""

import subprocess
import sys
import pytest


def run_cli_command(*args: str, timeout: int = 5) -> tuple[str, str, int]:
    """Run the CLI command with a timeout to prevent it from getting stuck."""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "clinguin", *args],
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        return result.stdout, result.stderr, result.returncode
    except subprocess.TimeoutExpired:
        return "", "Process timed out!", 1


@pytest.mark.parametrize(
    "command",
    [
        ["server", "--port", "9000"],
        ["client", "--port", "8001"],
    ],
)
def test_cli_runs_without_errors(command: list[str]):
    """Ensure CLI commands run without crashing."""
    _, stderr, exit_code = run_cli_command(*command, timeout=3)
    assert exit_code in (0, 1)
    assert "Usage:" not in stderr, "CLI showed help instead of running."


def test_cli_help():
    """Ensure `clinguin --help` prints help information."""
    stdout, _, exit_code = run_cli_command("--help")
    assert exit_code == 0
    assert "Clinguin CLI - Start the server or client." in stdout


def test_cli_invalid_command():
    """Ensure invalid commands fail with an error."""
    _, stderr, exit_code = run_cli_command("invalid_command")
    assert exit_code != 0
    assert "invalid choice" in stderr.lower()


def test_cli_missing_command():
    """Ensure running `clinguin` without arguments fails."""
    _, stderr, exit_code = run_cli_command()
    assert exit_code != 0
    assert "the following arguments are required" in stderr.lower()
