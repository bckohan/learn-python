from pathlib import Path
import os
import typer
from contextlib import contextmanager


app = typer.Typer()
doc_dir = Path(__file__).parent.parent / 'docs'


@contextmanager
def doc_context():
    assert doc_dir.is_dir()
    start_dir = os.getcwd()
    os.chdir(doc_dir)
    yield
    os.chdir(start_dir)



@app.command()
def build():
    """Build the project."""
    with doc_context():
        os.system('make html')


@app.command()
def clean():
    """Clean the project."""
    with doc_context():
        os.system('make clean')


if __name__ == "__main__":
    app()
