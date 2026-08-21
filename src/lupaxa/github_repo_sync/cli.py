"""
Command-line interface for Lupaxa GitHub Repository Sync.

This module defines the flat command-line interface, applies presentation
options, selects the requested operating mode, and returns process exit codes.
Application behaviour is implemented in commands.py.
"""

from __future__ import annotations

import argparse
from collections.abc import Sequence
from pathlib import Path
import sys

from .commands import (
    run_plan,
    run_status,
    run_sync,
    run_validate,
)
from .constants import (
    DEFAULT_CONFIG_FILENAME,
    EXIT_FAILURE,
    PROGRAM_ALIAS,
    PROGRAM_VERSION_STRING,
)
from .display import (
    configure_console,
    print_error,
    print_unhandled_error,
)


def create_parser() -> argparse.ArgumentParser:
    """
    Create the application argument parser.

    Returns:
        Configured argument parser.

    """

    parser = argparse.ArgumentParser(
        prog=PROGRAM_ALIAS,
        description=(
            "Clone and update configured GitHub repositories while "
            "protecting repositories with unsafe local states."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            f"  {PROGRAM_ALIAS}\n"
            f"  {PROGRAM_ALIAS} --config repositories.yaml\n"
            f"  {PROGRAM_ALIAS} --validate\n"
            f"  {PROGRAM_ALIAS} --plan\n"
            f"  {PROGRAM_ALIAS} --status\n"
            f"  {PROGRAM_ALIAS} --status --ignore-clean --offline\n"
            f"  {PROGRAM_ALIAS} --results-table\n"
            f"  {PROGRAM_ALIAS} --recover-rewritten-history\n"
            f"  {PROGRAM_ALIAS} --no-progress --no-repository-output\n"
            "\n"
            "Repository synchronisation is performed by default. Use "
            "--validate or --plan to inspect the configuration without "
            "modifying repositories. Use --status to audit cleanliness "
            "without changing working trees, branches, or commits (online "
            "mode may fetch remote-tracking refs)."
        ),
    )

    _add_mode_arguments(parser)
    _add_status_arguments(parser)
    _add_sync_behaviour_arguments(parser)
    _add_configuration_arguments(parser)
    _add_presentation_arguments(parser)
    _add_sync_output_arguments(parser)

    return parser


def _add_mode_arguments(
    parser: argparse.ArgumentParser,
) -> None:
    """
    Add mutually exclusive operating mode arguments.

    Synchronisation is the default operation and therefore does not require
    an explicit option.

    Args:
        parser:
            Application argument parser.

    """

    group = parser.add_argument_group(
        "operating modes",
        (
            "Select an alternative operating mode. When none is selected, "
            "configured repositories are synchronised."
        ),
    )

    modes = group.add_mutually_exclusive_group()

    modes.add_argument(
        "--validate",
        action="store_true",
        help=(
            "Validate and normalise the configuration, print a compact "
            "validation result, and exit without synchronising repositories."
        ),
    )

    modes.add_argument(
        "--plan",
        action="store_true",
        help=(
            "Display the resolved synchronisation plan, including effective "
            "clone protocols and repository destinations, then exit without "
            "modifying repositories."
        ),
    )

    modes.add_argument(
        "--status",
        action="store_true",
        help=(
            "Check configured repositories for unclean or unpushed local state "
            "and exit without changing working trees, branches, or commits "
            "(online mode may fetch remote-tracking refs)."
        ),
    )


def _add_status_arguments(
    parser: argparse.ArgumentParser,
) -> None:
    """
    Add status-check options.

    Args:
        parser:
            Application argument parser.

    """

    status = parser.add_argument_group("status options")

    status.add_argument(
        "--ignore-clean",
        action="store_true",
        help="With --status, omit repositories that are fully clean from output.",
    )

    status.add_argument(
        "--offline",
        action="store_true",
        help=(
            "With --status, skip fetching remotes and compare against existing "
            "remote-tracking refs."
        ),
    )


def _add_sync_behaviour_arguments(
    parser: argparse.ArgumentParser,
) -> None:
    """
    Add synchronisation behaviour arguments.

    Args:
        parser:
            Application argument parser.

    """

    group = parser.add_argument_group("synchronisation")

    group.add_argument(
        "--recover-rewritten-history",
        action="store_true",
        help=(
            "Reset a clean local branch onto rewritten remote history "
            "(no shared ancestor). Without this flag those repositories "
            "are skipped."
        ),
    )


def _add_configuration_arguments(
    parser: argparse.ArgumentParser,
) -> None:
    """
    Add configuration-related arguments.

    Args:
        parser:
            Application argument parser.

    """

    group = parser.add_argument_group("configuration")

    group.add_argument(
        "-c",
        "--config",
        dest="config_path",
        type=Path,
        default=Path(DEFAULT_CONFIG_FILENAME),
        metavar="FILE",
        help=(
            "Path to the YAML, JSON, or JSON5 configuration file "
            f"(default: {DEFAULT_CONFIG_FILENAME}, then "
            ".yml, .json, or .json5 in the same directory)."
        ),
    )


