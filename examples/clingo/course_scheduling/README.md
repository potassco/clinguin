# Student project on course scheduling

The project is based on [*clingun*](https://github.com/krr-up/clinguin)

## Install

Install using the conda environment with

```
conda env create -f environment.yml
```

Then run

## Use
Run the demo by running *clinguin* as follows

```
clinguin client-server --source-files encoding.lp courses.lp --ui-files ui.lp
```

## Hints

- Multiple selection dropdowns are not given by the basic *clinguin*, but you can be creative and create a nice workaround.
- You can see more information on the models computed by clinguin by changing the log level to debug `--server-log-level DEBUG`.
- If you see the need, you can create a custom backend or just use the *ClingoBackend*.