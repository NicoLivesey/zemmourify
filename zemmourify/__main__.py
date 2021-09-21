"""Entry point for zemmourify

Can be use as script or as binary
```
python -m zemmourify square --number 2
zemmourify square --number 2
```
"""
import typer

app = typer.Typer()


@app.command("square")
def square(number: int = typer.Option(2, help="Input number")):
    """Compute square of the given number"""
    typer.echo(f"Square of {number} is {number}")


@app.command("pow4")
def pow4(x: int):
    """Compute x^4"""
    typer.echo(f"Power 4 of {x} is {x}")


if __name__ == "__main__":
    app()
