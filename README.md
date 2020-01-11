# SPM_vs_XGBOOST
Performance comparison between SPM and XGBoost

The purpose of this exercise is to compare holdout sample ROC between TreeNet and XGBoost using multiple publicly data sets, each randomly partitioned in multiple ways.  In all cases, half the data are used for learning with the rest evenly divided between test (pruning) and holdout.  Because XGBoost does not support pruning, only the learning sample is used to build the model there; but the number of trees to use is automatically set equal to the optimal number according to TreeNet.

## Prerequisites
* Salford Predictive Modeler (SPM) 8.3 non-GUI (the GUI absolutely will not work here).  Available from [Salford Systems](https://www.salford-systems.com/products/spm).  Because SPM is now supported only under Windows and Linux, this project supports only those two platforms.
* [XGBoost](https://github.com/dmlc/xgboost).  You will need to build the stand-alone version.  See the [installation guide](https://xgboost.readthedocs.io/en/latest/build.html) for details.
* [Python 3](https://www.python.org/).  The following modules are required:
  * copy
  * getopt
  * numpy
  * os
  * pandas
  * random
  * string
  * sys
  * tempfile
  * time
* [Exact Data Partitioner](https://github.com/jlries61/xpartition).  The script `xpartition` will need to be put in the path.

## Analysis Data
The data sets available for use in the analysis are listed in [Datasets4.xlsx](Datasets4.xlsx) and present in subdirectories under the directory [Data](Data/).  At present, only binary classification models are built, so all files are under the [Classification subdirectory](Data/Classification), but when the time comes to compare regression models, a `Regression` subdirectory will be created as well.  All data sets mentioned in the above named spreadsheet are present in the repository, except for [Springleaf](Data/Classification/Springleaf), which must be downloaded and prepared separately (see the associated [README.txt](Data/Classification/Springleaf/README.txt)).
