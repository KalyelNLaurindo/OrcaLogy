"""Tests for the Typer CLI root controller and base commands.

Verifies that the CLI entry point is wired up correctly: help output is
formatted, the version flag returns the right string, and unknown commands
are rejected with a non-zero exit code.
"""

from typer.testing import CliRunner

from orcalogy.cli.commands import VERSION, app

runner = CliRunner()


class TestCliBaseCommands:
    """Group: base CLI setup — help, version, and error handling."""

    def test_help_flag_returns_exit_zero(self) -> None:
        """Invoking --help should succeed without any errors."""
        result = runner.invoke(app, ["--help"])
        assert result.exit_code == 0

    def test_help_output_contains_program_name(self) -> None:
        """Help text must reference the CLI name so users recognise the tool."""
        result = runner.invoke(app, ["--help"])
        assert "orca" in result.output.lower()

    def test_help_output_contains_version_option(self) -> None:
        """Help text must advertise --version so users can check what is installed."""
        result = runner.invoke(app, ["--help"])
        assert "--version" in result.output

    def test_version_flag_returns_version_string(self) -> None:
        """--version must print the current package version and exit cleanly."""
        result = runner.invoke(app, ["--version"])
        assert result.exit_code == 0
        assert VERSION in result.output

    def test_unknown_command_returns_nonzero_exit(self) -> None:
        """An unrecognized subcommand must be rejected with a non-zero exit code."""
        result = runner.invoke(app, ["nonexistent-command"])
        assert result.exit_code != 0
