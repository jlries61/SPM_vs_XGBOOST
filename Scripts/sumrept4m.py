# Generate a summary report on the models built by rgboost4_test.py

import os
import pandas as pd
import re
from sklearn.metrics import roc_auc_score

def rng(series):
  return series.max() - series.min()

def gtct(series1, series2):
  cmp = series1.gt(series2)
  count = 0
  for bigger in cmp:
    if bigger:
      count = count + 1
  return count

# Define constants
SPREAD = "../Datasets4.xlsx" # Input dataset information spreadsheet
OUTFILE = "../Reports/tn_vs_xgb_sumrept4m.xlsx" # Summary report workbook to create
fields1 = ["Name", "N Replications", "N Features", "N Learn", "N Holdout",
           "Avg ROC (TN; MART)", "Avg ROC (TN; RGBOOST, MHESS=0)", "Avg ROC (TN; RGBOOST, MHESS=1)",
           "Avg ROC (XGB)", "StdDev ROC (TN; MART)", "StdDev ROC (TN; RGB MHESS=0)",
           "StdDev ROC (TN; RGB MHESS=1)", "StdDev ROC (XGB)", "Avg Delta_ROC (Best TN vs XGB)",
           "Min Delta ROC (Best TN vs XGB)", "Max Delta ROC (Best TN vs XGB)",
           "StdDev Delta ROC (Best TN vs XGB)"]
fields2 = ["Name", "Stat", "ROC(TN; MART)", "ROC(TN; RGBOOST; MHESS=0)",
           "ROC(TN; RGBOOST; MHESS=1)", "ROC(XGBoost)"]
fields3 = ["Name", "N Replications", "N Features", "N Learn", "N Holdout", "Avg ROC (TN)",
           "Avg ROC (XGB)", "Min ROC (TN)", "Min ROC (XGB)", "Max ROC (TN)", "Max ROC (XGB)",
           "StdDev ROC (TN)", "StdDev ROC (XGB)", "Avg Delta ROC", "Min Delta ROC",
           "Max Delta ROC", "StdDev Delta ROC", "# times TN beats XGB"]
REPTDIR = "../Reports/RGBOOST4M" # Directory from which to pull the model results
DATADIR = "../Data/Classification" # Repository of classification model datasets
SLASH = "/"
MODSET = "_RGLs-0_INF-0.0_SUBS-1.0_LR-0.1_DEPTH-7_PREDS-500_NTREES-400" # Model set to use
scorenames = ["Class", "Prob"] # Names of fields in score datasets
filename_root = ["mart", "treenet", "treenet2", "xgb"] # Input Filename prefixes
fltfmt = "%.5f"

# Define list of fields for the roc data frame (created once per input dataset)
roccols = filename_root.copy()
roccols.append("Delta")

# Read input dataset information spreadsheet
dsl = pd.read_excel(SPREAD)

