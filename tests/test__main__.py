import subprocess

from typer.testing import CliRunner

from zemmourify.__main__ import app

runner = CliRunner()


def test_app():
    result = runner.invoke(app, ["square", "--number", "3"])
    assert result.exit_code == 0
    assert "9" in result.stdout


def test_run_as_scrip():
    cmd = "python -m zemmourify square --number 2"
    out = subprocess.check_output(cmd.split(" "))
    assert "4" in str(out)
