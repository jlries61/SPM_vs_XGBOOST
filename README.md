# SPM_vs_XGBOOST
Performance comparison between SPM and XGBOOST

The purpose of this exercise is to compare holdout sample ROC between TreeNet and XGBOOST using multiple publicly data sets, each randomly partitioned in multiple ways.  In all cases, half the data are used for learning with the rest evenly divided between test (pruning) and holdout.  Because XGBOOST does not support pruning, only the learning sample is used to build the model there; but the number of trees to use is automatically set equal to the optimal number according to TreeNet.

## Prerequisites
* Salford Predictive Modeler (SPM) 8.3 non-GUI (the GUI absolutely will not work here).  Available from [Salford Systems](https://www.salford-systems.com/products/spm).  Because SPM is now supported only under Windows and Linux, this project supports only those two platforms.
* [XGBoost](https://github.com/dmlc/xgboost).  You will need to build the stand-alone version.  See the [installation guide](https://xgboost.readthedocs.io/en/latest/build.html) for details.
* [Python 3](https://www.python.org/)
* [Exact Data Partitioner](https://github.com/jlries61/xpartition).  The script `xpartition` will need to be put in the path.