def _add_presentation_arguments(
    parser: argparse.ArgumentParser,
) -> None:
    """
    Add console presentation arguments.

    Args:
        parser:
            Application argument parser.

    """

    group = parser.add_argument_group("presentation")

    group.add_argument(
        "--no-header",
        action="store_true",
        help="Do not print the application heading.",
    )

    group.add_argument(
        "--no-colour",
        "--no-color",
        dest="no_colour",
        action="store_true",
        help="Disable coloured console output.",
    )

    group.add_argument(
        "--console-width",
        type=_positive_integer,
        metavar="COLUMNS",
        help=(
            "Set the console width explicitly. The application will still "
            "constrain the value to its supported range."
        ),
    )

    group.add_argument(
        "--version",
        action="version",
        version=PROGRAM_VERSION_STRING,
        help="Show the program version and exit.",
    )


def _add_sync_output_arguments(
    parser: argparse.ArgumentParser,
) -> None:
    """
    Add synchronisation output arguments.

    These options affect normal repository synchronisation. They are ignored
    when validation or planning mode is selected.

    Args:
        parser:
            Application argument parser.

    """

    group = parser.add_argument_group("synchronisation output")

    group.add_argument(
        "--no-configuration",
        action="store_true",
        help="Do not print the configuration summary before synchronising.",
    )

    group.add_argument(
        "--no-progress",
        action="store_true",
        help="Disable the repository synchronisation progress display.",
    )

    group.add_argument(
        "--no-repository-output",
        action="store_true",
        help=("Do not print an individual result for each synchronised repository."),
    )

    group.add_argument(
        "--results-table",
        action="store_true",
        help=("Print a detailed table containing every repository result."),
    )

    group.add_argument(
        "--no-failure-table",
        action="store_true",
        help="Do not print the detailed repository failure table.",
    )

    group.add_argument(
        "--no-summary-table",
        action="store_true",
        help="Do not print the Rich synchronisation summary table.",
    )


def _positive_integer(
    value: str,
) -> int:
    """
    Parse a positive integer argument.

    Args:
        value:
            Raw command-line value.

    Returns:
        Parsed positive integer.

    Raises:
        argparse.ArgumentTypeError:
            If the supplied value is not a positive integer.

    """

    try:
        parsed_value = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"{value!r} is not an integer.") from exc

    if parsed_value <= 0:
        raise argparse.ArgumentTypeError("value must be greater than zero.")

    return parsed_value


def _run_selected_mode(
    arguments: argparse.Namespace,
) -> int:
    """
    Execute the selected operating mode.

    Synchronisation is performed when no alternative operating mode was
    selected.

    Args:
        arguments:
            Parsed command-line arguments.

    Returns:
        Process exit code.

    """

    show_header = not arguments.no_header

    if arguments.ignore_clean and not arguments.status:
        print_error("--ignore-clean can only be used with --status.")
        return EXIT_FAILURE

    if arguments.offline and not arguments.status:
        print_error("--offline can only be used with --status.")
        return EXIT_FAILURE

    if arguments.recover_rewritten_history and (
        arguments.status or arguments.validate or arguments.plan
    ):
        print_error("--recover-rewritten-history can only be used when synchronising.")
        return EXIT_FAILURE

    if arguments.validate:
        return run_validate(
            config_path=arguments.config_path,
            show_header=show_header,
        )

    if arguments.plan:
        return run_plan(
            config_path=arguments.config_path,
            show_header=show_header,
        )

    if arguments.status:
        return run_status(
            config_path=arguments.config_path,
            show_header=show_header,
            ignore_clean=arguments.ignore_clean,
            offline=arguments.offline,
            show_progress=not arguments.no_progress,
            show_repository_output=not arguments.no_repository_output,
            show_results_table=arguments.results_table,
            show_summary_table=not arguments.no_summary_table,
        )

    return run_sync(
        config_path=arguments.config_path,
        show_header=show_header,
        show_configuration=not arguments.no_configuration,
        show_progress=not arguments.no_progress,
        show_repository_output=not arguments.no_repository_output,
        show_results_table=arguments.results_table,
        show_failure_table=not arguments.no_failure_table,
        show_summary_table=not arguments.no_summary_table,
        recover_rewritten_history=arguments.recover_rewritten_history,
    )


def main(
    argv: Sequence[str] | None = None,
) -> int:
    """
    Run the command-line interface.

    Synchronisation is the default operation. Alternative modes are selected
    using mutually exclusive top-level options.

    Args:
        argv:
            Optional command-line arguments excluding the executable name.
            When omitted, arguments are read from ``sys.argv``.

    Returns:
        Process exit code.

    """

    parser = create_parser()

    effective_arguments = list(sys.argv[1:] if argv is None else argv)

    try:
        arguments = parser.parse_args(effective_arguments)

        configure_console(
            width=arguments.console_width,
            no_colour=arguments.no_colour,
        )

        return int(_run_selected_mode(arguments))
    except KeyboardInterrupt:
        print_error("Operation interrupted by the user.")
        return EXIT_FAILURE
    except BrokenPipeError:
        return EXIT_FAILURE
    except Exception as exc:
        print_unhandled_error(exc)
        return EXIT_FAILURE


if __name__ == "__main__":
    raise SystemExit(main())
