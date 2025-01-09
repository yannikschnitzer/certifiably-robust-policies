# Certifiably Robust Policies for Uncertain Parametric Environments 


This is the artifact for the paper **"Certifiably Robust Policies for Uncertain Parametric Environments"** (TACAS 2025). 

The corresponding Git repository is: https://github.com/yannikschnitzer/certifably-robust-policies.

We claim the artifact to be **available** and **functional**. We describe its structure and usage below.

Integral parts of our implementation build up on the repository https://github.com/LAVA-LAB/luiaard, for the paper "Robust Anytime Learning of Markov Decision Processes" (NeurIPS 2022), which the thankfully acknowledge. This repository and our implementation further form extensions of the PRISM probabilistic model checker: https://github.com/prismmodelchecker/prism.

## Artifact Requirements

The artifact comes as a `Dockerfile`, which automatically sets up a container containing all relevant files, software, and dependencies. 

The artifact contains our software and third-party software used internally. We recommend the following minimal system specifications, used in our evaluation:
* **CPU**: 3.3GHz 8-core 
* **RAM**: 16GB
* **Disk Space**: 32GB

The setup via Docker installs all required software and dependencies. This should complete relatively quick (~10 minutes).

## Structure and Content

The artifact contains a `Dockerfile` which automatically sets up the environment for evaluation. The environment is structured as follows

* **TACAS25** - Main Folder containing the artifact.
  * **certifably-robust-policies** - Repository folder
    * ***PRISM-upmdps***: Repository containing our implementation and experiments, building up on the PRISM model checker.
    * ***Performance_Plotting***: Scripts for visualising the resulting learning process as depicted in Figures 5 and 7.
    * ***Risk_Plotting***: Scripts to produce a visualisation of the resulting risk bounds as per Theorems 1 and 2, depicted in Figure 4.

## Getting Started

After unpacking the artifact, the `Dockerfile` can be turned into an image by running:

```bash
sudo docker build -t artifact .
```

in the directoy of the file. The image can be run in a container by executing:

```bash
sudo docker run -it artifact 
```

After the setup, the container should start in the `TACAS25`-folder, whose structure is described in the **Structure and Content** section.

### Smoke-Tests

We provide seperate smoke tests for the main implementation (Java) and the visualisation scripts (Python).

To run the smoke tests for the main implementation, execute the following commands:

```bash
    cd certifiably-robust-policies/PRISM-upmdps/prism
    PRISM_MAINCLASS=lava.LearnVerify bin/prism -smoke
```
The script will run one small test benchmark with a reduced number of iterations which should complete in a few minutes. If finished successfully, the script should print:
```
PRISM smoke test finished successfully :)
```

To run the smoke tests for the visualistion scripts, run the following (**back in the main TACAS25/certifiably-robust-policies/ directory**):
```bash
    python3 smoke_test.py
```
This script will check whether all required libaries are successfully installed and print their versions. If everything is set up correctly, the script will exit with:
```
Python smoke test finished successfully :)
```

## Running Experiments


## Dependencies and Libraries
Our artifact builds up on the following dependencies and libraries:

  * [PRISM](https://github.com/prismmodelchecker/prism) - Probabilistic model checker.
  * [FasterXML/Jackson](https://github.com/FasterXML/jackson-core) - JSON parsing library used for parsing the computed RL strategies into PRISM format.
  * [picocli](https://github.com/remkop/picocli) - Java command line interface.
  * [NumPy](https://github.com/numpy/numpy) - Used to compute risk bounds according to Theorems 1 and 2.
  * [scipy](https://github.com/scipy/scipy) - Used in computation of risk bounds.
  * [matplotlib](https://matplotlib.org/) - Used for visualizing the resulting risk bounds and performance plots.
  * [pandas](https://pandas.pydata.org/) - Used in precomputation for visualising performance plots.


  
## License

Copyright (c) 2024  Yannik Schnitzer

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.