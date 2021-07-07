# Myo-LSL
Python script for the Myo armband (Thalmic Labs, now discontinued) to stream data using [LSL](https://github.com/sccn/labstreaminglayer).

This relies heavily on Niklas Rosenstein's [Myo-Python](https://github.com/NiklasRosenstein/myo-python). A version of the wrapper is included in this repository. The main script is based on the examples provided.

The Myo armband must be installed and connected. Due to changes in how the DLLs are loaded in Python 3.8, a previous version of Python (such as Python 3.7.1) is recommended unless the code is adjusted to the changes.
