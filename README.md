# SPM_vs_XGBOOST
Performance comparison between SPM and XGBOOST

The purpose of this exercise is to compare holdout sample ROC between TreeNet and XGBOOST using multiple publicly data sets, each randomly partitioned in multiple ways.  In all cases, half the data are used for learning with the rest evenly divided between test (pruning) and holdout.  Because XGBOOST does not support pruning, only the learning sample is used to build the model there; but the number of trees to use is automatically set equal to the optimal number according to TreeNet.

## Prerequisites
