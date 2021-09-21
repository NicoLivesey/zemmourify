import subprocess

from typer.testing import CliRunner

from zemmourify.__main__ import app

runner = CliRunner()


def test_app():
    result = runner.invoke(app, ["Jindun"])
    assert result.exit_code == 0
    assert "Jourdain" in result.stdout


def test_run_as_scrip():
    cmd = "python -m zemmourify Jindun"
    out = subprocess.check_output(cmd.split(" "))
    assert "Justin" in str(out)
