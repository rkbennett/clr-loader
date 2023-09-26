# clr-loader

[![CI](https://github.com/pythonnet/clr-loader/workflows/Python%20Tests/badge.svg)](https://github.com/pythonnet/clr-loader/actions)
[![Pypi](https://img.shields.io/pypi/v/clr-loader.svg)](https://pypi.org/project/clr-loader/)
[![Conda Version](https://img.shields.io/conda/vn/conda-forge/clr_loader.svg)](https://anaconda.org/conda-forge/clr_loader)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Implements a generic interface for loading one of the CLR (.NET) runtime
implementations and calling simple functions on them.

## Updates

This version has been modified so that the clrloader dll is a managed assembly instead of a mix-mode assembly. This was done to work with another project I have called [pyclrhost](https://github.com/rkbennett/pyclrhost) so that this package could be imported from memory.

Documentation is available at https://pythonnet.github.io/clr-loader/.
