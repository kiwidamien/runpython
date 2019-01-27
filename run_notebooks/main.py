import click
import logging

from .config import Config
from .run_all_notebooks import process_file_or_directory
from .setup_log import setup_logger

# This SO answer gives a nice demonstration of how to subclass
# click.Command to allow for loading from a yaml file
# https://stackoverflow.com/questions/46358797/python-click-supply-arguments-and-options-from-a-configuration-file


def CommandWithConfigFile(config_file_param_name):
    class CustomCommandClass(click.Command):
        def invoke(self, context):
            file_config = Config()
            # specified file takes precedence over default, so load
            # it later
            file_config.load_default_config()
            file_config.load_config_from_file(config_file_param_name)

            param_map = {
                'summary': 'log_summary',
                'detail': 'log_detail',
                'summary_file': 'log_summary_name',
                'detail_file': 'log_summary_name'
            }
            # only supply values not given on command line
            for param, value in context.params.items():
                config_key = param_map.get(param, param)
                if (value is None) and (config_key in file_config.__dict__):
                    context.params[param] = file_config.__dict__[config_key]

            return super().invoke(context)

    return CustomCommandClass


@click.command(cls=CommandWithConfigFile('config-file'))
@click.argument('notebooks', nargs=-1)
@click.option('-t', '--timeout', type=int,
              help="Number of seconds before timing out a notebook run")
@click.option('-c', '--config-file', type=click.Path(),
              help="Config file to load settings from")
@click.option('-k', '--kernel_name',
              help="Name of the kernel to use "
                   "'jupyter kernelspec list' gets a list")
@click.option('--summary/--no-summary', default=True,
              help="Determines if summary log is written")
@click.option('--detail/--no-detail', default=True,
              help="Determines if detailed log is written")
@click.option('--summary-file', type=click.Path(),
              help="Location of the file for summary of results")
@click.option('--detail-file', type=click.Path(),
              help="Location of the file for detailed list of errors")
@click.pass_context
def pythonrunner(context, *args, **kwargs):
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
    params = type('', (object,), context.params)()

    if params.summary and params.summary_file:
        setup_logger(params.summary_file, level=logging.INFO)
    if params.detail and params.detail_file:
        setup_logger(params.detail_file)

    for notebook_name in params.notebooks:
        process_file_or_directory(notebook_name, kernel=params.kernel_name,
                                  timeout=params.timeout)


if __name__ == '__main__':
    pythonrunner()
