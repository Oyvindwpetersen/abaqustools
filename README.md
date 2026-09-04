# abaqustools

Python tools for generating, running, and post-processing Abaqus finite-element models.

## Features

### `kw`

- Generate Abaqus `.inp` files efficiently.
- Write common Abaqus keywords for beam-oriented structural models.
- Create beam joints with user-defined stiffness for six degrees of freedom.

### `abq`

- Run Abaqus jobs from Python.
- Check input files for duplicate nodes and elements.

### `odbexport`

- Export static and modal-analysis results from Abaqus ODB files.
- Write text and HDF5 output.
- Export displacements, node coordinates, section forces, natural frequencies,
  generalized mass, element sets, and other result data.

### `post`

- Assemble and label result images for reports and presentations.
- Available as an optional plotting feature.

## Installation

Install the package from PyPI:

```console
python -m pip install abaqustools
```

Install the optional image and plotting dependencies when using `abaqustools.post`:

```console
python -m pip install "abaqustools[plotting]"
```

The package requires Python 3 or later. Running Abaqus jobs and reading ODB files
also requires a compatible Abaqus installation and its Python modules.

## Usage

Import the main modules from the package:

```python
from abaqustools import abq, kw, odbexport
```

Create part and node keywords in an Abaqus input file:

```python
import numpy as np
from abaqustools import kw

nodes = np.array([
    [1, 0.0, 0.0, 0.0],
    [2, 5.0, 0.0, 0.0],
])

with open("model.inp", "w", encoding="utf-8") as output:
    kw.part(output, "beam")
    kw.node(output, nodes, "beam_nodes")
    kw.partend(output)
```

Run an Abaqus input file:

```python
from abaqustools import abq

abq.runjob(
    foldername="path/to/model",
    inputname="model.inp",
    cpus=4,
)
```

Export modal results from an ODB file:

```python
from pathlib import Path

from abaqustools import odbexport

odbexport.export.modal(
    folder_odb="path/to/results",
    jobname="model",
    folder_save="path/to/export",
    folder_python=str(Path(odbexport.__file__).parent),
)
```

More complete scripts are available in the `example/` and `example/odbexport/`
directories.

## Abaqus compatibility

Functions that launch Abaqus or import `odbAccess`, `abaqusConstants`, and other
Abaqus modules must run in an environment where those modules are available.
Pure input-file generation and validation utilities can run in standard Python.

Compatibility depends on the Python version bundled with the installed Abaqus
release. If a particular Abaqus release causes a problem, please include its exact
version when opening an issue.

## Dependencies

Core dependencies are NumPy, h5py, and
[putools](https://github.com/Oyvindwpetersen/putools). Image composition and
plotting additionally require Matplotlib and Pillow.

## Contributing and support

Bug reports and proposed improvements are welcome through the
[GitHub issue tracker](https://github.com/Oyvindwpetersen/abaqustools/issues).
When reporting an Abaqus-related problem, include the Abaqus version, Python
version, operating system, and a minimal input example when possible.

The package is also available on [PyPI](https://pypi.org/project/abaqustools/).

## License

This project is licensed under the GNU General Public License, version 3 or later.
See [`LICENSE`](LICENSE) for the full terms.
