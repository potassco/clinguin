import os
from argparse import ArgumentParser
from dataclasses import dataclass, field, fields
from types import SimpleNamespace
from typing import Optional


@dataclass
class ClinguinMessage:
    """
    Represents a message in the Clinguin UI.
    Messages can then be used in the Clinguin UI to display alerts and notifications.
    They are included in the domain state using predicate `_clinguin_message`.

    Attributes:
        message_id (str): Unique identifier for the message.
        message_type (str): Type of the message (e.g., "success", "error", "info", "warning").
        title (str): Title of the message.
        content (str): Content or body of the message.
    """

    message_id: str
    message_type: str
    title: str
    content: str


@dataclass
class BackendArgs:
    """Base arguments for ClingoBackend."""

    VALID_OPT_MODES = {"opt", "enum", "optN", "ignore"}

    domain_files: list[str] = field(default_factory=list)
    ui_files: list[str] = field(default_factory=list)
    const: list[str] = field(default_factory=list)
    clingo_ctl_arg: list[str] = field(default_factory=list)
    default_opt_mode: str = "ignore"
    opt_timeout: Optional[int] = None

    def __post_init__(self):
        """Validates that file paths exist and are actual files."""
        for file_path in self.domain_files + self.ui_files:
            if not os.path.isfile(file_path):
                raise ValueError(f"Invalid file path: {file_path} does not exist or is not a file.")

        # Validate `default_opt_mode`
        if self.default_opt_mode not in self.VALID_OPT_MODES:
            valid_options = ", ".join(self.VALID_OPT_MODES)
            raise ValueError(
                f"Invalid default_opt_mode: '{self.default_opt_mode}'. " f"Must be one of: {valid_options}"
            )

        for c in self.const:
            values = c.split("=")
            if (len(values) != 2) or (not values[0]) or (not values[1]):
                raise ValueError("Invalid constant format. Expected name=value.")

    @classmethod
    def from_args(cls, args: SimpleNamespace):
        """Creates BackendArgs from `args`, filtering out extra fields."""
        valid_fields = {f.name for f in fields(cls)}  # Get valid field names
        filtered_args = {k: v for k, v in vars(args).items() if k in valid_fields}  # Keep only valid fields
        return cls(**filtered_args)

    @classmethod
    def register_options(cls, parser: ArgumentParser):
        """Registers CLI options dynamically based on BackendArgs fields."""
        defaults = cls()  # Create a BackendArgs instance to get default values

        parser.add_argument(
            "--domain-files",
            nargs="+",
            help="Files with the domain-specific encodings.",
            default=defaults.domain_files,
            metavar="",
        )
        parser.add_argument(
            "--ui-files", nargs="+", help="Files defining the UI encodings.", default=defaults.ui_files, metavar=""
        )
        parser.add_argument(
            "-c",
            "--const",
            action="append",
            help="Constant passed to Clingo, e.g., <id>=<term>.",
            default=defaults.const,
            metavar="",
        )
        parser.add_argument(
            "--clingo-ctl-arg",
            action="append",
            help="Arguments passed to the Clingo control object.",
            default=defaults.clingo_ctl_arg,
            metavar="",
        )
        parser.add_argument(
            "--default-opt-mode",
            type=str,
            help="Default optimization mode.",
            default=defaults.default_opt_mode,
            metavar="",
        )
        parser.add_argument(
            "--opt-timeout",
            type=int,
            help="Optional timeout for optimization.",
            default=defaults.opt_timeout,
            metavar="",
        )
