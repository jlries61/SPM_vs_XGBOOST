# SPM_vs_XGBOOST
Performance comparison between Salford Systems' [TreeNet](https://www.salford-systems.com/products/treenet) and [XGBoost][]

The purpose of this exercise is to compare holdout sample ROC between TreeNet and XGBoost using multiple publicly data sets, each randomly partitioned in multiple ways.  In all cases, half the data are used for learning with the rest evenly divided between test (pruning) and holdout.  Because XGBoost does not support pruning, only the learning sample is used to build the model there; but the number of trees to use is automatically set equal to the optimal number according to TreeNet.

## Prerequisites
* Salford Predictive Modeler (SPM) 8.3 non-GUI (the GUI absolutely will not work here).  Available from [Salford Systems](https://www.salford-systems.com/products/spm).  Because SPM is now supported only under Windows and Linux, this project supports only those two platforms.  Alternatively, stand-alone TreeNet could be used.
* [XGBoost][].  You will need to build the stand-alone version.  See the [installation guide](https://xgboost.readthedocs.io/en/latest/build.html) for details.
* [Python 3](https://www.python.org/).  The following modules are required:
  * copy
  * getopt
  * numpy
  * os
  * pandas
  * random
  * re
  * sklearn
  * string
  * sys
  * tempfile
  * time
* [Exact Data Partitioner](https://github.com/jlries61/xpartition).  The script `xpartition` will need to be put in the path.

Our scripts expect the SPM executable to be named `spmu`.  If it is not, change the value *spm_executable* in the class *TreeNetModel* (defined in [TreeNet.py][] accordingly.  All other scripts and executables are expected to have their default names.

## Analysis Data
The data sets available for use in the analysis are listed in [Datasets4.xlsx](Datasets4.xlsx) and present in subdirectories under the directory [Data][].  At present, only binary classification models are built, so all files are under the [Classification subdirectory](Data/Classification), but when the time comes to compare regression models, a `Regression` subdirectory will be created as well.  All data sets mentioned in the above named spreadsheet are present in the repository, except for [Springleaf][], which must be downloaded and prepared separately (see the associated [README.txt](Data/Classification/Springleaf/README.txt)).  See the READMEs in the individual data directories for information on sources and (sometimes) data preparation.

## Conducting the Analysis
Change directory to [Scripts](Scripts).  To change the set of data sets to use, edit the variable *datasets_nums* in both `create_data_samples4.py` and `rgboost4_test.py`.  These are lists of data set indeces, as given in [Datasets4.xlsx][].  In the present code, all are used, except for [DEXTER](Data/Classification/DEXTER) and [Springleaf][].  You may also want to change the values of *TreeNetModel.GENERAL_THREADS* (defined in [TreeNet.py][]) and *XGBoostModel.gen_nthread* (defined in [xgBoost.py][]) to suit available computing resources.  The following three jobs should be run in order:
1. [create_data_samples4.py](Scripts/create_data_samples4.py): Randomly partitions the source data sets as specified in [Datasets4.xlsx](Datasets4.xlsx).
2. [rgboost4_test.py][]: Builds the requested models and generates the associated reports (found in the `../REPORTS` subdirectory).
3. [sumrept4.py](Scripts/sumrept4.py): Creates the summary spreadsheet `tn_vs_xgb_sumrept4.xlsx`.
The default TN and XGBoost settings are defined in [TreeNet.py][] and [xgBoost.py][], respectively, but some are changed in [rgboost4_test.py][].

[Data]: Data
[Datasets4.xlsx]: Datasets4.xlsx
[rgboost4_test.py]: Scripts/rgboost4_test.py
[Springleaf]: Data/Classification/Springleaf
[TreeNet.py]: Scripts/TreeNet.py
[XGBoost]: https://github.com/dmlc/xgboost
[xgBoost.py]: Scripts/xgBoost.py
