# run_notebooks

## Purpose

This is a command-line application for running Jupyter notebooks, and logging errors that occur. This enables you to do
bulk testing of lessons/notebooks without loading each one independently. This is particualarly useful for tutorials or
lessons.

It also supports kernels, so that you can test notebooks within a specific kernel. An environment that you have created
has to be "registered" to be a kernel accessible to Jupyter. You can find a list of kernels available with
```bash
$ jupyter kernelspec list
```
If the kernel is not specified, then `run_notebooks` uses the kernel specified in the notebook.

## Installation 

There are two different installation methods (depending on whether you are cloning the repo, or just using the CLI).

### Develop

If cloning this repo, you can install a development version from the top-level repo directory with
```bash
$ pip install -e .
```

### Using CLI only

If just trying to use the CLI, you can install this package via
```bash
$ pip install git+https://github.com/kiwidamien/runpython
```

Eventually I want to have this package hosted on PyPI.

## Uninstall

```bash
$ pip uninstall run_notebooks
```

## Usage 

```bash
# displays help message
$ run_notebooks --help

# runs individual notebooks
$ run_notebooks test_notebooks/the_good.ipynb test_notebooks/nested_folder/the_ugly.ipynb

# runs all notebooks in test_notebooks/ (excluding files in checkpoint directories)
$ run_notebooks test_notebooks/

# runs all notebooks using the Python2 kernel
$ run_notebooks -k python2 test_notebooks/

# runs ALL notebooks in test_notebooks/ (including those in checkpoint directories)
# The is more to emphasize it works with redirects
$ find test_notebooks/ -iname "*.ipynb" | xargs run_notebooks
```

By default, the output gets written to the (hidden) files `.error_log_summary` and `.error_log_detail`.

You can change these defaults with the options `--summary-file` and `--detail-file` respectively.
