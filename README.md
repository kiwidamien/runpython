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

## Running

```bash
# displays help message
$ run_notebooks --help

# runs notebook test.ipynb
$ run_notebooks test.ipynb

# runs all notebooks in notebooks/
$ run_notebooks notebooks/
```

