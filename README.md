# abaqustools
This repo contains useful tools for the pre and post processing of Abaqus models, mostly via python.

## Contents overview

### odbexport
- Package for export from Abaqus ODB files
- Export data from static analysis and modal analysis
- Export to txt and h5 files supported
- Supported exports: displacements, node coordinates, section forces, natural frequencies, generalized mass, element sets, ...

### abq
- Module to interact with Abaqus
- Run jobs from python
- Check input file for duplicate nodes/elements

### gen
- Module to generate Abaqus .inp files efficiently
- Supports most Abaqus keyword (*) for analysis of primarily beam structures
- Additional useful custom functions: beam joints with used-defined joint stiffness

## Required packages
The following list of packages are required:
["numpy","os","sys","time","scipy","nexusformat","datetime","h5py","timeit","warnings","putools","ypstruct"]


