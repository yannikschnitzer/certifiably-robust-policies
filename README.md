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

### Plotting Risk Bounds as per Theorems 1 and 2, depicted in Figure 4

To obtain the risk bounds for example values of $\gamma$, $\eta$ and $N$, as depicted in Figure 4, run the Python script provided in the ***Risk_Plotting*** directory:

```bash
    cd Risk_Plotting
    python3 risk_bounds.py
```
This will print, for example values of $\gamma$ and $\eta$, the optimal risk bound optained via Theorems 1 and 2 in dependence of $N \in \{1,\dots,500\}$, with the automatically computed optimal $K$. Since more $K$'s have to be checked for increasing $N$, the computation will slow down with time. The overall runtime should be ~5 minutes. 

The resulting plots will be put into a newly generated directory ***risk_plots*** in PDF format.

### Running Case Studies and producing table rows as per Tables 2 and 4

To run our case studies and produce the rows of the Tables 2 and 4, we provide a PRISM command line interface. First go into the PRISM directory:

```bash
    cd PRISM-upmdps/prism
```
The main function to call the tool interface is:

```bash
    PRISM_MAINCLASS=lava.LearnVerify bin/prism -arg1 [-arg2 ...]
```

which comes with the following options:

* `-c`,`--casestudy`: Which case study to run, can be any of `aircraft`, `betting`, `sav`, `chain`, `drone`, `firewire`. If no case study is provided, all case studies are run in sequence.
* `-a`,`--algorithm`(optional): Which IMDP learning algorithm to run, can be any of `LUI`, `PAC`, `MAP`, `UCRL`. The reinforcement-learning policies are evaluated for any choice, see the ***Important Remarks*** below for further information. If no algorithm is provided, all algorithms are run in sequence.
* `-no-opt`,`--without-optimisations` (optional): Run algorithms without model-based optimisations, i.e., without parameter-tying.
* `-seed` (optional): Integer seed for the internal pseudo-random generator. Per default each selected case study will be run for multiple seeds, the results are aggregated for visualisation.
* `-all` (optional): Run the full benchmark set with full sample set sizes. **Note:** Very extensive with very long total runtime, see the ***Important Remarks*** below for further information. 
* `-h`,`--help`: Show this tool help description.
  
**Important Remarks (please read carefully)**
* Our full set of benchmarks is very extensive, if the full sample sizes of $N=300$ for training and verification is used. This can result in runtimes of many hours for a single case study and algorithm and a total runtime of weeks for the entire benchmark set. Therefore, we followed the suggestions of the artifact guidelines and adapted our code to run with a much smaller sample size, in order to make a feasible review time possible. We exploited regularities and monotonicities in the case studies which allows to produce (almost) identical results with less samples, by adding the extreme-case samples to the respective training and verification sets. 
  
* If the `-c`and `-a` options are used, these optimisations are applied. Still, the runtime of all case studies and all algorithms is expected to be multiple hours / day. 
  
* In accordance with the guidelines, the `-all` option can be used to run the entire benchmark set, with the full sample sizes.

* The policies obtained via Robust Meta Reinforcement Learning (RoML) are precomputed via PyTorch and the resulting policies are stored in the `prism/policies` directory. These are automatically parsed into PRISM strategies and evaluated on the MDPs / learned IMDPs for any run case study and benchmark.


**Example Commands**

Since the runtime for all case studies and algorithms can be extensive despite optimisations, we provide a range of example commands which run the quicker case studies and are expected to terminate in a reasonable time (all together in less than a working day):

Run the ***Aircraft*** case study with and without optimisations:
```bash
    PRISM_MAINCLASS=lava.LearnVerify bin/prism -c aircraft [-no-opt]
```

Run the ***Betting Game*** case study with and without optimisations:
```bash
    PRISM_MAINCLASS=lava.LearnVerify bin/prism -c betting [-no-opt]
```

Run the ***Semi-Autonomous Vehicle*** case study with and without optimisations:
```bash
    PRISM_MAINCLASS=lava.LearnVerify bin/prism -c sav [-no-opt]
```

The results are stored in the `prism/artifact_eval/results/basic` directory, split by case study, seeds (per default run on a range of random seeds), used algorithm and used optimisation (parameter-tying - "tied", and without - "naive"). For each combination there will be a *.csv* file with the full learning process and a *.yaml* file with the final results in a readable format. 

To make the evaluation more enjoyable, we provide a script which automatically reads out the *.yaml* files for completed case studies and prints the final results, which form the rows of the Tables 2 and 4 (modulo **Important Remarks**). This can be run from the `TACAS25/certifiably-robust-policies` main directory with:

```bash
    python3 table_row_printer.py -c <casestudy>
```

and produces a readable output. For example:

```bash
    python3 table_row_printer.py -c betting

Output:
=== Results for Model: BETTING_GAME_FAVOURABLE ===
IMDP policy performance on true MDPs (J): 30.785437150253898
IMDP policy performance on IMDPs (J̃): 30.62636123828767
RL policy performance on true MDPs (J): 28.513832442938444
RL policy performance on IMDPs (J̃): 28.37533025861897
existential guarantee: 30.785437150253898
empirical risk for k = 0: 0.005
empirical risk for k = 5: 0.016
empirical risk for k = 10: 0.026
runtime per 10k trajectories: 0.8721466666666667sec
```

**Note** that for this to run successfully, at least the `LUI` IMDP learning algorithm with optimisations has to be completed for the given case study.

### Visualising Case Studies and producing figures as per Figures 5 and 7

We also provide a script to visualise the learning process saved in the *.csv* files, aggregated over all seeds. This can be run from the `TACAS25/certifiably-robust-policies/Performance_Plotting` directory as:

```bash
    python3 plotting_performances.py -c <casestudy> [-no_optimizations]
```

This will generate the plots as depicted in Figures 5 and 7 for the provided case study, automatically for all completed algorithms and aggregated over all seeds. Those will be stored in the `Performance_Plotting` directory with a timestamp and in PDF format. By default this will generate the left and the middle column figures of Figure 7 for the given case study. With the `no-optimizations` option this will produce the right column figure (if the corresponding runs are completed). As always, the `-h` option is available for help on script usage.

## Dependencies and Libraries
Our artifact builds up on the following dependencies and libraries:

  * [PRISM](https://github.com/prismmodelchecker/prism) - Probabilistic model checker.
  * [FasterXML/Jackson](https://github.com/FasterXML/jackson-core) - JSON parsing library used for parsing the computed RL strategies into PRISM format.
  * [picocli](https://github.com/remkop/picocli) - Java command line interface.
  * [NumPy](https://github.com/numpy/numpy) - Used to compute risk bounds according to Theorems 1 and 2.
  * [scipy](https://github.com/scipy/scipy) - Used in computation of risk bounds.
  * [matplotlib](https://matplotlib.org/) - Used for visualizing the resulting risk bounds and performance plots.
  * [pandas](https://pandas.pydata.org/) - Used in precomputation for visualising performance plots.
  * [PyYAML](https://github.com/yaml/pyyaml) - Used to parse .yaml result files.
  * [PyTorch](https://pytorch.org/) - Used to train policies via RoML.
  * [Gymnasium](https://github.com/Farama-Foundation/Gymnasium) - Used to train policies via RoML.


  
## License

Copyright (c) 2024  Yannik Schnitzer

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.