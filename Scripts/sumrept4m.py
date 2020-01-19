# Generate a summary report on the models built by rgboost4_test.py

import os
import pandas as pd
import re
from sklearn.metrics import roc_auc_score

# Define constants
SPREAD = "../Datasets4.xlsx" # Input dataset information spreadsheet
OUTFILE = "../Reports/tn_vs_xgb_sumrept4m.xlsx" # Summary report spreadsheet to create
fields = ["Name", "N Replications", "N Features", "N Learn", "N Holdout",
          "Avg ROC (TN; MART)", "Avg ROC (TN; RGBOOST, MHESS=0)", "Avg ROC (TN; RGBOOST, MHESS=1)",
          "Avg ROC (XGB)", "StdDev ROC (TN; MART)", "StdDev ROC (TN; RGB MHESS=0)",
          "StdDev ROC (TN; RGB MHESS=1)", "StdDev ROC (XGB)", "Avg Delta_ROC (Best TN vs XGB)",
          "Min Delta ROC (Best TN vs XGB)", "Max Delta ROC (Best TN vs XGB)",
          "StdDev Delta ROC (Best TN vs XGB)"] # Report field names
REPTDIR = "../Reports/RGBOOST4M" # Directory from which to pull the model results
DATADIR = "../Data/Classification" # Repository of classification model datasets
SLASH = "/"
MODSET = "_RGLs-0_INF-0.0_SUBS-1.0_LR-0.1_DEPTH-7_PREDS-500_NTREES-400" # Model set to use
scorenames = ["Class", "Prob"] # Names of fields in score datasets
filename_root = ["mart", "treenet", "treenet2", "xgb"] # Input Filename prefixes

# Define list of fields for the roc data frame (created once per input dataset)
roccols = filename_root.copy()
roccols.append("Delta")

# Read input dataset information spreadsheet
dsl = pd.read_excel(SPREAD)

# Initialize output data frame
summary = pd.DataFrame(columns=fields)

for i in dsl.index: # For each input dataset
  dataname = dsl.loc[i, "Name"]
  reptdir = REPTDIR + SLASH + dataname + MODSET # Directory containing model results
  if not os.path.isdir(reptdir): # If it does not exist, then skip it
    continue
  nrepl = dsl.loc[i, "N_data_samples"]
  datadir = DATADIR + SLASH + dataname + SLASH + "SAMPLES4" # Directory containing partioned data
  trainfile1 = datadir + SLASH + "data_train_1.csv" # Training dataset (file)
  holdfile1 = datadir + SLASH + "data_hold_1.csv" # Holdout dataset (file)
  rept = REPTDIR + SLASH + dataname + "_summary_report" + MODSET + ".txt"

  # Initialize summary report row
  row = dict()
  row["Name"] = dataname
  row["N Replications"] = nrepl
  row["N Features"] = dsl.loc[i, "N_features"]

  # Extract record counts from the input datasets
  traindata = pd.read_csv(trainfile1, low_memory=False) # Training data frame
  holddata = pd.read_csv(holdfile1, low_memory=False)   # Holdout data frame
  row["N Learn"] = len(traindata.index)
  row["N Holdout"] = len(holddata.index)
  del traindata, holddata # These can be quite large, so free up the memory now

  # Determine best performing TN model
  besttn = -1
  with open(rept) as fh:
    for line in fh:
      if re.match("^Mean ", line):
        values = line.split()
        values.pop(0)
        nval = len(values)
        maxroc_tn = 0
        for i in range(nval):
          if i == 3:
            continue
          value = float(values[i])
          if value > maxroc_tn:
            besttn = i
            maxroc_tn = value
        break

  # Define ROC data frame
  roc = pd.DataFrame(columns=roccols)
  for irepl in range(1, nrepl):
    roc_row = dict()
    for rootname in filename_root:
      score_file = reptdir + SLASH + rootname + "_score_test_" + str(irepl) + ".csv"
      modscores = pd.read_csv(score_file, names=scorenames)
      roc_row[rootname] = roc_auc_score(modscores["Class"], modscores["Prob"])
    roc_row["Delta"] = roc_row[filename_root[besttn]] - roc_row["xgb"]
    roc = roc.append(roc_row, ignore_index=True)

  # Add ROC statistics to summary report
  row["Avg ROC (TN; MART)"] = roc["mart"].mean()
  row["Avg ROC (TN; RGBOOST, MHESS=0)"] = roc["treenet"].mean()
  row["Avg ROC (TN; RGBOOST, MHESS=1)"] = roc["treenet2"].mean()
  row["Avg ROC (XGB)"] = roc["xgb"].mean()
  row["StdDev ROC (TN; MART)"] = roc["mart"].std()
  row["StdDev ROC (TN; RGB MHESS=0)"] = roc["treenet"].std()
  row["StdDev ROC (TN; RGB MHESS=1)"] = roc["treenet2"].std()
  row["StdDev ROC (XGB)"] = roc["xgb"].std()
  row["Avg Delta_ROC (Best TN vs XGB)"] = roc["Delta"].mean()
  row["Min Delta ROC (Best TN vs XGB)"] = roc["Delta"].min()
  row["Max Delta ROC (Best TN vs XGB)"] = roc["Delta"].max()
  row["StdDev Delta ROC (Best TN vs XGB)"] = roc["Delta"].std()
  del roc # Why keep it around longer than I need to?
  summary = summary.append(row, ignore_index=True)

# Write summary frame to the output spreadsheet
summary.to_excel(OUTFILE, index=False)