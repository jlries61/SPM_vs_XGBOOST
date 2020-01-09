More scripts will be added in due course, but run the following to perform an analysis:

1.  create_data_samples4.py: Create the data partitions.
2.  rgboost4_test.py: Build the models and create the reports.  TN and XGBoost models will be built and reports generated for each partition scheme; and plots and aggregate reports are generated for each source data set.  The resulting reports will reside in ../Reports/RGBOOST4.
3.  sumrept4.py: Generate a summary spreadsheet on the models run (tn_vs_xgb_sumrept4.xlsx).

The spreadsheet Datasets4.xlsx (in the parent directory) describes the source data sets available.  The data sets actually used are sepecified by the variable datasets_nums (a list of integers) in both create_data_samples4.py.  sumrept4.py will summarize whatever models were built.

arfftocsv is an auxilliary script that converts ARFF files to CSV.  The remaining Python files specify classes used by create_data_samples4.py and rgboost4_test.py.
