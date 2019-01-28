from pathlib import Path
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from .notebook import Notebook
from .setup_log import logger


def run_and_record_errors(notebook_contents, path, kernel=None,
                          timeout=600):
    kwargs = {'timeout': timeout}
    if kernel:
        kwargs['kernel_name'] = kernel
    ep = ExecutePreprocessor(allow_errors=True, **kwargs)
    path_metadata = {'metadata': {'path': path}}
    nb, _ = ep.preprocess(notebook_contents, path_metadata)
    output_notebook = Notebook(nb)
    return (not output_notebook.contains_errors(),
            ep.kernel_name,
            output_notebook.summarize_errors())


def load_and_run_notebook(file_path, kernel=None, timeout=600):
    with open(file_path) as nb_handle:
        nb_contents = nbformat.read(nb_handle, as_version=4)

    path = Path(file_path).parent
    return run_and_record_errors(nb_contents, path, kernel, timeout)


def process_file(filename, kernel=None, timeout=600):
    """Execute single file.
    See process_file_or_directory for parameter description.
    """
    notebook_okay, kernel_name, error_message = load_and_run_notebook(filename,
                                                         kernel, timeout)  # noqa E128
    status = "Success" if notebook_okay else "Failure"
    summary = f'{filename}:\t{status}\t(kernel: {kernel_name})'
    logger.info(summary)
    if not notebook_okay:
        logger.debug(error_message)


def process_directory(dirname, kernel=None, timeout=600):
    """Recursively executes notebooks in dirname.

    See process_file_or_directory for parameter description.
    """
    filenames = [f for f in Path(dirname).glob('**/*.ipynb')
                 if '.ipynb_checkpoints' not in str(f)]
    for filename in filenames:
        process_file(filename, kernel, timeout)


def process_file_or_directory(path, kernel=None, timeout=600):
    """Runs file at path, or all files in directory path.

    If directory is passed, it is searched recursively, finding
    all notebooks outside of .ipynb_checkpoint files.

    Parameters
    ----------
    path : string or Path
       Location of file to process (or directory to process)
    kernel: string
       Name of kernel (as listed as kernel display name in
       Jupyter). List of names can be found from 
       $ jupyter kernelspec list
    timeout: integer
       Number of seconds to run a notebook before it times
       out.

    Returns
    -------
    None

    Instead, writes to stdout and registered loggers.
    """
    if Path(path).is_dir():
        process_directory(path, kernel, timeout)
    else:
        process_file(path, kernel, timeout)
