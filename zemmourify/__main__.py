"""Entry point for zemmourify

Can be use as script or as binary
```
python -m zemmourify Jindun
zemmourify Jindun
```
"""
import typer

from zemmourify.utils import query

app = typer.Typer()


@app.command("change")
def change(name: str):
    """Change any firstname into french firstname"""
    typer.echo(f"{query(name)}")


if __name__ == "__main__":
    app()
