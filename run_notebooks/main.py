import click
import logging

from .config import Config
from .run_all_notebooks import process_file_or_directory
from .setup_log import setup_logger


# Useful technique as there is only one command in this application
# More sophisticated approaches are
# 1. Setting a custom command class
#    https://stackoverflow.com/questions/46358797/python-click-supply-arguments-and-options-from-a-configuration-file
# 2. Creating a new context object to pass along
#    https://www.brianthicks.com/post/2014/11/03/build-modular-command-line-tools-with-click/
#
class Parameters():
    "Simplified class for resolving config files and pass parameters."
    def __init__(self, context, config_file=None):
        # Load config first, so it can be overwritten by context
        config = Config()
        config.load_default_config()
        if config_file:
            config.load_config_from_file(config_file)
        self.__dict__ = {key: value for key, value in config.__dict__.items()}
        for key, value in context.params.items():
            if value is not None:
                self.__dict__[key] = value


@click.command()
@click.argument('notebooks', nargs=-1)
@click.option('-t', '--timeout', type=int,
              help="Number of seconds before timing out a notebook run")
@click.option('-c', '--config-file', type=click.Path(),
              help="Config file to load settings from")
@click.option('-k', '--kernel-name',
              help="Name of the kernel to use "
                   "'jupyter kernelspec list' gets a list")
@click.option('--summary/--no-summary', default=None,
              help="Determines if summary log is written")
@click.option('--detail/--no-detail', default=None,
              help="Determines if detailed log is written")
@click.option('--summary-file', type=click.Path(),
              help="Location of the file for summary of results")
@click.option('--detail-file', type=click.Path(),
              help="Location of the file for detailed list of errors")
@click.pass_context
def pythonrunner(context, config_file, *args, **kwargs):
    """Processes NOTEBOOKS and logs errors.

    Running these notebooks does not save the notebook,
    but if the notebook writes files or alters records
    running this command will execute those commands.

    NOTEBOOKS can be individual notebook files, or
    directories. Files in .ipynb_checkpoints are excluded
    when searching directories.

    By default, output is logged in the hidden files
    .error_log_summary and .error_log_detail
    """
    params = Parameters(context, config_file)
    if params.summary and params.summary_file:
        setup_logger(params.summary_file, level=logging.INFO)
    if params.detail and params.detail_file:
        setup_logger(params.detail_file)

    for notebook_name in params.notebooks:
        process_file_or_directory(notebook_name, kernel=params.kernel_name,
                                  timeout=params.timeout)


if __name__ == '__main__':
    pythonrunner()
