from pathlib import Path
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from notebook import Notebook
from setup_log import logger

# use 'jupyter kernelspec list' to get names of all kernels

def does_nb_run_without_errors(notebook_contents, path, kernel=None,
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

    path = file_path.parent
    return does_nb_run_without_errors(nb_contents, path, kernel)


def get_start_processing_message(filename):
    str_filename = str(filename)
    line2 = '-'*len(str_filename)
    return f'{str_filename}\n{line2}'


def process_file(filename, kernel=None, timeout=600):
    notebook_okay, kernel_name, error_message = load_and_run_notebook(filename,
                                                         kernel, timeout)
    status = "Success" if notebook_okay else "Failure"
    summary = f'{filename}:\t{status}\t(kernel: {kernel_name})'
    logger.info(summary)
    if not notebook_okay:
        logger.debug(error_message)


if __name__ == '__main__':
    filenames = [f for f in Path('..').glob('**/*.ipynb')
                 if r'.ipynb_checkpoints' not in str(f)]

    for filename in filenames:
        process_file(filename)
