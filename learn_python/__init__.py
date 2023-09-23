import typer
import logging
from termcolor import colored


def main(catch=True):
    def wrap_main(main_func):
        def invoke_main():
            try:
                from learn_python.utils import configure_logging
                configure_logging()
                typer.run(main_func)
            except Exception as err:
                if not catch:
                    raise
                typer.echo(colored(f'Unexpected Error: {str(err)}', 'red'))
                logging.getLogger('learn_python').exception(err)

        return invoke_main
    return wrap_main
