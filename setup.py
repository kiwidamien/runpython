from setuptools import setup, find_packages

setup(
    name='run_notebooks',
    version='0.0.1',
    url='https://github.com/kiwidamien/runpython',
    author='kiwidamien',
    packages=find_packages(),
    install_requires=[
        'Click',
        'jupyter_client',
        'pyyaml',
        'jupyter_core',
        'nbconvert',
        'nbformat',
    ],
    entry_points="""
        [console_scripts]
        run_notebooks=bin.main:pythonrunner
    """,
    include_package_data=True
)
