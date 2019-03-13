# Nemenyi

Library to perform the Friedman statistical test and Nemenyi post-hoc analysis.

## Instalation
```bash
git clone https://github.com/gabrielj12/nemenyi.git
```


# How to use

The input file must be a .csv file, and the output is a .tex file. The [CRE|DEC] parameter is used to define if the data is crescent or decrescent. The last parameter is optional,
if you want to skip the first column of the dataset, sometimes used for identification of the sample.

```bash
python nemenyi.py input_file output_file [ASC|DESC] [skip]
```

### This work is a port from an old Java code to Python
