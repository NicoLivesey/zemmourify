"""Entry point for zemmourify

Can be use as script or as binary
```
python -m zemmourify Jindun
zemmourify Jindun
zemmourify Jindun --log
```
"""
import typer

from zemmourify.logs import mute_logger
from zemmourify.utils import query

app = typer.Typer()


@app.command("change")
def change(name: str, log: bool = False):
    """Change any firstname into french firstname"""
    if not log:
        mute_logger()
    names = query(name, log)
    typer.echo("You have been zemmourified, you can choose your new name among this list:")
    typer.echo(f"{names}")


if __name__ == "__main__":
    app()
