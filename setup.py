from setuptools import setup, find_packages
from pathlib import Path

VERSION = "0.0.1"
DESCRIPTION = "NetShare"
this_directory = Path(__file__).parent
LONG_DESCRIPTION = (this_directory / "README.md").read_text()

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="netshare",
    version=VERSION,
    author="Yucheng Yin, Zinan Lin, Minhao Jin, Giulia Fanti, Vyas Sekar",
    author_email="yyin4@andrew.cmu.edu",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        "pyparsing==2.4.7",     # pyparsing of higher version is incompatible with python3.6
        "tensorflow==1.15",
        "tensorflow-privacy==0.5.0",
        "tqdm",
        "matplotlib",
        "pandas",
        "scikit-learn",
        "more-itertools",
        "gensim==3.8.3",
        "networkx",
        "notebook",
        "ipyplot",
        "jupyterlab",
        "statsmodels",
        "gdown",
        "annoy",
        "pyshark",
        "scapy",
        "ray",
        "ray[default]",
        "multiprocess",
        "addict",
        "config_io==0.4.0",
        "flask"
    ],  # add any additional packages that
    # needs to be installed along with your package. Eg: 'caer'

    keywords=['python', 'netshare'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3.6",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires='>=3.6.1'
)