# Initialize output data frames
summary = pd.DataFrame(columns = fields1)
detail = pd.DataFrame(columns = fields2)
MARTvXGB = pd.DataFrame(columns = fields3)
TNRGBM0 = pd.DataFrame(columns = fields3)
TNRGBM1 = pd.DataFrame(columns = fields3)
BestTN = pd.DataFrame(columns = fields3)

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

  row_mart = row.copy()

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
  for irepl in range(1, nrepl + 1):
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
  summary = summary.append(row, ignore_index=True)

  # Add by model type descriptive stats to the detail report
  mean_row = dict({"Name":dataname, "Stat":"Mean", fields2[2]:row["Avg ROC (TN; MART)"],
                   fields2[3]:row["Avg ROC (TN; RGBOOST, MHESS=0)"],
                   fields2[4]:row["Avg ROC (TN; RGBOOST, MHESS=1)"],
                   fields2[5]:row["Avg ROC (XGB)"]})
  min_row = dict({"Name":dataname, "Stat":"Min", fields2[2]:roc["mart"].min(),
                  fields2[3]:roc["treenet"].min(), fields2[4]:roc["treenet2"].min(),
                  fields2[5]:roc["xgb"].min()})
  max_row = dict({"Name":dataname, "Stat":"Max", fields2[2]:roc["mart"].max(),
                  fields2[3]:roc["treenet"].max(), fields2[4]:roc["treenet2"].max(),
                  fields2[5]:roc["xgb"].min()})
  range_row = dict({"Name":dataname, "Stat":"Range", fields2[2]:rng(roc["mart"]),
                    fields2[3]:rng(roc["treenet"]), fields2[4]:rng(roc["treenet2"]),
                    fields2[5]:rng(roc["xgb"])})
  std_row = dict({"Name":dataname, "Stat":"Std", fields2[2]:row["StdDev ROC (TN; MART)"],
                  fields2[3]:row["StdDev ROC (TN; RGB MHESS=0)"],
                  fields2[4]:row["StdDev ROC (TN; RGB MHESS=1)"],
                  fields2[5]:row["StdDev ROC (XGB)"]})
  detail = detail.append(pd.DataFrame([mean_row, min_row, max_row, range_row, std_row]),
                         ignore_index=True)

  row_mart["Avg ROC (XGB)"] = mean_row[fields2[5]]
  row_mart["Min ROC (XGB)"] = min_row[fields2[5]]
  row_mart["Max ROC (XGB)"] = max_row[fields2[5]]
  row_mart["StdDev ROC (XGB)"] = std_row[fields2[5]]

  row_rgb0 = row_mart.copy()
  row_rgb1 = row_mart.copy()
  row_best = row_mart.copy()

  row_mart["Avg ROC (TN)"] = mean_row[fields2[2]]
  row_mart["Min ROC (TN)"] = min_row[fields2[2]]
  row_mart["Max ROC (TN)"] = max_row[fields2[2]]
  row_mart["StdDev ROC (TN)"] = std_row[fields2[2]]
  delta_mart = roc["mart"].subtract(roc["xgb"])
  row_mart["Avg Delta ROC"] = delta_mart.mean()
  row_mart["Min Delta ROC"] = delta_mart.min()
  row_mart["Max Delta ROC"] = delta_mart.max()
  row_mart["StdDev Delta ROC"] = delta_mart.std()
  row_mart["# times TN beats XGB"] = gtct(roc["mart"], roc["xgb"])
  MARTvXGB = MARTvXGB.append(row_mart, ignore_index=True)

  row_rgb0["Avg ROC (TN)"] = mean_row[fields2[3]]
  row_rgb0["Min ROC (TN)"] = min_row[fields2[3]]
  row_rgb0["Max ROC (TN)"] = max_row[fields2[3]]
  row_rgb0["StdDev ROC (TN)"] = std_row[fields2[3]]
  delta_rgb0 = roc["treenet"].subtract(roc["xgb"])
  row_rgb0["Avg Delta ROC"] = delta_rgb0.mean()
  row_rgb0["Min Delta ROC"] = delta_rgb0.min()
  row_rgb0["Max Delta ROC"] = delta_rgb0.max()
  row_rgb0["StdDev Delta ROC"] = delta_rgb0.std()
  row_rgb0["# times TN beats XGB"] = gtct(roc["treenet"], roc["xgb"])
  TNRGBM0 = TNRGBM0.append(row_rgb0, ignore_index=True)

  row_rgb1["Avg ROC (TN)"] = mean_row[fields2[4]]
  row_rgb1["Min ROC (TN)"] = min_row[fields2[4]]
  row_rgb1["Max ROC (TN)"] = max_row[fields2[4]]
  row_rgb1["StdDev ROC (TN)"] = std_row[fields2[4]]
  delta_rgb1 = roc["treenet2"].subtract(roc["xgb"])
  row_rgb1["Avg Delta ROC"] = delta_rgb1.mean()
  row_rgb1["Min Delta ROC"] = delta_rgb1.min()
  row_rgb1["Max Delta ROC"] = delta_rgb1.max()
  row_rgb1["StdDev Delta ROC"] = delta_rgb1.std()
  row_rgb1["# times TN beats XGB"] = gtct(roc["treenet2"], roc["xgb"])
  TNRGBM1 = TNRGBM1.append(row_rgb1, ignore_index=True)

  index = besttn + 2
  row_best["Avg ROC (TN)"] = mean_row[fields2[index]]
  row_best["Min ROC (TN)"] = min_row[fields2[index]]
  row_best["Max ROC (TN)"] = max_row[fields2[index]]
  row_best["StdDev ROC (TN)"] = std_row[fields2[index]]
  delta_best = roc[filename_root[besttn]].subtract(roc["xgb"])
  row_best["Avg Delta ROC"] = delta_best.mean()
  row_best["Min Delta ROC"] = delta_best.min()
  row_best["Max Delta ROC"] = delta_best.max()
  row_best["StdDev Delta ROC"] = delta_best.std()
  row_best["# times TN beats XGB"] = gtct(roc[filename_root[besttn]], roc["xgb"])
  BestTN = BestTN.append(row_best, ignore_index=True)

# Write frames to the output spreadsheet
with pd.ExcelWriter(path = OUTFILE) as outwrite:
  summary.to_excel(outwrite, sheet_name = "Summary", index = False, float_format = fltfmt)
  detail.to_excel(outwrite, sheet_name = "ByDataset", index = False, float_format = fltfmt)
  MARTvXGB.to_excel(outwrite, sheet_name = "TreeNet-MART vs XGB", index = False,
                    float_format = fltfmt)
  TNRGBM0.to_excel(outwrite, sheet_name = "TreeNet-RGBOOST (MHESS=0) vs XGB", index = False,
                   float_format = fltfmt)
  TNRGBM1.to_excel(outwrite, sheet_name = "TreeNet-RGBOOST (MHESS=1) vs XGB", index = False,
                   float_format = fltfmt)
  BestTN.to_excel(outwrite, sheet_name = "Best TreeNet vs XGB", index = False, float_format = fltfmt)
