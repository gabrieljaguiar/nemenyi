# Nemenyi

Library to perform the Friedman statistical test and Nemenyi post-hoc analysis.

## Instalation
```bash
git clone https://github.com/gabrielj12/nemenyi.git
```


## Instructions

The input file must be a .csv file, and the output is a .tex file. The [ASC|DEC] parameter is used to define if the data is ascending or descending. The last parameter is optional,
if you want to skip the first column of the dataset, sometimes used for identification of the sample.

```bash
python nemenyi/nemenyi.py examples/input.csv examples/output.tex --descending
```

## Requirements

The following Python packages are required.

* pandas
* numpy
* scipy

## References

[01] DEMŠAR, Janez. Statistical comparisons of classifiers over multiple data sets. Journal of Machine learning research, v. 7, n. Jan, p. 1-30, 2006. Avaiable [here](http://www.jmlr.org/papers/volume7/demsar06a/demsar06a.pdf)

### This work is a port from an old Java code to Python
